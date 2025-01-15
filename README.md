<div align="center">

# XOAS: Your Personal Buddy 😊

<div align="center">
  <img src="logo.png" alt="XOAS Logo" width="200" />
</div>

XOAS is a locally hosted chatbot designed to process domain-specific queries from PDF files and deliver precise, conversational responses. Built with privacy and efficiency in mind, it operates entirely on local infrastructure, ensuring robust data security and seamless operation.

---

## 🚀 Features

- **PDF Embedding:** Converts PDF files into vector embeddings using Hugging Face’s BGE model.
- **Q&A Retrieval:** Utilizes Qdrant for efficient retrieval of domain-specific data.
- **Chatbot Responses:** Generates concise and professional replies using LLaMA 3.2.
- **Interactive Interface:** Powered by Streamlit for a user-friendly experience.
- **Localized Docker Infrastructure:** Operates without reliance on external APIs, ensuring data privacy.

---
## 🔧 Technology Stack

| Technology            | Logo                                                                 |
|------------------------|----------------------------------------------------------------------|
| **Vector Database**    | ![Qdrant](https://img.shields.io/badge/Qdrant-002438?logo=qdrant&logoColor=white) |
| **Embedding Model**    | ![Hugging Face](https://img.shields.io/badge/HuggingFace-FFD55F?logo=huggingface&logoColor=black) |
| **Language Model**     | ![LLaMA](https://img.shields.io/badge/LLaMA-0033CC?logo=ai&logoColor=white)       |
| **Frontend**           | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)   |
| **Programming Language** | ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) |
| **Containerization**   | ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white) |



---

## 🎥 Demo

![Demo Video](https://www.loom.com/embed/5969e8c373e94f51985bfa4829f89186)

---

## 🌐 Application Workflow

1. **PDF Embedding:**

   - Extracts and splits text from PDFs into manageable chunks.
   - Converts text into vector embeddings using Hugging Face BGE.
   - Stores embeddings in Qdrant with metadata for retrieval.

2. **Chatbot Interaction:**

   - Routes domain-specific queries to Qdrant for embedding-based retrieval.
   - Handles general queries with LLaMA for conversational responses.

3. **User-Friendly Interface:**

   - Upload PDFs and interact seamlessly via a Streamlit-based interface.

---

## 💡 Advantages

1. **Localized Infrastructure:** Operates without reliance on external APIs, reducing costs and enhancing privacy.
2. **Data Security:** Ensures sensitive data remains within the local network.
3. **Efficiency:** Avoids redundant embedding creation with JSON-based tracking and ensures concise responses with optimized LLaMA settings.
4. **Scalability:** Modular design supports future feature integration and model upgrades.

---

## 🛠️ Prerequisites

Ensure the following are installed on your system:

- Python 3.10.9 or later
- Docker
- Ollama
- IDE (e.g., VS Code)

---

## 🔧 Setup Instructions

### 1. Install Ollama and Download LLaMA Model:

```bash
# Install Ollama from https://ollama.com/
ollama pull llama 3.2:3b
ollama run llama 3.2:3b
```

### 2. Set Up Qdrant with Docker:

```bash
docker pull qdrant/qdrant
docker run -p 6333:6333 -v .:/qdrant/storage qdrant/qdrant
```

### 3. Install Python Dependencies:

```bash
python -m venv env
source env/bin/activate  # For Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the Application:

```bash
streamlit run app.py
```

---

## 🔎 Challenges Faced

- **Hardware Limitations:** The system runs locally with 12GB of RAM and 256GB SSD storage without GPU support.
- **Latent Response Times:** Resource constraints result in slightly longer response times.



---

Feel free to fork, clone, and contribute to XOAS! Your feedback and enhancements are always welcome. 🌟

