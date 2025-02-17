"""
------------------------------------------------------------
File: main.py
Description:
    Acts as a backend for TutorAI

Author: Steven Akiyama
Date: 05
Version: 1.0

Usage:
    Handles API calls from the front-end

Future Updates:
    When live, will need to modify allow_origins to accomadate 
    the actual link. Will also need add features as TutorAI gains them.
------------------------------------------------------------
"""
from tutorai import TutorAI
from qdrant import QdrantConnect

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import Depends

from dotenv import load_dotenv # Allows you to load environment variables from a .env file
import os # Allows you to access environment variables


##############################
# Environment Variables      #
##############################
load_dotenv() 
openai_api_key = os.getenv("OPENAI_API_KEY") # Retrieves the API key from the .env file
qdrant_api_key = os.getenv("QDRANT_API_KEY") # Retrieves the API key from the .env file
qdrant_link = os.getenv("QDRANT_URL") # Retrieves the API key from the .env file
environment = os.getenv("ENVIRONMENT", "local")
if environment == "production":
    frontend_url = os.getenv("FRONTEND_URL_PRODUCTION")
    backend_url = os.getenv("BACKEND_URL_PRODUCTION")
else:
    frontend_url = os.getenv("FRONTEND_URL_LOCAL")
    backend_url = os.getenv("BACKEND_URL_LOCAL")

##############################
# Initialize Instances       #
##############################
app = FastAPI()
my_tutor = TutorAI(openai_api_key=openai_api_key, temp=0.3)
my_db = QdrantConnect(host=qdrant_link, api_key=qdrant_api_key)

##############################
# Add CORS Middleware        #
##############################
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],  # Adjust to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

##############################
# Setup Document (Temporary) #
##############################
active_document = my_db.get_subchapter_from_section("Psychology2e", "6.1")


##############################
# Returns a new TutorAI      #
##############################
def get_tutor():
    tutor = TutorAI(openai_api_key=openai_api_key, temp=0.3)
    # tutor.set_document_text(my_db.get_subchapter_from_title("Psychology2e", "1.1 What Is Psychology?"))
    return tutor

class Query(BaseModel):
    question: str

# Define a basic route for testing
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/generate-summary-and-questions")
async def generate_summary_and_questions(section: str = "6.1"):
    # Update the currently active document
    active_document = my_db.get_subchapter_from_section("Psychology2e", section)
    
    # Retrieve summary and questions
    summary = my_tutor.summarize_text(text=active_document)
    questions = my_tutor.shortanswer_questions(5, text=active_document)

    # Return the summary and questions
    return{"summary": summary, "questions": questions}

@app.get("/retrieve-document")
async def retrieve_document():
    document = active_document
    return {"document": document}

# Define the Query model to accept question and user_answer
class Query(BaseModel):
    question: str
    user_answer: str

@app.post("/query")
async def query_llm(query: Query):
    # Extract the question and user answer from the request body
    user_question = query.question
    user_answer = query.user_answer

    # Process the question and user answer with your tutor instance
    # Assuming `my_tutor.process_query` handles both the question and answer
    response, score = my_tutor.shortanswer_evaluate(user_question, user_answer)

    return {"response": response, "score": score}