from qdrantConnection import client as qdrant_client
from qdrant_client.models import PayloadSchemaType

print("Starting...")

try:
    print("Connecting to Qdrant...")

    result = qdrant_client.create_payload_index(
        collection_name="resume_readmes",
        field_name="user_id",
        field_schema=PayloadSchemaType.KEYWORD
    )

    print("Index created:", result)

except Exception as e:
    print("ERROR:", e)