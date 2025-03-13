# 🚀 Capstone Project (WIP)

## Participants
- Varsha Narayan
- Maile Look
- Grant O'Connor
- Steven Akiyama

## Project Description
[View Project Details](https://eecs.engineering.oregonstate.edu/capstone/submission/pages/viewSingleProject.php?id=Qb8Mgf4wM8AXlkcX)

## 📖 Textbook Access
[Psychology 2e (OpenStax)](https://assets.openstax.org/oscms-prodcms/media/documents/Psychology2e_WEB.pdf)

---

## 📝 Abstract
College psychology students often struggle to retain textbook material through traditional study methods. While textbooks provide essential knowledge, they lack dynamic engagement, preventing students from fully comprehending or retaining key concepts. This problem is exacerbated by the need for tailored feedback and adaptive learning paths.

Our software addresses this gap using **Large Language Models (LLMs) with Retrieval-Augmented Generation (RAG)** to provide an interactive, personalized learning experience that adapts to individual student progress. This solution helps psychology students improve their understanding of complex topics more efficiently and engagingly.

### 🌟 Project Goals
- Develop an **adaptive learning system** that personalizes the study experience.
- Evaluate students' progress and adjust topic flow accordingly.
- Provide **contextually accurate responses** based on textbook content and academic resources.
- Implement **advanced NLP and knowledge retrieval** techniques for better learning assessment.
- Enhance retention and engagement beyond static study tools.

### 🔍 Research & Testing
- Conduct trials with psychology students.
- Track progress through pre- and post-assessments.
- Measure effectiveness by analyzing comprehension improvements and retention rates.

---

## ⚙️ General Requirements
- **OpenAI API Key**
- **QDrant Cloud API Key**
- **Existing QDrant Cloud Cluster** (Formatted correctly, see below)
- **`.env` file with necessary configurations** (See below)

---

## 🗄️ QDrant Cloud Formatting
Each point in the QDrant Cloud database should have the following structure:
```json
{
  "title": "<string>",
  "chapter": "<string>",
  "text": "<string>"
}
```
A future update will include a program to **automatically process textbooks** for this format.

---

## 🔑 `.env` Configuration
This project requires a `.env` file containing essential credentials and environment variables:
```ini
OPENAI_API_KEY="<Your Key Here!>"

# Environment setting: local or production
ENVIRONMENT=local  # Change to 'production' when deploying to EC2

# URLs based on environment
FRONTEND_URL_LOCAL=http://localhost:3000
FRONTEND_URL_PRODUCTION=http://<EC2.server.IP.address>:3000
BACKEND_URL_LOCAL=http://localhost:8000
BACKEND_URL_PRODUCTION=http://<EC2.server.IP.address>:8000

# QDrant Access
QDRANT_API_KEY="<Your Key Here!>"
QDRANT_URL="<Your QDrant Cloud Cluster URL Here!>"
```

---

## 🚀 Launching the Backend
### Locally:
```sh
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### On EC2 Server:
```sh
ssh <your-ec2-instance>
cd backend
git pull origin main  # Pull latest changes
./deploy.sh  # If applicable
nohup uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
```

### With `tmux` (Persistent Hosting on EC2):
```sh
tmux new -s backend_session
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# Detach session with Ctrl + B, then D
# Reattach with: tmux attach -t backend_session
```

---

## 🎨 Launching the Frontend
### Locally:
```sh
cd frontend-react
npm run dev
```

### On EC2 Server:
```sh
ssh <your-ec2-instance>
cd frontend-react
git pull origin main  # Pull latest changes
./deploy.sh  # If applicable
npm install  # Install dependencies if not installed
nohup npm run dev &
```

### With `tmux` (Persistent Hosting on EC2):
```sh
tmux new -s frontend_session
cd frontend-react
npm run dev
# Detach session with Ctrl + B, then D
# Reattach with: tmux attach -t frontend_session
```

---

## ✅ Check if Services are Running (EC2 Only)
**Backend:**
```sh
ps aux | grep uvicorn
```

**Frontend:**
```sh
ps aux | grep vite
```

---

## 🌍 Accessing the Sites
| Environment | Backend | Frontend |
|------------|---------|----------|
| **EC2** | `http://<EC2_PUBLIC_IP>:8000` | `http://<EC2_PUBLIC_IP>:3000` |
| **Local** | `http://localhost:8000` | `http://localhost:3000` |

---

## ⚠️ Important Notes
- Ensure **EC2 security group** allows traffic on **ports 8000 (backend) and 3000 (frontend)**.
- If running both services on EC2, update **CORS settings** to allow frontend-backend communication.
- Switch between local and production environments by modifying `.env` file URLs.

---

## 🛠️ Future Improvements
- **Automated textbook processing** for QDrant storage.
- **Enhanced student comprehension assessment methods** (e.g., quizzes, interactive exercises).
- **Better user interface & accessibility improvements**.
- **Expanded LLM fine-tuning for domain-specific learning**.

---

## 📌 Acknowledgments
Special thanks to **Oregon State University** for supporting this capstone project!

