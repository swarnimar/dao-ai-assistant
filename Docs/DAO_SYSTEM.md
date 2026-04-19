\# Dao💫 Architecture Document



\---



\## 🧠 Section 1 — System Overview



\### 1.1 Purpose of the System



Dao💫 is a \*\*domain-specific Retrieval-Augmented Generation (RAG) assistant\*\* designed to provide reliable, contextual answers about elephants and elephant conservation.



The system demonstrates how a general-purpose Large Language Model can be transformed into a specialized knowledge assistant through curated data ingestion, semantic retrieval, and grounded response generation.



While the application is framed around elephant conservation, its primary objective is \*\*technical\*\*: to showcase end-to-end design and implementation of an LLM system. The intended audience includes recruiters and technical evaluators assessing capabilities in applied AI system design, RAG architecture, and production-style LLM pipelines.



\### 1.2 System Scope and User Interaction Flow



Dao💫 is delivered as an interactive web application built around a conversational interface.



When a user accesses the application, they are presented with two primary interface regions:



* \*\*Chat Window\*\* — the main conversational workspace where all interactions occur.
* \*\*Sidebar Panel\*\* — a contextual control and reference area containing system information, configurable settings, and retrieved sources.



\#### User Interaction Flow



1. \*\*Application Entry\*\*
* The user lands on the main interface displaying the chat window and sidebar.
* Introductory guidance explains the types of questions Dao💫 can answer and informs users that supporting sources will appear in the sidebar.



2\. \*\*Query Submission\*\*

* The user enters a natural-language question related to elephants or elephant conservation.



3\. \*\*Response Generation\*\*

* The system processes the query and generates a grounded response.
* A brief “thinking” state indicates active processing.



4\. \*\*Answer Delivery\*\*

* Dao💫 returns a conversational response within the chat window.
* When available, supporting knowledge sources are surfaced in the sidebar to promote transparency and verifiability.



5\. \*\*User Configuration\*\*

* Users can control response language via sidebar settings.
* Currently supported languages:

  * English (EN)
  * Thai (TH)



This interaction model combines conversational usability with explainability by exposing retrieved knowledge sources alongside generated answers.



\### 1.3 High-Level System Components



Dao💫 follows a Retrieval-Augmented Generation (RAG) architecture composed of several cooperating system layers. At a high level, the system consists of the following components:



\#### 1. User Interface Layer



The Streamlit-based interface provides the conversational experience through a chat window and sidebar controls.

This layer manages user interaction, displays responses, exposes retrieved sources, and allows configuration such as response language selection.



\#### 2. LLM Runtime / Orchestration Layer



The runtime layer coordinates the end-to-end request lifecycle. It handles query processing, retrieval execution, prompt construction, and response generation by orchestrating interactions between system components.



\#### 3. Large Language Model (LLM) Layer



The LLM is responsible for natural language understanding and response generation. Rather than relying solely on pretrained knowledge, the model operates in a grounded setting by incorporating externally retrieved context.



\#### 4. Retrieval Layer



The retrieval logic identifies relevant information from the knowledge base using semantic similarity search. This component enables domain specialization by supplying context specific to elephants and conservation topics.



\#### 5. Knowledge Base / Vector Database



Domain documents are transformed into embeddings and stored in a vector database. This repository serves as the external memory of Dao💫, enabling factual grounding and source attribution.



\#### 6. Prompt \& Behavior Control Layer



System prompts define Dao💫’s personality, scope, language behavior, and response constraints. This layer ensures consistent tone, safety boundaries, and structured answer generation.



Together, these components enable Dao💫 to function as a domain-aware conversational assistant rather than a generic chatbot.



\### 1.4 Architectural Approach: Retrieval-Augmented Generation (RAG)



Dao💫 is implemented using a \*\*Retrieval-Augmented Generation (RAG)\*\* architecture to enable reliable domain-specific responses.



A standalone general-purpose Large Language Model possesses broad knowledge but may lack depth, accuracy, or up-to-date information in specialized domains such as elephant biology and conservation. To address this limitation, Dao💫 augments the LLM with an external knowledge base curated specifically for elephant-related content.



Under the RAG paradigm:



* User queries are first used to retrieve relevant information from the elephant knowledge base.
* Retrieved context is then supplied to the LLM during response generation.
* The model produces answers grounded in retrieved documents rather than relying solely on pretrained knowledge.



This design provides several advantages:



* \*\*Domain Specialization\*\* — Enables deep expertise without retraining the model.
* \*\*Improved Factual Reliability\*\* — Responses are anchored to known sources.
* \*\*Transparency\*\* — Supporting documents can be exposed to users.
* \*\*educed Hallucination Risk\*\* — Generation is constrained by retrieved evidence.



Through RAG, Dao💫 behaves as a knowledge-grounded assistant rather than a generic conversational chatbot.



\### 1.5 Design Goals



The design of Dao💫 was guided by both technical learning objectives and real-world impact motivations.



\#### Primary Goals



\*\*1. Applied Learning and Skill Demonstration\*\*

Dao💫 was developed as a hands-on implementation project to apply concepts related to Large Language Models, Retrieval-Augmented Generation (RAG), prompt engineering, and end-to-end AI system design. The system serves as a demonstrable portfolio artifact showcasing practical LLM engineering capabilities.



