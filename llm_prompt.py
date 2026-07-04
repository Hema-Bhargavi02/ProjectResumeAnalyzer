from google import genai
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from typing import List

from github_service import fetch_readme
from qdrantConnection import client as qdrant_client

from generateEmbeddings import get_embedding
from qdrant_client.models import PointStruct

import uuid

load_dotenv(".env")


api_key = os.getenv("LLM_API_KEY")

client = genai.Client(api_key=api_key)

app = FastAPI()

class ResumeInfo(BaseModel):
    text: str
    githubProfile: str
    githubRepositories: List[str]

class LLMRequest(BaseModel):
    prompt: str
    resumeInfo: ResumeInfo


@app.post("/indexResume")
def index_resume(request: ResumeInfo):

    for repo_url in request.githubRepositories:
        repo_name, readme = fetch_readme(repo_url)

        if readme is None:
            continue

        embedding = get_embedding(readme)

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "type": "readme",
                "repo_name": repo_name,
                "repo_url": repo_url,
                "content": readme
            }
        )

        qdrant_client.upsert(
            collection_name="resume_readmes",
            points=[point]
        )

    info = qdrant_client.get_collection("resume_readmes")
    total_points = info.points_count

    return {
        "message": "Indexing completed",
        "total_points_in_collection": total_points
    }


@app.post("/ask")
def ask(request: LLMRequest):

    # 1. Convert question → embedding
    query_embedding = get_embedding(request.prompt)

    # 2. Search Qdrant
    search_result = qdrant_client.query_points(collection_name="resume_readmes",
                                                query=query_embedding, 
                                                limit=3)

    # 3. Build context from matches
    matched_readmes = ""

    for point in search_result.points:
        matched_readmes += f"""
            Repository: {point.payload['repo_name']}
            URL: {point.payload['repo_url']}
            README: {point.payload['content']}

            ========================
        """

    # 4. Build LLM input
    llm_input = f"""
        Resume: {request.resumeInfo.text}
        Relevant GitHub Projects: {matched_readmes}
        Question: {request.prompt}
        """

    # 5. Call Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=llm_input
    )

    return {
        "answer": response.text
    }
   

@app.get("/checkQdrantConnection")
def check_qdrant_connection():
    try:
        qdrant_client.get_collections()
        return {"status": "Qdrant connection is working" + str(qdrant_client.get_collections())}
    except Exception as e:
        return {"status": "Qdrant connection failed", "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)