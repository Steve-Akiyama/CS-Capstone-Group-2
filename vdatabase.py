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

# connect to Qdrant database
client = QdrantClient(host="127.0.0.1", port=6333)

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