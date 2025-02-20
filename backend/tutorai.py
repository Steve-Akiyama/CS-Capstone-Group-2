from langchain_openai import OpenAI # Creates an instance of OpenAI's language model ("It's a ChatGPT!")
from langchain_core.runnables.base import RunnableSequence # Used to chain together runnable components such as prompts and models, to let you invoke sequentially
from langchain.prompts import PromptTemplate  # Allows you to create templates for prompts you send to the model
import re

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
    set_document_text()
        Sets a default option for text being inputted.
    """
    
    def __init__(self, api_key="", temp=0.5, rec_accuracy=0.85, req_accuracy=0.6, system_message="You are a kind and helpful tutor teaching a student."):
        # Initialize OpenAI's model with desired temperature, which defines the randomness of the output. Higher = more random!
        self.__llm = OpenAI(temperature=temp, api_key=api_key)

        # Initalizes some base variables
        self.rec_accuracy = rec_accuracy
        self.req_accuracy = req_accuracy
        self.system_message = system_message

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
        sum_template = self.system_message + " Summarize the following text:\n\n{text}\n\nSummary:"
        sum_prompt = PromptTemplate(input_variables=["text"], template=sum_template)
        self.summarization_chain = RunnableSequence(sum_prompt | self.__llm) # Set up the summarization chain

        # Short-Answer Questions
        shortanswer_question_template = self.system_message + " You are tasked with asking students {count} questions about the following text:\n\n{text}\n\nQuestions should be seperated by a new line. Questions:"
        shortanswer_question_prompt = PromptTemplate(input_variables=["text"], template=shortanswer_question_template)
        self.shortanswer_question_chain = RunnableSequence(shortanswer_question_prompt | self.__llm)

        # Multiple-Choice Questions
        multiplechoice_question_template = self.system_message + " Create {count} multiple-choice questions about the text. The format should be as follows: \"Question 1: <Question>\"\"A) <Answer A>\"\"B) <Answer B>\"\"C) <Answer C>\"\"D) <Answer D>\"\"Correct Answer: <Letter of correct answer> Text:\n\n{text}\n\n"
        multiplechoice_question_prompt = PromptTemplate(input_variables=["text"], template=multiplechoice_question_template)
        self.multiplechoice_question_chain = RunnableSequence(multiplechoice_question_prompt | self.__llm)

        # True/False Questions
        truefalse_question_template = self.system_message + " Create {count} true/false questions about the text.  The format should be as follows: \"Question 1: <Question>\"\"T: True\"\"F: False\"\"Correct Answer: <true or false> Text: \n\n{text}\n\n"
        truefalse_question_prompt = PromptTemplate(input_variables=["text"], template=truefalse_question_template)
        self.truefalse_question_chain = RunnableSequence(truefalse_question_prompt | self.__llm)

        # Short-Answer Evaluation
        shortanswer_evaluation_template = self.system_message + " Use the following text:\n\n{text}\n\nTo evaluate the following question and answer. Please evaluate the answer based on the text with a score of 1-10 and an explanation for your score, quoting the text. Question:\n\n{question}\n\n Student's answer:\n\n{answer}\n\n The template should look like this: Score:\nEvaluation:"
        shortanswer_evaluation_prompt = PromptTemplate(input_variables=["text", "question", "answer"], template=shortanswer_evaluation_template)
        self.shortanswer_evaluation_chain = RunnableSequence(shortanswer_evaluation_prompt | self.__llm)

        # MCQ Evaluation
        multiplechoice_evaluation_template = self.system_message + " Use the following text:\n\n{text}\n\nTo explain why {correct_answer} is correct if applicable why {user_answer} is incorrect"
        multiplechoice_evaluation_prompt = PromptTemplate(input_variables=["text", "question", "correct_answer", "user_answer"], template=multiplechoice_evaluation_template)
        self.multiplechoice_evaluation_chain = RunnableSequence(multiplechoice_evaluation_prompt | self.__llm)

        # TF Evaluation
        truefalse_evaluation_template = self.system_message + " Use the following text:\n\n{text}\n\nTo explain why {correct_answer} is correct if applicable why {user_answer} is incorrect"
        truefalse_evaluation_prompt = PromptTemplate(input_variables=["text", "question", "correct_answer", "user_answer"], template=truefalse_evaluation_template)
        self.truefalse_evaluation_chain = RunnableSequence(truefalse_evaluation_prompt | self.__llm)

    def summarize_text(self, text=None):
        """
        Summarizes text through OpenAI's API
    
        Parameters:
        ----------
        text : str
            Text to be summarized. If blank, uses the instances' document_text.
    
        Returns:
        -------
        str
            Summary of the text provided.
    
        Raises:
        ------
        None:

        """
        if not text: text = self.document_text
        summary = self.summarization_chain.invoke({"text": text})
        self.summary = summary # Caches the summary
        return summary
    
    def shortanswer_questions(self, count, text=None):
        """
        Creates <count> short answer questions about the provided text.
    
        Parameters:
        ----------
        count : int
            How many questions to generate.
        text : str
            The text to create questions from. Will evaluate to document_text if not set.
    
        Returns:
        -------
        list
            List of str, where each str is one question.
            
        Raises:
        ------
        None
            
        """
        if not text: text = self.document_text
        questions = self.shortanswer_question_chain.invoke({"count": count, "text": text}) # Get the set of questions
        question_set = questions.strip().strip('\n').split('\n') # Split the questions into a list
        if '' in question_set:
            question_set.remove('')
        for i in range(len(question_set)):
            question_set[i] = re.sub(r'^\d+\.\s*', '', question_set[i])

        return question_set
    
    def multiplechoice_questions(self, count, text=None):
        # Set up the document text as default
        if not text: text = self.document_text

        # Invoke the question chain
        questions = self.multiplechoice_question_chain.invoke({"count": count, "text": text})
        
        # Split the return value by question
        question_set = questions.replace('\n', '').split('Question')
        question_set = [x for x in question_set if x != ''] # Clean the list

        # Create a regex string
        pattern = r"(?i)(question )?q?\d*: |A\) |B\) |C\) |D\) |Correct Answer: "

        # Split each question into question and answer segments
        for idx, question in enumerate(question_set):
            question_set[idx] = re.split(pattern, question.strip())

        question_set = [x for x in question_set if len(x) == 13]

        return question_set
    
    def truefalse_questions(self, count, text=None):
        # Set up the document text as default
        if not text: text = self.document_text

        # Invoke the question chain
        questions = self.truefalse_question_chain.invoke({"count": count, "text": text})

        # Split the return value by question
        question_set = questions.replace('\n', '').split('Question')
        question_set = [x for x in question_set if x != ''] # Clean the list

        # Create a regex string
        pattern = r"(?i)(question )?q?\d*: |T: |F: |Correct Answer: "

        # Split each question into question and answer segments
        for idx, question in enumerate(question_set):
            question_set[idx] = re.split(pattern, question.strip())

        question_set = [x for x in question_set if len(x) == 9]

        return question_set

    def multiplechoice_evaluate(self, question, answer, text=None):
        if not text: text = self.document_text

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
        
        question = question.split("$%^")
        
        c_ans = question[letters_to_number(question[-1])]
        u_ans = question[letters_to_number(answer)]
        evaluation = self.multiplechoice_evaluation_chain.invoke({"text": text, "question": question[0], "correct_answer": c_ans, "user_answer": u_ans})
        
        if answer == letters_to_number(question[-1]) or letters_to_number(answer) == letters_to_number(question[-1]):
            return evaluation, 10
        else:
            return evaluation, 0
        
    def truefalse_evaluate(self, question, answer, text=None):
        if not text: text = self.document_text

        def tf_to_num(ans):
            ans = ans.lower()
            if ans[0] == "t":
                return 1
            return 2


        question = question.split("$%^")
        c_ans = question[tf_to_num(question[-1])]
        u_ans = question[tf_to_num(answer)]

        evaluation = self.truefalse_evaluation_chain.invoke({"text": text, "question": question, "correct_answer": c_ans, "user_answer": u_ans})
        if answer == tf_to_num(question[-1]) or tf_to_num(answer) == tf_to_num(question[-1]):
            return evaluation, 10
        else:
            return evaluation, 0


    
    def shortanswer_evaluate(self, question, answer, text=None):
        """
        Evaluates the responses to short-answer questions.
    
        Parameters:
        ----------
        question : str
            The question that is being evaluated
        answer : str
            The answer that is being evaluated
        text : str 
            The document that is being evaluated against. Will initalize to document_text if not set.
    
        Returns:
        -------
        str
            Answer, Score (1-10)
    
        Raises:
        ------
        None
            
        """
        if not text: text = self.document_text # Get the default text if text is not specified

        # Have the llm evaluate
        evaluation = self.shortanswer_evaluation_chain.invoke({"text": text, "question": question, "answer": answer})
        score = " ".join(evaluation.split("/"))

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

    ####################################################################
    # Setter functions
    ####################################################################

    # Updates the document text
    def set_document_text(self, new_text):
        self.document_text = new_text

    ####################################################################
    # Old/Decomissioned functions
    ####################################################################

    # Should not be used
    def shortanswer_complete_terminal(self, text, count):
        questions = self.shortanswer_questions(count, text)
        total_score = 0
        for question in questions:
            score = "N/A"

            answer = input("\n\nPlease answer the following question:\n" + question + "\n: ")
            evaluation = self.shortanswer_evaluate(question, answer, text)
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