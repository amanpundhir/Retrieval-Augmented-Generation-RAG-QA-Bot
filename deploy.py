import streamlit as st
import pdfplumber
from pinecone import Pinecone
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

# Access API keys from Streamlit's secrets
genai_api_key = st.secrets["GENAI_API_KEY"]
pinecone_api_key = st.secrets["PINECONE_API_KEY"]

# Configure Generative AI and Pinecone with secure keys
genai.configure(api_key=genai_api_key)
pc = Pinecone(api_key=pinecone_api_key)

