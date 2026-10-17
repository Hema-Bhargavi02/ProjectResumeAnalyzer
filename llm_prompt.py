from insertQdrantPoint import insert_resume
from google import genai
from dotenv import load_dotenv
import os
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import List
import uuid

from github_service import fetch_readme
from qdrantConnection import client as qdrant_client
from qdrantCollection import create_collection
from generateEmbeddings import get_embedding
from insertQdrantPoint import insert_readme
from fetchRelevanceReadme import search_readmes


load_dotenv(".env")


api_key = os.getenv("LLM_API_KEY")

client = genai.Client(api_key=api_key)

app = FastAPI()


# ---------------- DTO Classes ----------------

class ResumeInfo(BaseModel):
    userId: str
    text: str
    githubProfile: str
    githubRepositories: List[str]


class LLMRequest(BaseModel):
    userId: str
    prompt: str
    resumeInfo: ResumeInfo



# ---------------- Index Resume ----------------

@app.post("/indexResume")
def index_resume(request: ResumeInfo):
    try:
        create_collection()

        user_id = request.userId
        resume_chunks = 0
        readme_chunks = 0

        if request.text and request.text.strip():
            resume_chunks = insert_resume(user_id,request.text)

        for repo_url in request.githubRepositories or []:
            repo_name, readme = fetch_readme(repo_url)

            if readme and readme.strip():
                readme_chunks += insert_readme(
                    user_id=user_id,
                    repo_name=repo_name,
                    repo_url=repo_url,
                    readme=readme
                )

        info = qdrant_client.get_collection(
            collection_name="resume_readmes"
        )

        return {
            "message": "Indexing completed successfully.",
            "user_id": user_id,
            "resume_chunks": resume_chunks,
            "readme_chunks": readme_chunks,
            "total_points_in_collection": info.points_count
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while indexing resume: {str(e)}"
        )




# ---------------- Ask LLM ----------------

@app.post("/ask")
def ask(userId: str, prompt: str):
    try:
        matched_points = search_readmes(userId, prompt)

        if not matched_points:
            return {
                "answer": "No relevant information found in the indexed documents."
            }

        context = ""

        for point in matched_points:
            payload = point.payload or {}

            context += f"""
Document Type: {payload.get('type', 'unknown')}
Repository: {payload.get('repo_name', 'N/A')}
Chunk Index: {payload.get('chunk_index', 'N/A')}

Content:
{payload.get('content', '')}

-------------------------
"""

        llm_input = f"""
Answer the question using only the relevant document chunks below.

If the context does not contain enough information, say so.
Do not invent information.

Relevant Chunks:
{context}

Question:
{prompt}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=llm_input
        )

        return {
            "answer": response.text,
            "retrieved_chunks": len(matched_points)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while asking LLM: {str(e)}"
        )



# ---------------- Qdrant Health Check ----------------

@app.get("/checkQdrantConnection")
def check_qdrant_connection():

    try:

        collections = qdrant_client.get_collections()

        return {
            "status": "Qdrant connection is working",
            "collections": str(collections)
        }


    except Exception as e:

        return {
            "status": "Qdrant connection failed",
            "error": str(e)
        }



# ---------------- Main ----------------

if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )