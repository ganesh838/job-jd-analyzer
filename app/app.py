# import streamlit as st
# from groq import Groq
# import spacy
# import warnings
# warnings.filterwarnings('ignore')

# # ── Page Config ───────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="JD Analyzer & Bias Detector",
#     page_icon="🤖",
#     layout="wide"
# )

# # ── Load Models ───────────────────────────────────────────────────────────────
# @st.cache_resource
# def load_nlp():
#     return spacy.load("en_core_web_sm")

# @st.cache_resource
# def load_groq():
#      # ← your key here

# nlp    = load_nlp()
# client = load_groq()

# # ── Lexicons ──────────────────────────────────────────────────────────────────
# male_coded = [
#     "ninja", "rockstar", "dominant", "aggressive", "competitive",
#     "fearless", "assertive", "driven", "ambitious", "strong",
#     "determined", "hero", "warrior", "champion", "genius",
#     "master", "mankind", "manpower", "chairman", "spokesman"
# ]
# female_coded = [
#     "nurturing", "collaborative", "cooperative", "supportive",
#     "caring", "empathetic", "compassionate", "warm", "gentle",
#     "sensitive", "interpersonal", "submissive", "soft", "pleasant"
# ]
# age_biased = [
#     "young", "digital native", "recent graduate", "fresh",
#     "energetic", "youthful", "new blood", "junior only", "early career"
# ]
# toxic_words = [
#     "work hard play hard", "ping pong", "beer fridge", "bro culture",
#     "hustler", "grind", "crush it", "kill it", "dominate",
#     "savage", "beast mode", "boys club", "fraternity"
# ]
# technical_skills = [
#     "python", "r", "sql", "java", "scala", "julia", "c++",
#     "machine learning", "deep learning", "nlp", "computer vision",
#     "tensorflow", "pytorch", "keras", "scikit-learn", "xgboost",
#     "huggingface", "spacy", "nltk", "pandas", "numpy",
#     "matplotlib", "tableau", "power bi", "spark", "hadoop",
#     "airflow", "databricks", "snowflake", "aws", "azure",
#     "gcp", "docker", "kubernetes", "mlflow", "fastapi", "flask",
#     "mysql", "postgresql", "mongodb", "statistics",
#     "hypothesis testing", "a/b testing", "regression",
#     "classification", "clustering", "forecasting"
# ]
# soft_skills = [
#     "communication", "teamwork", "leadership", "problem solving",
#     "critical thinking", "time management", "collaboration",
#     "presentation", "analytical", "attention to detail",
#     "creativity", "adaptability", "project management", "mentoring"
# ]

# # ── Functions ─────────────────────────────────────────────────────────────────
# def detect_bias(text):
#     t = text.lower()
#     found_male   = [w for w in male_coded   if w in t]
#     found_female = [w for w in female_coded if w in t]
#     found_age    = [w for w in age_biased   if w in t]
#     found_toxic  = [w for w in toxic_words  if w in t]
#     score = min(
#         len(found_male)*10 + len(found_female)*10 +
#         len(found_age)*15  + len(found_toxic)*20, 100
#     )
#     if score == 0:    level = "None"
#     elif score <= 20: level = "Low"
#     elif score <= 50: level = "Medium"
#     else:             level = "High"
#     return {
#         'male_coded_words':   found_male,
#         'female_coded_words': found_female,
#         'age_biased_words':   found_age,
#         'toxic_words':        found_toxic,
#         'bias_score':         score,
#         'bias_level':         level
#     }

# import re

# def extract_skills(text):
#     t = text.lower()
#     found_technical = []
#     found_soft = []

#     for skill in technical_skills:
#         # Use word boundary for single letters like 'r'
#         pattern = r'\b' + re.escape(skill) + r'\b'
#         if re.search(pattern, t):
#             found_technical.append(skill)

#     for skill in soft_skills:
#         pattern = r'\b' + re.escape(skill) + r'\b'
#         if re.search(pattern, t):
#             found_soft.append(skill)

#     return {
#         'technical_skills': found_technical,
#         'soft_skills':      found_soft
#     }

# def rewrite_jd(original_jd, bias_result):
#     prompt = f"""You are an expert HR consultant and DEI specialist.

# Rewrite this job description to remove ALL bias.

# ORIGINAL JD:
# {original_jd[:1000]}

# BIAS WORDS TO REMOVE:
# - Male-coded  : {bias_result.get('male_coded_words', [])}
# - Female-coded: {bias_result.get('female_coded_words', [])}
# - Age-biased  : {bias_result.get('age_biased_words', [])}
# - Toxic words : {bias_result.get('toxic_words', [])}

# Rules:
# 1. Remove ALL biased words above
# 2. Replace with neutral inclusive alternatives
# 3. Keep same job role and core requirements
# 4. Make it welcoming to ALL qualified candidates
# 5. Keep it professional and well structured

# Return ONLY the rewritten job description."""

#     try:
#         response = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=2048,
#             temperature=0.7
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         return f"Error: {str(e)}"

# def highlight_words(text, bias_result):
#     all_biased = (
#         bias_result['male_coded_words'] +
#         bias_result['female_coded_words'] +
#         bias_result['age_biased_words'] +
#         bias_result['toxic_words']
#     )
#     for word in all_biased:
#         text = text.replace(word,
#             f'<span style="background:#FF6B6B; color:white; '
#             f'padding:2px 6px; border-radius:4px;">{word}</span>')
#     return text

# def score_color(score):
#     if score == 0:    return "#2E7D32"
#     elif score <= 20: return "#F9A825"
#     elif score <= 50: return "#E65100"
#     else:             return "#B71C1C"

