from qdrantConnection import client as qdrant_client
from qdrant_client.models import VectorParams, Distance


def create_collection():

    collections = qdrant_client.get_collections().collections

    if not any(c.name == "resume_readmes" for c in collections):

        qdrant_client.create_collection(
            collection_name="resume_readmes",
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE
            )
        )