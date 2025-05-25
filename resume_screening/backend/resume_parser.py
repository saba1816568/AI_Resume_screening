# Extract text from resumes
import os
import pdfminer.high_level
import docx
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download stopwords if not already downloaded
nltk.download("punkt")
nltk.download("stopwords")
nltk.download('punkt_tab')

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        text = pdfminer.high_level.extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

def clean_text(text):
    """Preprocess the extracted text: remove special characters and stopwords."""
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W+', ' ', text)  # Remove special characters
    words = word_tokenize(text)  # Tokenize
    words = [word for word in words if word not in stopwords.words("english")]  # Remove stopwords
    return " ".join(words)

def parse_resume(file_path):
    """Extract and clean text from a resume (PDF/DOCX)."""
    ext = file_path.split(".")[-1].lower()
    
    if ext == "pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == "docx":
        text = extract_text_from_docx(file_path)
    else:
        print("Unsupported file format!")
        return None

    return clean_text(text)

# Example Usage
if __name__ == "__main__":
    resume_path = "F://SABA_RESUME.pdf"  # Change to your test resume
    text = parse_resume(resume_path)
    print(text)
