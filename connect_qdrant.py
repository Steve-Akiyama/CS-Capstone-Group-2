from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

client = QdrantClient("localhost", port=6333)

#Create a collection
client.create_collection(
    collection_name="collection",
    vectors_config=VectorParams(size=128, distance=Distance.COSINE),
)
print("Collection created successfully.")