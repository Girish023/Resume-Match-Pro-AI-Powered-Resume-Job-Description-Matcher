from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import spacy
import pdfplumber
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
CORS(app) 
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load NLP models
nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Sample job descriptions
job_descriptions = [
    {"title": "Data Scientist", "description": "Build ML models, analyze data, write Python scripts, deploy with Flask."},
    {"title": "AI Engineer", "description": "Work on deep learning, computer vision, transformers, and deploy AI models."},
    {"title": "Backend Developer", "description": "Design APIs, manage databases, work with Django/Flask, and cloud services."},
    {"title": "NLP Engineer", "description": "Text classification, named entity recognition, embeddings, and LLM fine-tuning."}
]

# Precompute job embeddings
job_corpus = [job["description"] for job in job_descriptions]
job_embeddings = embedder.encode(job_corpus, convert_to_tensor=True)

def parse_resume(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    
    lower_text = text.lower()

    # Simple skill matcher
    skills_keywords = [
        "python", "c++", "c", "sql", "java", "opencv", "tensorflow", "rasa", "docker",
        "matplotlib", "pandas", "scikit-learn", "gen ai", "data science", "nlp", 
        "communication", "leadership", "team work"
    ]
    skills = [kw for kw in skills_keywords if kw in lower_text]

    # Simple experience matcher
    experience = []
    if "vaisesika" in lower_text:
        experience.append("AI Engineer at Vaisesika")
    if "samsung" in lower_text:
        experience.append("Intern at Samsung Prism")
    if "drone" in lower_text:
        experience.append("Drone Vision Project")
    if "kpmg" in lower_text:
        experience.append("KPMG Virtual Internship")

    resume_summary = f"Skills: {', '.join(skills)}. Experience: {', '.join(experience)}."
    return resume_summary, {"skills": skills, "experience": experience}


def match_jobs(resume_summary, skills, top_k=3):
    resume_embedding = embedder.encode(resume_summary, convert_to_tensor=True)
    similarities = util.cos_sim(resume_embedding, job_embeddings)[0]

    results = []
    for i, job in enumerate(job_descriptions):
        job_title = job["title"]
        job_desc = job["description"].lower()

        # Skill match score
        matched_skills = [skill for skill in skills if skill in job_desc]
        skill_score = len(matched_skills) / max(len(skills), 1)

        # Semantic similarity score
        sem_score = float(similarities[i])

        # Weighted total score
        total_score = 0.6 * sem_score + 0.4 * skill_score

        results.append({
            "job_title": job_title,
            "semantic_score": round(sem_score, 2),
            "skill_score": round(skill_score, 2),
            "total_score": round(total_score, 2),
            "matched_skills": matched_skills
        })

    # Sort by total score
    results = sorted(results, key=lambda x: x["total_score"], reverse=True)[:top_k]
    return results



@app.route('/')
def home():
    return "✅ Resume Parser + Job Matcher API is running."

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No filename provided'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # ✅ REPLACEMENT: Call enhanced parsing + matching quality
    resume_summary, entities = parse_resume(filepath)
    matches = match_jobs(resume_summary, entities["skills"])  # 🔥 improved!

    return jsonify({
        "extracted_entities": entities,
        "job_matches": matches
    })


if __name__ == '__main__':
    app.run(debug=True)
