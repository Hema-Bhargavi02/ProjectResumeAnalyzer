from qdrantConnection import client as qdrant_client
from generateEmbeddings import get_embedding
# pyrefly: ignore [missing-import]
from qdrant_client.models import Filter, FieldCondition, MatchValue

COLLECTION_NAME = "resume_readmes"


def search_readmes(user_id, question):

    query_embedding = get_embedding(question)
    search_result = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding ,
        limit=3,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=user_id)
                )
            ]
        )
    )
    return search_result.points