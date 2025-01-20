from qdrant_client import QdrantClient
from qdrant_client.http import models
import numpy as np
import os
import re
import uuid

# Connect to Qdrant database
# Initializes the Qdrant client to interact with a locally running Qdrant instance.
client = QdrantClient(host="127.0.0.1", port=6333)

# Helper Functions
def clean_newlines(input_string):
    """Replaces newline escape characters with spaces to make the text more readable."""
    return input_string.replace('\n', ' ')


def preprocess_text_by_subjects(file_path):
    """Splits the text into chunks by detecting subject boundaries such as headings or chapters."""
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
        return []

    try:
        # Open the file and read its content line by line
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        chunks = []  # Store processed text chunks
        current_chunk = []  # Store the current chunk being processed

        for line in lines:
            # Detect potential subject headers (e.g., lines in ALL CAPS, starting with numbers, or specific keywords)
            if line.strip().isupper() or re.match(r'^\d+(\.|:)?\s', line) or re.match(r'^(Chapter|Section|Topic)\s', line, re.IGNORECASE):
                if current_chunk:  # Save the current chunk before starting a new one
                    chunks.append(" ".join(current_chunk).strip())
                    current_chunk = []
            current_chunk.append(line.strip())  # Add the current line to the chunk

        # Add the last chunk if it exists
        if current_chunk:
            chunks.append(" ".join(current_chunk).strip())

        print(f"Text split into {len(chunks)} chunks based on subjects.")
        return chunks
    except Exception as e:
        print(f"Error processing text: {e}")
        return []


def add_textbook_to_qdrant(collection_name, file_path):
    """Processes a textbook and adds its chunks to a specified Qdrant collection."""
    # Preprocess the text file to generate chunks
    chunks = preprocess_text_by_subjects(file_path)
    if not chunks:
        return

    # Generate random vector embeddings for each chunk
    embeddings = [np.random.rand(128).tolist() for _ in chunks]

    # Create data points with unique IDs, embeddings, and text payloads
    points = [
        models.PointStruct(
            id=str(uuid.uuid4()),  # Generate a unique ID for each point
            vector=embedding,      # Assign the random embedding
            payload={"text": chunk, "chunk_index": i}  # Store the chunk and its index as metadata
        )
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
    ]

    # Recreate the collection in Qdrant with specified vector size and distance metric
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=128, distance=models.Distance.COSINE)
    )
    # Insert the points into the collection
    client.upsert(collection_name=collection_name, points=points)
    print(f"Added {len(points)} chunks to collection '{collection_name}'.")

# CRUD Operations
def create_collection(collection_name, vector_size=128):
    """Creates a new collection in Qdrant with the specified vector size."""
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE)
    )
    print(f"Collection '{collection_name}' created with vector size {vector_size}.")


def list_collections():
    """Lists all existing collections in Qdrant."""
    # Fetch and display all collections
    collections = client.get_collections().collections
    print("Available Collections:")
    for collection in collections:
        print(f"- {collection.name}")


def delete_collection(collection_name):
    """Deletes a specified collection from Qdrant."""
    client.delete_collection(collection_name=collection_name)
    print(f"Collection '{collection_name}' deleted.")


def add_collection_from_file():
    """Prompts the user to create a new collection from a text file."""
    # Get the collection name and file path from the user
    collection_name = input("Enter the name of the new collection: ")
    filename = input("Enter the name of the text file to add (e.g., textbook.txt): ")

    # Check if the file exists
    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' not found.")
        return

    try:
        # Process the file into chunks
        chunks = preprocess_text_by_subjects(filename)
        # Recreate the collection if it already exists
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
    """Adds new chunks to an existing Qdrant collection."""
    # Create data points with random embeddings and add them to the collection
    points = [
        models.PointStruct(
            id=str(uuid.uuid4()),  # Generate a unique ID for each point
            vector=np.random.rand(128).tolist(),  # Generate a random vector for each chunk
            payload={"text": chunk}  # Store the chunk as metadata
        )
        for chunk in new_chunks
    ]
    client.upsert(collection_name=collection_name, points=points)
    print(f"Added {len(points)} chunks to collection '{collection_name}'.")

# Test Function
def test_preprocess_text_by_subjects():
    """Tests the text preprocessing function using a sample file."""
    file_path = "textbook.txt"  # Specify a sample file for testing
    chunks = preprocess_text_by_subjects(file_path)  # Process the file into chunks
    print(f"Generated {len(chunks)} chunks.")
    # Display the first 5 chunks for verification
    for idx, chunk in enumerate(chunks[:5]):
        print(f"\nChunk {idx + 1}:\n{chunk}\n")

# Main Menu
def main_menu():
    """Interactive menu for managing Qdrant collections."""
    while True:
        # Display menu options
        print("\nQdrant Vector Database Management")
        print("1. List Collections")
        print("2. Create Collection")
        print("3. Delete Collection")
        print("4. Add Collection from File")
        print("5. Add Textbook to Qdrant")
        print("6. Test Textbook Preprocessing")
        print("0. Exit")
        # Get user input for menu choice
        choice = input("Enter your choice: ")

        # Execute the corresponding function based on user choice
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
            chunks = preprocess_text_by_subjects(file_path)
            for idx, chunk in enumerate(chunks[:3]):
                print(f"\nChunk {idx + 1}:\n{chunk}\n")
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Start the main menu
    main_menu()