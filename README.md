# XOAS: Your Personal Buddy 😊

## Description
XOAS is an AI-powered tool that facilitates quick target identification and drug discovery, powered by state-of-the-art models and efficient infrastructure. With embedded PDF processing, chatbot functionality, and scalable architecture, XOAS aims to streamline decision-making in drug discovery. The project integrates Qdrant for local data storage, BGE for embedding generation, and LLaMA 3.2 for conversational AI.

## Technology Stack

Here’s the core stack that powers XOAS:

- **Vector Database**: [Qdrant (local instance via Docker)](https://qdrant.tech)
- **Embedding Model**: [BAAI BGE](https://huggingface.co/BAAI/BGE)
- **Language Model**: [LLaMA 3.2 (3B model)](https://huggingface.co/MetaAI/LLaMA) - locally hosted via [Ollama](https://ollama.com)
- **Frontend**: [Streamlit](https://streamlit.io) - for interactive user interfaces
- **Programming Language**: Python 3.10+

### Tech Stack Logos:
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python" width="100" />
  <img src="https://img.shields.io/badge/Streamlit-1.0%2B-blue" alt="Streamlit" width="100" />
  <img src="https://img.shields.io/badge/Docker-20.10%2B-blue" alt="Docker" width="100" />
  <img src="https://img.shields.io/badge/Qdrant-1.0.0-green" alt="Qdrant" width="100" />
  <img src="https://img.shields.io/badge/HuggingFace-Transformers-yellow" alt="HuggingFace" width="100" />
  <img src="https://img.shields.io/badge/Ollama-LLaMA-blue" alt="Ollama" width="100" />
</p>

### Cluster of Logos (Portfolio)
Below are some of the technologies I have worked with in various projects, displayed here as a visual portfolio:

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/6/69/Python_logo_2020.svg" alt="Python" width="100" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/0/06/Docker_logo.png" alt="Docker" width="100" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/a/af/Ollama_logo.svg" alt="Ollama" width="100" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/8/88/Streamlit_logo.png" alt="Streamlit" width="100" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/c/cf/Qdrant_logo.svg" alt="Qdrant" width="100" />
</p>

## Features

- **PDF Embedding**: Converts PDF files into vector embeddings using the Hugging Face BGE model.
- **Q&A Retrieval**: Utilizes Qdrant to store and retrieve similar embeddings for domain-specific queries.
- **Chatbot Responses**: LLaMA 3.2 generates conversational and professional responses.

## Components

### Embedding Management (vectors.py)
- **Embedding Model**: BGE embedding model from Hugging Face ensures normalized and device-specific embeddings.
- **Qdrant Vector Store**: Hosted locally via Docker (`http://localhost:6333`).
  - Collections are created dynamically if not already present.
- **PDF Processing**: Splits PDF text into manageable chunks using RecursiveCharacterTextSplitter and generates embeddings for storage in Qdrant.
- **Tracking Processed PDFs**: Uses a JSON-based tracking system to avoid reprocessing files.

### Chatbot Management (chatbot.py)
- **Model Configuration**: 
  - Embedding model: BGE (small-en) from Hugging Face.
  - Language model: Ollama-based LLaMA 3.2 (3B), configured with low-temperature settings for concise responses.
- **Prompts**:
  - Domain-specific Prompt: Context-driven, focused on personal PDF-based queries.
  - General Prompt: Provides conversational and professional responses for non-domain-specific queries.
- **Retrieval and Query Handling**: 
  - Uses Qdrant as the retriever to find relevant embeddings for user queries.
  - Implements a fallback mechanism for general queries using LLaMA.

### Application Interface (app.py)
- **File Upload**: Allows users to upload PDF documents in the “data folder” via Streamlit.
- **Embedding Creation**: Automatically processes uploaded PDFs, generating embeddings if not already stored.
- **Query Input**: Users can input questions into the chatbot interface, with the system routing queries based on whether they are domain-specific or general.

## Advantages of the Solution

- **Localized Infrastructure**: 
  - Eliminates reliance on external APIs like Pinecone, reducing operational costs.
  - Enhances data security by keeping everything on the local network or within your own network.
  
- **Scalability**: 
  - Modular design supports additional functionality, such as integrating new data sources or upgrading models.
  
- **Efficiency**:
  - JSON-based file tracking avoids redundant embedding creation.
  - Low-temperature LLaMA configuration ensures concise and accurate responses.

- **Qdrant and Local Data Hosting**:
  - Data is stored locally within the internal network, ensuring privacy and data security.
  - The Docker-based Qdrant solution offers full control over the data.

## Challenges Faced

- **Resource Constraints (CPU-based Only)**:
  - Latent response times may occur due to hardware limitations (12GB RAM and 256GB SSD, without GPU).

## Prerequisites

Before starting, make sure you have the following installed:

- **Python 3.10.9** (or a compatible version)
- **Ollama** (for downloading and running the LLaMA model)
- **Docker** (for setting up Qdrant)
- **VS Code** (or your preferred IDE)

### Steps to Install and Set Up:

#### Download and Install Ollama:
1. Visit [Ollama](https://ollama.com) and download the software.
2. Open the Ollama Command Prompt and run:
   ```bash
   ollama pull llama 3.2:3b
   ollama run llama 3.2:3b
