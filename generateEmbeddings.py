from fastembed import TextEmbedding
import os
from huggingface_hub import login
from dotenv import load_dotenv

load_dotenv()

login(token=os.getenv("HF_TOKEN"))
# Load the model once when the application starts
embedding_model = TextEmbedding(
    model_name="nomic-ai/nomic-embed-text-v1.5"
)

def get_embedding(text: str):
    """
    Returns the embedding vector as a list of floats.
    """
    embedding = next(embedding_model.embed([text]))
    return embedding.tolist()