\*\*2. Domain-Specific Knowledge Delivery\*\*

The system aims to transform a general-purpose language model into a specialized assistant focused on elephants and elephant conservation through curated knowledge grounding.



\*\*3. Transparency and Trust\*\*

By exposing retrieved sources alongside generated answers, Dao💫 emphasizes explainability and encourages users to verify information rather than passively consume AI-generated text.



\*\*4. Multilingual Accessibility\*\*

Dao💫 supports both English and Thai responses to make the application accessible to international users and Thai-speaking audiences connected to elephant conservation communities.



\#### Secondary Goals



\*\*5. Awareness and Educational Impact\*\*

Beyond technical experimentation, Dao💫 seeks to increase awareness about elephants, their intelligence and behavior, and the communities that care for them. The project highlights locations such as Ban Taklang village in Thailand, promoting responsible tourism that can support mahouts and elephant caretakers.



\*\*6. Human-Centered AI Design\*\*

The system intentionally combines technical rigor with emotional engagement, demonstrating how AI applications can serve educational and cultural storytelling purposes alongside engineering goals.



\### 1.6 System Non-Goals and Limitations



Dao💫 is intentionally designed as a domain-constrained assistant rather than a general-purpose AI system.



\#### Defined Non-Goals



\*\*1. General Knowledge Assistant\*\*

Dao💫 is not intended to answer broad, open-domain questions. The system is deliberately restricted to elephants and elephant conservation topics. When users ask questions outside this scope, Dao💫 explicitly communicates its lack of knowledge instead of attempting speculative responses.



\*\*2. Real-Time Internet Search\*\*

The system does not perform live web searches or dynamically retrieve external information. All responses are grounded exclusively in the curated elephant knowledge base.



\*\*3. Production-Scale Deployment\*\*

Dao💫 is designed as a learning and demonstration system rather than a horizontally scalable production platform. Infrastructure optimization, distributed serving, and high-throughput performance are outside the current scope.



\*\*4. Autonomous Decision System\*\*

Dao💫 functions as an informational assistant only. It does not provide professional, medical, legal, or safety-critical recommendations.



By clearly constraining system capabilities, Dao💫 prioritizes reliability, transparency, and responsible AI behavior within its intended domain.



\---



\## 🔄 Section 2 — Architecture \& Pipeline Design



\### 2.1 Query Lifecycle



Dao💫 follows a structured request-processing pipeline that transforms a user query into a grounded conversational response. The system separates query understanding, retrieval, generation, and presentation into distinct stages to improve reliability and maintainability.



\#### End-to-End Request Flow



\*\*1. Query Submission\*\*



A user submits a question through the chat interface. The application captures the input along with current session state, including conversation history and user-selected language settings.



\*\*2. Query Analysis and Normalization\*\*



The incoming query undergoes preprocessing to prepare it for retrieval and generation:



* The system determines whether the query is:

  * an \*\*identity question\*\* (e.g., greetings, questions about Dao💫 itself, or capability-related prompts), or
  * a knowledge-seeking query related to elephants or conservation.
* The query is cleaned and normalized.
* Follow-up questions are rewritten into standalone queries using conversation context to preserve semantic meaning.



This step ensures consistent retrieval performance and coherent multi-turn conversations.



\*\*3. Retrieval Phase\*\*



The normalized query is used to perform semantic search against the elephant knowledge base.



* Relevant document chunks are retrieved from the vector database.
* Retrieved passages form the \*\*context\*\* used to ground the response.



This stage provides Dao💫 with domain-specific knowledge external to the base language model.



\*\*4. Prompt Construction\*\*



A structured prompt is assembled containing:



* system instructions defining Dao💫’s behavior,
* retrieved contextual knowledge,
* the rewritten user query,
* relevant conversation history.



The prompt serves as the orchestration mechanism guiding the LLM toward accurate and domain-constrained responses.



\*\*5. Response Generation\*\*



The constructed prompt is sent to the Large Language Model.



The LLM generates a response conditioned on both retrieved context and conversational state, producing a grounded answer.



\*\*6. Post-Processing\*\*



The generated response undergoes refinement:



* formatting and cleanup,
* consistency adjustments,
* optional translation when Thai language output is selected.



\*\*7. Conversation Logging\*\*



Selected conversational variables and metadata are recorded for session continuity, debugging, and future evaluation.



\*\*8. Response Delivery\*\*



The final answer and associated sources are returned to the application interface:



* the response appears in the chat window,
* supporting sources are displayed in the sidebar for reference and transparency.



\### 2.2 Responsibility Split: Application vs. LLM



Dao💫 separates system orchestration from language reasoning by clearly dividing responsibilities between the application layer and the Large Language Model (LLM).



\#### Application Responsibilities (Dao💫 System)



The Dao💫 application controls the overall lifecycle of each interaction and is responsible for all operational and architectural decisions, including:



* managing the user interface and session state,
* receiving and preprocessing user queries,
* detecting identity questions and handling conversational context,
* performing semantic retrieval from the elephant knowledge base,
* constructing structured prompts,
* orchestrating LLM invocation,
* handling post-processing steps such as formatting and translation,
* logging conversation variables and metadata,
* presenting responses and supporting sources to the user.



