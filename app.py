# app.py
#Xoas chatbot

import streamlit as st
import time
from vectors import EmbeddingsManager
from chatbot import ChatbotManager
from streamlit_lottie import st_lottie
import json

# Set Page Configuration
st.set_page_config(
    page_title="XOAS: Your Personal Buddy 😊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
        .centered-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: orange;
        }
        .centered-logo img {
            display: block;
            margin: 0 auto;
            width: 150px;
        }
        .white-text {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to load Lottie animations
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Initialize Embeddings in Backend
@st.cache_resource
def initialize_embeddings():
    embeddings_manager = EmbeddingsManager(
        model_name="BAAI/bge-small-en",
        device="cpu",
        encode_kwargs={"normalize_embeddings": True},
        qdrant_url="http://localhost:6333",
        collection_name="vector_db",
    )
    data_folder = "data"
    embeddings_manager.create_embeddings(data_folder)
    chatbot_manager = ChatbotManager(
        model_name="BAAI/bge-small-en",
        device="cpu",
        encode_kwargs={"normalize_embeddings": True},
        llm_model="llama3.2:3b",
        llm_temperature=0.7,
        qdrant_url="http://localhost:6333",
        collection_name="vector_db",
    )
    return chatbot_manager

# Initialize chatbot backend during app startup
if "chatbot_manager" not in st.session_state:
    with st.spinner("Initializing system and embedding PDFs..."):
        st.session_state["chatbot_manager"] = initialize_embeddings()

# Sidebar
with st.sidebar:
    st.image("logo.png", width=300)  # Adjust the width as necessary
    st.markdown("### 🤖 XOAS: Your Personal Buddy 😊")
    st.markdown("---")
    menu = ["🤖 Chatbot", "📧 Contact"]
    choice = st.selectbox("Navigate", menu)

# Chatbot Page
if choice == "🤖 Chatbot":
    # Centered title
    st.markdown('<div class="centered-title">XOAS: Your Personal Buddy 😊</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Load chatbot doodle animation
    chatbot_doodle = load_lottie_file("Animation.json")  # Replace with your Lottie file path
    st_lottie(chatbot_doodle, height=150, key="chatbot_doodle")

    # Chat Interface
    if st.session_state["chatbot_manager"] is None:
        st.info("🤖 System is initializing. Please wait...")
    else:
        # Display chat messages
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        for msg in st.session_state["messages"]:
            role_class = "user" if msg["role"] == "user" else "assistant"
            st.chat_message(msg["role"]).markdown(msg["content"], unsafe_allow_html=True)

        # Input for user query
        user_input = st.chat_input("Chat with XOAS: Type your question here...")
        if user_input:
            # Display user message
            st.chat_message("user").markdown(f"<span class='white-text'>{user_input}</span>", unsafe_allow_html=True)
            st.session_state["messages"].append({"role": "user", "content": user_input})

            # Generate and display chatbot response
            with st.spinner("😊 Responding..."):
                try:
                    response = st.session_state["chatbot_manager"].get_response(user_input)
                    time.sleep(1)  # Simulate processing
                except Exception as e:
                    response = f"⚠️ Error: {e}"

            st.chat_message("assistant").markdown(f"<span class='white-text'>{response}</span>", unsafe_allow_html=True)
            st.session_state["messages"].append({"role": "assistant", "content": response})

# Contact Page
elif choice == "📧 Contact":
    st.title("📬 Contact Us")
    st.markdown("""
    We'd love to hear from you! Whether you have a question, feedback, or want to contribute, feel free to reach out.
    - **Email:** [info@developer.com](mailto:saqlainjuna@gmail.com)
    - **Email:** [saqlainjuna@gmail.com](mailto:saqlainjuna@gmail.com)

                
    """)