# # ── Session State ─────────────────────────────────────────────────────────────
# if 'bias_result'  not in st.session_state:
#     st.session_state.bias_result  = None
# if 'skill_result' not in st.session_state:
#     st.session_state.skill_result = None
# if 'jd_text'      not in st.session_state:
#     st.session_state.jd_text      = ""
# if 'rewritten'    not in st.session_state:
#     st.session_state.rewritten    = ""

# # ── Header ────────────────────────────────────────────────────────────────────
# st.markdown("""
# <div style="background:linear-gradient(135deg,#1A237E,#1565C0);
#             padding:30px; border-radius:15px; text-align:center;
#             margin-bottom:30px;">
#     <h1 style="color:white; margin:0;">🤖 AI Job Description Analyzer</h1>
#     <p style="color:#BBDEFB; margin-top:8px;">
#         Detect Bias · Extract Skills · Rewrite with LLaMA3 AI
#     </p>
# </div>
# """, unsafe_allow_html=True)

# # ── Sidebar ───────────────────────────────────────────────────────────────────
# with st.sidebar:
#     st.title("⚙️ Settings")
#     st.markdown("---")
#     show_skills = st.toggle("🧠 Show Skill Analysis", value=True)
#     st.markdown("---")
#     st.markdown("### 📊 About")
#     st.info("Analyzes JDs for bias and rewrites using LLaMA3.")
#     st.markdown("**Built by:** Ganesh")
#     st.markdown("**Model:** LLaMA3-8B via Groq")
#     st.markdown("**Dataset:** 1.6M JDs")

# # ── Input ─────────────────────────────────────────────────────────────────────
# # st.markdown("### 📝 Paste Your Job Description")
# # jd_input = st.text_area(
# #     "Job Description Input",
# #     height=200,
# #     placeholder="Paste any job description here...",
# #     label_visibility="collapsed"
# # )

# # col1, col2, col3 = st.columns([1, 1, 1])
# # with col2:
# #     analyze_btn = st.button(
# #         "🔍 Analyze JD",
# #         use_container_width=True,
# #         type="primary"
# #     )

# # # ── Run Analysis ──────────────────────────────────────────────────────────────
# # if analyze_btn:
# #     if jd_input.strip():
# #         with st.spinner("🔍 Analyzing..."):
# #             st.session_state.bias_result  = detect_bias(jd_input)
# #             st.session_state.skill_result = extract_skills(jd_input)
# #             st.session_state.jd_text      = jd_input
# #             st.session_state.rewritten    = ""
# #     else:
# #         st.warning("⚠️ Please paste a job description first!")

# # # ── Show Results ──────────────────────────────────────────────────────────────
# # if st.session_state.bias_result:
# #     bias_result  = st.session_state.bias_result
# #     skill_result = st.session_state.skill_result
# #     jd_text      = st.session_state.jd_text
# #     score        = bias_result['bias_score']
# #     level        = bias_result['bias_level']

# #     st.markdown("---")
# #     st.markdown("## 📊 Analysis Results")

# #     # Score cards
# #     total_biased = sum([
# #         len(bias_result['male_coded_words']),
# #         len(bias_result['female_coded_words']),
# #         len(bias_result['age_biased_words']),
# #         len(bias_result['toxic_words'])
# #     ])
# #     total_skills = (
# #         len(skill_result['technical_skills']) +
# #         len(skill_result['soft_skills'])
# #     )

# #     c1, c2, c3, c4 = st.columns(4)
# #     for col, val, label, bg in [
# #         (c1, score,        "Bias Score",    score_color(score)),
# #         (c2, level,        "Bias Level",    "#1565C0"),
# #         (c3, total_biased, "Biased Words",  "#6A1B9A"),
# #         (c4, total_skills, "Skills Found",  "#2E7D32"),
# #     ]:
# #         col.markdown(f"""
# #         <div style="background:{bg}; padding:20px; border-radius:10px;
# #                     text-align:center; color:white;">
# #             <h1 style="margin:0; font-size:2.2em;">{val}</h1>
# #             <p style="margin:0;">{label}</p>
# #         </div>""", unsafe_allow_html=True)

# #     st.markdown("<br>", unsafe_allow_html=True)

# #     # Bias details
# #     st.markdown("## 🔍 Bias Details")
# #     col1, col2 = st.columns(2)

# #     with col1:
# #         st.markdown("#### Original JD (biased words highlighted)")
# #         highlighted = highlight_words(jd_text, bias_result)
# #         st.markdown(
# #             f'<div style="background:#F5F5F5; padding:15px; '
# #             f'border-radius:10px; height:280px; overflow-y:auto; '
# #             f'line-height:1.7;">{highlighted}</div>',
# #             unsafe_allow_html=True)

# #     with col2:
# #         st.markdown("#### Detected Bias Words")
# #         if bias_result['male_coded_words']:
# #             st.error(f"🔵 Male-coded: {', '.join(bias_result['male_coded_words'])}")
# #         if bias_result['female_coded_words']:
# #             st.warning(f"🟡 Female-coded: {', '.join(bias_result['female_coded_words'])}")
# #         if bias_result['age_biased_words']:
# #             st.warning(f"🟠 Age-biased: {', '.join(bias_result['age_biased_words'])}")
# #         if bias_result['toxic_words']:
# #             st.error(f"🔴 Toxic: {', '.join(bias_result['toxic_words'])}")
# #         if total_biased == 0:
# #             st.success("✅ No bias detected! This is a clean JD.")

# #     st.markdown("<br>", unsafe_allow_html=True)

