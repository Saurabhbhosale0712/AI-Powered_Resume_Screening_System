import os
import spacy
import streamlit as st
from pdfminer.high_level import extract_text as extract_text_from_pdf
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        os.system("python -m spacy download en_core_web_sm")
        return spacy.load("en_core_web_sm")

nlp = load_spacy_model()



def extract_text(file):
    """Extract text from PDF or DOCX file."""
    text = ""
    if file.name.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
    return text.lower()

def extract_keywords(text):
    """Extract meaningful keywords from text using spaCy."""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    return keywords

def calculate_match_score(resume_text, job_desc):
    """Calculate similarity score between resume and job description."""
    vectorizer = TfidfVectorizer()
    documents = [job_desc, resume_text]
    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return round(similarity_score * 100, 2)

def match_keywords(resume_text, job_desc_text):
    """Find matching keywords between job description and resume."""
    resume_keywords = set(extract_keywords(resume_text))
    job_desc_keywords = set(extract_keywords(job_desc_text))
    return resume_keywords.intersection(job_desc_keywords)

def main():
    st.title("📄 Resume Screening App")
    st.write("Upload your resume (PDF/DOCX) and enter a job description to get a match score.")
    
    job_description = st.text_area("Enter Job Description:")
    uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    
    if uploaded_file and job_description:
        resume_text = extract_text(uploaded_file)
        job_desc_cleaned = extract_keywords(job_description)
        resume_text_cleaned = extract_keywords(resume_text)
        
        score = calculate_match_score(" ".join(resume_text_cleaned), " ".join(job_desc_cleaned))
        matched_keywords = match_keywords(resume_text, job_description)
        
        st.subheader("Results:")
        st.write(f"✅ **Match Score:** {score}%")
        st.write(f"✅ **Matched Keywords:** {', '.join(matched_keywords)}")
        st.write(f"🔢 **Total Matches:** {len(matched_keywords)}")

if __name__ == "__main__":
    main()


# # Inside your main function, after calculating results:
# st.write(f"✅ **Match Score:** {score} %")
# with st.expander("🔍 **View Matched Keywords**"):
#     st.write(matched_keywords)  # Show matched keywords inside an expandable section
# st.write(f"🔢 **Total Matches:** {len(matched_keywords)}")
