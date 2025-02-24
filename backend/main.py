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
    When live, will need to modify allow_origins to accommodate 
    the actual link. Will also need to add features as TutorAI gains them.
------------------------------------------------------------
"""

from tutorai import TutorAI
from qdrant import QdrantConnect

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import Depends # Currently unused
from logger import logger

from dotenv import load_dotenv # Allows you to load environment variables from a .env file
import os # Allows you to access environment variables
import uvicorn
from fastapi.responses import FileResponse
import os

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
# Returns a new TutorAI      #
##############################
def get_tutor():
    tutor = TutorAI(openai_api_key=openai_api_key, temp=0.3)
    # tutor.set_document_text(my_db.get_subchapter_from_title("Psychology2e", "1.1 What Is Psychology?"))
    return tutor

def qdrant_search(cluster, section):
    # Response includes text, chapter, title
    response = my_db.get_subchapter_from_section(cluster, section)
    
    return response

backend_router = APIRouter()

# Define a basic route for testing
@backend_router.get("/")
def read_root():
    return {"message": "Hello, World!"}

@backend_router.get("/generate-summary-and-questions")
async def generate_summary_and_questions(section: str = "1.1"):
    # Get a response for the current section
    logger.debug(f"Section: {section}")
    response = qdrant_search("Psychology2e", section)
    
    # Retrieve summary and questions
    summary = my_tutor.summarize_text(text="Section " + str(section) + " of " + response["chapter"] + ": " + response["text"])
    questions = my_tutor.shortanswer_questions(5, text=summary)

    # Return the summary and questions
    return{"summary": summary, "questions": questions}

# Define the Query model to accept question, user answer and summary
class Query(BaseModel):
    question: str
    user_answer: str
    summary: str
    user_id: str
    id: str

@backend_router.post("/query")
async def query_llm(query: Query):
    # Extract the question and user answer from the request body
    user_question = query.question
    user_answer = query.user_answer
    summary = query.summary
    user_id = query.user_id
    id = query.id

    # Process the question and user answer with your tutor instance
    # Assuming `my_tutor.process_query` handles both the question and answer
    response, score = my_tutor.shortanswer_evaluate(user_question, user_answer, text=summary)

    logger.info(f"User ID: {id}.{user_id} Q/A: {user_question} / {user_answer} | Score: {score.strip()} Evaluation: {response.strip()}")

    return {"response": response, "score": score}

app.include_router(backend_router, prefix="/tutorai/api")

# Serve favicon.ico explicitly
@app.get("/favicon.ico")
async def favicon():
    if os.path.exists("favicon.ico"):
        return FileResponse("favicon.ico")
    else:
        return {"message": "Favicon not found."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
