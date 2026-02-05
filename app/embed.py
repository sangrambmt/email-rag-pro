import chromadb
from chromadb.utils import embedding_functions
from app.config import settings

_client = chromadb.PersistentClient(path="data/index/chroma")
_embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
    api_key=settings.OPENAI_API_KEY,
    model_name=settings.EMBEDDING_MODEL
)

_collection = _client.get_or_create_collection(
    name="emails",
    embedding_function=_embedding_fn
)

def get_collection():
    return _collection