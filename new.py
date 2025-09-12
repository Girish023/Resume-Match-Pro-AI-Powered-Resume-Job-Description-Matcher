# --- Imports ---
import streamlit as st
import plotly.express as px
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import os
import io

# ✅ This MUST come immediately after import
st.set_page_config(
    page_title="💼 Advanced Resume Matcher",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def load_embed_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_embed_model()

# --- Multi-language Support --
lang = st.sidebar.selectbox("🌐 Select Language", ["English", "Spanish"])
labels = {
    "English": {
        "title": "💼 Resume Match Pro",
        "upload_resume": "📄 Upload Resume (PDF)",
        "paste_job": "📝 Paste Job Description",
        "adjust_weights": "⚖️ Adjust Matching Weights",
        "skills_weight": "Skill Matching Weight",
        "experience_weight": "Experience Matching Weight",
        "results": "📊 Results",
        "controls": "⚙️ Controls",
        "skills_header": "🧠 Extracted Skills",
        "experience_header": "🧠 Experience",
        "job_matches": "🔗 Top Job Matches",
        "skill_gap": "🔍 Skill Gap Analysis",
        "missing_skills": "Suggested skills to learn for better fit:",
        "no_gaps": "✅ No major skill gaps!",
        "download_resume": "⬇️ Download Resume",
        "visualizations": "📈 Visualizations",
        "experience_timeline": "📅 Experience Timeline",
        "learning_recs": "🎓 Learning Suggestions",
        "no_resume": "📎 Please upload a resume.",
        "paste_jd_info": "✍️ Paste job description to analyze match.",
        "resume_required_for_jd": "⚠️ Please upload a resume first.",
        "star_rating": "⭐ Match Rating"
    },
    "Spanish": {
        "title": "💼 Emparejador de CV",
        "upload_resume": "📄 Subir CV (PDF)",
        "paste_job": "📝 Pegar Descripción del Trabajo",
        "adjust_weights": "⚖️ Ajustar Pesos de Coincidencia",
        "skills_weight": "Peso de Habilidades",
        "experience_weight": "Peso de Experiencia",
        "results": "📊 Resultados",
        "controls": "⚙️ Controles",
        "skills_header": "🧠 Habilidades Extraídas",
        "experience_header": "🧠 Experiencia",
        "job_matches": "🔗 Coincidencias de Trabajo",
        "skill_gap": "🔍 Brecha de Habilidades",
        "missing_skills": "Habilidades que podrías aprender:",
        "no_gaps": "✅ ¡Sin brechas significativas!",
        "download_resume": "⬇️ Descargar CV",
        "visualizations": "📈 Visualizaciones",
        "experience_timeline": "📅 Línea de Tiempo de Experiencia",
        "learning_recs": "🎓 Rutas de Aprendizaje",
        "no_resume": "📎 Por favor sube un CV.",
        "paste_jd_info": "✍️ Pega la descripción del trabajo para analizar.",
        "resume_required_for_jd": "⚠️ Primero sube un CV.",
        "star_rating": "⭐ Evaluación de Ajuste"
    }
}
L = labels[lang]

# --- Page Title ---
st.title(L["title"])

# --- Session State ---
if "resume_data" not in st.session_state:
    st.session_state.resume_data = {}
if "uploaded_resume" not in st.session_state:
    st.session_state.uploaded_resume = None
if "mode" not in st.session_state:
    st.session_state.mode = "resume_to_job"
if "weights" not in st.session_state:
    st.session_state.weights = {"skills": 0.5, "experience": 0.5}

# --- Layout ---
left_col, center_col, right_col = st.columns([1.2, 2.5, 1.3])

# --- Left Column: Controls ---
with left_col:
    st.subheader(L["controls"])
    mode = st.radio("Matching Mode", [L["title"], "Job Description to Resume Match"], index=0)
    st.session_state.mode = "resume_to_job" if mode == L["title"] else "job_to_resume"

    if st.session_state.mode == "resume_to_job":
        uploaded_file = st.file_uploader(L["upload_resume"], type=["pdf"])
        if uploaded_file:
            st.session_state.uploaded_resume = uploaded_file
            st.session_state.resume_data = {}
    else:
        job_description = st.text_area(L["paste_job"], height=250)

    # Weight sliders
    st.markdown("#### " + L["adjust_weights"])
    skills_w = st.slider(L["skills_weight"], 0.0, 1.0, st.session_state.weights["skills"], 0.05)
    experience_w = st.slider(L["experience_weight"], 0.0, 1.0, st.session_state.weights["experience"], 0.05)
    total = skills_w + experience_w if (skills_w + experience_w) != 0 else 1
    st.session_state.weights = {
        "skills": skills_w / total,
        "experience": experience_w / total
    }
# --- Center Column: Results Display ---
with center_col:
    st.subheader(L["results"])

    def parse_resume(file):
        # Simulated parser - replace with actual backend/API if needed
        return {
            "extracted_entities": {
                "skills": ["python", "c++", "sql", "docker", "tensorflow", "pandas"],
                "experience": [
                    "AI Engineer at Vaisesika (2019-2022)",
                    "Intern at Samsung Prism (2018)",
                    "KPMG Virtual Internship (2020)"
                ]
            },
            "job_matches": [
                {
                    "job_title": "AI Engineer", "skill_score": 0.6,
                    "semantic_score": 0.7, "total_score": 0.65,
                    "matched_skills": ["python", "tensorflow"]
                },
                {
                    "job_title": "Data Scientist", "skill_score": 0.55,
                    "semantic_score": 0.6, "total_score": 0.57,
                    "matched_skills": ["python", "pandas"]
                },
                {
                    "job_title": "Backend Developer", "skill_score": 0.4,
                    "semantic_score": 0.5, "total_score": 0.45,
                    "matched_skills": ["docker"]
                }
            ]
        }

    if st.session_state.mode == "resume_to_job":
        if st.session_state.uploaded_resume and not st.session_state.resume_data:
            st.session_state.resume_data = parse_resume(st.session_state.uploaded_resume)

        data = st.session_state.resume_data

        if not data:
            st.info(L["no_resume"])
        else:
            # Extracted Skills
            with st.expander(L["skills_header"], expanded=True):
                st.markdown(", ".join(data["extracted_entities"]["skills"]))

            # Experience + Timeline Plot (fixed date parsing)
            with st.expander(L["experience_header"], expanded=True):
                for exp in data["extracted_entities"]["experience"]:
                    st.markdown(f"- {exp}")

                timeline = []
                for item in data["extracted_entities"]["experience"]:
                    try:
                        title = item.split(" at ")[0]
                        years_part = item.split("(")[-1].replace(")", "")
                        if "-" in years_part:
                            start_str, end_str = years_part.split("-")
                            start = int(start_str)
                            end = int(end_str)
                        else:
                            # Single year experience
                            start = end = int(years_part)
                        timeline.append({"Title": title, "Start": start, "End": end})
                    except:
                        continue

                if timeline:
                    df = pd.DataFrame(timeline)
                    fig = px.timeline(df, x_start="Start", x_end="End", y="Title", color="Title",
                                      title=L["experience_timeline"])
                    fig.update_yaxes(autorange="reversed")
                    fig.update_layout(
                        xaxis_title="Year",
                        yaxis_title="Position",
                        margin=dict(l=20, r=20, t=40, b=20)
                    )
                    st.plotly_chart(fig, use_container_width=True)

            # Job Matches with Star Ratings
            with st.expander(L["job_matches"], expanded=True):
                matches = data["job_matches"]
                for m in matches:
                    weight = (m["skill_score"] * st.session_state.weights["skills"] +
                              m["semantic_score"] * st.session_state.weights["experience"])
                    stars = "⭐" * int(round(weight * 5))

                    st.markdown(f"""
                    <div style='
                        background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
                        border-left: 8px solid #00796b;
                        padding: 15px;
                        margin-bottom: 15px;
                        border-radius: 10px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        color: #004d40;
                    '>
                        <h4 style='margin-bottom:5px;'>{m['job_title']}</h4>
                        🔹 <b>Weighted Score:</b> {weight:.2f}<br>
                        🔹 <b>Skill Score:</b> {m['skill_score']:.2f}<br>
                        🔹 <b>Semantic Score:</b> {m['semantic_score']:.2f}<br>
                        ✅ <b>Skills Matched:</b> <i>{', '.join(m['matched_skills'])}</i><br>
                        <b>{L['star_rating']}:</b> {stars}
                    </div>
                    """, unsafe_allow_html=True)

            # Skill Gap + Learning Resources
            with st.expander(L["skill_gap"], expanded=True):
                job_skills = set()
                for m in data["job_matches"]:
                    job_skills.update([s.lower() for s in m["matched_skills"]])
                resume_skills = set([s.lower() for s in data["extracted_entities"]["skills"]])
                missing = job_skills - resume_skills

                if missing:
                    st.write(L["missing_skills"])
                    for skill in sorted(missing):
                        u_link = f"https://www.udemy.com/courses/search/?q={skill}"
                        c_link = f"https://www.coursera.org/courses?query={skill}"
                        st.markdown(f"- **{skill.title()}** → [Udemy]({u_link}) | [Coursera]({c_link})")
                else:
                    st.success(L["no_gaps"])

            # Resume download
            if st.session_state.uploaded_resume:
                st.download_button(
                    label=L["download_resume"],
                    data=st.session_state.uploaded_resume.getvalue(),
                    file_name=st.session_state.uploaded_resume.name,
                    mime="application/pdf"
                )

    # Job Description to Resume Match
    else:
        if not st.session_state.resume_data:
            st.warning(L["resume_required_for_jd"])
        elif job_description:
            jd_embed = model.encode(job_description, convert_to_tensor=True)
            resume_skills = st.session_state.resume_data.get("extracted_entities", {}).get("skills", [])
            skill_embeds = model.encode(resume_skills, convert_to_tensor=True)
            cos_scores = util.cos_sim(jd_embed, skill_embeds)[0]
            matches = [(resume_skills[i], cos_scores[i].item()) for i in range(len(resume_skills))]
            matches = sorted(matches, key=lambda x: x[1], reverse=True)
            matched = [s for s, score in matches if score > 0.5]
            st.markdown(f"**Matched Skills:** {', '.join(matched) if matched else 'None'}")

# --- Right Column: Visualizations & Chatbot ---
with right_col:
    st.subheader(L["visualizations"])

    data = st.session_state.resume_data
    skills = data.get("extracted_entities", {}).get("skills", []) if data else []

    if skills:
        skill_counts = pd.Series(skills).value_counts().reset_index()
        skill_counts.columns = ["Skill", "Count"]

        fig = px.imshow(
            skill_counts["Count"].values.reshape(1, -1),
            labels=dict(x="Skill", y="", color="Count"),
            x=skill_counts["Skill"],
            y=["Count"],
            color_continuous_scale="Viridis"
        )
        fig.update_layout(height=150, margin=dict(t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No skills data available to display heatmap.")

    # --- Simple Chatbot ---
    st.subheader("💬 Chatbot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def chatbot_response(user_input):
        skills = st.session_state.resume_data.get("extracted_entities", {}).get("skills", [])
        if "skill" in user_input.lower():
            if skills:
                return f"This candidate's skills are: {', '.join(skills)}"
            else:
                return "No skills data found."
        return "Sorry, I can only answer questions about skills right now."


    input_col, button_col = st.columns([8, 1])

    with input_col:
        user_msg = st.text_input("Ask me about your resume match:", key="chat_input")

    with button_col:
        clear_button = st.button("Clear", key="clear_chat_button", help="Clear chat history")

    if clear_button:
        st.session_state.chat_history = []
        st.experimental_rerun()

    if user_msg:
        bot_reply = chatbot_response(user_msg)
        st.session_state.chat_history.append(("You", user_msg))
        st.session_state.chat_history.append(("Bot", bot_reply))

    for speaker, message in st.session_state.chat_history:
        if speaker == "You":
            st.markdown(f"**{speaker}:** {message}")
        else:
            st.markdown(f"*{speaker}:* {message}")

    # --- Save / Load Session in Box ---
    st.markdown("""
    <style>
    .session-box {
        border: 1px solid #ddd;
        padding: 12px;
        border-radius: 8px;
        background-color: #f9f9f9;
        margin-top: 20px;
    }
    /* Clear Button Styling */
    div.stButton > button[kind='secondary'] {
        background-color: transparent;
        color: #d9534f;
        border: none;
        padding: 4px 10px;
        font-weight: bold;
        font-size: 13px;
        cursor: pointer;
        height: 28px;
        line-height: 20px;
    }
    div.stButton > button[kind='secondary']:hover {
        color: #c9302c;
        background-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="session-box">', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Session"):
                # Save logic already defined outside (or you can define here)
                if st.session_state.uploaded_resume:
                    with open("saved_resume.pdf", "wb") as f:
                        f.write(st.session_state.uploaded_resume.getbuffer())
                    st.success("Session saved!")
                else:
                    st.warning("No resume to save.")

        with col2:
            if st.button("Load Session"):
                if os.path.exists("saved_resume.pdf"):
                    import io
                    with open("saved_resume.pdf", "rb") as f:
                        bytes_data = f.read()
                        st.session_state.uploaded_resume = io.BytesIO(bytes_data)
                        st.session_state.uploaded_resume.name = "saved_resume.pdf"
                    st.success("Session loaded!")
                else:
                    st.warning("No saved session found.")

#Streamlit run Frontend Resume