# #     # Skill analysis
# #     if show_skills:
# #         st.markdown("## 🧠 Skill Analysis")
# #         col1, col2 = st.columns(2)
# #         with col1:
# #             st.markdown("#### 💻 Technical Skills")
# #             if skill_result['technical_skills']:
# #                 badges = " ".join([
# #                     f'<span style="background:#1565C0; color:white; '
# #                     f'padding:4px 10px; border-radius:15px; '
# #                     f'margin:3px; display:inline-block;">{s}</span>'
# #                     for s in skill_result['technical_skills']
# #                 ])
# #                 st.markdown(badges, unsafe_allow_html=True)
# #             else:
# #                 st.info("No technical skills detected.")

# #         with col2:
# #             st.markdown("#### 🤝 Soft Skills")
# #             if skill_result['soft_skills']:
# #                 badges = " ".join([
# #                     f'<span style="background:#2E7D32; color:white; '
# #                     f'padding:4px 10px; border-radius:15px; '
# #                     f'margin:3px; display:inline-block;">{s}</span>'
# #                     for s in skill_result['soft_skills']
# #                 ])
# #                 st.markdown(badges, unsafe_allow_html=True)
# #             else:
# #                 st.info("No soft skills detected.")

# #     st.markdown("<br>", unsafe_allow_html=True)

# #     # ── Rewriter ──────────────────────────────────────────────────────────────
# #     st.markdown("## ✍️ AI-Powered JD Rewriter")

# #     rewrite_btn = st.button(
# #         "🤖 Rewrite JD with LLaMA3",
# #         type="primary",
# #         use_container_width=False
# #     )

# #     if rewrite_btn:
# #         with st.spinner("🤖 LLaMA3 is rewriting your JD... please wait..."):
# #             st.session_state.rewritten = rewrite_jd(jd_text, bias_result)

# #     if st.session_state.rewritten:
# #         col1, col2 = st.columns(2)
# #         with col1:
# #             st.markdown("#### 📋 Original JD")
# #             st.markdown(
# #                 f'<div style="background:#FFEBEE; padding:15px; '
# #                 f'border-radius:10px; height:400px; overflow-y:auto; '
# #                 f'line-height:1.7;">{jd_text}</div>',
# #                 unsafe_allow_html=True)

# #         with col2:
# #             st.markdown("#### ✅ Rewritten JD")
# #             st.markdown(
# #                 f'<div style="background:#E8F5E9; padding:15px; '
# #                 f'border-radius:10px; height:400px; overflow-y:auto; '
# #                 f'line-height:1.7;">{st.session_state.rewritten}</div>',
# #                 unsafe_allow_html=True)

# #         st.download_button(
# #             label="💾 Download Rewritten JD",
# #             data=st.session_state.rewritten,
# #             file_name="rewritten_jd.txt",
# #             mime="text/plain"
# #         )

# # # ── Footer ────────────────────────────────────────────────────────────────────
# # st.markdown("---")
# # st.markdown("""
# # <div style="text-align:center; color:#9E9E9E; font-size:0.85em;">
# #     Built by Ganesh | AI-Powered JD Analyzer | LLaMA3 + spaCy + Streamlit
# # </div>
# # """, unsafe_allow_html=True)
# # ── Mode Selection ────────────────────────────────────────────────────────────
# st.markdown("### 🎯 Choose Mode")
# mode = st.radio(
#     "Select Mode",
#     ["🔍 Analyze & Fix Existing JD", "✍️ Generate Fresh JD from Job Role"],
#     horizontal=True,
#     label_visibility="collapsed"
# )

# st.markdown("---")

# # ════════════════════════════════════════════════════════════════════════════
# # MODE 1 — ANALYZE EXISTING JD
# # ════════════════════════════════════════════════════════════════════════════
# if mode == "🔍 Analyze & Fix Existing JD":

#     st.markdown("### 📝 Paste Your Job Description")
#     jd_input = st.text_area(
#         "Job Description Input",
#         height=200,
#         placeholder="Paste any job description here...",
#         label_visibility="collapsed"
#     )

#     col1, col2, col3 = st.columns([1, 1, 1])
#     with col2:
#         analyze_btn = st.button(
#             "🔍 Analyze JD",
#             use_container_width=True,
#             type="primary"
#         )

#     if analyze_btn:
#         if jd_input.strip():
#             with st.spinner("🔍 Analyzing..."):
#                 st.session_state.bias_result  = detect_bias(jd_input)
#                 st.session_state.skill_result = extract_skills(jd_input)
#                 st.session_state.jd_text      = jd_input
#                 st.session_state.rewritten    = ""
#         else:
#             st.warning("⚠️ Please paste a job description first!")

#     if st.session_state.bias_result:
#         bias_result  = st.session_state.bias_result
#         skill_result = st.session_state.skill_result
#         jd_text      = st.session_state.jd_text
#         score        = bias_result['bias_score']
#         level        = bias_result['bias_level']

#         st.markdown("---")
#         st.markdown("## 📊 Analysis Results")

#         total_biased = sum([
#             len(bias_result['male_coded_words']),
#             len(bias_result['female_coded_words']),
#             len(bias_result['age_biased_words']),
#             len(bias_result['toxic_words'])
#         ])
#         total_skills = (
#             len(skill_result['technical_skills']) +
#             len(skill_result['soft_skills'])
#         )

#         c1, c2, c3, c4 = st.columns(4)
#         for col, val, label, bg in [
#             (c1, score,        "Bias Score",   score_color(score)),
#             (c2, level,        "Bias Level",   "#1565C0"),
#             (c3, total_biased, "Biased Words", "#6A1B9A"),
#             (c4, total_skills, "Skills Found", "#2E7D32"),
#         ]:
#             col.markdown(f"""
#             <div style="background:{bg}; padding:20px; border-radius:10px;
#                         text-align:center; color:white;">
#                 <h1 style="margin:0; font-size:2.2em;">{val}</h1>
#                 <p style="margin:0;">{label}</p>
#             </div>""", unsafe_allow_html=True)