In essence, the application governs \*\*how the system thinks and operates\*\*.



\#### LLM Responsibilities



The Large Language Model is responsible for cognitive and linguistic tasks once provided with structured inputs by the application:



* understanding natural language queries,
* interpreting retrieved contextual information,
* following behavioral and system instructions,
* synthesizing knowledge into coherent responses,
* generating fluent conversational output.



The LLM therefore focuses exclusively on \*\*reasoning and language generation\*\*, while the surrounding system ensures grounding, control, and reliability.



\### 2.3 Retrieval Strategy



Dao💫 employs a semantic retrieval strategy to identify relevant knowledge from its curated elephant conservation corpus.



\#### Knowledge Indexing (Ingestion Phase)



During the ingestion process, source documents are transformed into vector representations:



* Elephant-related documents are segmented into smaller text chunks.
* Each chunk is converted into a numerical embedding using an embedding model.
* These embeddings are stored in a vector database, which serves as Dao💫’s external knowledge memory.



This process enables semantic search based on meaning rather than keyword matching.



\#### Query-Time Retrieval



When a user submits a question:



1. The query is converted into an embedding using the same embedding model applied during ingestion.

2\. A vector similarity search is performed against the stored document embeddings.

3\. The system retrieves the \*\*top two most semantically relevant chunks\*\*.

4\. Retrieved passages are assembled into contextual grounding material for response generation.



By retrieving only the highest-relevance results, Dao💫 balances contextual richness with prompt efficiency, ensuring that the LLM receives focused and relevant information.



\### 2.4 Context Construction and Grounding



Following retrieval, Dao💫 transforms retrieved search results into structured contextual input for the language model.



\#### Retrieved Output Structure



The retrieval stage returns multiple artifacts:



* relevant document chunks,
* associated metadata,
* vector similarity distances,
* contextual snippets derived from retrieved documents.



These elements collectively enable both grounded response generation and source transparency.



\#### Context Assembly



The system constructs a unified context object before invoking the LLM:



1. Retrieved documents are processed to extract \*\*relevant excerpts and snippets\*\*, rather than passing entire source documents.

2\. Selected excerpts are consolidated into structured contextual passages used for grounding.

3\. Conversation history is appended to preserve multi-turn dialogue continuity.

4\. The finalized context block is injected into the prompt template used for LLM invocation.



By supplying only targeted excerpts, Dao💫 optimizes prompt efficiency while ensuring that generated responses remain focused on the most relevant knowledge.



\#### Relevance Evaluation



Vector similarity distances are used as a relevance signal:



* Retrieved results exceeding a predefined distance threshold are considered less relevant.
* Distance values help determine whether supporting sources and metadata should be surfaced to the user alongside the generated answer.



This mechanism allows Dao💫 to balance response generation with transparent evidence presentation.



\#### Grounded Generation



The final constructed context is incorporated into the prompt used for response generation, ensuring that answers are grounded in retrieved elephant knowledge rather than relying solely on pretrained model information.



\### 2.5 Prompt Architecture



Dao💫 uses a structured prompt construction strategy to ensure domain grounding, conversational coherence, and consistent response formatting.



\#### Prompt Components



Each LLM invocation is driven by a composite prompt consisting of multiple coordinated elements.



\*\*1. System and Identity Instructions\*\*



The prompt begins with system-level instructions defining Dao💫’s behavioral constraints and role:



* establishes Dao💫 as an elephant-focused assistant,
* restricts responses to elephant and conservation-related topics,
* enforces domain boundaries to reduce hallucinations,
* defines response tone and assistant identity.



These instructions act as persistent behavioral controls guiding every response.



\*\*2. Contextual Knowledge (Retrieved Excerpts)\*\*



Relevant excerpts extracted from retrieved documents are inserted into the prompt as contextual grounding material.



This context enables the LLM to generate answers based on curated elephant knowledge rather than relying solely on pretrained information.



\*\*3. Conversation History\*\*



Selected prior conversation turns are included to preserve dialogue continuity and allow Dao💫 to correctly interpret follow-up questions.



\*\*4. Rewritten User Query\*\*



The normalized standalone version of the user’s question is supplied to ensure clarity during response generation, particularly for multi-turn interactions.



\*\*5. Formatting and Interaction Rules\*\*



Additional prompt instructions guide output structure based on interaction mode, such as:



* identity responses,
* follow-up conversational replies,
* structured answer formatting.



These rules maintain consistent response presentation across conversations.



\### 2.6 LLM Invocation Strategy



Dao💫 employs a multi-stage LLM invocation strategy in which different model calls are assigned specialized responsibilities within the request lifecycle.



\#### LLM Calls per User Query



The number of LLM invocations varies depending on the selected response language.



\*\*English Response Flow\*\*



For English interactions, Dao💫 performs \*\*two LLM calls\*\*:



\*\*1. Query Rewriting Call\*\*



* Converts follow-up or conversational questions into standalone queries.
* Incorporates conversation context to improve retrieval accuracy.
* Ensures semantic clarity before retrieval execution.



\*\*2. Response Generation Call\*\*



