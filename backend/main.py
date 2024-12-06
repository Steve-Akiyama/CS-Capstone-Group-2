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
from fastapi import FastAPI
from pydantic import BaseModel
from tutorai import TutorAI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import Depends

from dotenv import load_dotenv # Allows you to load environment variables from a .env file
import os # Allows you to access environment variables

load_dotenv() # Loads environment variables
api_key = os.getenv("OPENAI_API_KEY") # Retrieves the API key from the .env file

app = FastAPI()
my_tutor = TutorAI(api_key=api_key, temp=0.3)

# Dependancy to create a new instance of TutorAI for each request
def get_tutor():
    return TutorAI(api_key=api_key, temp=0.3) # Creates an instance of TutorAI

class Query(BaseModel):
    question: str

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define a basic route for testing
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/generate-summary-and-questions")
async def generate_summary_and_questions():
    summary = my_tutor.summarize_text()
    questions = my_tutor.shortanswer_questions(5, text=summary)
    return{"summary": summary, "questions": questions}

@app.get("/retrieve-document")
async def retrieve_document():
    document = my_tutor.document_text
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