#         st.markdown("<br>", unsafe_allow_html=True)

#         # Bias details
#         st.markdown("## 🔍 Bias Details")
#         col1, col2 = st.columns(2)

#         with col1:
#             st.markdown("#### Original JD (biased words highlighted)")
#             highlighted = highlight_words(jd_text, bias_result)
#             st.markdown(
#                 f'<div style="background:#F5F5F5; padding:15px; '
#                 f'border-radius:10px; height:280px; overflow-y:auto; '
#                 f'line-height:1.7;">{highlighted}</div>',
#                 unsafe_allow_html=True)

#         with col2:
#             st.markdown("#### Detected Bias Words")
#             if bias_result['male_coded_words']:
#                 st.error(f"🔵 Male-coded: {', '.join(bias_result['male_coded_words'])}")
#             if bias_result['female_coded_words']:
#                 st.warning(f"🟡 Female-coded: {', '.join(bias_result['female_coded_words'])}")
#             if bias_result['age_biased_words']:
#                 st.warning(f"🟠 Age-biased: {', '.join(bias_result['age_biased_words'])}")
#             if bias_result['toxic_words']:
#                 st.error(f"🔴 Toxic: {', '.join(bias_result['toxic_words'])}")
#             if total_biased == 0:
#                 st.success("✅ No bias detected! This is a clean JD.")

#         st.markdown("<br>", unsafe_allow_html=True)

#         # Skill analysis
#         if show_skills:
#             st.markdown("## 🧠 Skill Analysis")
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.markdown("#### 💻 Technical Skills")
#                 if skill_result['technical_skills']:
#                     badges = " ".join([
#                         f'<span style="background:#1565C0; color:white; '
#                         f'padding:4px 10px; border-radius:15px; '
#                         f'margin:3px; display:inline-block;">{s}</span>'
#                         for s in skill_result['technical_skills']
#                     ])
#                     st.markdown(badges, unsafe_allow_html=True)
#                 else:
#                     st.info("No technical skills detected.")
#             with col2:
#                 st.markdown("#### 🤝 Soft Skills")
#                 if skill_result['soft_skills']:
#                     badges = " ".join([
#                         f'<span style="background:#2E7D32; color:white; '
#                         f'padding:4px 10px; border-radius:15px; '
#                         f'margin:3px; display:inline-block;">{s}</span>'
#                         for s in skill_result['soft_skills']
#                     ])
#                     st.markdown(badges, unsafe_allow_html=True)
#                 else:
#                     st.info("No soft skills detected.")

#         st.markdown("<br>", unsafe_allow_html=True)

#         # Rewriter
#         st.markdown("## ✍️ AI-Powered JD Rewriter")
#         rewrite_btn = st.button(
#             "🤖 Rewrite JD with LLaMA3",
#             type="primary"
#         )

#         if rewrite_btn:
#             with st.spinner("🤖 LLaMA3 is rewriting your JD..."):
#                 st.session_state.rewritten = rewrite_jd(jd_text, bias_result)

#         if st.session_state.rewritten:
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.markdown("#### 📋 Original JD")
#                 st.markdown(
#                     f'<div style="background:#FFEBEE; padding:15px; '
#                     f'border-radius:10px; height:400px; overflow-y:auto; '
#                     f'line-height:1.7;">{jd_text}</div>',
#                     unsafe_allow_html=True)
#             with col2:
#                 st.markdown("#### ✅ Rewritten JD")
#                 st.markdown(
#                     f'<div style="background:#E8F5E9; padding:15px; '
#                     f'border-radius:10px; height:400px; overflow-y:auto; '
#                     f'line-height:1.7;">{st.session_state.rewritten}</div>',
#                     unsafe_allow_html=True)

#             st.download_button(
#                 label="💾 Download Rewritten JD",
#                 data=st.session_state.rewritten,
#                 file_name="rewritten_jd.txt",
#                 mime="text/plain"
#             )

# # ════════════════════════════════════════════════════════════════════════════
# # MODE 2 — GENERATE FRESH JD
# # ════════════════════════════════════════════════════════════════════════════
# else:
#     st.markdown("### ✍️ Generate a Fresh Inclusive JD")

#     col1, col2 = st.columns(2)

#     with col1:
#         job_role = st.text_input(
#             "Job Role",
#             placeholder="e.g. Data Scientist, HR Manager, Python Developer",
#             label_visibility="visible"
#         )
#         experience = st.selectbox(
#             "Experience Level",
#             ["Entry Level (0-2 years)",
#              "Mid Level (3-5 years)",
#              "Senior Level (6-10 years)",
#              "Lead / Manager (10+ years)"]
#         )
#         work_type = st.selectbox(
#             "Work Type",
#             ["Full-Time", "Part-Time", "Remote", "Hybrid", "Contract"]
#         )

#     with col2:
#         industry = st.selectbox(
#             "Industry",
#             ["Technology", "Healthcare", "Finance", "Education",
#              "Retail", "Manufacturing", "Marketing", "Consulting",
#              "E-commerce", "Other"]
#         )
#         skills_input = st.text_input(
#             "Key Skills (optional)",
#             placeholder="e.g. Python, SQL, Machine Learning",
#             label_visibility="visible"
#         )
#         company_culture = st.selectbox(
#             "Company Culture",
#             ["Collaborative & Inclusive",
#              "Fast-paced & Innovative",
#              "Structured & Process-driven",
#              "Creative & Flexible"]
#         )

