from rag_pipeline import rag_answer 

def ask_dao (query, chat_history, language = "TH"): 
    return rag_answer(query, chat_history, language)