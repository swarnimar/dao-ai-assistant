import ollama 
from ollama import generate 
from chromadb import PersistentClient
from identity import DAO_IDENTITY 
import re

client = PersistentClient(path="chroma")
collection = client.get_collection("documents")

def retrieve(query, n_results=3):

    query_embedding = ollama.embeddings(
        model="nomic-embed-text",
        prompt=query
    )["embedding"]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # build highlighted snippets
    snippets = [doc[:300] + "..." for doc in documents]
        
    return documents, metadatas, snippets, distances 

def format_chat_history(chat_history, max_turns=4):
    """
    Convert Streamlit chat history into text the LLM can understand.
    """

    history_text = ""

    recent_history = chat_history[-max_turns:]

    for msg in recent_history:

        if msg["role"] == "user":
            history_text += f"User: {msg["content"]}\n"

        elif msg["role"] == "dao":
            history_text += f"Dao: {msg['answer']}\n"

    return history_text

def extract_bullet_reference(query):
    match = re.search(r"#?(\d+)", query)
    if match:
        return int(match.group(1))
    return None

def extract_bullet_text(answer, bullet_number):

    lines = answer.split("\n")

    for line in lines:
        if line.strip().startswith(f"{bullet_number}."):
            return line

    return None

def build_prompt(query, context, history_text, language = "EN"):

    is_first_turn = len(history_text) <= 1

    language_instruction = ""

    if language == "TH":
        language_instruction = """
IMPORTANT LANGUAGE RULE:
You MUST answer only in Thai.
Do not use English.
"""

    prompt = f"""
    {language_instruction}
You are Dao, a friendly wildlife knowledge assistant who explains
animal behavior and conservation in a warm and engaging way.

Use the conversation history and the retrieved document context to
answer the user's question.

Instructions:
- Start with a short natural sentence introducing the topic.
- Then explain the answer clearly.
- Refer to research naturally if present.
- If listing facts, introduce the list first.
- Use bullet points when listing multiple facts.
- Do not include headings like "Introduction" or "Answer". Respond naturally in plain text.
- If the user asks a follow-up question referring to something mentioned earlier
(such as "bullet 2", "that point", or "tell me more"), use the previous
assistant response to understand the reference and expand on that topic.

Rules:
- Use ONLY the information in the provided context.
- If the answer cannot be found, say you couldn't find it in the documents.
- Do not invent facts.
- If the context is not relevant to the question, answer generally without referring to sources.

Conversation rule:
- Only greet the user if First turn is True.
- Otherwise continue the conversation without greeting.
- Do not address yourself by name in the answer.
- Do not repeat the user's wording like "Dao".

{DAO_IDENTITY}

First turn: {is_first_turn}

Conversation history:
{history_text}

Context:
{context}

User question:
{query}

Respond using this format:

Introduction:
(one natural sentence introducing the topic)

Answer:
(the main explanation)
"""

    return prompt

def rewrite_query(query, chat_history):

    history_text = format_chat_history(chat_history)

    rewrite_prompt = f"""
You are helping improve search queries for a document retrieval system.

Conversation history:
{history_text}

User question:
{query}

Rewrite the user question so it is a clear, standalone question that can be used for document retrieval.

If the question already makes sense, return it unchanged.

Only output the rewritten question.
"""

    response = generate(
        model="mistral",
        prompt=rewrite_prompt
    )

    return response["response"].strip()

def rag_answer(query, chat_history, language = "EN"):

    def clean_query(query):
        query = re.sub(r"\bdao\b[:,]?\s*", "", query, flags=re.IGNORECASE)
        return query.strip()

    query = clean_query(query)
    rewritten_query = rewrite_query(query, chat_history)

    bullet_number = extract_bullet_reference(query)

    previous_answer = None
    for msg in reversed(chat_history):
        if msg.get("role") == "dao":
            message = msg.get("answer", "")

            if any(f"{i}." in message for i in range(1, 10)):
                previous_answer = message
                break

    bullet_text = None

    if bullet_number and previous_answer:
        bullet_text = extract_bullet_text(previous_answer, bullet_number)

    history_text = format_chat_history(chat_history)

    if bullet_text:
        context = f"The user is asking to elaborate on this point:\n{bullet_text}"
        metas = []
        snippets = []
    else:
        docs, metas, snippets, distances = retrieve(rewritten_query)

        RELEVANCE_THRESHOLD = 0.5  # lower = more strict

        is_relevant = any(d < RELEVANCE_THRESHOLD for d in distances)
    
        context = f"""
        Conversation so far:
        {history_text}
        
        Relevant document excerpts:
        {"\n\n".join(d[:800] for d in docs)}
        """
    prompt = build_prompt(query, context, history_text, language)
    
    sources_list = []

    if is_relevant: 
    
        for i in range(len(metas)):
            
            sources_list.append({
                "source": metas[i].get("source", "Unknown document"),
                "page": metas[i].get("page", "Unknown page"),
                "pdf_link": f"data/{metas[i].get('source','Unknown document')}#page={metas[i].get('page','Unknown page')}",
                "snippet": snippets[i]
            })
      
    response = ollama.chat(
        model="mistral",
        messages=[
            {
                "role": "system",
                "content": f"{DAO_IDENTITY}\nRespond in {language}."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    answer = response["message"]["content"]
    answer = answer.replace("Introduction:", "").replace("Answer:", "").strip()
        
    return {
        "answer": answer,
        "sources": sources_list
    }