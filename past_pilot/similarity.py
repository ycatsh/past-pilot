import os
from pathlib import Path

from sentence_transformers import SentenceTransformer, util
import PyPDF2

from past_pilot.directory_modifier import get_data_dir


MODEL = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')

# directory parameter refers to the folder containing all pdfs for a key
def get_chunks(directory):
    chunks = []
    files = Path(directory).glob('*')
    for pdf_file in files:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            chunks.append((pdf_file.resolve(), page_num, text))

    return chunks


def calculate_similarity(user_input_embedding, chunk_embeddings):
    sim_scores = util.cos_sim(user_input_embedding, chunk_embeddings).squeeze().tolist()
    return sim_scores


def chunks_similarity(user_input, chunks):
    user_input_embedding = MODEL.encode(user_input, convert_to_tensor=True)

    chunk_texts = [chunk[2] for chunk in chunks]
    chunk_embeddings = MODEL.encode(chunk_texts, convert_to_tensor=True)
    
    sim_scores = calculate_similarity(user_input_embedding, chunk_embeddings)
    
    return [((chunk[0], chunk[1]), sim) for chunk, sim in zip(chunks, sim_scores)]


def get_similar(user_input, keys):
    directory = get_data_dir()
    sim_scores = []
    for key in keys:
        key_dir = os.path.join(directory, key)
        chunks = get_chunks(key_dir)
        sim_scores.extend(chunks_similarity(user_input, chunks))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    length = len(sim_scores)

    return sim_scores, length