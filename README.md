# 🤖 AI Chatbot

> A RAG-powered AI chatbot that allows users to upload PDF documents and ask questions based on their content.

---

## 🌐 Live Demo

🚀 **Live Application:**  
https://ai-chatbot-g7hm.onrender.com

---

## 📌 About the Project

**AI Chatbot** is a web-based AI application built using **Retrieval-Augmented Generation (RAG)**.

The chatbot allows users to provide PDF documents and interact with them using natural language. Instead of relying only on the AI model's existing knowledge, the system retrieves relevant information from the uploaded documents and uses it to generate responses.

The project was developed to understand how modern AI applications combine:

- 🤖 Large Language Models
- 📚 Document processing
- 🔎 Semantic search
- 🧠 Vector embeddings
- 🗃️ Vector databases
- 🌐 Web development
- ☁️ Cloud deployment

---

# ✨ Features

### 📄 PDF Document Processing

Users can upload PDF documents and use them as the knowledge source for the chatbot.

### 💬 Document Question Answering

Ask natural-language questions about the uploaded documents.

Example:

```text
What are the main topics discussed in this document?
```
# 🏗️ System Architecture

```text
                         ┌──────────────────┐
                         │       USER       │
                         └────────┬─────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │       FRONTEND          │
                    │     HTML / CSS / JS     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │        FASTAPI          │
                    │        BACKEND          │
                    └────────────┬────────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
                ▼                ▼                ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │     PDF      │ │    TOOLS     │ │    CHAT      │
        │  PROCESSING  │ │ Date & Time  │ │   REQUEST    │
        └──────┬───────┘ └──────────────┘ └──────┬───────┘
               │                                  │
               ▼                                  │
        ┌──────────────┐                          │
        │ PyPDFLoader  │                          │
        └──────┬───────┘                          │
               │                                  │
               ▼                                  │
        ┌──────────────┐                          │
        │ TEXT         │                          │
        │ CHUNKING     │                          │
        │ 1000 / 200   │                          │
        └──────┬───────┘                          │
               │                                  │
               ▼                                  │
        ┌──────────────┐                          │
        │   GEMINI     │                          │
        │  EMBEDDINGS  │                          │
        └──────┬───────┘                          │
               │                                  │
               ▼                                  │
        ┌──────────────┐                          │
        │    FAISS     │◄─────────────────────────┘
        │ VECTOR SEARCH │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │  RELEVANT    │
        │  DOCUMENT    │
        │    CHUNKS    │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │    GEMINI    │
        │     AI       │
        │  GENERATION  │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │  AI RESPONSE │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │     USER     │
        └──────────────┘
```
### Architecture Flow

The system follows a RAG-based architecture:

1. User interacts with the chatbot through the web interface.
2. Frontend sends requests to the FastAPI backend.
3. PDF Processing extracts text from uploaded documents using PyPDFLoader.
4. Text Chunking divides the extracted text into manageable chunks.
5. Gemini Embeddings convert the chunks into vector representations.
6. FAISS stores and searches the vector representations.
7. When a question is asked, the system retrieves the most relevant document chunks.
8. Gemini AI uses the retrieved context to generate the response.
9. The generated AI Response is returned to the user.

# 🔄 How the RAG Pipeline Works

The core of the AI Chatbot is a **Retrieval-Augmented Generation (RAG)** pipeline. It allows the chatbot to retrieve relevant information from uploaded PDF documents before generating an AI response.

### RAG Workflow

```text
PDF Document
     │
     ▼
┌──────────────────┐
│  PDF Processing  │
│   PyPDFLoader    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Text Chunking   │
│  1000 / 200      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Gemini Embeddings│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│      FAISS       │
│  Vector Search   │
└────────┬─────────┘
         │
         │
    User Question
         │
         ▼
┌──────────────────┐
│ Semantic Search  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Relevant Chunks  │
│     Top 4        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    Gemini AI     │
│ Response Generate│
└────────┬─────────┘
         │
         ▼
     AI Response
```

---

📂 Project Structure

The project is organized into separate backend and frontend components to keep the application modular and maintainable.

```text
llm/
│
├── backend/
│   │
│   ├── documents/
│   │   └── PDF documents
│   │
│   ├── __init__.py
│   ├── main.py
│   ├── rag.py
│   └── tools.py
│
├── frontend/
│   │
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── app.js
│   │
│   └── index.html
│
├── env/
│   └── .env
│
├── .gitignore
├── requirements.txt
└── README.md

```

# 📸 Screenshots

## 🖥️ Desktop Interface

The main chatbot interface with the modern responsive UI.
<img width="1600" height="801" alt="image" src="https://github.com/user-attachments/assets/621fda6a-8ee4-437f-9812-fc7f8dfc2e12" />
<img width="1600" height="768" alt="image" src="https://github.com/user-attachments/assets/0a97fd76-da82-4d86-995d-354d0c2a24a6" />
<img width="1600" height="797" alt="image" src="https://github.com/user-attachments/assets/e8523449-054c-4b59-9b3b-7a54cd4e2b98" />

