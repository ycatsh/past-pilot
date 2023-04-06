from sentence_transformers import SentenceTransformer, util

#model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')
model = SentenceTransformer('bert-base-nli-mean-tokens')

def calculate_similarity(user_input, data):
    embeddings = model.encode([user_input, data], convert_to_tensor=True)
    sim = util.cos_sim(embeddings[0], embeddings[1]).item()

    return sim