* Receives the structured prompt containing:

  * system and identity instructions,
  * retrieved contextual excerpts,
  * conversation history,
  * rewritten query.
* Generates the final grounded response.



\*\*Thai Response Flow\*\*



When Thai is selected as the response language, Dao💫 performs \*\*an additional LLM call\*\*:



\*\*3. Translation Call\*\*



* Translates the generated English response into Thai.
* Preserves meaning and conversational tone while adapting language output.



This modular invocation strategy separates reasoning, generation, and translation concerns, improving maintainability and enabling multilingual support without modifying the core retrieval pipeline.



\### 2.7 Memory \& Conversation Handling



Dao💫 supports multi-turn conversations through controlled conversational memory management implemented at the application level.



\#### Conversation State Management



Conversation history is maintained using Streamlit session state, which stores prior user and assistant messages throughout an interaction session.



This stored chat history enables Dao💫 to preserve conversational continuity across multiple turns.



\#### Context Window Strategy



Rather than passing the entire conversation to the LLM, Dao💫 applies a \*\*windowed memory approach\*\*:



* Only the \*\*last four conversational turns\*\* are included during prompt construction.
* This limits prompt size while preserving sufficient context for follow-up interactions.
* The approach balances contextual awareness with computational efficiency.



\#### Follow-Up Question Handling



Dao💫 detects follow-up queries using rule-based analysis:



* The system checks incoming queries for conversational indicators suggesting reference to prior responses.
* When detected, the system consults recent chat history to interpret the user’s intent relative to earlier answers.



This prevents ambiguity in multi-turn conversations.



\#### Query Rewriting with Conversational Context



During query normalization:



* Conversation history is supplied to the query rewriting stage.
* Based on system instructions, the LLM converts follow-up questions into standalone queries.
* The rewritten query is then used for retrieval and prompt construction.



This mechanism ensures accurate semantic retrieval even when users ask incomplete or context-dependent questions.



\### 2.8 Guardrails and Domain Boundaries



Dao💫 enforces strict domain boundaries to maintain response reliability and prevent unsupported knowledge generation.



\#### Domain Restriction Strategy



Dao💫 is intentionally designed as a \*\*domain-specific assistant\*\* focused exclusively on elephants and elephant conservation. When users submit questions unrelated to this domain, the system does not attempt speculative responses.



Instead, Dao💫:



* clearly communicates that sufficient context is unavailable,
* avoids generating answers based on general pretrained knowledge,
* redirects the conversation back toward elephant-related topics.



\#### Behavioral Guardrails



Domain adherence is enforced through system and identity instructions embedded within the prompt architecture. These instructions guide the LLM to:



* decline out-of-scope requests,
* avoid hallucinated information,
* maintain consistent assistant identity.



By restricting responses to grounded knowledge, Dao💫 prioritizes transparency and trustworthiness over broad conversational capability.



\#### User Experience Consideration



Rather than abruptly rejecting queries, Dao💫 maintains a friendly conversational tone and encourages users to continue exploring elephant-related discussions. This preserves engagement while reinforcing system boundaries.



\### 2.9 Logging and Observability



Dao💫 incorporates lightweight logging mechanisms to support debugging, evaluation, and iterative system improvement.



\#### Logged Interaction Data



During each interaction, the system records selected intermediate variables generated throughout the pipeline, including:



* the rewritten standalone query,
* the user-selected response language,
* retrieved document excerpts,
* vector similarity distances associated with retrieval results,
* LLM interaction metadata.



These logs provide visibility into how user queries are interpreted, how retrieval decisions are made, and how responses are generated.



\#### Purpose of Logging



The logging system enables:



* debugging retrieval or response issues,
* evaluating retrieval relevance,
* diagnosing prompt or translation behavior,
* monitoring overall pipeline performance during development.



Dao💫 intentionally maintains \*\*minimal, development-focused observability\*\*, prioritizing learning and experimentation over production-scale telemetry.



\### 2.10 Model Deployment Strategy



Dao💫 utilizes a locally hosted LLM runtime instead of a cloud-based API deployment.



\#### Local LLM Infrastructure



The system runs language models locally using a dedicated LLM runtime environment. Model inference executes directly on the developer’s machine, leveraging local GPU acceleration.



This setup enables Dao💫 to operate without dependency on external model hosting services.



\#### Rationale for Local Deployment



The decision to adopt a local LLM architecture was driven by the following considerations:



\*\*Cost Efficiency\*\*



* Eliminates per-request API usage costs.
* Enables unrestricted experimentation during development and testing.



\*\*Hardware Utilization\*\*



* The system leverages a high-performance local GPU (RTX 4070), allowing efficient on-device inference.
* Maximizes available computational resources already dedicated to development work.



\*\*Learning Objectives\*\*



* Supports deeper understanding of LLM systems beyond API consumption.
* Provides hands-on experience with model runtime management, performance trade-offs, and local inference workflows.



\#### Architectural Implications



Local deployment introduces several characteristics:



* reduced operational cost,
* improved experimentation flexibility,
* independence from external service availability,
* increased control over system behavior.



\---



\## 🧩 Section 3 — Data \& Knowledge Architecture



\### 3.1 Knowledge Sources



