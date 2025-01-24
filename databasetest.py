from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, CollectionParams, Field
import numpy as np
from uuid import uuid4

class QdrantCluster:
    def __init__(self, url, api_key):
        # Initialize the Qdrant client with the provided URL and API key
        self.client = QdrantClient(url=url, api_key=api_key)
    
    def read_cluster(self):
        """
        Reads all collections in the cluster and returns their names and attributes.
        """
        try:
            collections = self.client.get_collections()
            collection_data = []
            if collections.collections:
                for collection in collections.collections:
                    data = {
                        "name": collection.name,
                        "vectors_count": collection.vectors_count if hasattr(collection, 'vectors_count') else 'N/A',
                        "fields": dir(collection)  # All available fields/attributes
                    }
                    collection_data.append(data)
            return collection_data
        except Exception as e:
            print(f"Error reading collections: {e}")
            return []

    def find_collection(self, collection_name_or_id):
        """
        Fetches and returns all data from a specific collection by its name or ID.
        """
        try:
            collection = self.client.get_collection(collection_name_or_id)
            if collection:
                # Retrieve all points from the collection
                points = self.client.scroll(collection_name_or_id)
                return points
            else:
                print(f"Collection '{collection_name_or_id}' not found.")
                return []
        except Exception as e:
            print(f"Error retrieving collection '{collection_name_or_id}': {e}")
            return []

    def create_collection(self, collection_name):
        """
        Creates a new collection in the Qdrant cluster.
        """
        try:
            # Check if collection already exists
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]

            if collection_name not in collection_names:
                print(f"Creating collection: {collection_name}")
                
                # Create the collection with vector configuration
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(  # Correct argument name: vectors_config
                        size=300,  # Adjust the vector size as necessary
                        distance="Cosine"  # Adjust the distance metric as necessary
                    )
                )
                print(f"Collection '{collection_name}' created.")
            else:
                print(f"Collection '{collection_name}' already exists.")
        except Exception as e:
            print(f"Error creating collection '{collection_name}': {e}")



    def update_collection(self, collection_name, new_items):
        """
        Adds new items (points) to the specified collection.
        """
        try:
            for item in new_items:
                # Generate a unique ID for each item
                item_id = str(uuid4())
                
                # Example: generating a random vector for the new item (replace with actual data if available)
                vector = np.random.rand(300).tolist()
                
                # Upsert the item into the collection
                self.client.upsert(
                    collection_name=collection_name,
                    points=[{
                        "id": item_id,
                        "vector": vector,
                        "payload": item  # The item payload (data)
                    }]
                )
                print(f"Added item: {item['title']}")
        except Exception as e:
            print(f"Error updating collection '{collection_name}': {e}")

    def delete_collection_data(self, collection_name, ids=None):
        """
        Deletes data from a collection. If no IDs are provided, deletes all data from the collection.
        """
        try:
            if ids is None:
                # Delete all data from the collection
                self.client.delete_collection(collection_name)
                print(f"Deleted all data from collection '{collection_name}'.")
            else:
                # Delete specified data by IDs
                self.client.delete(
                    collection_name=collection_name,
                    ids=ids
                )
                print(f"Deleted data with IDs {ids} from collection '{collection_name}'.")
        except Exception as e:
            print(f"Error deleting data from collection '{collection_name}': {e}")


# Example usage of the QdrantCluster class:
if __name__ == "__main__":
    # Replace with your Qdrant Cloud details
    QDRANT_URL = "https://d78f9534-0fb0-4cc3-a76c-1ccdcd660b1e.eu-central-1-0.aws.cloud.qdrant.io:6333"
    QDRANT_API_KEY = "C8kMn22gHIG0bTa3aRYDeykuNe8VIdo_LnTDisloesyylIqEkDkWag"

    # Instantiate the QdrantCluster class
    qdrant = QdrantCluster(QDRANT_URL, QDRANT_API_KEY)

    # Read all collections
    print("Reading all collections in the cluster:")
    collections = qdrant.read_cluster()
    print(collections)

    # Find a specific collection by name or ID
    collection_name = "movies_80s_90s"
    print(f"Finding collection '{collection_name}':")
    data = qdrant.find_collection(collection_name)
    print(data)

    # Create a new collection
    collection_name = "new_movies"
    print(f"Creating collection '{collection_name}':")
    qdrant.create_collection(collection_name)

    # Add new items to an existing collection
    new_items = [
        {"title": "The Matrix Reloaded", "release_year": 2003, "genre": "Sci-Fi", "director": "Lana Wachowski, Lilly Wachowski"},
        {"title": "The Dark Knight", "release_year": 2008, "genre": "Action, Crime", "director": "Christopher Nolan"}
    ]
    print(f"Updating collection '{collection_name}' with new items:")
    qdrant.update_collection(collection_name, new_items)

    # Delete data from a collection (example: delete specific items by IDs)
    print(f"Deleting data from collection '{collection_name}':")
    qdrant.delete_collection_data(collection_name, ids=[1, 2])

    # Or delete all data from the collection
    # qdrant.delete_collection_data(collection_name)
