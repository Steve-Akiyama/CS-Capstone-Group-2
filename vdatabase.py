from qdrant_client import QdrantClient
from qdrant_client.http import models
import numpy as np
import os
import re
import uuid


# Connect to Qdrant database
client = QdrantClient(host="127.0.0.1", port=6333)

# Helper Functions
def clean_newlines(input_string):
    """Replaces newline escape characters with spaces."""
    return input_string.replace('\n', ' ')


def preprocess_text_by_subjects(file_path):
    """Splits the text into chunks by detecting subject boundaries."""
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()  # Read the file line by line

        chunks = []
        current_chunk = []

        for line in lines:
            # Detect potential subject headers (e.g., lines in ALL CAPS or starting with numbers)
            if line.strip().isupper() or re.match(r'^\d+(\.|:)?\s', line) or re.match(r'^(Chapter|Section|Topic)\s', line, re.IGNORECASE):
                if current_chunk:  # Save the current chunk before starting a new one
                    chunks.append(" ".join(current_chunk).strip())
                    current_chunk = []
            current_chunk.append(line.strip())

        # Add the last chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk).strip())

        print(f"Text split into {len(chunks)} chunks based on subjects.")
        return chunks
    except Exception as e:
        print(f"Error processing text: {e}")
        return []

def add_textbook_to_qdrant(collection_name, file_path):
    """Processes a textbook and adds chunks to Qdrant."""
    chunks = preprocess_text_by_subjects(file_path)
    if not chunks:
        return

    # Generate random embeddings for simplicity
    embeddings = [np.random.rand(128).tolist() for _ in chunks]

    points = [
        models.PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": chunk, "chunk_index": i}
        )
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
    ]

    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=128, distance=models.Distance.COSINE)
    )
    client.upsert(collection_name=collection_name, points=points)
    print(f"Added {len(points)} chunks to collection '{collection_name}'.")

# CRUD Operations
def create_collection(collection_name, vector_size=128):
    """Creates a new collection in Qdrant."""
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE)
    )
    print(f"Collection '{collection_name}' created with vector size {vector_size}.")

def list_collections():
    """Lists all collections in Qdrant."""
    collections = client.get_collections().collections
    print("Available Collections:")
    for collection in collections:
        print(f"- {collection.name}")

def delete_collection(collection_name):
    """Deletes a collection."""
    client.delete_collection(collection_name=collection_name)
    print(f"Collection '{collection_name}' deleted.")

def add_collection_from_file():
    """Adds a collection by reading a text file and processing it into chunks."""
    collection_name = input("Enter the name of the new collection: ")
    filename = input("Enter the name of the text file to add (e.g., textbook.txt): ")

    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' not found.")
        return

    try:
        chunks = preprocess_text_by_subjects(filename)  # Correct function for subject splitting
        if client.collection_exists(collection_name):
            print(f"Collection '{collection_name}' already exists. Recreating...")
            client.delete_collection(collection_name=collection_name)
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=128, distance=models.Distance.COSINE)
        )
        print(f"Collection '{collection_name}' created. Adding chunks...")
        add_to_collection(collection_name, chunks)
        print(f"Successfully added {len(chunks)} chunks from '{filename}' to the '{collection_name}' collection.")
    except Exception as e:
        print(f"Error: {e}")

def add_to_collection(collection_name, new_chunks):
    """Adds chunks to an existing collection."""
    points = [
        models.PointStruct(
            id=str(uuid.uuid4()),  # Generate a valid UUID for each point ID
            vector=np.random.rand(128).tolist(),  # Example: Random 128-dimensional vector
            payload={"text": chunk}  # Add the chunk as payload
        )
        for chunk in new_chunks
    ]
    client.upsert(collection_name=collection_name, points=points)
    print(f"Added {len(points)} chunks to collection '{collection_name}'.")

# Test Function
def test_preprocess_text_by_subjects():
    file_path = "textbook.txt"  # Ensure this file exists with your sample text
    chunks = preprocess_text_by_subjects(file_path)  # Correct function call
    print(f"Generated {len(chunks)} chunks.")
    for idx, chunk in enumerate(chunks[:5]):  # Display the first 5 chunks for verification
        print(f"\nChunk {idx + 1}:\n{chunk}\n")

# Main Menu
def main_menu():
    """Main menu for Qdrant vector database management."""
    while True:
        print("\nQdrant Vector Database Management")
        print("1. List Collections")
        print("2. Create Collection")
        print("3. Delete Collection")
        print("4. Add Collection from File")
        print("5. Add Textbook to Qdrant")
        print("6. Test Textbook Preprocessing")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            list_collections()
        elif choice == '2':
            collection_name = input("Enter the name of the new collection: ")
            create_collection(collection_name)
        elif choice == '3':
            collection_name = input("Enter the name of the collection to delete: ")
            delete_collection(collection_name)
        elif choice == '4':
            add_collection_from_file()
        elif choice == '5':
            collection_name = input("Enter the collection name: ")
            file_path = input("Enter the path to the textbook file: ")
            add_textbook_to_qdrant(collection_name, file_path)
        elif choice == '6':
            file_path = input("Enter the path to the textbook file: ")
            chunks = preprocess_text_by_subjects(file_path)  # Correct function call
            for idx, chunk in enumerate(chunks[:3]):  # Display first 3 chunks
                print(f"\nChunk {idx + 1}:\n{chunk}\n")
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