Dao💫 operates as a domain-specific Retrieval-Augmented Generation (RAG) system whose knowledge base is constructed from curated elephant-focused materials.



The current knowledge base consists of:



* Multiple large-scale elephant conservation research PDFs obtained from reputable elephant conservation sources.
* A supplementary text file describing \*\*Thai Elephant Day\*\*, providing cultural and contextual information.



These documents collectively provide domain coverage across elephant biology, conservation, behavior, and related educational content.



Dao does not access external internet sources; all responses originate exclusively from this curated dataset.



\### 3.2 Data Ingestion Pipeline



Knowledge enters Dao through a structured ingestion pipeline designed to transform raw documents into searchable semantic representations.



The ingestion workflow consists of:



1. \*\*Document Loading\*\*
* Source files are read from local storage.



2\. \*\*Text Cleaning\*\*

* Non-essential elements such as author citations and formatting artifacts are removed to improve embedding quality.



3\. \*\*Chunking\*\*

* Documents are divided into smaller semantic units using:

  * \*\*Chunk size:\*\* 1200 characters
* Chunking improves retrieval granularity and ensures compatibility with LLM context limits.



4\. \*\*Embedding Generation\*\*

* Each chunk is converted into a vector embedding.



5\. \*\*Vector Storage\*\*

* Generated embeddings are stored in a persistent \*\*ChromaDB\*\* collection.



This process converts static research documents into a semantic knowledge system optimized for retrieval.



\### 3.3 Chunking Strategy



Entire documents are not passed directly to the LLM. Instead, Dao uses chunking to improve retrieval precision and contextual relevance.



Chunking provides several advantages:



* Enables semantic search at a fine-grained level.
* Prevents irrelevant sections of large documents from entering prompts.
* Helps maintain coherent context within LLM token limits.
* Improves answer grounding by retrieving only relevant excerpts.



This design choice was informed by foundational RAG learning during early project development.



\### 3.4 Vector Database Design



All knowledge embeddings are stored within a single ChromaDB collection.



Each stored chunk contains associated metadata, including:



* Source file name
* Page number
* Chunk text
* Chunk index



This metadata enables traceability, source attribution, and user-facing transparency during answer generation.



\### 3.5 Retrieval Configuration



When a user submits a query:



1. The query is converted into an embedding vector.

2\. A \*\*vector similarity search\*\* is performed between the query embedding and stored document embeddings.

3\. The system retrieves the \*\*top two most similar chunks\*\*.



Retrieved results include:



* Relevant document excerpts (snippets)
* Metadata
* Vector distance scores indicating semantic similarity



These excerpts are later used for context construction during prompt generation.



\### 3.6 Knowledge Scope Control



Dao is intentionally constrained to operate strictly within its elephant-focused knowledge domain.



The system ensures scope control through:



* Reliance solely on retrieved document context.
* System and identity instructions restricting responses to elephant-related topics.
* Explicit refusal behavior when queries fall outside the knowledge domain.



If no relevant context exists, Dao informs the user that it lacks information while encouraging elephant-related discussion.



This prevents hallucinations and reinforces domain reliability.



\### 3.7 Source Attribution \& Transparency



Dao prioritizes answer transparency by exposing supporting sources to users.



After response generation:



* Retrieved sources are displayed in the \*\*sidebar interface\*\*.
* Each source includes:

  * File name
  * Page number
  * Retrieved snippet



Vector distance thresholds determine whether sources are shown.

Sources are displayed only when sufficiently relevant to the query, preventing misleading or weakly related citations.



\### 3.8 Knowledge Base Limitations



Dao’s knowledge capabilities are constrained by its dataset.



Current limitations include:



* Knowledge derived from only five research documents.
* No internet access or real-time information retrieval.
* Static knowledge requiring manual updates.
* Coverage limited to available conservation materials.



These constraints are intentional to maintain domain accuracy and controlled experimentation.



\### 3.9 Knowledge Update Strategy



Knowledge expansion follows a deterministic update workflow:



1. New source documents are added.

2\. Existing ChromaDB embeddings are deleted.

3\. The ingestion pipeline is re-executed.

4\. New embeddings are generated and stored.



This regeneration process ensures consistency between the knowledge base and retrieval system.



\---



\## ⚙️ Section 4 — Model \& Prompt Engineering



\### 4.1 Model Selection



Dao💫 operates using locally hosted Large Language Models executed through the \*\*Ollama runtime\*\*.



Current models include:



* \*\*Llama\*\* — primary model for reasoning and answer generation.
* \*\*Qwen 2.5\*\* — specialized model used for multilingual translation tasks.



Earlier development phases utilized \*\*Mistral\*\*, which was later replaced as experimentation progressed and system requirements evolved.



Using Ollama enables local model execution, eliminating external API dependencies while providing full control over experimentation and deployment.



\### 4.2 Model Role Assignment



Dao employs multiple LLM calls, each assigned a distinct functional responsibility.



Instead of relying on a single model invocation, responsibilities are separated as follows:



| \*\*LLM Call\*\* | \*\*Responsibility\*\* | 

|--------------|--------------------| 

| Query Rewriting | Reformulates user queries using conversation context | 

