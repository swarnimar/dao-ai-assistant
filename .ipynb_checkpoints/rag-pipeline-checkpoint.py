import ollama
from retrieve import retrieve


def rag_answer(query):

    docs, metas = retrieve(query)

    context = "\n\n".join(docs)

    prompt = f"""
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{query}

Answer:
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response["message"]["content"]

    return answer, docs, metas