import ollama 
from ollama import generate 
from chromadb import PersistentClient
from identity import DAO_IDENTITY 
import re

client = PersistentClient(path="chroma")
collection = client.get_collection("documents")

def retrieve(query, n_results=2):

    query_embedding = ollama.embeddings(
        model="nomic-embed-text",
        prompt=query
    )["embedding"]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={"topic": "elephant"},
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

def build_prompt(query, context, history_text, response_mode, identity_mode):

    if response_mode == "STANDARD":

        formatting_rules = """
    Formatting rules:
    - Start with a short natural introduction to the topic.
    - Then present ALL facts as bullet points.
    - Every fact must start with "• ".
    - Do not mix paragraphs and bullets.
    """
    elif response_mode == "IDENTITY":
        formatting_rules = """
    Formatting rules:
    - Write a warm conversational paragraph.
    - Do NOT use bullet points.
    - Do NOT greet.
    - Speak naturally and personally.
    """
    else: 
        formatting_rules = """
Formatting rules:
- Write a natural paragraph explanation.
- DO NOT use bullet points.
- DO NOT create lists.
- Continue the conversation naturally.
"""

    
    prompt = f"""
You are Dao, a friendly wildlife knowledge assistant who explains
animal behavior and conservation in a warm and engaging way.

Use the conversation history and the retrieved document context to
answer the user's question.

Instructions:
- Start with a short natural sentence introducing the topic.
- Then explain the answer clearly.
- You MUST answer the user's question using the provided context.
- Refer to research naturally if present.
- Do not include headings like "Introduction" or "Answer". Respond naturally in plain text.
- If the user asks a follow-up question referring to something mentioned earlier
(such as "bullet 2", "that point", or "tell me more"), use the previous
assistant response to understand the reference and expand on that topic.
- Combine related information across multiple context excerpts to produce a complete answer.
- If the user requests multiple facts, extract as many distinct facts as possible from the context.
- If the question is about a specific animal,
maintain that same animal throughout the answer.
Do not replace it with another species.


Rules:
- Prefer information from the provided context.
- If the context does not contain the answer, say you could not find it in the documents.
- Do not invent facts.
- Focus only on information directly related to the user's question.
- Ignore unrelated research details even if present in the context.

Conversation rule:
- Do not address yourself by name in the answer.
- Do not repeat the user's wording like "Dao".

Conversation State:
Identity mode: {identity_mode}

STRICT Conversation Rules:
- Identity mode responses are explanations, NOT introductions.
- In Identity mode:
  • NEVER greet.
  • NEVER introduce yourself.
  • NEVER say Hello, Hi, or similar phrases.
  • Start directly with the explanation.

CRITICAL FORMATTING RULE:
The structure of the answer MUST follow the Formatting Rules section below.
All earlier instructions describe content only, NOT formatting.

{DAO_IDENTITY}

Conversation history:
{history_text}

Context:
{context}

User question:
{query}

Follow the formatting rules below when writing the response.

{formatting_rules}
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
        model="llama3",
        prompt=rewrite_prompt
    )

    return response["response"].strip()

def normalize_answer_format(answer):

    import re

    # remove labels
    answer = re.sub(r"(Introduction:|Answer:)", "", answer)

    # normalize bullets (THE IMPORTANT LINE)
    answer = re.sub(r"\s*•\s*", "\n• ", answer)

    # ensure intro separated from list
    answer = re.sub(r"([^\n])\n•", r"\1\n\n•", answer)

    # remove excessive blank lines
    answer = re.sub(r"\n{3,}", "\n\n", answer)

    # if bullets exist but first fact isn't bulleted, fix it
    if "•" in answer:
        parts = answer.split("\n")
    
        intro = parts[0]
        rest = "\n".join(parts[1:]).strip()
    
        if not rest.startswith("•"):
            sentences = re.split(r'(?<=[.!?])\s+', rest, maxsplit=1)
    
            if len(sentences) > 1:
                first_fact, remaining = sentences
                rest = f"• {first_fact}\n{remaining}"
    
        answer = intro + "\n\n" + rest

    return answer.strip()

def remove_greeting(answer):
    greeting_patterns = [
        r"^hello[!,. ]*",
        r"^hi[!,. ]*",
        r"^hey[!,. ]*",
        r"^greetings[!,. ]*",
        r"^สวัสดี[!,. ]*"
    ]

    for pattern in greeting_patterns:
        answer = re.sub(pattern, "", answer, flags=re.IGNORECASE)

    return answer.strip()

def translate_text(text):

    translation_response = ollama.chat(
        model="qwen2.5",
        messages=[
            {
                "role": "system",
                "content": """You are a professional Thai wildlife translator.

Translate into natural, fluent Thai suitable for native speakers.