| Main Generation | Produces grounded elephant-domain responses | 

| Translation (Thai Mode) | Converts English output into natural Thai | 



This modular design improves response quality, contextual understanding, and multilingual reliability.



\### 4.3 System Prompt Design



System prompts act as the primary mechanism for controlling Dao’s behavior.



Prompt instructions define:



* Domain restriction to \*\*elephant-related knowledge\*\*
* Assistant identity and personality
* Conversational tone
* Greeting behavior
* Formatting rules
* Follow-up handling
* Refusal behavior for out-of-scope questions



Through prompt engineering, Dao behaves as a specialized domain assistant rather than a general-purpose chatbot.



\### 4.4 Prompt Composition



Before each response generation, Dao constructs a structured prompt composed of multiple elements:



* System and behavioral instructions
* Answer mode (standard, follow-up, or identity question)
* Conversation history
* Rewritten user query
* Retrieved knowledge context (document excerpts only)
* Formatting rules



Only relevant excerpts are injected into the prompt rather than entire documents, ensuring efficient token usage and stronger grounding.



\### 4.5 Grounded Generation Strategy



Dao follows a strict grounding strategy to minimize hallucinations.



The system prompts explicitly instruct the LLM to:



* Answer only using retrieved context.
* Avoid generating unsupported facts.
* Clearly acknowledge when insufficient information exists.



If adequate context is unavailable, Dao transparently informs the user and redirects conversation toward elephant-related topics.



This design enforces domain reliability and controlled response behavior.



\### 4.6 Multilingual Prompt Strategy



Dao supports bilingual interaction through a controlled multilingual pipeline.



When the user selects Thai (TH) from the interface:



1. The primary answer is generated in English using \*\*Llama\*\*.

2\. The generated response is sent to \*\*Qwen 2.5\*\* for translation.

3\. Translation prompts instruct the model to produce natural, native Thai phrasing.



This two-stage approach was chosen after observing inconsistencies in Asian language handling by the primary model.

Qwen 2.5 demonstrated stronger performance for Thai language fluency.



\### 4.7 Prompt Iteration \& Debugging



Prompt engineering underwent multiple refinement cycles during development.



Key issues addressed included:



* Translation inaccuracies
* Repetitive greetings on every query
* Self-referencing behavior (assistant naming itself unnecessarily)
* Bullet formatting inconsistencies
* Leakage of internal instructions into responses
* Occasional out-of-context answers



Iterative prompt tuning significantly improved response stability and user experience.



\### 4.8 Design Decisions \& Engineering Constraints



The architectural choices in Dao were intentional design decisions aligned with project goals rather than tradeoffs.



Key decisions included:



* Using \*\*local LLMs\*\* to control cost and enable experimentation.
* Employing \*\*multiple specialized LLM calls\*\* to improve multilingual accuracy.
* Enforcing \*\*strict grounding\*\* to maintain domain specialization.
* Designing Dao as a focused elephant knowledge assistant rather than a general chatbot.



These constraints ensured alignment between technical implementation and the project’s educational and conservation-oriented objectives.



\---



\## 🧪 Section 5 — Evaluation, Testing \& Observability



\### 5.1 Evaluation Philosophy



The primary evaluation objective for Dao💫 was behavioral correctness rather than traditional benchmark accuracy.



Successful system performance was defined as Dao:



* Responding strictly using retrieved elephant-domain context
* Demonstrating correct understanding of user queries
* Maintaining the identity of a friendly elephant knowledge assistant
* Displaying relevant sources accurately
* Handling conversational follow-up questions correctly
* Refusing out-of-domain queries appropriately
* Producing reliable multilingual responses
* Adhering consistently to system prompt instructions



Evaluation focused on verifying that the assistant behaved exactly as designed.



\### 5.2 Testing Methodology



Testing was conducted through iterative User Acceptance Testing (UAT).



The system was evaluated using diverse interaction scenarios, including:



* Simple factual questions
* Complex informational queries
* Follow-up conversational questions
* Identity-related questions
* Out-of-context prompts
* Thai language response testing



Testing was repeated after architectural or prompt changes to ensure regressions were not introduced.



\### 5.3 Evaluation Dimensions



Responses were assessed across multiple qualitative dimensions:



* \*\*Factual Correctness\*\* — Accuracy of elephant-related information
* \*\*Context Relevance\*\* — Alignment between answers and retrieved documents
* \*\*Source Grounding\*\* — Correct display of supporting sources
* \*\*Tone \& Formatting Quality\*\* — Consistency with assistant personality and formatting rules
* \*\*Translation Quality\*\* — Naturalness and correctness of Thai responses
* \*\*Refusal Correctness\*\* — Appropriate handling of unsupported or unrelated queries



This multidimensional evaluation ensured both technical and conversational quality.



\### 5.4 Observed Failure Modes



During testing, several system limitations were identified:



* Incorrect or unnatural translations
* Incomplete responses
* Formatting inconsistencies (e.g., unintended bullet usage)
* Occasional hallucinations
* Incorrect answers due to retrieval mismatch
* Prompt instruction leakage into responses
* Repetitive greeting behavior
* UI freezing and Streamlit rerun issues



Identifying these failure modes guided subsequent system improvements.



