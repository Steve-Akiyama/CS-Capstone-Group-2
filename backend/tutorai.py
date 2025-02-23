from langchain_openai import OpenAI # Creates an instance of OpenAI's language model ("It's a ChatGPT!")
from langchain_core.runnables.base import RunnableSequence # Used to chain together runnable components such as prompts and models, to let you invoke sequentially
from langchain.prompts import PromptTemplate  # Allows you to create templates for prompts you send to the model
import re
from logger import logger

class TutorAI:
    """
    Description: To make calls to OpenAI's API.

    Attributes:
    ----------
    api_key : str
        API key for OpenAI's API
    temp : float
        Determinicity of the LLM responses.
    rec_accuracy : float
        Recommended accuracy for answers and responses.
    req_accuracy : float
        Required accuracy for answers and responses.
    system_message : str
        Startup message at the beginning of given prompts. 

    Methods:
    -------
    summarize_text()
        Summarizes the text inputted.
    shortanswer_questions()
        Creates short answer questions about the text inputted.
    multiplechoice_questions()
        Creates multiple-choice questions about the text inputted.
    shortanswer_evaluate()
        Evaluates short answer question and answer pairs.
    """
    
    def __init__(self, openai_api_key="", temp=0.5, rec_accuracy=0.85, req_accuracy=0.6, system_message="You are a kind and helpful tutor teaching me, a student."):
        # Initialize OpenAI's model with desired temperature, which defines the randomness of the output. Higher = more random!
        self.__llm = OpenAI(temperature=temp, api_key=openai_api_key, max_tokens=1096)

        # Initalizes some base variables
        self.rec_accuracy = rec_accuracy
        self.req_accuracy = req_accuracy
        self.system_message = system_message

        # Initalize prompts
        self.__prompt_init()

    def __prompt_init(self):
        """
        Initalizes the prompt templates.

        Parameters:
        ----------
        None

        Returns:
        -------
        None

        Raises:
        ------
        None

        """
        # Summarization
        sum_template = self.system_message + " Give a list of learning objectives, then an extensive summary about the following text. Be thorough, and make sure you don't leave out details. Text:\n\n{text}\n\nSummary:"
        sum_prompt = PromptTemplate(input_variables=["text"], template=sum_template)
        self.summarization_chain = RunnableSequence(sum_prompt | self.__llm) # Set up the summarization chain

        # Short-Answer Questions
        shortanswer_question_template = self.system_message + " You are tasked with asking students {count} questions about the content within the following text. Please make sure you address each learning objective.:\n\n{text}\n\nQuestions should be seperated by a new line. Questions:"
        shortanswer_question_prompt = PromptTemplate(input_variables=["text"], template=shortanswer_question_template)
        self.shortanswer_question_chain = RunnableSequence(shortanswer_question_prompt | self.__llm)

        # Multiple-Choice Questions
        multiplechoice_question_template = self.system_message + " Create {count} multiple-choice questions about the text. The format should be as follows: \"Question 1: <Insert Question>\"\"A) <Answer A>\"\"B) <Answer B>\"\"C) <Answer C>\"\"D) <Answer D>\"\"Correct Answer: <Letter of correct answer> Text:\n\n{text}\n\n"
        multiplechoice_question_prompt = PromptTemplate(input_variables=["text"], template=multiplechoice_question_template)
        self.multiplechoice_question_chain = RunnableSequence(multiplechoice_question_prompt | self.__llm)

        # Short-Answer Evaluation
        shortanswer_evaluation_template = self.system_message + " Use the following text:\n\n{text}\n\nTo evaluate the following question and answer, directing the evaluation me, your student. Please evaluate the answer based on the text with a score of 1-10 and a short explanation for your score, quoting the text if necessary. Question:\n\n{question}\n\n Student's answer:\n\n{answer}\n\n The template should look like this: Score:\nEvaluation:"
        shortanswer_evaluation_prompt = PromptTemplate(input_variables=["text", "question", "answer"], template=shortanswer_evaluation_template)
        self.shortanswer_evaluation_chain = RunnableSequence(shortanswer_evaluation_prompt | self.__llm)

    def summarize_text(self, text):
        """
        Summarizes text through OpenAI's API
    
        Parameters:
        ----------
        text : str
            Text to be summarized. 
    
        Returns:
        -------
        str
            Summary of the text provided.
    
        Raises:
        ------
        None:

        """
        if not text: 
            # Gives error text (Prevents program crash)
            text = "ERROR" 
            logger.error("No text provided for shortanswer evaluation.")
        
        logger.debug(f"Sending summarization request: {text[:1000]}")
        
        # Retrieve the summary
        summary = self.summarization_chain.invoke({"text": text[:3000]})
        self.summary = summary # Caches the summary
        
        logger.debug(f"Summary recieved: {summary[:1000]}")
        
        return summary
    
    def shortanswer_questions(self, count, text):
        """
        Creates <count> short answer questions about the provided text.
    
        Parameters:
        ----------
        count : int
            How many questions to generate.
        text : str
            The text to create questions from. 
    
        Returns:
        -------
        list
            List of str, where each str is one question.
            
        Raises:
        ------
        None
            
        """
        if not text: 
            # Gives error text (Prevents program crash)
            text = "ERROR" 
            logger.error("No text provided for shortanswer evaluation.")

        logger.debug(f"Sending shortanswer request for {count} questions: {text[:1000]}")
        questions = self.shortanswer_question_chain.invoke({"count": count, "text": text}) # Get the set of questions
        question_set = questions.strip().strip('\n').split('\n') # Split the questions into a list
        logger.debug(f"Recieved questions: {questions[:1000]}")
        if '' in question_set:
            question_set.remove('')
        for i in range(len(question_set)):
            question_set[i] = re.sub(r'^\d+\.\s*', '', question_set[i])

        return question_set
    
    def multiplechoice_questions(self, count, text):
        # Set up the document text as default
        if not text: 
            # Gives error text (Prevents program crash)
            text = "ERROR" 
            logger.error("No text provided for shortanswer evaluation.")

        # Invoke the question chain
        questions = self.multiplechoice_question_chain.invoke({"count": count, "text": text})
        
        # Split the return value by question
        question_set = questions.replace('\n', '').split('Question')
        question_set = [x for x in question_set if x != ''] # Clean the list

        # Create a regex string
        pattern = r"A\) |B\) |C\) |D\) |Correct Answer: "

        # Split each question into question and answer segments
        for idx, question in enumerate(question_set):
            question_set[idx] = re.split(pattern, question.strip())

        return question_set
    
    def multiplechoice_evaluate(self, question, answer):

        def letters_to_number(s):
            """
            Convert a letter sequence (A = 1, B = 2, ..., Z = 26, AA = 27, etc.) back to its corresponding number.

            Args:
                s (str): The letter sequence.

            Returns:
                int: The corresponding number.
            """
            s = s.upper()  # Ensure the input is in uppercase
            n = 0

            for char in s:
                n = n * 26 + (ord(char) - 65 + 1)

            return n
        
        if answer == letters_to_number(question[-1]) or letters_to_number(answer) == letters_to_number(question[-1]):
            return True
        else:
            return False
    
    def shortanswer_evaluate(self, question, answer, text):
        """
        Evaluates the responses to short-answer questions.
    
        Parameters:
        ----------
        question : str
            The question that is being evaluated
        answer : str
            The answer that is being evaluated
        text : str 
            The document that is being evaluated against.
    
        Returns:
        -------
        str
            Answer, Score (1-10)
    
        Raises:
        ------
        None
            
        """
        if not text: 
            # Gives error text (Prevents program crash)
            text = "ERROR" 
            logger.error("No text provided for shortanswer evaluation.")

        # Have the llm evaluate
        evaluation = self.shortanswer_evaluation_chain.invoke({"text": text, "question": question, "answer": answer})
        score = " ".join(evaluation.split("/"))

        if not any(char.isdigit() for char in score):
            score = "0"

        logger.info(f"Q/A: {question} / {answer} | Evaluation: {evaluation.strip()}")


        # If possible, parse the evaluation so it is less ugly.
        match = re.search(r'(?<=Evaluation: ).*', evaluation)
        if match:
            evaluation = match.group(0)  # Return the part after "Evaluation: "

        # Retrieve the score from the evaluation
        for word in score.split():
            if word.isdigit():
                score = word
                break
            
        return evaluation, score