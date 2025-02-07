"""
------------------------------------------------------------
File: terminal.py
Description:
    This script acts as a terminal frontend for the backend. 
    Should go unused in the final product.

Author: Steven Akiyama
Date: November 2024
Version: 1.0

Usage:
    From parent directory: python backend/terminal.py
    From local directory: python terminal.py 

Future Updates:
    None planned.
------------------------------------------------------------
"""

from tutorai import TutorAI
from qdrant import QdrantConnect

from dotenv import load_dotenv # Allows you to load environment variables from a .env file
import os # Allows you to access environment variables

load_dotenv() # Loads environment variables
openai_api_key = os.getenv("OPENAI_API_KEY") # Retrieves the API key from the .env file
qdrant_api_key = os.getenv("QDRANT_API_KEY") # Retrieves the API key from the .env file
qdrant_url = os.getenv("QDRANT_URL") # Retrieves the API key from the .env file


# Create an instance of the tutor
my_tutor = TutorAI(openai_api_key=openai_api_key, temp=0.5)
my_db = QdrantConnect(host=qdrant_url, api_key=qdrant_api_key)

print(my_db.get_subchapter_from_title("Psychology2e", "1.1 What Is Psychology?"))
print(my_db.get_chapter_from_chapter("Psychology2e", "Chapter 1 Introduction to Psychology"))