\### 5.5 Debugging \& Improvement Workflow



Issues discovered during testing were addressed through iterative refinement.



Typical improvement steps included:



* System prompt adjustments
* Chunk size experimentation
* Document re-ingestion and embedding regeneration
* Code-level logic improvements
* Retrieval and formatting refinements



This iterative loop of testing, diagnosis, and refinement formed the core development workflow.



\### 5.6 Observability Signals



Dao implements lightweight logging to support debugging and behavioral validation.



Key observed signals include:



* Rewritten user queries
* Selected response model
* Retrieved documents and vector similarity distances



These signals helped verify whether retrieval, prompt construction, and model selection behaved as expected during testing.



Additional logs exist but were primarily used for internal debugging rather than formal evaluation.



\### 5.7 Current Evaluation Limitations



Evaluation of Dao currently relies on manual testing and qualitative assessment.



The system does not yet include:



* Automated evaluation metrics
* Benchmark datasets
* Human rating pipelines
* Continuous monitoring dashboards
* Quantitative performance tracking



Future work includes expanding evaluation methodologies to enable systematic measurement of model quality and reliability.



\---



\## 🚀 Section 6 — Deployment, Performance \& Scalability



\### 6.1 Deployment Environment



Dao💫 is currently deployed locally on the developer’s personal machine.



The application runs as a \*\*Streamlit-based web interface\*\* and is accessible only within the local environment. This setup supports experimentation, rapid iteration, and development-focused testing rather than public access.



\### 6.2 Runtime Architecture



When active, Dao operates as a multi-component local AI system consisting of:



* Streamlit application (user interface)
* Python backend orchestration logic
* Ollama local LLM runtime
* Locally hosted LLM models (Llama, Qwen 2.5)
* ChromaDB vector database
* GPU-accelerated inference using an NVIDIA RTX 4070 laptop GPU



These components run simultaneously to support retrieval, generation, translation, and response rendering.



\### 6.3 Performance Characteristics



In practical usage, Dao demonstrates acceptable interactive performance for a locally hosted RAG system.



Observed behavior includes:



* Moderate response latency during initial queries
* Faster responses for conversational follow-up questions
* Increased latency when Thai translation is enabled due to an additional LLM invocation



Overall performance is suitable for development and experimentation scenarios.



\### 6.4 Performance Bottlenecks



The primary performance constraints identified during testing are:



* \*\*Translation Step\*\* — additional LLM call significantly increases response time
* \*\*Streamlit Reruns\*\* — UI refresh behavior occasionally introduces delays



These factors contribute more to perceived latency than retrieval operations.



\### 6.5 Scalability Limitations



The current deployment architecture is not designed for multi-user scalability.



Key limitations include:



* Execution on a single local machine
* Dependence on local GPU resources
* Lack of server-based deployment
* No concurrent user handling
* Manual application startup



As a result, Dao presently functions as a single-user development system.



\### 6.6 Future Deployment Vision



Dao is intended to evolve toward a publicly accessible application following industry deployment best practices.



While a production deployment has not yet been implemented, future directions may include:



* Cloud-based hosting
* Dedicated GPU-backed inference servers
* Web-accessible Streamlit or API-driven architecture
* Support for multiple concurrent users



This represents a planned area of future learning and system expansion.



\---



\## 💡 Section 7 - Engineering Reflection \& Key Learnings



\### 7.1 Prompt Design as System Control



One of the most important realizations during the development of Dao💫 was how strongly simple, natural-language prompts control the behavior of Large Language Model systems.



Initially, I approached prompts as supporting instructions around the model. However, during iterative development and testing, it became clear that prompt engineering functions as a \*\*primary system control layer\*\* rather than a minor configuration step.



Small changes in wording significantly affected:



* Response tone and personality
* Formatting consistency
* Greeting behavior
* Hallucination frequency
* Translation quality
* Refusal behavior for out-of-scope questions
* Adherence to domain constraints (elephant-only responses)



Many issues that appeared to be model limitations were actually \*\*prompt alignment problems\*\*. Through repeated experimentation, I learned that well-structured system prompts can reliably guide model behavior without modifying model weights or infrastructure.



This shifted my understanding of LLM systems:



> In traditional software, logic lives primarily in code.

> In LLM applications, \*\*behavioral logic largely lives in prompts\*\*.



As a result, prompt engineering in Dao evolved into a structured design activity involving:



* identity definition,
* behavioral constraints,
* formatting rules,
* conversation management,
* and safety grounding to retrieved context.



This experience fundamentally changed how I view LLM system design — prompts are not auxiliary instructions but a core component of application architecture.



\### 7.2 Reliability Through Constraints and Structured Design



A key engineering learning from building Dao💫 was recognizing that reliable AI systems emerge not from increased model intelligence alone, but from carefully designed constraints and structured control mechanisms.



During development, it became evident that Large Language Models do not inherently behave consistently or predictably. Reliability had to be engineered through deliberate system design decisions, including:



* restricting responses to elephant-related knowledge,
* grounding answers strictly in retrieved context,
* defining explicit refusal behavior for out-of-scope queries,
* enforcing formatting and conversational rules through structured prompts, and
* applying relevance thresholds before displaying sources.



