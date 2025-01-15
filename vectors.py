# vectors.py

import os
import json
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from hashlib import md5
from transformers import AutoModel
from qdrant_client.http.models import Distance, VectorParams

class EmbeddingsManager:
    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en",
        device: str = "cpu",
        encode_kwargs: dict = {"normalize_embeddings": True},
        qdrant_url: str = "http://localhost:6333",
        collection_name: str = "vector_db",
        tracking_file: str = "processed_files.json"
    ):
        self.model_name = model_name
        self.device = device
        self.encode_kwargs = encode_kwargs
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name
        self.tracking_file = tracking_file

        # Initialize embeddings
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": self.device},
            encode_kwargs=self.encode_kwargs,
        )

        # Retrieve vector size dynamically
        model = AutoModel.from_pretrained(self.model_name)
        self.vector_size = model.config.hidden_size

        # Initialize Qdrant client and create collection if it doesn't exist
        self.qdrant_client = QdrantClient(url=self.qdrant_url)
        existing_collections = self.qdrant_client.get_collections()

        if self.collection_name not in [col.name for col in existing_collections.collections]:
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )

        # Load or initialize the tracking file
        if not os.path.exists(self.tracking_file):
            with open(self.tracking_file, 'w') as f:
                json.dump({}, f)


    def pdf_to_id(self, pdf_path: str) -> str:
        """Generate a unique ID for the PDF using its filename."""
        filename = os.path.basename(pdf_path).encode()
        return md5(filename).hexdigest()

    def load_tracking_data(self):
        """Load the processed files tracking data."""
        with open(self.tracking_file, 'r') as f:
            return json.load(f)

    def save_tracking_data(self, tracking_data):
        """Save the processed files tracking data."""
        with open(self.tracking_file, 'w') as f:
            json.dump(tracking_data, f, indent=4)

    def create_embeddings(self, data_folder: str):
        """
        Process new PDFs in the folder, create embeddings, and store them in Qdrant.
        
        Args:
            data_folder (str): Path to the folder containing PDFs.
        """
        if not os.path.exists(data_folder):
            raise FileNotFoundError(f"The folder {data_folder} does not exist.")

        pdf_files = [
            os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".pdf")
        ]

        if not pdf_files:
            raise ValueError("No PDF files found in the data folder.")

        # Load tracking data
        tracking_data = self.load_tracking_data()

        qdrant_store = Qdrant(
            client=self.qdrant_client,
            collection_name=self.collection_name,
            embeddings=self.embeddings,
        )

        for pdf_path in pdf_files:
            pdf_id = self.pdf_to_id(pdf_path)

            # Skip already processed files
            if pdf_id in tracking_data:
                print(f"⚠️ Embeddings for '{os.path.basename(pdf_path)}' already exist. Skipping.")
                continue

            # Process and create embeddings for the new PDF
            print(f"🔄 Creating embeddings for '{os.path.basename(pdf_path)}'...")
            loader = UnstructuredPDFLoader(pdf_path)
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=250)
            splits = text_splitter.split_documents(docs)

            try:
                qdrant_store.add_texts(
                    [chunk.page_content for chunk in splits],
                    metadatas=[{"id": pdf_id, "filename": os.path.basename(pdf_path)} for _ in splits],
                )
                print(f"✅ Embeddings for '{os.path.basename(pdf_path)}' added successfully.")
                tracking_data[pdf_id] = pdf_path  # Mark as processed
            except Exception as e:
                print(f"⚠️ Failed to add embeddings for '{os.path.basename(pdf_path)}': {e}")

        # Save updated tracking data
        self.save_tracking_data(tracking_data)