#     col1, col2, col3 = st.columns([1, 1, 1])
#     with col2:
#         generate_btn = st.button(
#             "✨ Generate JD",
#             use_container_width=True,
#             type="primary"
#         )

#     if generate_btn:
#         if job_role.strip():
#             with st.spinner(f"✨ Generating inclusive JD for {job_role}..."):

#                 gen_prompt = f"""You are an expert HR consultant specializing in 
# inclusive hiring practices.

# Generate a complete, professional, and bias-free job description for:

# Job Role      : {job_role}
# Experience    : {experience}
# Work Type     : {work_type}
# Industry      : {industry}
# Key Skills    : {skills_input if skills_input else 'Based on the role'}
# Culture       : {company_culture}

# Requirements:
# 1. Use completely inclusive, neutral language
# 2. No gender-coded words (no ninja, rockstar, dominant etc.)
# 3. No age-biased language (no young, digital native etc.)
# 4. No toxic culture words (no hustle, beast mode etc.)
# 5. Include: Job Summary, Responsibilities, Requirements, Nice to Have, Benefits
# 6. Make it attractive to ALL qualified candidates
# 7. Be realistic with requirements — no unicorn JDs
# 8. End with an inclusion statement

# Write a complete professional job description now."""

#                 try:
#                     response = client.chat.completions.create(
#                         model="llama-3.3-70b-versatile",
#                         messages=[{"role": "user", "content": gen_prompt}],
#                         max_tokens=2048,
#                         temperature=0.7
#                     )
#                     generated_jd = response.choices[0].message.content.strip()
#                     st.session_state.generated_jd = generated_jd

#                 except Exception as e:
#                     st.error(f"Error: {str(e)}")

#         else:
#             st.warning("⚠️ Please enter a job role first!")

#     # Show generated JD
#     if 'generated_jd' in st.session_state and st.session_state.generated_jd:

#         st.markdown("---")
#         st.markdown("## ✅ Generated Job Description")

#         # Analyze the generated JD for bias
#         gen_bias = detect_bias(st.session_state.generated_jd)
#         gen_skills = extract_skills(st.session_state.generated_jd)

#         # Score cards
#         c1, c2, c3, c4 = st.columns(4)
#         total_skills = (
#             len(gen_skills['technical_skills']) +
#             len(gen_skills['soft_skills'])
#         )
#         for col, val, label, bg in [
#             (c1, gen_bias['bias_score'], "Bias Score",   score_color(gen_bias['bias_score'])),
#             (c2, gen_bias['bias_level'], "Bias Level",   "#1565C0"),
#             (c3, "Inclusive",            "JD Quality",   "#2E7D32"),
#             (c4, total_skills,           "Skills Added", "#6A1B9A"),
#         ]:
#             col.markdown(f"""
#             <div style="background:{bg}; padding:20px; border-radius:10px;
#                         text-align:center; color:white;">
#                 <h1 style="margin:0; font-size:2em;">{val}</h1>
#                 <p style="margin:0;">{label}</p>
#             </div>""", unsafe_allow_html=True)

#         st.markdown("<br>", unsafe_allow_html=True)

#         # Show JD
#         st.markdown(
#             f'<div style="background:#E8F5E9; padding:20px; '
#             f'border-radius:10px; line-height:1.8; font-size:0.95em;">'
#             f'{st.session_state.generated_jd}</div>',
#             unsafe_allow_html=True)

#         st.markdown("<br>", unsafe_allow_html=True)

#         # Skills found
#         if show_skills:
#             st.markdown("### 🧠 Skills in Generated JD")
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.markdown("#### 💻 Technical Skills")
#                 if gen_skills['technical_skills']:
#                     badges = " ".join([
#                         f'<span style="background:#1565C0; color:white; '
#                         f'padding:4px 10px; border-radius:15px; '
#                         f'margin:3px; display:inline-block;">{s}</span>'
#                         for s in gen_skills['technical_skills']
#                     ])
#                     st.markdown(badges, unsafe_allow_html=True)
#                 else:
#                     st.info("No technical skills detected.")
#             with col2:
#                 st.markdown("#### 🤝 Soft Skills")
#                 if gen_skills['soft_skills']:
#                     badges = " ".join([
#                         f'<span style="background:#2E7D32; color:white; '
#                         f'padding:4px 10px; border-radius:15px; '
#                         f'margin:3px; display:inline-block;">{s}</span>'
#                         for s in gen_skills['soft_skills']
#                     ])
#                     st.markdown(badges, unsafe_allow_html=True)

#         # Download
#         st.download_button(
#             label="💾 Download Generated JD",
#             data=st.session_state.generated_jd,
#             file_name=f"{job_role.replace(' ', '_')}_JD.txt",
#             mime="text/plain"
#         )

# # ── Footer ────────────────────────────────────────────────────────────────────
# st.markdown("---")
# st.markdown("""
# <div style="text-align:center; color:#9E9E9E; font-size:0.85em;">
#     Built by Ganesh | AI-Powered JD Analyzer | LLaMA3 + spaCy + Streamlit
# </div>
# """, unsafe_allow_html=True)


import streamlit as st
from groq import Groq
import spacy
import re
import warnings
warnings.filterwarnings('ignore')

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="JD Analyzer & Bias Detector",
    page_icon="🤖",
    layout="wide"
)

# ── Load Models ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        import subprocess, sys
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        return spacy.load("en_core_web_sm")

@st.cache_resource
def load_groq():
    return Groq(api_key=st.secrets["GROQ_API_KEY"]) # ← your key here
    
nlp    = load_nlp()
client = load_groq()