Structured prompts and guardrails effectively functioned as operational boundaries that guided model behavior. Rather than relying on model capability alone, Dao’s stability was achieved by combining retrieval grounding, prompt constraints, and controlled response rules.



This experience reinforced an important systems insight: \*\*LLM applications succeed when intelligence is constrained and guided, not when autonomy is maximized\*\*.



\### 7.3 Unexpected Engineering Challenge: Managing Streamlit Reruns in Stateful LLM Applications



One of the most unexpected challenges during Dao💫 development was handling Streamlit’s rerun-based execution model within a conversational AI application.



Streamlit automatically reruns the entire script whenever user interaction occurs. While this behavior simplifies traditional UI development, it introduces complexity when building stateful LLM systems that rely on:



* conversation history,
* intermediate pipeline outputs,
* retrieved context,
* model responses, and
* UI synchronization between chat and sidebar components.



Early iterations of Dao experienced issues such as:



* repeated message generation,
* UI freezing or inconsistent rendering,
* duplicated responses,
* delayed updates after LLM execution,
* challenges maintaining stable chat history across interactions.



Resolving these issues required careful management of session\_state, separation of computation from rendering logic, and explicit control over when LLM calls were triggered.



This experience highlighted an important practical lesson: \*\*building LLM applications is not only an AI problem but also a state management and application architecture challenge\*\*.



\### 7.4 Shift in Perspective: From Traditional NLP Engineering to Instruction-Driven Systems



Before building Dao💫, AI system development was perceived primarily as a complex combination of traditional Natural Language Processing techniques and extensive backend engineering.



Through hands-on implementation, this perspective evolved significantly. The development process revealed that modern LLM applications are less about building language intelligence from scratch and more about \*\*designing effective interaction frameworks around pre-trained models\*\*.



A substantial portion of system behavior — including reasoning style, tone, response structure, refusal logic, and conversational flow — was controlled through carefully engineered prompts rather than conventional algorithmic implementation.



This experience introduced a new understanding of LLM application development as an \*\*instruction-driven paradigm\*\*, where developers guide model behavior through structured language interfaces instead of implementing linguistic capabilities directly.



While underlying infrastructure and orchestration remain essential, Dao demonstrated that modern AI engineering increasingly blends software development with prompt design, system constraints, and iterative experimentation.



\### 7.5 Development of an Iterative Engineering Mindset



The most significant personal skill developed during the creation of Dao💫 was patience with iterative system improvement.



An initial implementation successfully validated the core concepts of retrieval, prompting, and response generation. At this stage, the system was functionally operational, fulfilling its primary objective as a domain-specific conversational assistant.



However, structured User Acceptance Testing (UAT) revealed numerous practical challenges, including formatting inconsistencies, translation errors, hallucinations, prompt leakage, UI instability, and behavioral edge cases.



Addressing these issues required multiple cycles of:



* prompt refinement,
* pipeline adjustments,
* document re-ingestion,
* parameter tuning, and
* systematic testing across diverse query types.



Over time, these iterative improvements significantly enhanced system stability, response quality, and conversational reliability. The development process demonstrated that building dependable AI applications is inherently iterative rather than a one-time implementation task.



This experience reinforced an essential engineering lesson: \*\*robust AI systems emerge through continuous experimentation, evaluation, and incremental refinement\*\*.



\---



\## 🧭 Section 8 — Future Work \& Roadmap



\### 8.1 Evaluation Framework Improvement



One of the primary next steps for Dao💫 is strengthening its evaluation capabilities.



Currently, system evaluation is entirely manual and based on qualitative User Acceptance Testing (UAT). While this has been effective during development, it does not provide a scalable or systematic way to measure performance over time.



Future improvements include:



* introducing structured evaluation metrics for:

  * retrieval relevance
  * factual correctness
  * grounding quality
  * translation accuracy
  * conversational consistency
* building a repeatable test set of elephant-related queries
* developing a lightweight benchmarking pipeline for regression testing
* exploring semi-automated evaluation approaches using LLM-as-judge techniques



This would enable more objective tracking of system improvements across iterations.



\### 8.2 Knowledge Base Expansion \& Ingestion Automation



Another key area of future improvement is expanding and maintaining the underlying knowledge base.



Currently, Dao’s knowledge is derived from a small number of curated elephant conservation documents. While this ensures high-quality grounding, it limits coverage and diversity of information.



Future enhancements include:



* adding more elephant conservation and research sources
* improving domain coverage (behavior, ecology, conservation policy, human-elephant interaction, etc.)
* automating ingestion workflows to reduce manual intervention
* enabling incremental updates without full reprocessing of the vector database
* improving document structuring before embedding for better retrieval quality



This would make Dao a more comprehensive and continuously evolving knowledge system.



\### 8.3 Long-Term Vision



Beyond immediate improvements, Dao is envisioned as a continuously evolving domain-specific AI assistant that:



* maintains high factual grounding through curated knowledge
* supports systematic evaluation and quality tracking
* evolves with new conservation data sources
* and remains a transparent, explainable RAG-based system



The long-term goal is to refine Dao into a robust example of a \*\*domain-specialized, retrieval-grounded AI assistant architecture\*\*.

