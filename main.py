from tutorai import TutorAI

from dotenv import load_dotenv # Allows you to load environment variables from a .env file
import os # Allows you to access environment variables

load_dotenv() # Loads environment variables

# Make sure you have a .env file with an API key!
api_key = os.getenv("OPENAI_API_KEY") # Retrieves the API key from the .env file



# Create an instance of the tutor
my_tutor = TutorAI(api_key=api_key, temp=0.3, topic="Psychology")

# Summarize the text
# summary = my_tutor.summarize_text(my_tutor.document_text)
# print("Summary:", summary)

my_tutor.shortanswer_complete_terminal(my_tutor.document_text, 5)