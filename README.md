# Resume-Screening-App--Streamlit

### **1. How to Create a Virtual Environment in VS Code?**  
A **virtual environment (venv)** helps to manage dependencies and prevent conflicts between different projects.

#### **Steps to Create and Activate a Virtual Environment:**
1️⃣ **Open VS Code Terminal** (`Ctrl + ~`)  
2️⃣ **Navigate to Your Project Folder**  
   ```bash
   cd "C:\VS TECH\Resume_Screener"
   ```
3️⃣ **Create a Virtual Environment**  
   ```bash
   python -m venv venv
   ```
   - This creates a `venv` folder inside your project.
4️⃣ **Activate the Virtual Environment**  
   - **For Windows (PowerShell):**  
     ```bash
     venv\Scripts\activate
     ```
   - **For Mac/Linux:**  
     ```bash
     source venv/bin/activate
     ```
5️⃣ **Install Required Libraries** (from `requirements.txt`):  
   ```bash
   pip install -r requirements.txt
   ```

---

### **2. Why is the `requirements.txt` File Important?**  
The `requirements.txt` file stores a list of all the dependencies (libraries) needed for your project.  

🔹 **Why is it important?**  
✅ Helps in quick project setup on a new system  
✅ Ensures everyone working on the project has the same dependencies  
✅ Avoids compatibility issues  

🔹 **How to Create It?**  
```bash
pip freeze > requirements.txt
```
🔹 **How to Use It?**  
To install all dependencies from this file:  
```bash
pip install -r requirements.txt
```

---

### **3. Which Libraries Must Be Installed and Why?**  

| **Library**           | **Why It’s Needed?** |
|----------------------|-------------------|
| `streamlit`          | To create the web app |
| `pdfminer.six`       | Extract text from PDFs |
| `python-docx`        | Extract text from DOCX files |
| `spacy`              | Perform NLP tasks like keyword extraction |
| `scikit-learn`       | Calculate **match score** using TF-IDF & cosine similarity |
| `nltk`               | Text preprocessing (optional) |
| `fuzzywuzzy`         | Fuzzy matching for similar words (optional) |
| `pandas`             | Data handling and manipulation |

**Install all these using:**  
```bash
pip install streamlit pdfminer.six python-docx spacy scikit-learn nltk fuzzywuzzy pandas
```
---

### **4. Understanding Match Score, Keyword Matches & Total Match (with Example)**  

#### **🔹 What Are They?**
- **Match Score (%)** → How similar the resume is to the job description  
- **Keyword Matches** → Common words found in both  
- **Total Matches** → Count of matched keywords  

#### **🔹 Simple Example**  
Imagine the **Job Description (JD)** contains these keywords:  
➡ **"Python, SQL, Machine Learning, Data Science"**  

And the **Resume** contains:  
➡ **"Python, SQL, Tableau, Excel"**  

🔸 **Keyword Matches** = `{Python, SQL}`  
🔸 **Total Matches** = **2**  
🔸 **Match Score** (Using TF-IDF and Cosine Similarity) = **50%** (example value)

#### **🔹 How Is Match Score Calculated?**  
1️⃣ Convert **resume & job description** into **numerical vectors** (TF-IDF)  
2️⃣ Use **cosine similarity** to compare them  
3️⃣ Multiply by 100 to get a percentage  
   ```python
   from sklearn.feature_extraction.text import TfidfVectorizer
   from sklearn.metrics.pairwise import cosine_similarity

   def calculate_match_score(resume_text, job_desc_text):
       vectorizer = TfidfVectorizer()
       tfidf_matrix = vectorizer.fit_transform([job_desc_text, resume_text])
       score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
       return round(score * 100, 2)

   job_description = "Python SQL Machine Learning Data Science"
   resume_text = "Python SQL Tableau Excel"

   score = calculate_match_score(resume_text, job_description)
   print("Match Score:", score, "%")
   ```
✔ **Higher score = better match!** 🚀  

---

### **Understanding Match Score, Keyword Matches, and Total Matches in Resume Screening**  

In resume screening, we compare a **resume** with a **job description (JD)** to find how well they match. The key metrics used are:  
1. **Match Score (%)** – Measures overall similarity  
2. **Keyword Matches** – Identifies common words between the resume and JD  
3. **Total Matches** – Counts the number of matched words  

---

## **1️⃣ Understanding Match Score (%)**
The **Match Score** tells us how similar a resume is to a job description using **TF-IDF and Cosine Similarity**.

### **What is Cosine Similarity?**
- It calculates how **close** two texts are based on word frequency.
- If **Match Score = 100%**, the resume and job description are **exactly the same**.
- If **Match Score = 0%**, there are **no matching words**.