## 📱 Mobile Interface

The responsive mobile version of the AI Chatbot.
<img width="844" height="1600" alt="image" src="https://github.com/user-attachments/assets/cbc6ff70-e2ef-427f-b751-5083b57006ee" />
<img width="772" height="1600" alt="image" src="https://github.com/user-attachments/assets/74d21beb-dbce-445d-90c6-ebb7ac0446f2" />
<img width="787" height="1600" alt="image" src="https://github.com/user-attachments/assets/d4d35ee6-c89f-40cc-a54b-02007283b948" />


# ☁️ Deployment

The AI Chatbot is deployed as a web application using **Render**.

---

# ⚠️ Limitations

The current version of AI Chatbot is primarily designed as a learning and demonstration project.

- **API Quotas:** Google Gemini API requests are subject to usage quotas and rate limits.
- **Free Hosting:** The Render free-tier service may sleep after a period of inactivity, which can cause a delay when the application is accessed again.
- **File Persistence:** Files stored on an ephemeral hosting environment should not be considered permanent storage.
- **Scalability:** The current FAISS-based implementation is suitable for a small document knowledge base. Large-scale applications may require a persistent and scalable vector database.
- **Authentication:** User authentication and account management are not currently implemented.
- **Multi-User Support:** Separate user accounts, conversations, and document collections are not currently implemented.
- **Document Formats:** The current implementation primarily focuses on PDF documents.
- **Processing Time:** Large PDF documents may require additional processing time for text extraction, chunking, and embedding generation.

---

# 🔮 Future Improvements

The project can be extended with the following features:

- 🔐 User authentication and authorization
- 👥 Multi-user support
- 💾 Persistent document storage
- 🗃️ Scalable cloud-based vector database
- 📚 Support for DOCX, TXT, CSV, and PPTX files
- 🧠 Improved conversation memory
- 📑 Advanced document citations
- 📊 Usage and analytics dashboard
- ☁️ Cloud-based document storage
- ⚡ Optimized document processing
- 🔍 Improved search and retrieval
- 📱 Progressive Web App (PWA) support

---

---

# 🎓 Learning Outcomes

Developing this project provided practical experience in building and deploying an AI-powered web application.

### 🤖 Artificial Intelligence

- Understanding Generative AI and Large Language Models
- Integrating Google Gemini into an application
- Building AI-powered question-answering systems

### 🔄 Retrieval-Augmented Generation

- Understanding the RAG architecture
- PDF document processing
- Text extraction and chunking
- Vector embeddings
- Semantic similarity search
- Context-based response generation

### 🔎 Vector Search

- Understanding vector representations
- Working with FAISS
- Implementing similarity-based document retrieval

### 🔗 LangChain

- Creating retrieval pipelines
- Integrating embeddings and vector stores
- Building tools for AI applications

### ⚡ Backend Development

- Python
- FastAPI
- REST API development
- Uvicorn
- Backend and frontend integration

### 🎨 Frontend Development

- HTML
- CSS
- JavaScript
- Responsive web design
- Interactive chatbot interface

### ☁️ Deployment

- Git and GitHub
- Environment variables
- Cloud deployment
- Render hosting

### 🧩 Overall Learning

The project provided hands-on experience in connecting multiple technologies into a complete AI application:

```text
Frontend
   ↓
FastAPI Backend
   ↓
Document Processing
   ↓
RAG Pipeline
   ↓
Vector Search
   ↓
Gemini AI
   ↓
AI Response
   ↓
Cloud Deployment

```
---

# 📝 Conclusion

The **AI Chatbot** project demonstrates how modern Generative AI can be combined with **Retrieval-Augmented Generation (RAG)** to create a document-based question-answering system.

The application processes PDF documents, converts their content into vector embeddings, retrieves relevant information using **FAISS**, and uses **Google Gemini** to generate context-aware responses.

By combining **Python, FastAPI, LangChain, Gemini, FAISS, HTML, CSS, and JavaScript**, the project provides a complete AI application workflow from document processing and semantic search to frontend interaction and cloud deployment.

This project also provided practical experience in building an end-to-end AI system and understanding how RAG can be used to make AI applications more useful when working with specific document-based knowledge.

---

# 👨‍💻 Developer

## Anugrah R

**B.Tech Computer Science & Engineering**

### Areas of Interest

- 🤖 Artificial Intelligence
- 🧠 Machine Learning
- 🌐 Full Stack Development
- 💻 Software Development
- ☁️ Cloud Technologies



<p align="center">

### 🤖 AI Chatbot

**Ask your documents. Get intelligent answers.**

Built with **Python • FastAPI • LangChain • Gemini • FAISS**

</p>




