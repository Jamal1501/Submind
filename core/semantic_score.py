from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_semantic_similarity(texts, query):
    """
    Calculate the semantic similarity between a list of texts and a query using cosine similarity.

    Args:
    - texts (list of str): List of memory entries (texts).
    - query (str): The user input prompt to compare against.

    Returns:
    - similarities (list): A list of similarity scores between the query and each text.
    """
    # Combine all texts with the query into one corpus
    corpus = texts + [query]
    
    # Vectorize the texts and the query
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    # Extract the query vector (last vector in the matrix)
    query_vec = tfidf_matrix[-1]
    
    # Extract the text vectors (all except the last one)
    text_vecs = tfidf_matrix[:-1]
    
    # Compute the cosine similarity between the query and each text
    similarities = cosine_similarity(query_vec, text_vecs).flatten()
    
    # Debugging: Print similarity scores
    print(f"Similarity scores for query: {query}")
    print(similarities)
    
    return similarities
