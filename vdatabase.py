# Steps to Access and Use the Qdrant Database:

# 1. **Access the AWS EC2 Instance:**
#    - To access the EC2 instance where Qdrant is hosted, open your terminal and run:
#      ssh -i "Capstonekeypair.pem" ec2-user@18.117.232.211
#    - This connects to the EC2 instance using the provided `.pem` file.

# 2. **Verify Qdrant is Running on EC2:**
#    - Once connected to the EC2 instance, ensure Qdrant is running by executing:
#      curl http://127.0.0.1:6333
#    - If successful, you will see a response like:
#      {"title":"qdrant - vector search engine","version":"1.12.4","commit":"5b578c4f34188f0474f901e49d4726213596433d"}

# 3. **Test External Access to Qdrant (EC2):**
#    - On your local machine or browser, access the Qdrant service using the EC2 public IP:
#      http://18.117.232.211:6333
#    - If the setup is correct, you will see the same JSON response as above.

# 4. **Run the Python Script to Interact with Qdrant (Hosted on EC2):**
#    - The Python script is designed to manage Qdrant collections and vectors. Ensure the following setup:
#      - The Qdrant client in the script is configured to use the EC2 public IP and port:
#        client = QdrantClient(host="18.117.232.211", port=6333)
#    - Run the script from your local machine using:
#      python vdatabase.py
#    - Follow the menu prompts to:
#      1. Create a collection
#      2. Add vectors to a collection
#      3. Search collections for similar vectors
#      4. List all collections
#      5. Delete collections

# 5. **Run Qdrant Locally on Your Computer (Optional):**
#    - If you prefer to run Qdrant on your local machine, follow these steps:
#      1. **Install Docker Desktop**:
#         - Download and install Docker Desktop from https://www.docker.com/products/docker-desktop/.
#      2. **Pull the Qdrant Docker Image**:
#         - Open a terminal and run:
#           docker pull qdrant/qdrant
#      3. **Start the Qdrant Service**:
#         - Run the Qdrant container on your local machine:
#           docker run -p 6333:6333 qdrant/qdrant
#      4. **Verify Qdrant is Running Locally**:
#         - Open a browser and navigate to:
#           http://127.0.0.1:6333
#         - You should see the JSON response:
#           {"title":"qdrant - vector search engine","version":"1.12.4","commit":"5b578c4f34188f0474f901e49d4726213596433d"}

# 6. **Run the Python Script Locally with Local Qdrant:**
#    - If Qdrant is running on your local machine, update the Python script to use the local Qdrant host:
#      client = QdrantClient(host="127.0.0.1", port=6333)
#    - Run the script using:
#      python vdatabase.py
#    - This connects to the local Qdrant service and provides the same functionality.

# 7. **Allow Others to Access Qdrant (EC2):**
#    - For external users to access Qdrant hosted on EC2, share the public IP and port:
#      - URL: http://18.117.232.211:6333
#    - Ensure the EC2 instance’s security group (ID: sg-0a74a55e3b79b7008) allows inbound traffic on port 6333.

# 8. **Verify Connectivity from Other Machines:**
#    - Users can test connectivity by opening the URL in a browser or running:
#      curl http://18.117.232.211:6333
#    - If they see the JSON response, Qdrant is accessible.

# 9. **Troubleshooting:**
#    - If access fails:
#      1. Confirm the EC2 instance is running and Qdrant is active.
#      2. Verify the security group allows inbound traffic on port 6333.
#      3. Ensure no network/firewall restrictions are blocking access.

# With this setup, Qdrant can be run and accessed either on the EC2 instance or locally on your computer.


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

def split_text_with_context(text):
    """Splits the text into sentences and groups them with context."""
    sentence_endings = r'(?<=[.!?])\s+'
    sentences = re.split(sentence_endings, text)
    chunks_with_context = []
    for i, sentence in enumerate(sentences):
        preceding = sentences[max(0, i-2):i]  # Two preceding sentences
        following = sentences[i+1:i+2]       # One following sentence
        chunk = " ".join(preceding + [sentence] + following)
        chunks_with_context.append(chunk)
    return chunks_with_context

def process_string_to_chunks(input_string):
    """Processes a string into contextual chunks."""
    cleaned_string = clean_newlines(input_string)
    return split_text_with_context(cleaned_string)

def generate_random_vectors(num_vectors, vector_size):
    """Generates random vectors for testing."""
    vectors = np.random.rand(num_vectors, vector_size).tolist()
    payloads = [{"info": f"Vector {i}"} for i in range(num_vectors)]
    return vectors, payloads

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

def search_collection(collection_name, query_vector, top_k=5):
    """Searches for similar vectors in a collection."""
    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k
    )
    print("Search Results:")
    for i, result in enumerate(search_result):
        print(f"{i + 1}. ID: {result.id}, Score: {result.score}, Payload: {result.payload}")

def add_collection_from_file():
    """Adds a collection by reading a text file and processing it into chunks."""
    collection_name = input("Enter the name of the new collection: ")
    filename = input("Enter the name of the text file to add (e.g., textbook.txt): ")

    if not os.path.isfile(filename):
        print(f"Error: File '{filename}' not found.")
        return

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            chunks = process_string_to_chunks(content)
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


def main_menu():
    """Main menu for Qdrant vector database management."""
    while True:
        print("\nQdrant Vector Database Management")
        print("1. List Collections")
        print("2. Create Collection")
        print("3. Delete Collection")
        print("4. Add Collection from File")
        print("5. Search Collection")
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
            collection_name = input("Enter the name of the collection to search: ")
            query_vector = np.random.rand(128).tolist()  # Example query vector
            top_k = int(input("Enter the number of results to retrieve: "))
            search_collection(collection_name, query_vector, top_k)
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()