# ── Lexicons ──────────────────────────────────────────────────────────────────
male_coded = [
    "ninja", "rockstar", "dominant", "aggressive", "competitive",
    "fearless", "assertive", "driven", "ambitious", "strong",
    "determined", "hero", "warrior", "champion", "genius",
    "master", "mankind", "manpower", "chairman", "spokesman"
]
female_coded = [
    "nurturing", "collaborative", "cooperative", "supportive",
    "caring", "empathetic", "compassionate", "warm", "gentle",
    "sensitive", "interpersonal", "submissive", "soft", "pleasant"
]
age_biased = [
    "young", "digital native", "recent graduate only",
    "youthful", "new blood", "junior only",
    "mature candidates only", "seasoned only"
]
toxic_words = [
    "work hard play hard", "ping pong", "beer fridge", "bro culture",
    "hustler", "grind", "crush it", "kill it", "dominate",
    "savage", "beast mode", "boys club", "fraternity"
]
technical_skills = [
    # Programming
    "python", "r", "sql", "java", "scala", "julia", "c++",
    "javascript", "typescript", "html", "css", "php", "ruby",
    "swift", "kotlin", "go", "rust",
    # ML & AI
    "machine learning", "deep learning", "nlp", "computer vision",
    "reinforcement learning", "large language models", "llm",
    "generative ai", "neural networks", "transfer learning",
    # ML Libraries
    "tensorflow", "pytorch", "keras", "scikit-learn", "xgboost",
    "lightgbm", "huggingface", "spacy", "nltk", "opencv",
    # Data Tools
    "pandas", "numpy", "matplotlib", "seaborn", "plotly",
    "tableau", "power bi", "excel", "jupyter",
    # Web Frameworks
    "react", "angular", "vue", "django", "fastapi",
    "flask", "node", "express", "spring",
    # DevOps & Version Control
    "git", "github", "gitlab", "docker", "kubernetes",
    "jenkins", "linux", "bash",
    # Cloud
    "aws", "azure", "gcp", "google cloud",
    "mlflow", "airflow", "dbt",
    # Big Data
    "spark", "hadoop", "kafka",
    "databricks", "snowflake", "redshift", "bigquery",
    # Databases
    "mysql", "postgresql", "mongodb", "cassandra", "redis",
    # Statistics
    "statistics", "probability", "hypothesis testing",
    "a/b testing", "regression", "classification",
    "clustering", "forecasting",
    # Other
    "agile", "scrum", "jira", "figma",
    "rest api", "graphql", "microservices", "wcag"
]
soft_skills = [
    "communication", "teamwork", "leadership", "problem solving",
    "critical thinking", "time management", "collaboration",
    "presentation", "analytical", "attention to detail",
    "creativity", "adaptability", "project management", "mentoring"
]

# ── Functions ─────────────────────────────────────────────────────────────────
def detect_bias(text):
    t = text.lower()

    def find_words(word_list):
        found = []
        for w in word_list:
            pattern = r'\b' + re.escape(w) + r'\b'
            if re.search(pattern, t):
                found.append(w)
        return found

    found_male   = find_words(male_coded)
    found_female = find_words(female_coded)
    found_age    = find_words(age_biased)
    found_toxic  = find_words(toxic_words)

    score = min(
        len(found_male)*10 + len(found_female)*10 +
        len(found_age)*15  + len(found_toxic)*20, 100
    )

    if score == 0:    level = "None"
    elif score <= 20: level = "Low"
    elif score <= 50: level = "Medium"
    else:             level = "High"

    return {
        'male_coded_words':   found_male,
        'female_coded_words': found_female,
        'age_biased_words':   found_age,
        'toxic_words':        found_toxic,
        'bias_score':         score,
        'bias_level':         level
    }

def extract_skills(text):
    t = text.lower()
    found_technical = []
    found_soft = []

    for skill in technical_skills:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, t):
            found_technical.append(skill)

    for skill in soft_skills:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, t):
            found_soft.append(skill)

    return {
        'technical_skills': found_technical,
        'soft_skills':      found_soft
    }

