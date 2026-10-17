
import uuid

from qdrant_client.models import PointStruct
from qdrantConnection import client as qdrant_client
from generateEmbeddings import get_embedding
from chuncking import chunkText

COLLECTION_NAME = "resume_readmes"


def insert_document(user_id,document_type,text,repo_name=None,repo_url=None):

    chunks = chunkText(text)

    if not chunks:
        return 0

    points = []

    for index, chunk in enumerate(chunks):
        embedding_text = chunk

        if repo_name:
            embedding_text = (
                f"Repository: {repo_name}\n"
                f"Content: {chunk}"
            )

        embedding = get_embedding(embedding_text)

        payload = {
            "user_id": user_id,
            "type": document_type,
            "chunk_index": index,
            "content": chunk
        }

        if repo_name:
            payload["repo_name"] = repo_name

        if repo_url:
            payload["repo_url"] = repo_url

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload=payload
            )
        )

    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
        wait=True
    )

    return len(points)


def insert_readme(user_id, repo_name, repo_url, readme):
    return insert_document(
        user_id=user_id,
        document_type="readme",
        text=readme,
        repo_name=repo_name,
        repo_url=repo_url
    )



def insert_resume(user_id, resume_text):
    return insert_document(
        user_id=user_id,
        document_type="resume",
        text=resume_text,
        repo_name=None,
        repo_url=None
    )
