from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load model once
model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)


def calculate_semantic_similarity(
    resume_text,
    jd_text
):

    # Convert text into embeddings
    embeddings = model.encode(
        [resume_text, jd_text]
    )

    # Calculate cosine similarity
    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(similarity * 100, 2)