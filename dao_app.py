import streamlit as st
from main import ask_dao
import os 
from datetime import datetime
import builtins
import uuid 

st.set_page_config(page_title="Dao💫 Elephant Assistant", page_icon="🐘")

today = datetime.today()

if today.month == 3 and today.day == 13:
    st.success("🐘 Today is Thai Elephant Day! A day celebrating elephant conservation in Thailand. 🤗🥰")

st.title("Dao💫")

st.subheader("Your Elephant Knowledge Companion 🐘")
st.caption("Ask Dao anything about elephants, their behavior, and conservation.")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

if "latest_sources" not in st.session_state:
    st.session_state.latest_sources = []

if "active_source_index" not in st.session_state:
    st.session_state.active_source_index = None

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "pending_result" not in st.session_state:
    st.session_state.pending_result = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "sources_by_question" not in st.session_state:
    st.session_state.sources_by_question = {}

if "active_question_id" not in st.session_state:
    st.session_state.active_question_id = None

if "current_sources" not in st.session_state:
    st.session_state.current_sources = []

if "is_generating" not in st.session_state:
    st.session_state.is_generating = False

with st.sidebar:

    # ---------- CONTROLS ----------
    st.markdown("## ⚙️ Dao💫 Controls")   

    col1, col2 = st.columns([2, 2])
    
    with col1:
        st.subheader("🌐 Language")
    
    with col2:
        language = st.selectbox(
            "",
            ["EN","TH"],
            key="language_selector",
            label_visibility="collapsed"
        )

    st.divider()

    st.title("Dao💫")

    with st.expander("**🐘 About Dao💫**", expanded=False):
        st.markdown("---")

        st.markdown("""
    **Elephant Knowledge Companion**
    
    A friendly AI assistant dedicated to learning and sharing knowledge about elephants.
    
    ---
    
    🌏 **Inspired by:**  
    The elephants of **Ban Taklang village, Thailand**
    
    👩🏻‍💻 **Created by:**  
    Swarnima Roy
    
    ---
    
    Dao’s name means **“star” in Thai** ⭐  
    A tribute to the beautiful elephants who inspired this project.
    """)
    
    with st.expander("**⛏️ Built With**"):
        st.markdown("---")
    
        st.markdown("""
        
        • Streamlit – user interface  
        • Ollama – local LLM runtime  
        • Llama 3 – conversational reasoning  
        • Qwen 2.5 – translation & multilingual understanding  
        • Nomic Embed Text – semantic embeddings  
        • ChromaDB – vector database  
        • Retrieval-Augmented Generation (RAG)
        
        ---
        
        📚 **Knowledge Source**
        
        Research reports and conservation studies about elephants.
        """)

    st.markdown("---")
    st.subheader("📎 Sources")

    sidebar_sources_container = st.container()

    active_qid = st.session_state.get("active_question_id")
    dao_thinking = st.session_state.get("dao_thinking", False)

    # ---- Dao currently answering ----
    if dao_thinking:
        st.info("🔎 Dao💫 is preparing sources...")

    elif not active_qid:
        st.caption("Sources will appear here.")

    # ---- Show sources normally ----
    else:
        sources = st.session_state.sources_by_question.get(active_qid, [])

        if not sources:
            st.caption("No sources available for this question.")
        else:
            st.success("Sources ready!")
            for i, src in enumerate(sources):
                st.write(f"📄 {src['source']} — Page {src['page']}")
                st.caption(src["snippet"])
    
                pdf_path = f"data/{src['source']}"
    
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "Open PDF ⬇",
                            data=f.read(),
                            file_name=src["source"],
                            mime="application/pdf",
                            key=f"download_{active_qid}_{i}"
                        )

                    
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
    st.info("📄 Click **View Sources** under any answer to open references in the sidebar ⬅️")
                   
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

            if sources:
                if st.button(
                    f"📎 View Sources ({len(sources)})",
                    key=f"view_sources_{idx}"
                ):
                    st.session_state.active_question_id = message["question_id"]
                    st.rerun()
            
if user_question:

    # Save user message
    st.session_state.history.append({
        "role": "user",
        "content": user_question
    })

    # store question ONLY
    st.session_state.dao_thinking = True
    qid = str(uuid.uuid4())

    st.session_state.pending_question = {
        "question": user_question,
        "question_id": qid
    }
    
    st.session_state.active_question_id = qid
    st.session_state.dao_thinking = True

    st.rerun()

if st.session_state.pending_question and st.session_state.get("dao_thinking"):
     
    # Show Dao response
    assistant_placeholder = st.empty()
    with assistant_placeholder.container():
        with st.chat_message("assistant"):
            with st.spinner("Dao💫 is thinking... 🐘"):
                pending = st.session_state.pending_question
                result = ask_dao(pending["question"], st.session_state.history, language)   
            answer = result["answer"]
            sources = result.get("sources", [])
    
            st.markdown(f"**Dao💫:** {answer}")

    qid = pending["question_id"]

    # Save Dao response
    st.session_state.history.append({
        "role": "dao",
        "answer": answer,
        "sources": sources, 
        "question_id": qid
    })
    
    st.session_state.sources_by_question[qid] = sources
        
    st.session_state.dao_thinking = False
    st.session_state.pending_question = None
        
    st.rerun()