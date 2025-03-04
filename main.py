import os
import spacy
import streamlit as st
from pdfminer.high_level import extract_text as extract_text_from_pdf
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import subprocess

# Ensure 'en_core_web_sm' model is installed
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.warning("Downloading 'en_core_web_sm' model...")
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

st.title("📄 Resume Screening App")
st.write("Upload your resume (PDF/DOCX) and enter a job description to get a match score.")

# Function to extract text from PDF/DOCX
def extract_resume_text(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file).lower()
    else:  # DOCX
        doc = Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs]).lower()

# User inputs job description
job_description = st.text_area("📝 Enter Job Description:")

# User uploads resume file
uploaded_file = st.file_uploader("📂 Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

if uploaded_file and job_description:
    resume_text = extract_resume_text(uploaded_file)

    # Extract keywords using NLP
    def extract_keywords(text):
        doc = nlp(text)
        return {token.text.lower() for token in doc if token.is_alpha and not token.is_stop}

    resume_keywords = extract_keywords(resume_text)
    job_desc_keywords = extract_keywords(job_description)

    # TF-IDF + Cosine Similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([" ".join(job_desc_keywords), " ".join(resume_keywords)])
    score = round(cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0] * 100, 2)

    matched_keywords = resume_keywords.intersection(job_desc_keywords)

    # Display Results
    st.subheader("📊 Results:")
    st.write(f"✅ **Match Score:** {score}%")
    st.write(f"🔢 **Total Matched Keywords:** {len(matched_keywords)}")

    # Show Matched Keywords
    with st.expander("🔍 **View Matched Keywords**"):
        st.write(", ".join(matched_keywords))
