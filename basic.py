from qdrant_client import QdrantClient
from qdrant_client.http import models
import numpy as np
import os

# Initialize Qdrant client
client = QdrantClient(host="localhost", port=6333)

VECTOR_INPUT_DIR = "vector_input"
TEXTBOOK_FILE = os.path.join(VECTOR_INPUT_DIR, "textbook.txt")
COLLECTION_NAME = "test_collection"
VECTOR_SIZE = 128  # Ensure this matches the vector size in the main script

def create_test_collection():
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE)
    )
    print(f"Collection '{COLLECTION_NAME}' created.")

def process_textbook_file():
    if not os.path.isfile(TEXTBOOK_FILE):
        print(f"File '{TEXTBOOK_FILE}' not found.")
        return None, None

    with open(TEXTBOOK_FILE, 'r', encoding='utf-8') as file:
        content = file.read()

    sentences = content.split(". ")
    vectors = [np.random.rand(VECTOR_SIZE).tolist() for _ in sentences]
    payloads = [{"text": sentence} for sentence in sentences]

    print(f"Loaded {len(sentences)} sentences from textbook.txt")
    return vectors, payloads

def add_vectors_to_collection(vectors, payloads):
    points = [models.PointStruct(id=i, vector=vector, payload=payload)
              for i, (vector, payload) in enumerate(zip(vectors, payloads))]
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Added {len(points)} vectors to collection '{COLLECTION_NAME}'.")

def search_collection():
    query_vector = np.random.rand(VECTOR_SIZE).tolist()
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=3
    )
    print("Search Results:")
    for i, result in enumerate(search_result):
        print(f"{i + 1}. ID: {result.id}, Score: {result.score}, Payload: {result.payload}")

def list_collections():
    collections = client.get_collections().collections
    print("Available Collections:")
    for collection in collections:
        print(f"- {collection.name}")

def delete_test_collection():
    client.delete_collection(collection_name=COLLECTION_NAME)
    print(f"Collection '{COLLECTION_NAME}' deleted.")

def run_tests():
    print("Running Qdrant database tests...")

    # Step 1: Create a collection
    create_test_collection()

    # Step 2: Process and add textbook data
    vectors, payloads = process_textbook_file()
    if vectors and payloads:
        add_vectors_to_collection(vectors, payloads)

    # Step 3: Search the collection
    search_collection()

    # Step 4: List all collections
    list_collections()

    # Step 5: Delete the test collection
    delete_test_collection()
    print("Tests completed.")

if __name__ == "__main__":
    run_tests()