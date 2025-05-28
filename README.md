# 💼 Resume Match Pro – AI-Powered Resume & Job Description Matcher

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen)
![Framework](https://img.shields.io/badge/Framework-Flask%20%7C%20Streamlit-red)

An AI-powered tool that intelligently parses resumes and recommends top job roles based on semantic similarity and skill matching using **NLP**, **transformer-based embeddings**, and **interactive visualizations**.

---

## 🚀 Features

- 📄 Upload PDF Resumes for smart parsing
- 🧠 Skill & Experience Extraction from resume text
- 🔗 Top Job Matches using skill and semantic matching
- ⭐ Customizable Weightings for skills and experience
- 📈 Visualizations: Skill heatmaps and experience timelines
- 🎓 Skill Gap Analysis with direct learning recommendations
- 💬 Chatbot to answer questions about extracted resume data
- 🌐 Multi-language Interface (English, Spanish)
- 🔄 Session Save & Load for easy resume revisits

---

## 🖼️ Demo Screenshots

| Resume Upload | Job Match Results | Skill Gap & Timeline |
|---------------|-------------------|-----------------------|
| ![upload](assets/upload.png) | ![results](assets/results.png) | ![timeline](assets/timeline.png) |

---

## 🏗️ Project Structure

<pre> ``` resume-match-pro/ ├── app.py # Flask backend API ├── new.py # Streamlit frontend interface ├── uploads/ # Uploaded resumes (temporary storage) ├── assets/ # (optional) Demo screenshots ├── requirements.txt # Python dependencies ├── README.md # Project documentation └── saved_resume.pdf # (optional) Saved resume session ``` </pre>
This structure uses a <pre> block to preserve spacing and formatting, and includes consistent indentation and comments. Let me know if you'd like to add files like .env, .gitignore, or a Docker setup.



---

## 🧠 How It Works

1. **Resume Parsing**  
   Resumes are parsed using `pdfplumber`, and key skills/experiences are extracted using keyword matching and entity recognition.

2. **Semantic Embeddings**  
   Job descriptions and resume summaries are converted into vector embeddings using `sentence-transformers`.

3. **Matching Algorithm**  
   Each job role is scored based on:
   - 🔹 Skill match (keyword overlap)
   - 🔹 Semantic similarity (transformer-based embedding similarity)
   - 🔹 User-defined weights

4. **Visualization & Chatbot**  
   Visuals created using Plotly; a simple NLP-based chatbot answers resume-related questions.

---

## 🛠️ Tech Stack

| Layer       | Tools Used                                  |
|-------------|---------------------------------------------|
| Backend     | Flask, pdfplumber, spaCy, sentence-transformers |
| Frontend    | Streamlit, Plotly                           |
| ML/NLP      | SentenceTransformer (`all-MiniLM-L6-v2`)    |
| Parsing     | pdfplumber, regex                           |
| Deployment  | Localhost (can be deployed to Heroku, AWS)  |

---

## 📦 Installation & Setup

### 🔧 Requirements

- Python 3.8+
- `pip`

### 🔌 Clone the Repository

```bash
git clone https://github.com/Girish023/Resume-Match-Pro-AI-Powered-Resume-Job-Description-Matcher.git
cd Resume-Match-Pro-AI-Powered-Resume-Job-Description-Matcher


🐍 Create a Virtual Environment (optional but recommended)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


📥 Install Dependencies

pip install -r requirements.txt
Make sure you also download the en_core_web_sm spaCy model:
python -m spacy download en_core_web_sm

▶️ Running the App
1. Start the Flask Backend
python app.py
The backend runs at: http://localhost:5000

2. Start the Streamlit Frontend
streamlit run new.py
The frontend runs at: http://localhost:8501

🔍 Sample Job Descriptions
Job roles hardcoded in the backend for demo purposes:
Data Scientist
AI Engineer
Backend Developer
NLP Engineer

These can be expanded easily in app.py.

🌐 Internationalization
✅ English

✅ Spanish
Change language from the sidebar dropdown.

💡 Customization Tips
Add more job roles in app.py → job_descriptions
Enhance skill/experience extraction using spaCy NER or custom regex
Expand chatbot capabilities with LangChain or RAG architecture
Add database integration to persist users, resumes, and results

📁 Requirements File (for reference)
txt
Copy
Edit
flask
flask-cors
streamlit
spacy
pdfplumber
sentence-transformers
plotly
pandas


📜 License
This project is licensed under the MIT License.

🙌 Acknowledgments
HuggingFace for Sentence Transformers

spaCy for NLP

Streamlit for interactive UI

Plotly for charts

🤝 Contributing
Pull requests, issues, and feature suggestions are welcome!

Fork the repo

Create a new branch

Make changes

Submit a PR 🎉


