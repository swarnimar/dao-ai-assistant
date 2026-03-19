import chromadb
import ollama

client = chromadb.PersistentClient(path="chroma")

collection = client.get_or_create_collection(name="documents")


def retrieve(query, n_results=5):

    query_embedding = ollama.embeddings(
        model="nomic-embed-text",
        prompt=query
    )["embedding"]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
        include=["documents", "metadatas", "distances"]
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # build context for LLM
    context = "\n\n".join(documents)

    # build highlighted snippets
    snippets = []
    for doc in documents:
        snippets.append(doc[:300] + "...")

    return context, metadatas, snippets, distances 