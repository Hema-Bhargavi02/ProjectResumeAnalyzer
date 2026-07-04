from qdrantConnection import client as qdrant_client
from qdrant_client.models import PointStruct
import uuid


def insert_readme(repo_name, repo_url, readme, embedding):

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