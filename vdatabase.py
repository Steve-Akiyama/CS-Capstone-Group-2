# first download docker desktop
# to run the code we need 2 terminals. On the first terminal launch docker with this "docker run -p 6333:6333 qdrant/qdrant" line and on the 
# second terminal run the pythin script using "python vdatabase.py"

from qdrant_client import QdrantClient
from qdrant_client.http import models
import numpy as np
import os

# connect to Qdrant database
client = QdrantClient(host="localhost", port=6333) #we need to adjust the host and the port

# fucntion to create a new collection with the contents of the chapter
def create_collection(collection_name, vector_size):
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE)
    )
    print(f"Collection '{collection_name}' created with vector size {vector_size}.")

# function to add vectors into the collection
def add_vectors_to_collection(collection_name, vectors, payloads):
    points = [models.PointStruct(id=i, vector=vector, payload=payload)
              for i, (vector, payload) in enumerate(zip(vectors, payloads))]
    client.upsert(collection_name=collection_name, points=points)
    print(f"Added {len(points)} vectors to collection '{collection_name}'.")

# Function to search for similar vectors
def search_collection(collection_name, query_vector, top_k=5):
    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k
    )
    print("Search Results:")
    for i, result in enumerate(search_result):
        print(f"{i + 1}. ID: {result.id}, Score: {result.score}, Payload: {result.payload}")

# Function to list all collections
def list_collections():
    collections = client.get_collections().collections
    print("Available Collections:")
    for collection in collections:
        print(f"- {collection.name}")

# Function to delete a collection
def delete_collection(collection_name):
    client.delete_collection(collection_name=collection_name)
    print(f"Collection '{collection_name}' deleted.")

# Helper function to generate random vectors for testing
def generate_random_vectors(num_vectors, vector_size):
    vectors = np.random.rand(num_vectors, vector_size).tolist()
    payloads = [{"info": f"Vector {i}"} for i in range(num_vectors)]
    return vectors, payloads

# main function
def main():
    vector_size = 128  # Example vector size. this we probably will need to change
    while True:
        print("\nQdrant Vector Database Management")
        print("1. Create Collection")
        print("2. Add Vectors to Collection")
        print("3. Search Collection")
        print("4. List Collections")
        print("5. Delete Collection")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            collection_name = input("Enter collection name: ")
            create_collection(collection_name, vector_size)
        
        elif choice == '2':
            collection_name = input("Enter collection name: ")
            num_vectors = int(input("Enter the number of vectors to add: "))
            vectors, payloads = generate_random_vectors(num_vectors, vector_size)
            add_vectors_to_collection(collection_name, vectors, payloads)
        
        elif choice == '3':
            collection_name = input("Enter collection name: ")
            query_vector = np.random.rand(vector_size).tolist()  # Example random query vector
            top_k = int(input("Enter the number of results to retrieve: "))
            search_collection(collection_name, query_vector, top_k)
        
        elif choice == '4':
            list_collections()
        
        elif choice == '5':
            collection_name = input("Enter collection name: ")
            delete_collection(collection_name)
        
        elif choice == '0':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()