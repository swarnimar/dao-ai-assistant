import os
import chromadb
import ollama
from pypdf import PdfReader
import re

def clean_text(text):
    """
    Remove academic citation noise and normalize text
    before embedding.
    """

    # Remove citations like (Author 1999)
    text = re.sub(r"\([A-Za-z\s.,&\-]+?\d{4}[a-z]?\)", "", text)

    # Remove numbered references [12]
    text = re.sub(r"\[\d+\]", "", text)

    # Remove extra whitespace/newlines
    text = re.sub(r"\s+", " ", text)

    # remove line breaks inside sentences
    text = re.sub(r"\n+", " ", text)

    # fix hyphen line breaks
    text = re.sub(r"-\s+", "", text)

    text = re.sub(r"[^\w\s.,;:()%\-]", "", text)

    return text.strip()

client = chromadb.PersistentClient(path="chroma")

collection = client.get_or_create_collection(name="documents")

data_folder = "data"


def chunk_text(text, chunk_size=1200, overlap=250):

    chunks = []
    start = 0

    while start < len(text):

        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


for file in os.listdir(data_folder):

    if file.endswith(".pdf"):

        path = os.path.join(data_folder, file)

        reader = PdfReader(path)

        for page_num, page in enumerate(reader.pages):

            text = page.extract_text()

            if not text:
                continue

            text = clean_text(text)

            chunks = chunk_text(text)

            for i, chunk in enumerate(chunks):

                embedding = ollama.embeddings(
                    model="nomic-embed-text",
                    prompt=chunk
                )["embedding"]

                collection.add(
                    ids=[f"{file}_p{page_num}_c{i}"],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[{
                        "source": file,
                        "page": page_num + 1, 
                        "topic": "elephant"
                    }]
                )

    elif file.endswith(".txt"):
        path = os.path.join(data_folder, file)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        text = clean_text(text)
    
        chunks = chunk_text(text)
    
        for i, chunk in enumerate(chunks):
    
            embedding = ollama.embeddings(
                model="nomic-embed-text",
                prompt=chunk
            )["embedding"]
    
            collection.add(
                ids=[f"{file}_info_c{i}"],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{
                    "source": file,
                    "page": "Info",
                    "topic": "elephant"
                }]
        )

print("Ingestion complete.")
print("Total documents:", collection.count())