STRICT RULES:
- Thai language ONLY.
- No English.
- No Chinese characters.
- Preserve meaning exactly.
- Never explain.
- Never summarize.
- Never rewrite meaning.
- Preserve sentence boundaries exactly.
- Preserve formatting exactly.
- Do not add punctuation.
- Do not repeat sentences.
- Preserve animal species as elephants (ช้าง).
- elephant = ช้าง
- elephants = ช้าง
- herbivore = สัตว์กินพืช
- elephant trunk = งวง
- grass = หญ้า
- bark = เปลือกไม้
- Do NOT add explanations.
- Do NOT add emojis.
- Do NOT change formatting.
- Do NOT copy phrases from context in another language.
"""
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return translation_response["message"]["content"].strip(), translation_response["model"] 

def rag_answer(query, chat_history, language = "EN"):

    is_relevant = False

    def detect_identity_query(query: str) -> bool:

        identity_keywords = [
            "who are you",
            "what are you",
            "tell me about yourself",
            "what can you do",
            "who is dao",
            "about dao",
            "your purpose",
            "your role"
        ]
    
        query_lower = query.lower()
    
        return any(k in query_lower.strip("?!. ") for k in identity_keywords)

    is_identity_query = detect_identity_query(query)

    def detect_response_mode(query, chat_history):

        q = query.lower()
    
        followup_patterns = [
            "elaborate",
            "tell me more",
            "more about",
            "expand",
            "explain more",
            "point",
            "bullet",
            "that one",
            "that point"
        ]
    
        # keyword-based follow-up
        if any(p in q for p in followup_patterns):
            return "FOLLOWUP"
    
        # conversational follow-up
        if len(chat_history) > 0:
            previous_dao_message = None
    
            for msg in reversed(chat_history):
                if msg.get("role") == "dao":
                    previous_dao_message = msg.get("answer", "")
                    break
    
            # If previous answer had bullets,
            # assume continuation unless user asks new topic
            if previous_dao_message and "•" in previous_dao_message:
                return "FOLLOWUP"

        if is_identity_query:
            return "IDENTITY"
    
        return "STANDARD"

    response_mode = detect_response_mode(query, chat_history)

    is_first_turn = len(chat_history) == 0
    
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

            if "•" in message:
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

        # RELEVANCE_THRESHOLD = 260  # lower = more strict
        # avg_distance = sum(distances) / len(distances)
        # is_relevant = avg_distance < RELEVANCE_THRESHOLD

        RELEVANCE_THRESHOLD = 200  # stricter

        filtered_docs = []
        filtered_metas = []
        filtered_snippets = []
        
        for doc, meta, snippet, dist in zip(docs, metas, snippets, distances):
            if dist < RELEVANCE_THRESHOLD:
                filtered_docs.append(doc)
                filtered_metas.append(meta)
                filtered_snippets.append(snippet)
        
        is_relevant = len(filtered_docs) > 0
    
        context = f"""       
        Relevant document excerpts:
        {"\n\n".join(d[:800] for d in docs)}
        """

    prompt = build_prompt(
        query,
        context,
        history_text,
        response_mode, 
        is_identity_query
    )
    
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
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    response_model = response["model"] 
    
    answer = response["message"]["content"]
    # remove section labels safely
    answer = normalize_answer_format(answer)
    answer = remove_greeting(answer)

    retry_translation = False
    
    # 🌏 NEW: Translation step for Thai
    if language == "TH":

        original_answer = answer
        answer, response_model = translate_text(original_answer)
    
        def clean(text):
            text = re.sub(r"[，：]", "", text)
            text = normalize_answer_format(text)
            text = remove_greeting(text)
            text = re.sub(r"\b(Thai|English|Chinese|Translation)\b", "", text, flags=re.I)
            text = re.sub(r"[\u4e00-\u9fff]+", "", text)
            # ✅ remove stray English words ONLY when mixed inside Thai text
            text = re.sub(r"[A-Za-z<>|_]+", "", text)
            text = re.sub(r"[。，!！]+", "", text)
            # fix numbers broken across lines
            text = re.sub(r"(\d)\s*\n\s*(\d)", r"\1\2", text)
            
            # collapse double spaces created by cleanup
            text = re.sub(r"\s{2,}", " ", text).strip()
            text = re.sub(r"\s*•\s*", "\n• ", text)
            text = re.sub(r"\s*-\s*", "\n- ", text)
            return text
    
        def is_repetitive(text):

            words = text.split()
        
            if len(words) < 40:
                return False
        
            unique_ratio = len(set(words)) / len(words)
        
            return unique_ratio < 0.18
    
        answer = clean(answer)
    
        if is_repetitive(answer) and not retry_translation:
            retry_translation = True
            answer, response_model = translate_text(original_answer)
            answer = clean(answer)

            # FINAL stabilization pass
            answer = normalize_answer_format(answer)
            answer = remove_greeting(answer)

        def clean_special_tokens(text):
            patterns = [
                r"<\|.*?\|>",     # OpenAI tokens
                r"</?s>",         # sentence tokens
                r"\[INST\].*?\[/INST\]",
            ]
        
            for p in patterns:
                text = re.sub(p, "", text)
        
            return text.strip()

        def remove_english_leakage(text):
            # remove standalone English words only
            return re.sub(r"\b[A-Za-z]{2,}\b", "", text)

        answer = clean_special_tokens(answer)
        answer = remove_english_leakage(answer)
    
    if response_mode == "FOLLOWUP":
        answer = answer.replace("•", "")


    print("🔎 Rewritten Query:", rewritten_query)
    print("🌍 Language:", language)
    print("📄 Retrieved docs:", len(docs))
    print("📏 Distances:", distances)
    print("⚙️ Response model:", response_model) 
        
    return {
        "answer": answer,
        "sources": sources_list
    }