"""
------------------------------------------------------------
File: tutorai.py
Description:
    This class uses LangChain to access OpenAI's ChatGPT-4.

Author: Steven Akiyama, Grant O'Connor
Date: November 2024
Version: 1.0

Usage:
    Used as a method of accessing LLMs and getting their input,
    analysis, and summary on the document data.

Future updates:
    - TutorAI should incorperate RAG (Retreival-Augmented Generation)
    instead of hard-coded document content.
    - TutorAI should be able to present and evaluate multiple-choice
    questions and answers
------------------------------------------------------------
"""

from langchain_openai import OpenAI # Creates an instance of OpenAI's language model ("It's a ChatGPT!")
from langchain_core.runnables.base import RunnableSequence # Used to chain together runnable components such as prompts and models, to let you invoke sequentially
from langchain.prompts import PromptTemplate  # Allows you to create templates for prompts you send to the model

class TutorAI:

    __llm = "No LLM initalized! __init__ failed to run."
    summary = "No summary initalized"
    document_text = ""
    __topic = ""
    rec_accuracy = 0
    req_accuracy = 0

    # Initalizes the LLM, with temperature and prompt setup.
    def __init__(self, api_key=None, temp=0.5, topic=None, rec_accuracy=0.85, req_accuracy=0.6):
        # Initialize OpenAI's model with desired temperature, which defines the randomness of the output. Higher = more random!
        self.__llm = OpenAI(temperature=temp, api_key=api_key)

        # Initalizes it with a certain topic
        self.__topic = topic

        # Initalizes some base variables
        self.rec_accuracy = rec_accuracy
        self.req_accuracy = req_accuracy

        # Initalize prompts
        self.__prompt_init()

        # Import or create document text
        self.document_text = """
        According to the American Psychiatric Association, a psychological disorder, or mental disorder, is “a
        syndrome characterized by clinically significant disturbance in an individual's cognition, emotion regulation,
        or behavior that reflects a dysfunction in the psychological, biological, or developmental processes underlying
        mental functioning. Mental disorders are usually associated with significant distress in social, occupational, or
        other important activities” (2013). Psychopathology is the study of psychological disorders, including their
        symptoms, etiology (i.e., their causes), and treatment. The term
        psychopathology can also refer to the
        manifestation of a psychological disorder. Although consensus can be difficult, it is extremely important for
        mental health professionals to agree on what kinds of thoughts, feelings, and behaviors are truly abnormal in
        the sense that they genuinely indicate the presence of psychopathology. Certain patterns of behavior and inner
        experience can easily be labeled as abnormal and clearly signify some kind of psychological disturbance. The
        person who washes their hands 40 times per day and the person who claims to hear the voices of demons
        exhibit behaviors and inner experiences that most would regard as abnormal: beliefs and behaviors that
        suggest the existence of a psychological disorder. But, consider the nervousness a young man feels when
        talking to an attractive person or the loneliness and longing for home a first-year student experiences during
        her first semester of college—these feelings may not be regularly present, but they fall in the range of normal.
        So, what kinds of thoughts, feelings, and behaviors represent a true psychological disorder? Psychologists work
        to distinguish psychological disorders from inner experiences and behaviors that are merely situational,
        idiosyncratic, or unconventional.
        """
        

    # Initalizes prompts necessary for the tutor
    def __prompt_init(self):
        # Summarization
        sum_template = "You are a tutor teaching a student about " + self.__topic + ". Summarize the following text:\n\n{text}\n\nSummary:"
        sum_prompt = PromptTemplate(input_variables=["text"], template=sum_template)
        self.summarization_chain = RunnableSequence(sum_prompt | self.__llm) # Set up the summarization chain

        # Short-Answer Questions
        shortanswer_question_template = "You are a tutor teaching students " + self.__topic + ", tasked with asking students {count} questions about the following text:\n\n{text}\n\nQuestions should be seperated by a new line. Questions:"
        shortanswer_question_prompt = PromptTemplate(input_variables=["text"], template=shortanswer_question_template)
        self.shortanswer_question_chain = RunnableSequence(shortanswer_question_prompt | self.__llm)

        # Multiple-Choice Questions
        multiplechoice_question_template = "Create {count} multiple-choice questions about the following text in JSON format. Please state the correct answer before the question. Text:\n\n{text}\n\nQuestions:"
        multiplechoice_question_prompt = PromptTemplate(input_variables=["text"], template=multiplechoice_question_template)
        self.multiplechoice_question_chain = RunnableSequence(multiplechoice_question_prompt | self.__llm)

        # Short-Answer Evaluation
        shortanswer_evaluation_template = "You are a tutor teaching a student about " + self.__topic + ". Use the following text:\n\n{text}\n\nTo evaluate the following question and answer. Please evaluate the answer based on the text with a score of 1-10 and an explanation for your score, quoting the text. Question:\n\n{question}\n\n Student's answer:\n\n{answer}\n\n The template should look like this: Score:\nEvaluation:"
        shortanswer_evaluation_prompt = PromptTemplate(input_variables=["text", "question", "answer"], template=shortanswer_evaluation_template)
        self.shortanswer_evaluation_chain = RunnableSequence(shortanswer_evaluation_prompt | self.__llm)

    # Summarizes the text
    def summarize_text(self, text):
        summary = self.summarization_chain.invoke({"text": text})
        self.summary = summary # Caches the summary
        return summary
    
    # Creates short answer questions about the text
    def shortanswer_questions_text(self, text, count):
        questions = self.shortanswer_question_chain.invoke({"count": count, "text": text}) # Get the set of questions
        question_set = questions.strip().strip('\n').split('\n') # Split the questions into a list
        if '' in question_set:
            question_set.remove('')

        return question_set
    
    # Creates multiple choice questions about the text
    def multiplechoice_questions_text(self, text, count):
        questions = self.multiplechoice_question_chain.invoke({"count": count, "text": text})
        question_set = questions.rstrip(" \n").strip(" \n").split("\n\n")
        return question_set
    
    # Evaluates the response to a short-answer question
    def shortanswer_evaluate_answer(self, text, question, answer):
        evaluation = self.shortanswer_evaluation_chain.invoke({"text": text, "question": question, "answer": answer})
        return evaluation
    
    def shortanswer_complete_terminal(self, text, count):
        questions = self.shortanswer_questions_text(text, count)
        total_score = 0
        for question in questions:
            score = "N/A"

            answer = input("\n\nPlease answer the following question:\n" + question + "\n: ")
            evaluation = self.shortanswer_evaluate_answer(self.document_text, question, answer)
            print(evaluation)

            score = " ".join(evaluation.split("/"))
            for word in score.split():
                if word.isdigit():
                    score = word
                    break
            
            print("Your score was: " + score)
            total_score += int(score)

        print("Your total score was " + str(total_score) + "/" + str(count * 10) + ".")
        if ((self.req_accuracy * 10 * count) > (total_score)):
            print("You failed the segment questions.")
        elif ((self.rec_accuracy * 10 * count) > (total_score)):
            print("You passed the segement questions, but it's reccommended that you review some more.")
        else:
            print("Congrats! You passed this segment's questions.")