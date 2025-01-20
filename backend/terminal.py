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

from dotenv import load_dotenv # Allows you to load environment variables from a .env file
import os # Allows you to access environment variables

load_dotenv() # Loads environment variables

# Make sure you have a .env file with an API key!
api_key = os.getenv("OPENAI_API_KEY") # Retrieves the API key from the .env file


# Create an instance of the tutor
my_tutor = TutorAI(api_key=api_key, temp=0.5)

# Summarize the text
# summary = my_tutor.summarize_text(my_tutor.document_text)
# print("Summary:", summary)

# my_tutor.shortanswer_complete_terminal(my_tutor.document_text, 5)
question_set = my_tutor.multiplechoice_questions(my_tutor.document_text, 3)

print(question_set)

for question in question_set:
    print(question[:-1])
    if my_tutor.multiplechoice_evaluate(question, input()):
        print("Congrats! You got it correct.")
    else:
        print("Sorry, wrong answer! The correct answer was " + question[-1])