🔹 **Formula for Cosine Similarity:**  
\[
\text{cosine similarity} = \frac{A \cdot B}{||A|| \times ||B||}
\]
where:
- \( A \) and \( B \) are vectors representing words in the JD and resume.
- \( ||A|| \) and \( ||B|| \) are their magnitudes.

---

## **2️⃣ Understanding Keyword Matches**
- This tells us **which words from the job description** are found in the resume.  
- These keywords are often **technical skills** (e.g., "Python", "SQL") or **soft skills** (e.g., "communication", "leadership").  
- A higher **number of keyword matches** means the resume is **more relevant** to the job.

🔹 **Example:**
📌 **Job Description:** `"Python, SQL, Machine Learning, Data Science"`  
📌 **Resume:** `"Python, SQL, Tableau, Excel"`  

🔹 **Keyword Matches:** `{Python, SQL}`  
🔹 **Total Matches:** **2**

---

## **3️⃣ Understanding Total Matches**
- **Total Matches** is simply the **count of words that match** between the resume and the JD.
- A resume with **more matches** is **more relevant** to the job.

🔹 **Example:**  
📌 **Job Description:** `"Python, SQL, Machine Learning, Data Science"`  
📌 **Resume:** `"Python, SQL, Tableau, Excel, Machine Learning"`  

🔹 **Keyword Matches:** `{Python, SQL, Machine Learning}`  
🔹 **Total Matches:** **3**

---

## **4️⃣ Implementing Match Score Calculation in Python**
We can use **TF-IDF (Term Frequency-Inverse Document Frequency)** to convert text into **vectors** and then use **cosine similarity** to compare them.

### **🔹 Step 1: Install Required Libraries**
```bash
pip install scikit-learn
```

### **🔹 Step 2: Write Python Code to Compute Match Score**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text, job_desc_text):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([job_desc_text, resume_text])
    score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return round(score * 100, 2)  # Convert to percentage

# Example Job Description and Resume
job_description = "Python SQL Machine Learning Data Science"
resume_text = "Python SQL Tableau Excel"

# Calculate Match Score
score = calculate_match_score(resume_text, job_description)
print("Match Score:", score, "%")
```

---

1️⃣ **Convert Text to Vectors**  
- `TfidfVectorizer()` converts words into numerical values based on their importance.  
- **Example:**  
   - `"Python SQL Machine Learning Data Science"` → `[0.5, 0.3, 0.2, 0.4]`  
   - `"Python SQL Tableau Excel"` → `[0.5, 0.3, 0.0, 0.0]`  

2️⃣ **Apply Cosine Similarity**  
- Measures **how similar** these two vectors are.

3️⃣ **Multiply by 100**  
- Converts similarity into a percentage.

---

## **6️⃣ Displaying Keyword Matches**
To show **matching words and their count**, use this code:

```python
def keyword_matches(resume_text, job_desc_text):
    resume_words = set(resume_text.lower().split())
    job_desc_words = set(job_desc_text.lower().split())
    common_words = resume_words.intersection(job_desc_words)  # Find common words
    return list(common_words), len(common_words)

# Example Usage
matches, total_matches = keyword_matches(resume_text, job_description)
print("Keyword Matches:", matches)
print("Total Matches:", total_matches)
```

---

## **7️⃣ Full Example with Match Score + Keyword Matches**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text, job_desc_text):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([job_desc_text, resume_text])
    score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return round(score * 100, 2)

def keyword_matches(resume_text, job_desc_text):
    resume_words = set(resume_text.lower().split())
    job_desc_words = set(job_desc_text.lower().split())
    common_words = resume_words.intersection(job_desc_words)
    return list(common_words), len(common_words)

# Example Job Description and Resume
job_description = "Python SQL Machine Learning Data Science"
resume_text = "Python SQL Tableau Excel Machine Learning"

# Calculate Match Score
match_score = calculate_match_score(resume_text, job_description)
matches, total_matches = keyword_matches(resume_text, job_description)

# Print Results
print("Match Score:", match_score, "%")
print("Keyword Matches:", matches)
print("Total Matches:", total_matches)
```

---

## **8️⃣ Example Output**
```
Match Score: 65.32 %
Keyword Matches: ['python', 'sql', 'machine']
Total Matches: 3
```

---

## **9️⃣ Summary**
✅ **Match Score (%)** → Measures similarity using **TF-IDF + Cosine Similarity**  
✅ **Keyword Matches** → Words common between resume & job description  
✅ **Total Matches** → Number of matched words  

---

### **Summary**
✅ **Create Virtual Environment** → `python -m venv venv` & activate it  
✅ **Use `requirements.txt`** → Saves dependencies & ensures compatibility  
✅ **Install Important Libraries** → NLP, text extraction, Streamlit, ML tools  
✅ **Calculate Match Score** → Use **TF-IDF & Cosine Similarity**  
