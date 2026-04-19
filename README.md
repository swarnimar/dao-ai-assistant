# Dao💫 — Domain-Specific Elephant Knowledge Assistant

>🚀 Built as a portfolio project to demonstrate end-to-end LLM system design using Retrieval-Augmented Generation (RAG), including retrieval, query rewriting, and conversational memory.

>📄 **System Design & Architecture:** [View detailed architecture](Docs/DAO_SYSTEM.md)

---

## 🚧 Project Status

Dao💫 is an actively evolving LLM system.

The current implementation reflects a significantly improved architecture developed through iterative testing, user acceptance testing (UAT), and multiple system refinements, including:

- Improved retrieval grounding
- Query rewriting pipeline
- Structured prompt architecture
- Multilingual response support (EN / TH)
- Enhanced conversational memory handling

---

## 🌟 Overview

**Dao💫** is a domain-specific AI assistant designed to answer questions about elephant behavior, ecology, and conservation using a curated knowledge base.

The system is built to ensure responses are **grounded, explainable, and source-backed**, rather than relying on general model knowledge.

Inspired by real-world elephant conservation experiences in Thailand, Dao explores how LLMs can be used for focused, meaningful knowledge systems.

---

## ✨ Key Features

- 💬 Conversational AI interface for elephant-related queries  
- 🔎 Retrieval-Augmented Generation (RAG) for grounded responses  
- 🧠 Query rewriting for improved retrieval accuracy  
- 🔁 Follow-up question handling with conversation memory  
- 📚 Source-backed answers with document snippets  
- 🌏 Multilingual support (English + Thai)  
- ⚙️ Structured prompt-based behavior control  

---

## 🧠 Architecture Overview

📄 Full technical breakdown: [Docs/DAO_SYSTEM.md](Docs/DAO_SYSTEM.md)

Dao follows a modular RAG pipeline:

- Query processing & rewriting  
- Vector-based document retrieval (ChromaDB)  
- Context construction using retrieved chunks + history  
- LLM-based response generation (via Ollama)  
- Optional translation layer for Thai output  
- Source attribution and UI rendering  

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **LLM Runtime:** Ollama  
- **Models:** Llama / Qwen 2.5 
- **Embeddings:** nomic-embed-text  
- **Vector DB:** ChromaDB  
- **Pipeline:** Custom RAG orchestration  

---

## 📸 Demo

### 🏠 Main Interface
![Home](assets/Screenshot1.png)

### 💬 Conversational Response
![Chat](assets/Screenshot2.png)

### 📚 Source Attribution
![Sources](assets/Screenshot3.png)

---

## ⚙️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/your-username/dao-ai-assistant.git
cd dao-ai-assistant


### 2. Install dependencies
pip install -r requirements.txt


### 3. Run the application
streamlit run dao_app.py


### 4. Run required models (Ollama)
ollama run llama3 

ollama run qwen2.5 

ollama run nomic-embed-text

## 📌 Notes

- This project runs locally using GPU acceleration (RTX 4070 setup)
- Designed for experimentation with RAG-based LLM systems
- Focused on domain-specific grounding and interpretability
