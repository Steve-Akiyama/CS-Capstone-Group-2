"""
Qdrant Textbook Chunking and Management Script
===============================================

This script processes textbook files into logical chunks based on sections and headings, 
generates vector embeddings, and stores them in a Qdrant vector database. It also includes
CRUD operations for managing Qdrant collections.

Prerequisites:
--------------
1. Install Python 3.6 or later.
2. Install required libraries:
   - qdrant-client: `pip install qdrant-client`
   - numpy: `pip install numpy`
3. Run a Qdrant instance locally or remotely:
   - For local setup, use Docker:
     `docker run -p 6333:6333 qdrant/qdrant`
4. Prepare a text file (e.g., `textbook.txt`) containing the content to process.

How to Run:
-----------
1. Save this script as `qdrant_management.py`.
2. Run the script in your terminal:
   `python qdrant_management.py`
3. Follow the interactive menu to perform tasks:
   - Option 1: List existing collections.
   - Option 2: Create a new collection in Qdrant.
   - Option 3: Delete an existing collection.
   - Option 4: Add a textbook to Qdrant.
   - Option 5: Test the textbook chunking process.
   - Option 0: Exit the program.

Example Workflow:
-----------------
1. Start a local Qdrant instance using Docker.
2. Use Option 4 to upload `textbook.txt` to a collection.
3. Verify uploaded collections with Option 1.
4. Retrieve or manage collections using Options 2 or 3.

Notes:
------
- Ensure the text file is in the same directory or provide the full path.
- Edit the `file_path` variable in test functions as needed.
"""

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
    """Splits the text into chunks by detecting section boundaries."""
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        chunks = []
        current_chunk = []
        section_header = None

        for line in lines:
            # Detect main sections or subsections
            if re.match(r'^\d+\.\d+\s', line) or line.strip().isupper():
                # Save the current chunk with its section header
                if current_chunk:
                    chunks.append({
                        "title": section_header.strip() if section_header else "Untitled",
                        "content": " ".join(current_chunk).strip()
                    })
                    current_chunk = []
                section_header = line.strip()  # Update the current section header
            elif re.match(r'^LEARNING OBJECTIVES|FIGURE|LINK TO LEARNING|NOTABLE RESEARCHERS', line, re.IGNORECASE):
                # Treat these as sub-sections
                if current_chunk:
                    chunks.append({
                        "title": section_header.strip() if section_header else "Untitled",
                        "content": " ".join(current_chunk).strip()
                    })
                    current_chunk = []
                section_header = line.strip()
            else:
                current_chunk.append(line.strip())

        # Add the final chunk
        if current_chunk:
            chunks.append({
                "title": section_header.strip() if section_header else "Untitled",
                "content": " ".join(current_chunk).strip()
            })

        print(f"Text split into {len(chunks)} chunks based on textbook structure.")
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
            payload={"text": chunk['content'], "title": chunk['title'], "chunk_index": i}  # Store the chunk metadata
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

# Test Function
def test_preprocess_text_by_subjects():
    """Tests the text preprocessing function using a sample file."""
    file_path = "textbook.txt"  # Specify a sample file for testing
    chunks = preprocess_text_by_subjects(file_path)  # Process the file into chunks
    print(f"Generated {len(chunks)} chunks.")
    # Display the first 5 chunks for verification
    for idx, chunk in enumerate(chunks[:5]):
        print(f"\nChunk {idx + 1}:\nTitle: {chunk['title']}\nContent: {chunk['content']}\n")

# Main Menu
def main_menu():
    """Interactive menu for managing Qdrant collections."""
    while True:
        # Display menu options
        print("\nQdrant Vector Database Management")
        print("1. List Collections")
        print("2. Create Collection")
        print("3. Delete Collection")
        print("4. Add Textbook to Qdrant")
        print("5. Test Textbook Preprocessing")
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
            collection_name = input("Enter the collection name: ")
            file_path = input("Enter the path to the textbook file: ")
            add_textbook_to_qdrant(collection_name, file_path)
        elif choice == '5':
            file_path = input("Enter the path to the textbook file: ")
            test_preprocess_text_by_subjects()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Start the main menu
    main_menu()