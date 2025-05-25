# Ranking logic
import os
import resume_parser as rp
import gensim.downloader as api
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score


# Load Google's pre-trained Word2Vec model
word2vec_model = api.load("word2vec-google-news-300")

def get_word2vec_embedding(text):
    """Convert text into Word2Vec vector representation."""
    words = text.split()  # Tokenize text
    word_vectors = [word2vec_model[word] for word in words if word in word2vec_model]

    if len(word_vectors) == 0:
        return np.zeros(300)  # Return zero vector if no words match

    return np.mean(word_vectors, axis=0)  # Compute average word vector



def calculate_similarity(resume_text, job_description):
    """Compute Cosine Similarity between Resume and Job Description."""
    resume_vector = get_word2vec_embedding(resume_text)
    job_vector = get_word2vec_embedding(job_description)
    
    # Reshape vectors to 2D array for cosine similarity computation
    resume_vector = resume_vector.reshape(1, -1)
    job_vector = job_vector.reshape(1, -1)
    
    similarity = cosine_similarity(resume_vector, job_vector)[0][0]
    return similarity


def rank_resumes(resume_path, job_description):
    """
    Rank multiple resumes based on their similarity to the job description.
    
    Args:
        resume_texts (list): List of resume texts.
        job_description (str): Job description.

    Returns:
        list: Sorted list of tuples (resume_index, similarity_score)
    """
    scores = []
    
    for i, resume in enumerate(resume_path):
        text = rp.parse_resume(resume)
        similarity = calculate_similarity(text, job_description)
        scores.append((i, similarity))
    
    # Sort by similarity score in descending order (highest match first)
    ranked_resumes = sorted(scores, key=lambda x: x[1], reverse=True)
    return ranked_resumes

# for finding confusion/evaluation matrix 
# Example: True relevance scores (Human-labeled)
true_labels = [1, 2, 3, 4, 5]  # (1 = most relevant, 5 = least relevant)

# Predicted relevance scores (from ML model)
predicted_labels = [2, 1, 4, 5, 3]  # (Your model's ranking)

# Convert rankings into binary relevance (Top 3 are "relevant" = 1, others = 0)
true_binary = np.array([1 if x <= 3 else 0 for x in true_labels])
predicted_binary = np.array([1 if x <= 3 else 0 for x in predicted_labels])

# Calculate ML metrics
precision = precision_score(true_binary, predicted_binary)
recall = recall_score(true_binary, predicted_binary)
f1 = f1_score(true_binary, predicted_binary)

print(f"Precision: {precision:.2f}, Recall: {recall:.2f}, F1-score: {f1:.2f}")



# Example Usage
if __name__ == "__main__":
    resume_path = ["F://SABA_RESUME.pdf","F://Yash_Resume.pdf"] # Change to your test resume
    job_description = "Looking for a Data Scientist with Python, NLP, and deep learning skills."
    ranked_results = rank_resumes(resume_path, job_description)
    print("\n📑 Ranked Resumes:")
    for rank, (index, score) in enumerate(ranked_results):
        print(f"{rank+1}. Resume {index+1} - Similarity Score: {score:.2f}")

    # text = rp.parse_resume(resume_path)
    # similarity_score = calculate_similarity(text, job_descrition)
    # print(f"Resume-Job Similarity Score: {similarity_score:.2f}")
    # resume_embedding = get_word2vec_embedding(text)
    # print(resume_embedding.shape)
    #print(resume_embedding)  
