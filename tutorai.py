from langchain_openai import OpenAI # Creates an instance of OpenAI's language model ("It's a ChatGPT!")
from langchain_core.runnables.base import RunnableSequence # Used to chain together runnable components such as prompts and models, to let you invoke sequentially
from langchain.prompts import PromptTemplate  # Allows you to create templates for prompts you send to the model

class TutorAI:

    llm = "No LLM initalized! __init__ failed to run."
    summary = "No summary initalized"
    document_text = ""
    __topic = ""
    rec_accuracy = 0
    req_accuracy = 0

    # Initalizes the LLM, with temperature and prompt setup.
    def __init__(self, api_key=None, temp=0.5, topic=None, rec_accuracy=0.85, req_accuracy=0.6):
        # Initialize OpenAI's model with desired temperature, which defines the randomness of the output. Higher = more random!
        self.llm = OpenAI(temperature=temp, api_key=api_key)

        # Initalizes it with a certain topic
        self.__topic = topic

        # Initalizes some base variables
        self.rec_accuracy = rec_accuracy
        self.req_accuracy = req_accuracy

        # Initalize prompts
        self.__prompt_init()

        # Import or create textbook text
        self.document_text = """
        On Monday, September 16, 2013, a gunman killed 12 people as the workday began at the
        Washington Navy Yard in Washington, DC. Aaron Alexis, 34, had a troubled history: he thought that he was
        being controlled by radio waves. He called the police to complain about voices in his head and being under
        surveillance by “shadowy forces” (Thomas, Levine, Date, & Cloherty, 2013). While Alexis’s actions cannot be
        excused, it is clear that he had some form of mental illness. Mental illness is not necessarily a cause of
        violence; it is far more likely that the mentally ill will be victims rather than perpetrators of violence (Stuart,
        2003). If, however, Alexis had received the help he needed, this tragedy might have been averted.
        """

    # Initalizes prompts necessary for the tutor
    def __prompt_init(self):
        # Summarization
        sum_template = "You are a tutor teaching a student about " + self.__topic + ". Summarize the following text:\n\n{text}\n\nSummary:"
        sum_prompt = PromptTemplate(input_variables=["text"], template=sum_template)
        self.summarization_chain = RunnableSequence(sum_prompt | self.llm) # Set up the summarization chain

        # Short-Answer Questions
        shortanswer_question_template = "You are a tutor teaching students " + self.__topic + ", tasked with asking students {count} questions about the following text:\n\n{text}\n\nQuestions should be seperated by a new line. Questions:"
        shortanswer_question_prompt = PromptTemplate(input_variables=["text"], template=shortanswer_question_template)
        self.shortanswer_question_chain = RunnableSequence(shortanswer_question_prompt | self.llm)

        # Multiple-Choice Questions
        multiplechoice_question_template = "Create {count} multiple-choice questions about the following text in JSON format. Please state the correct answer before the question. Text:\n\n{text}\n\nQuestions:"
        multiplechoice_question_prompt = PromptTemplate(input_variables=["text"], template=multiplechoice_question_template)
        self.multiplechoice_question_chain = RunnableSequence(multiplechoice_question_prompt | self.llm)

        # Short-Answer Evaluation
        shortanswer_evaluation_template = "You are a tutor teaching a student about " + self.__topic + ". Use the following text:\n\n{text}\n\nTo evaluate the following question and answer. Please evaluate the answer based on the text with a score of 1-10 and an explanation for your score, quoting the text. Question:\n\n{question}\n\n Student's answer:\n\n{answer}\n\n The template should look like this: Score:\nEvaluation:"
        shortanswer_evaluation_prompt = PromptTemplate(input_variables=["text", "question", "answer"], template=shortanswer_evaluation_template)
        self.shortanswer_evaluation_chain = RunnableSequence(shortanswer_evaluation_prompt | self.llm)

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