def rewrite_jd(original_jd, bias_result):
    prompt = f"""You are an expert HR consultant and DEI specialist.

Rewrite this job description to remove ALL bias.

ORIGINAL JD:
{original_jd[:1000]}

BIAS WORDS TO REMOVE:
- Male-coded  : {bias_result.get('male_coded_words', [])}
- Female-coded: {bias_result.get('female_coded_words', [])}
- Age-biased  : {bias_result.get('age_biased_words', [])}
- Toxic words : {bias_result.get('toxic_words', [])}

Rules:
1. Remove ALL biased words above
2. Replace with neutral inclusive alternatives
3. Keep same job role and core requirements
4. Make it welcoming to ALL qualified candidates
5. Keep it professional and well structured

Return ONLY the rewritten job description."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def highlight_words(text, bias_result):
    all_biased = (
        bias_result['male_coded_words'] +
        bias_result['female_coded_words'] +
        bias_result['age_biased_words'] +
        bias_result['toxic_words']
    )
    for word in all_biased:
        text = text.replace(word,
            f'<span style="background:#FF6B6B; color:white; '
            f'padding:2px 6px; border-radius:4px;">{word}</span>')
    return text

def score_color(score):
    if score == 0:    return "#2E7D32"
    elif score <= 20: return "#F9A825"
    elif score <= 50: return "#E65100"
    else:             return "#B71C1C"

def skill_badge(skill, color):
    return (f'<span style="background:{color}; color:white; '
            f'padding:4px 10px; border-radius:15px; '
            f'margin:3px; display:inline-block;">{skill}</span>')

# ── Session State ─────────────────────────────────────────────────────────────
for key, val in {
    'bias_result':  None,
    'skill_result': None,
    'jd_text':      "",
    'rewritten':    "",
    'generated_jd': ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#1A237E,#1565C0);
            padding:30px; border-radius:15px; text-align:center;
            margin-bottom:30px;">
    <h1 style="color:white; margin:0;">🤖 AI Job Description Analyzer</h1>
    <p style="color:#BBDEFB; margin-top:8px;">
        Detect Bias · Extract Skills · Rewrite with LLaMA3 AI · Generate Fresh JDs
    </p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("---")
    show_skills = st.toggle("🧠 Show Skill Analysis", value=True)
    st.markdown("---")
    st.markdown("### 📊 About")
    st.info("Analyzes JDs for bias and rewrites using LLaMA3.")
    st.markdown("**Built by:** Ganesh")
    st.markdown("**Model:** LLaMA3-70B via Groq")
    st.markdown("**Dataset:** 1.6M JDs")

# ── Mode Selection ────────────────────────────────────────────────────────────
st.markdown("### 🎯 Choose Mode")
mode = st.radio(
    "Select Mode",
    ["🔍 Analyze & Fix Existing JD",
     "✍️ Generate Fresh JD from Job Role"],
    horizontal=True,
    label_visibility="collapsed"
)
st.markdown("---")

# ════════════════════════════════════════════════════════════════════════════
# MODE 1 — ANALYZE EXISTING JD
# ════════════════════════════════════════════════════════════════════════════
if mode == "🔍 Analyze & Fix Existing JD":

    st.markdown("### 📝 Paste Your Job Description")
    jd_input = st.text_area(
        "Job Description Input",
        height=200,
        placeholder="Paste any job description here...",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_btn = st.button(
            "🔍 Analyze JD",
            use_container_width=True,
            type="primary"
        )

    if analyze_btn:
        if jd_input.strip():
            with st.spinner("🔍 Analyzing..."):
                st.session_state.bias_result  = detect_bias(jd_input)
                st.session_state.skill_result = extract_skills(jd_input)
                st.session_state.jd_text      = jd_input
                st.session_state.rewritten    = ""
        else:
            st.warning("⚠️ Please paste a job description first!")

    if st.session_state.bias_result:
        bias_result  = st.session_state.bias_result
        skill_result = st.session_state.skill_result
        jd_text      = st.session_state.jd_text
        score        = bias_result['bias_score']
        level        = bias_result['bias_level']

        st.markdown("---")
        st.markdown("## 📊 Analysis Results")

        total_biased = sum([
            len(bias_result['male_coded_words']),
            len(bias_result['female_coded_words']),
            len(bias_result['age_biased_words']),
            len(bias_result['toxic_words'])
        ])
        total_skills = (
            len(skill_result['technical_skills']) +
            len(skill_result['soft_skills'])
        )

        c1, c2, c3, c4 = st.columns(4)
        for col, val, label, bg in [
            (c1, score,        "Bias Score",   score_color(score)),
            (c2, level,        "Bias Level",   "#1565C0"),
            (c3, total_biased, "Biased Words", "#6A1B9A"),
            (c4, total_skills, "Skills Found", "#2E7D32"),
        ]:
            col.markdown(f"""
            <div style="background:{bg}; padding:20px; border-radius:10px;
                        text-align:center; color:white;">
                <h1 style="margin:0; font-size:2.2em;">{val}</h1>
                <p style="margin:0;">{label}</p>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Bias details
        st.markdown("## 🔍 Bias Details")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Original JD (biased words highlighted)")
            highlighted = highlight_words(jd_text, bias_result)
            st.markdown(
                f'<div style="background:#F5F5F5; padding:15px; '
                f'border-radius:10px; height:280px; overflow-y:auto; '
                f'line-height:1.7;">{highlighted}</div>',
                unsafe_allow_html=True)

        with col2:
            st.markdown("#### Detected Bias Words")
            if bias_result['male_coded_words']:
                st.error(f"🔵 Male-coded: {', '.join(bias_result['male_coded_words'])}")
            if bias_result['female_coded_words']:
                st.warning(f"🟡 Female-coded: {', '.join(bias_result['female_coded_words'])}")
            if bias_result['age_biased_words']:
                st.warning(f"🟠 Age-biased: {', '.join(bias_result['age_biased_words'])}")
            if bias_result['toxic_words']:
                st.error(f"🔴 Toxic: {', '.join(bias_result['toxic_words'])}")
            if total_biased == 0:
                st.success("✅ No bias detected! This is a clean JD.")

        st.markdown("<br>", unsafe_allow_html=True)

        # Skill analysis
        if show_skills:
            st.markdown("## 🧠 Skill Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 💻 Technical Skills")
                if skill_result['technical_skills']:
                    badges = " ".join([skill_badge(s, "#1565C0")
                                       for s in skill_result['technical_skills']])
                    st.markdown(badges, unsafe_allow_html=True)
                else:
                    st.info("No technical skills detected.")
            with col2:
                st.markdown("#### 🤝 Soft Skills")
                if skill_result['soft_skills']:
                    badges = " ".join([skill_badge(s, "#2E7D32")
                                       for s in skill_result['soft_skills']])
                    st.markdown(badges, unsafe_allow_html=True)
                else:
                    st.info("No soft skills detected.")

        st.markdown("<br>", unsafe_allow_html=True)

        # Rewriter
        st.markdown("## ✍️ AI-Powered JD Rewriter")
        rewrite_btn = st.button(
            "🤖 Rewrite JD with LLaMA3",
            type="primary"
        )

        if rewrite_btn:
            with st.spinner("🤖 LLaMA3 is rewriting your JD..."):
                st.session_state.rewritten = rewrite_jd(jd_text, bias_result)

        if st.session_state.rewritten:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📋 Original JD")
                st.markdown(
                    f'<div style="background:#FFEBEE; padding:15px; '
                    f'border-radius:10px; height:400px; overflow-y:auto; '
                    f'line-height:1.7;">{jd_text}</div>',
                    unsafe_allow_html=True)
            with col2:
                st.markdown("#### ✅ Rewritten JD")
                st.markdown(
                    f'<div style="background:#E8F5E9; padding:15px; '
                    f'border-radius:10px; height:400px; overflow-y:auto; '
                    f'line-height:1.7;">{st.session_state.rewritten}</div>',
                    unsafe_allow_html=True)

            st.download_button(
                label="💾 Download Rewritten JD",
                data=st.session_state.rewritten,
                file_name="rewritten_jd.txt",
                mime="text/plain"
            )

