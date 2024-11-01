from dotenv import load_dotenv # Allows you to load environment variables from a .env file
import os # Allows you to access environment variables

load_dotenv() # Loads environment variables

# Make sure you have a .env file with an API key!
api_key = os.getenv("OPENAI_API_KEY") # Retrieves the API key from the .env file

from langchain_openai import OpenAI # Creates an instance of OpenAI's language model ("It's a ChatGPT!")
from langchain_core.runnables.base import RunnableSequence # Used to chain together runnable components such as prompts and models, to let you invoke sequentially
from langchain.prompts import PromptTemplate  # Allows you to create templates for prompts you send to the model

class TutorAI:

    def __init__(self, temp=0.7):
        # Initialize OpenAI's model with desired temperature, which defines the randomness of the output. Higher = more random!
        self.llm = OpenAI(temperature=temp)

        self.__prompt_init()

    def __prompt_init(self):
        # Define a prompt template for summarization
        self.sum_template = "Summarize the following text:\n\n{text}\n\nSummary:"
        self.sum_prompt = PromptTemplate(input_variables=["text"], template=self.sum_template)
        self.summarization_chain = RunnableSequence(self.sum_prompt | self.llm) # Set up the summarization chain

        # Define a prompt template for creating questions
        self.question_template = "Create some questions about the following text:\n\n{text}\n\nQuestions:"
        self.question_prompt = PromptTemplate(input_variables=["text"], template=self.question_template)
        self.question_chain = RunnableSequence(self.question_prompt | self.llm)

    # Define a function to summarize an input document
    def summarize_text(self, text):
        summary = self.summarization_chain.invoke({"text": text})
        return summary
    
    # Define a function to summarize an input document
    def quiz_text(self, text):
        summary = self.question_chain.invoke({"text": text})
        return summary
    


my_tutor = TutorAI()

# Example text for summarization
document_text = """
Artificial intelligence (AI) refers to the simulation of human intelligence in machines
that are programmed to think like humans and mimic their actions. The term may also be
applied to any machine that exhibits traits associated with a human mind such as learning
and problem-solving.
"""

# Summarize the text
summary = my_tutor.summarize_text(document_text)
print("Summary:", summary)

# Ask questions about the text
questions = my_tutor.quiz_text(document_text)
print("Questions:", questions)