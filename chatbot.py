
#chatbot.py

import os
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_qdrant import Qdrant
from langchain_ollama import ChatOllama
from qdrant_client import QdrantClient
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
import streamlit as st


class ChatbotManager:
    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en",
        device: str = "cpu",
        encode_kwargs: dict = {"normalize_embeddings": True},
        llm_model: str = "llama3.2:3b",  # LLAMA 3.2 model
        llm_temperature: float = 0.1,
        qdrant_url: str = "http://localhost:6333",
        collection_name: str = "vector_db",
    ):
        self.model_name = model_name
        self.device = device
        self.encode_kwargs = encode_kwargs
        self.llm_model = llm_model
        self.llm_temperature = llm_temperature
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name

        # Initialize Embeddings
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": self.device},
            encode_kwargs=self.encode_kwargs,
        )

        # Initialize Local LLM
        self.llm = ChatOllama(
            model=self.llm_model,
            temperature=self.llm_temperature,
        )

        # Define the prompt templates
        self.domain_prompt_template = """Use the following context to answer the user's question in a short, conversational tone. Be brief and relevant. If you're unsure, say 'I don't know.' Avoid making up answers.

Context: {context}
Question: {question}

Answer (brief and relevant):
"""

        self.general_prompt_template = """You are Personal Buddy, a virtual assistant designed to help users in a friendly, casual, and professional manner. Your role is to assist users with any questions or tasks they have while maintaining a warm and approachable tone.

1. If greeted (e.g., "Hi", "Hello"), respond warmly with something like: "Hey there! I'm your Personal Buddy. How can I help you today?"
2. If asked about your identity, state: "I'm your Personal Buddy, here to make your life easier. You can ask me anything!"
3. For general questions, provide clear, thoughtful, and conversational answers.

User Query: {question}

Answer:
"""

        # Initialize Qdrant client
        self.client = QdrantClient(url=self.qdrant_url, prefer_grpc=False)

        # Initialize the Qdrant vector store
        self.db = Qdrant(
            client=self.client,
            embeddings=self.embeddings,
            collection_name=self.collection_name,
        )

        # Initialize the retriever
        self.retriever = self.db.as_retriever(search_kwargs={"k": 1})

        # Define prompt templates
        self.domain_prompt = PromptTemplate(
            template=self.domain_prompt_template,
            input_variables=["context", "question"],
        )
        self.general_prompt = PromptTemplate(
            template=self.general_prompt_template,
            input_variables=["question"],
        )

        # Define chain type kwargs
        self.chain_type_kwargs = {"prompt": self.domain_prompt}

        # Initialize the RetrievalQA chain for domain-specific queries
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=False,
            chain_type_kwargs=self.chain_type_kwargs,
            verbose=False,
        )

    def is_general_query(self, query: str) -> bool:
        general_keywords = [ "hi", "hello", "hey", "howdy", "good morning", "good afternoon", "good evening",
    "how are you", "how's it going", "what's up", "who are you", "greeting",
    "how do you do", "nice to meet you", "pleasure to meet you", "yo", "sup",
    "what can you do", "tell me about yourself", "introduce yourself"]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in general_keywords)

    def handle_general_query(self, query: str) -> str:
        """
        Handles general queries by directly prompting the LLM.

        Args:
            query (str): The user's query.

        Returns:
            str: The response from the LLM.
        """
        try:
            # Format the input for the LLM
            prompt = self.general_prompt.format(question=query)
            response = self.llm.invoke(prompt)  # Pass the formatted prompt as a string
            return response.content.strip()  # Extract the content attribute and strip whitespace
        except Exception as e:
            st.error(f"⚠️ An error occurred while processing your general query: {e}")
            return "⚠️ Sorry, I couldn't process your query at the moment."

        


    def get_response(self, query: str) -> str:
        try:
            if self.is_general_query(query):
                return self.handle_general_query(query)
            response = self.qa.run(query)
            return response.strip()
        except Exception as e:
            st.error(f"⚠️ An error occurred while processing your request: {e}")
            return "⚠️ Sorry, I couldn't process your request at the moment."