# ════════════════════════════════════════════════════════════════════════════
# MODE 2 — GENERATE FRESH JD
# ════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("### ✍️ Generate a Fresh Inclusive JD")

    col1, col2 = st.columns(2)

    with col1:
        job_role = st.text_input(
            "Job Role",
            placeholder="e.g. Data Scientist, HR Manager, Python Developer",
            label_visibility="visible"
        )
        experience = st.selectbox(
            "Experience Level",
            ["Entry Level (0-2 years)",
             "Mid Level (3-5 years)",
             "Senior Level (6-10 years)",
             "Lead / Manager (10+ years)"]
        )
        work_type = st.selectbox(
            "Work Type",
            ["Full-Time", "Part-Time", "Remote", "Hybrid", "Contract"]
        )

    with col2:
        industry = st.selectbox(
            "Industry",
            ["Technology", "Healthcare", "Finance", "Education",
             "Retail", "Manufacturing", "Marketing", "Consulting",
             "E-commerce", "Other"]
        )
        skills_input = st.text_input(
            "Key Skills (optional)",
            placeholder="e.g. Python, SQL, Machine Learning",
            label_visibility="visible"
        )
        company_culture = st.selectbox(
            "Company Culture",
            ["Collaborative & Inclusive",
             "Fast-paced & Innovative",
             "Structured & Process-driven",
             "Creative & Flexible"]
        )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_btn = st.button(
            "✨ Generate JD",
            use_container_width=True,
            type="primary"
        )

    if generate_btn:
        if job_role.strip():
            with st.spinner(f"✨ Generating inclusive JD for {job_role}..."):
                gen_prompt = f"""You are an expert HR consultant specializing
in inclusive hiring practices.

Generate a complete, professional, bias-free job description for:

Job Role      : {job_role}
Experience    : {experience}
Work Type     : {work_type}
Industry      : {industry}
Key Skills    : {skills_input if skills_input else 'Based on the role'}
Culture       : {company_culture}

Requirements:
1. Use completely inclusive, neutral language
2. No gender-coded words (no ninja, rockstar, dominant etc.)
3. No age-biased language (no young, digital native etc.)
4. No toxic culture words (no hustle, beast mode etc.)
5. Include: Job Summary, Responsibilities, Requirements,
   Nice to Have, Benefits
6. Make it attractive to ALL qualified candidates
7. Be realistic — no unicorn JDs
8. End with an inclusion statement

Write a complete professional job description now."""

                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": gen_prompt}],
                        max_tokens=2048,
                        temperature=0.7
                    )
                    st.session_state.generated_jd = \
                        response.choices[0].message.content.strip()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a job role first!")

    if st.session_state.generated_jd:
        st.markdown("---")
        st.markdown("## ✅ Generated Job Description")

        gen_bias   = detect_bias(st.session_state.generated_jd)
        gen_skills = extract_skills(st.session_state.generated_jd)

        total_skills = (
            len(gen_skills['technical_skills']) +
            len(gen_skills['soft_skills'])
        )

        c1, c2, c3, c4 = st.columns(4)
        for col, val, label, bg in [
            (c1, gen_bias['bias_score'], "Bias Score",   score_color(gen_bias['bias_score'])),
            (c2, gen_bias['bias_level'], "Bias Level",   "#1565C0"),
            (c3, "Inclusive",            "JD Quality",   "#2E7D32"),
            (c4, total_skills,           "Skills Added", "#6A1B9A"),
        ]:
            col.markdown(f"""
            <div style="background:{bg}; padding:20px; border-radius:10px;
                        text-align:center; color:white;">
                <h1 style="margin:0; font-size:2em;">{val}</h1>
                <p style="margin:0;">{label}</p>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            f'<div style="background:#E8F5E9; padding:20px; '
            f'border-radius:10px; line-height:1.8; font-size:0.95em;">'
            f'{st.session_state.generated_jd}</div>',
            unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if show_skills:
            st.markdown("### 🧠 Skills in Generated JD")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 💻 Technical Skills")
                if gen_skills['technical_skills']:
                    badges = " ".join([skill_badge(s, "#1565C0")
                                       for s in gen_skills['technical_skills']])
                    st.markdown(badges, unsafe_allow_html=True)
                else:
                    st.info("No technical skills detected.")
            with col2:
                st.markdown("#### 🤝 Soft Skills")
                if gen_skills['soft_skills']:
                    badges = " ".join([skill_badge(s, "#2E7D32")
                                       for s in gen_skills['soft_skills']])
                    st.markdown(badges, unsafe_allow_html=True)

        st.download_button(
            label="💾 Download Generated JD",
            data=st.session_state.generated_jd,
            file_name=f"{job_role.replace(' ', '_')}_JD.txt",
            mime="text/plain"
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#9E9E9E; font-size:0.85em;">
    Built by Ganesh | AI-Powered JD Analyzer | LLaMA3 + spaCy + Streamlit
</div>
""", unsafe_allow_html=True)