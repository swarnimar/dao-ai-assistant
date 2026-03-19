import streamlit as st
from main import ask_dao
import os 
from datetime import datetime

st.set_page_config(page_title="Dao💫 Elephant Assistant", page_icon="🐘")

today = datetime.today()

if today.month == 3 and today.day == 16:
    st.success("🐘 Today is Thai Elephant Day! A day celebrating elephant conservation in Thailand. 🤗🥰")

col1, col2 = st.columns([6,1])

with col2:
    language = st.selectbox(
        "🌏",
        ["EN", "TH"],
        label_visibility="collapsed"
    )

st.title("Dao💫")

st.subheader("Your Elephant Knowledge Companion 🐘")
st.caption("Ask Dao anything about elephants, their behavior, and conservation.")
with st.sidebar:

    st.title("🐘 Dao💫")

    st.markdown("""
**Elephant Knowledge Companion**

A friendly AI assistant dedicated to learning and sharing knowledge about elephants.

---

🌏 **Inspired by:**  
The elephants of **Ban Taklang village, Thailand**

👩‍💻 **Created by:**  
Swarnima Roy

---

Dao’s name means **“star” in Thai** ⭐  
A tribute to the beautiful elephants who inspired this project.
""")

    st.markdown("""
---

⚙️ **Built With**

• Streamlit – user interface  
• Ollama – local LLM runtime  
• Mistral – language model  
• ChromaDB – vector database  
• Retrieval-Augmented Generation (RAG)

---

📚 **Knowledge Source**

Research reports and conservation studies about elephants.
""")


# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User input box
user_question = st.chat_input("Ask Dao something about elephants...")

if len(st.session_state.history) == 0 and user_question is None:
    st.info("""
You can ask things like:

• Tell me interesting facts about elephants  
• How do elephants communicate?  
• Why are elephants important to ecosystems?  
• Are Asian elephants endangered?
""")

# Display conversation
for idx, message in enumerate(st.session_state.history):

    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f"**You:** {message["content"]}")

    elif message["role"] == "dao":
        with st.chat_message("assistant"):
            answer = message["answer"]
            sources = message["sources"]
            st.markdown(f"**Dao💫:** {answer}")

            if sources and message["sources"]: 
                st.markdown("### Sources")
    
                for i, s in enumerate(sources):
    
                    with st.expander(f"📄 {s['source']}  |  Page {s['page']}"):
                
                        st.write(s["snippet"])
                
                        pdf_path = f"data/{s['source']}"
                
                        try:
                            with open(pdf_path, "rb") as file:
                                st.download_button(
                                    label="Open Source PDF",
                                    data=file,
                                    file_name=s["source"],
                                    mime="application/pdf",
                                    key=f"{s['source']}_{s['page']}_{i}_{len(st.session_state.history)}"
                                )

                        except: 
                            st.write("Source file not available.")

            
if user_question:

    # Save user message
    st.session_state.history.append({
        "role": "user",
        "content": user_question
    })
    
    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(f"**You:** {user_question}")

    # Show Dao response
    assistant_placeholder = st.empty()
    with assistant_placeholder.container():
        with st.chat_message("assistant"):
            with st.spinner("Dao💫 is thinking... 🐘"):
                result = ask_dao(user_question, st.session_state.history, language)
    
            answer = result["answer"]
            sources = result.get("sources", [])
    
            st.markdown(f"**Dao💫:** {answer}")

            if sources: 
                st.markdown("### Sources")
        
                for i, s in enumerate(sources):
        
                    with st.expander(f"📄 {s['source']}  |  Page {s['page']}"):
                    
                        st.write(s["snippet"])
                    
                        pdf_path = f"data/{s['source']}"
                    
                        try:
                            with open(pdf_path, "rb") as file:
                                st.download_button(
                                    label="Open Source PDF",
                                    data=file,
                                    file_name=s["source"],
                                    mime="application/pdf",
                                    key=f"new_{s['source']}_{s['page']}_{i}_{len(st.session_state.history)}"
                                )
                        except: 
                                st.write("Source file not available.")
       
    # Save Dao response
    st.session_state.history.append({
        "role": "dao",
        "answer": answer,
        "sources": sources
    })