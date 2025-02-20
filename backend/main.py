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

import json

from dotenv import load_dotenv # Allows you to load environment variables from a .env file
import os # Allows you to access environment variables

load_dotenv() # Loads environment variables
api_key = os.getenv("OPENAI_API_KEY") # Retrieves the API key from the .env file

# Retrieve the environment variable for the frontend and backend URLs
environment = os.getenv("ENVIRONMENT", "local")
if environment == "production":
    frontend_url = os.getenv("FRONTEND_URL_PRODUCTION")
    backend_url = os.getenv("BACKEND_URL_PRODUCTION")
else:
    frontend_url = os.getenv("FRONTEND_URL_LOCAL")
    backend_url = os.getenv("BACKEND_URL_LOCAL")

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
    allow_origins=[frontend_url],  # Adjust to your frontend URL
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
    questions = my_tutor.shortanswer_questions(5, my_tutor.document_text)
    mcq = my_tutor.multiplechoice_questions(5, my_tutor.document_text)
    return{"summary": summary, "questions": questions, "mcq": mcq}

@app.get("/retrieve-document")
async def retrieve_document():
    document = my_tutor.document_text
    return {"document": document}

@app.get("/generate-questions")
async def generate_questions():
    questions = my_tutor.shortanswer_questions(5, my_tutor.document_text)
    mcq = my_tutor.multiplechoice_questions(5, my_tutor.document_text)
    tf = my_tutor.truefalse_questions(5, my_tutor.document_text)
    return{"questions": questions, "mcq": mcq, "tf": tf}
    

# Define the Query model to accept question and user_answer
class Query(BaseModel):
    question: str
    user_answer: str

@app.post("/query")
async def query_llm(query: Query):
    # Extract the question and user answer from the request body
    user_question = query.question
    user_answer = query.user_answer

    question = user_question.split("$%^")
    print(question)

    q_type = "mcq"
    try:
        question[5]
    except:
        try:
            q_type = "tf"
            question[3]
        except:
            q_type = "short_ans"

    # Process the question and user answer with your tutor instance
    # Assuming `my_tutor.process_query` handles both the question and answer
    if (q_type == "short_ans"):
        response, score = my_tutor.shortanswer_evaluate(user_question, user_answer)
    if (q_type == "mcq"):
        response, score = my_tutor.multiplechoice_evaluate(user_question, user_answer)
    if (q_type == "tf"):
        response, score = my_tutor.truefalse_evaluate(user_question, user_answer)

    return {"response": response, "score": score}
