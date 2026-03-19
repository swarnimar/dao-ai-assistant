from rag_pipeline import rag_answer 
from identity import identity_answer 

def ask_dao (query, chat_history, language = "EN"): 
    identity_keywords = [
        "who are you",
        "tell me about yourself",
        "your name",
        "why are you called dao",
        "who created you"
    ]
       
    if any(k in query.lower() for k in identity_keywords):
        answer = identity_answer(query)
        answer = answer.replace("Introduction:", "").replace("Answer:", "")
        return {
        "answer": answer,
        }
        
    else: 
        
        results = rag_answer(query, chat_history, language)
        answer = results["answer"] 
        return results 