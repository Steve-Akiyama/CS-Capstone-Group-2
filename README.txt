Currently WIP capstone project!

Participants:
- Varsha Narayan
- Maile Look
- Grant O'Connor
- Steven Akiyama

Project Description:
https://eecs.engineering.oregonstate.edu/capstone/submission/pages/viewSingleProject.php?id=Qb8Mgf4wM8AXlkcX

Textbook Access:
https://assets.openstax.org/oscms-prodcms/media/documents/Psychology2e_WEB.pdf

Abstract:
College psychology students often struggle to retain textbook material through traditional study methods. While textbooks provide essential knowledge, they lack dynamic engagement, preventing students from fully comprehending or retaining key concepts. This problem is exacerbated by the need for tailored feedback and adaptive learning paths. Our software addresses this gap using large language models (LLMs) with Retrieval-Augmented Generation (RAG) to provide an interactive, personalized learning experience that adapts to individual student progress. This solution will be used by psychology students aiming to improve their understanding of complex topics more efficiently and engagingly.
The goal of the project is to create an adaptive learning system that helps psychology students better grasp textbook content by evaluating their progress and adjusting the flow of topics accordingly. This system will facilitate more effective study sessions by offering personalized guidance and learning paths.
Our initial design approach integrates LLMs with RAG, allowing the system to generate contextually accurate responses based on both the textbook content and external, relevant academic resources. The main design challenge lies in accurately assessing students' understanding and determining when they are ready to progress to new topics. This requires advanced techniques in natural language processing, knowledge retrieval, and learning evaluation. As the project evolves, we may explore additional methods for assessing student comprehension, such as quizzes or interactive exercises.
Existing study tools and platforms do not offer the same level of personalized feedback or adaptability. Unlike static learning platforms, our system dynamically evaluates student progress and adjusts the pace of learning based on real-time assessment. This provides a more tailored educational experience, helping students move past difficult concepts only when they're ready, and improving retention and engagement.
We will collect data by testing the system with psychology students, tracking their progress and improvements in comprehension through pre- and post-assessments. Our expected result is that students using the system will demonstrate a higher retention rate of textbook material and improved test scores compared to traditional study methods.

------------------------------------------------------------
Important: .env configuration
------------------------------------------------------------

This program requires a .env file that contains necessary data (Website links, API keys.) 
It should look like this:

OPENAI_API_KEY="<Your Key Here!>"
# Environment setting: local or production
ENVIRONMENT=local  # Change to 'production' when deploying to EC2

# URLs based on environment. Change PRODUCTION urls to match your EC2 server IP!
FRONTEND_URL_LOCAL=http://localhost:3000
FRONTEND_URL_PRODUCTION=http://52.15.75.24:3000
BACKEND_URL_LOCAL=http://localhost:8000
BACKEND_URL_PRODUCTION=http://52.15.75.24:8000

------------------------------------------------------------
Launching the Backend
------------------------------------------------------------

1. **Locally (on your local machine):**
    - Navigate to your `/backend` directory.
    - Run the following command to start the backend server:
    ```
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

2. **On the EC2 server:**
    - SSH into your EC2 instance.
    - Navigate to the `/backend` directory.
    - Pull the latest changes from your GitHub repository (if necessary):
    ```
    ./deploy.sh
    ```
    - Start the backend server using `nohup` to keep it running in the background:
    ```
    nohup uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
    ```

------------------------------------------------------------
Launching the Frontend
------------------------------------------------------------

1. **Locally (on your local machine):**
    - Navigate to your `/frontend-react` directory.
    - Run the following command to start the frontend server:
    ```
    npm run dev
    ```

2. **On the EC2 server:**
    - SSH into your EC2 instance.
    - Navigate to the `/frontend-react` directory.
    - Pull the latest changes from your GitHub repository (if necessary):
    ```
    ./deploy.sh
    ```
    - Install the necessary dependencies (if not already installed):
    ```
    npm install
    ```
    - Start the frontend server using `nohup` to keep it running in the background:
    ```
    nohup npm run dev &
    ```

------------------------------------------------------------
Check if running (EC2 only)
------------------------------------------------------------
1. **Backend**
    ps aux | grep uvicorn
2. **Frontend**
    ps aux | grep vite

------------------------------------------------------------
Accessing the Sites
------------------------------------------------------------

1. **Backend Access:**
    - On EC2, the backend should be accessible at: `http://<EC2_PUBLIC_IP>:8000`
    - Locally, the backend should be accessible at: `http://localhost:8000`

2. **Frontend Access:**
    - On EC2, the frontend should be accessible at: `http://<EC2_PUBLIC_IP>:3000`
    - Locally, the frontend should be accessible at: `http://localhost:3000`

------------------------------------------------------------
Important Notes
------------------------------------------------------------

- Ensure your EC2 instance allows traffic on ports 8000 (backend) and 3000 (frontend) in the security group settings.
- If you're running both backend and frontend on EC2, you might need to update the `CORS` settings to allow access from your frontend's URL.
- If you're switching between local and production environments, modify the `FRONTEND_URL` and `BACKEND_URL` in your `.env` file.
