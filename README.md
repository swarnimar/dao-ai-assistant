\# Dao💫 — Elephant Knowledge Companion (RAG-based AI System)



\## 🌟 Project Summary



\*\*Dao💫\*\* is an AI-powered elephant knowledge assistant designed to provide accurate, conversational answers about elephant behavior, ecology, and conservation.



Inspired by a personal experience in Thailand, the project explores how domain-specific AI systems can make learning more engaging and accessible.



It is built using a Retrieval-Augmented Generation (RAG) pipeline, combining a curated knowledge base with a conversational interface to deliver grounded, source-backed responses and handle follow-up questions effectively.





\## ✨ Features



\- 💬 \*\*Conversational AI Interface\*\*

&#x20; Ask natural language questions about elephants and receive clear, engaging responses.



\- 🔎 \*\*Retrieval-Augmented Generation (RAG)\*\*

&#x20; Uses a vector database to retrieve relevant knowledge and generate grounded answers.



\- 🔁 \*\*Follow-up Question Handling\*\*

&#x20; Maintains conversation context to handle queries like “tell me more” or “expand on point 2”.



\- 📚 \*\*Source-backed Responses\*\*

&#x20; Displays document sources and snippets to ensure transparency and trust.



\- 🌏 \*\*Multilingual Support (English + Thai)\*\*

&#x20; Supports Thai responses with dynamic translation from English knowledge sources.



\- 🧠 \*\*Query Rewriting for Better Retrieval\*\*

&#x20; Improves search quality by converting conversational queries into optimized search queries.





\## 🧠 Architecture



Dao💫 is built using a Retrieval-Augmented Generation (RAG) pipeline that combines document retrieval with large language model reasoning to generate accurate and context-aware responses.



\### 🔄 System Flow



1\. \*\*User Query\*\*  

&#x20;  The user asks a question through the Streamlit interface.



2\. \*\*Query Processing \& Rewriting\*\*  

&#x20;  The system cleans and rewrites the query to improve retrieval accuracy, especially for follow-up questions.



3\. \*\*Embedding Generation\*\*  

&#x20;  The query is converted into a vector embedding using an embedding model.



4\. \*\*Document Retrieval (ChromaDB)\*\*  

&#x20;  The system searches a vector database to find the most relevant document chunks.



5\. \*\*Context Construction\*\*  

&#x20;  Retrieved documents, along with conversation history, are combined to form the context.



6\. \*\*LLM Response Generation (Mistral via Ollama)\*\*  

&#x20;  The language model generates a response grounded in the retrieved context.



7\. \*\*Source Attribution\*\*  

&#x20;  Relevant document snippets and sources are displayed alongside the answer.



\---



\### 🧩 Key Design Decisions



\- \*\*RAG over Fine-tuning\*\*  

&#x20; Enables dynamic knowledge updates without retraining the model.



\- \*\*Query Rewriting\*\*  

&#x20; Improves retrieval performance for conversational and ambiguous queries.



\- \*\*Conversation History Integration\*\*  

&#x20; Allows the system to handle follow-up questions naturally.



\- \*\*Chunk-based Retrieval\*\*  

&#x20; Ensures precise and relevant context is passed to the model.



\- \*\*Local LLM (Ollama)\*\*  

&#x20; Keeps inference local and avoids dependency on external APIs.





\## 🛠️ Tech Stack



\- \*\*Frontend:\*\* Streamlit  

\- \*\*Backend:\*\* Python  

\- \*\*LLM:\*\* Mistral (via Ollama)  

\- \*\*Embeddings:\*\* nomic-embed-text  

\- \*\*Vector Database:\*\* ChromaDB  

\- \*\*PDF Processing:\*\* PyPDF  

\- \*\*Other Tools:\*\* Regex, Custom RAG Pipeline





\## 📸 Demo



\### 🏠 Home Interface

!\[Home](assets/Screenshot1.png)



\### 💬 Conversational Response

!\[Chat](assets/Screenshot2.png)



\### 📚 Source-backed Answer

!\[Sources](assets/Screenshot3.png)





\## ⚙️ How to Run



\### 1. Clone the repository



```bash

git clone https://github.com/your-username/dao.git

cd dao



\---



\### 2. Install dependencies



```bash

pip install -r requirements.txt



\---



\### 3. Run the application



```bash

streamlit run dao\_app.py



\---



\### 4. Run required models (Ollama)



```bash

ollama run mistral

ollama run nomic-embed-text



\---

