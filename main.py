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

        # Initalize prompts
        self.__prompt_init()

        # Import or create textbook text
        self.document_text = """
        Artificial intelligence (AI) refers to the simulation of human intelligence in machines
        that are programmed to think like humans and mimic their actions. The term may also be
        applied to any machine that exhibits traits associated with a human mind such as learning
        and problem-solving.
        """

    def __prompt_init(self):
        # Define a prompt template for summarization
        self.sum_template = "Summarize the following text:\n\n{text}\n\nSummary:"
        self.sum_prompt = PromptTemplate(input_variables=["text"], template=self.sum_template)
        self.summarization_chain = RunnableSequence(self.sum_prompt | self.llm) # Set up the summarization chain

        # Define a prompt template for creating questions
        self.question_template = "Create {count} questions about the following text, separated by a newline:\n\n{text}\n\nQuestions:"
        self.question_prompt = PromptTemplate(input_variables=["text"], template=self.question_template)
        self.question_chain = RunnableSequence(self.question_prompt | self.llm)

        # Define a prompt for evaluating answers
        self.evaluation_template = """Use the following text:\n\n{text}\n\nTo evaluate the following question and answer. 
        Please evaluate the answer based on the text with a score of 1-10 and an explanation for your score, in key-value pairs. 
        Question:\n\n{question}\n\n
        Answer:\n\n{answer}\n\n
        Evaluation:"""
        self.evaluation_prompt = PromptTemplate(input_variables=["text", "question", "answer"], template=self.evaluation_template)
        self.evaluation_chain = RunnableSequence(self.evaluation_prompt | self.llm)

    # Define a function to summarize an input document
    def summarize_text(self, text):
        summary = self.summarization_chain.invoke({"text": text})
        return summary
    
    # Define a function to summarize an input document
    def quiz_text(self, text, count):
        questions = self.question_chain.invoke({"count": count, "text": text}) # Get the set of questions
        question_set = questions.rstrip().split('\n') # Split the questions into a list
        question_set.remove('')
        question_set.remove(' ')

        return question_set
    
    # Define a function to evaluate an answer
    def evaluate_answer(self, text, question, answer):
        evaluation = self.evaluation_chain.invoke({"text": text, "question": question, "answer": answer})
        # print(evaluation)
        # eval_set = evaluation.rstrip().split('\n', 2)
        # evaluation = {"score": eval_set[0], "explanation": eval_set[1]}
        return evaluation

# Create an instance of the tutor
my_tutor = TutorAI()

# Summarize the text
summary = my_tutor.summarize_text(my_tutor.document_text)
print("Summary:", summary)

# Ask questions about the text
question_set = my_tutor.quiz_text(my_tutor.document_text, 5)
print("Questions:", question_set)

# For every question, prompt the user for an answer
for question in question_set:
    answer = input("\n\n" + question + "\nAnswer: ")
    evaluation = my_tutor.evaluate_answer(my_tutor.document_text, question, answer)
    print(evaluation)