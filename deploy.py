import os
import time
import streamlit as st
import pdfplumber
from pinecone import Pinecone
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from huggingface_hub import login
from requests.exceptions import HTTPError

# ------------------------------
# Configuration & Authentication
# ------------------------------

# Access API keys from Streamlit's secrets
genai_api_key = st.secrets["GENAI_API_KEY"]
pinecone_api_key = st.secrets["PINECONE_API_KEY"]
hf_api_token = st.secrets["HF_API_TOKEN"]  # Add your Hugging Face API token here

# Optional: If you need to run in offline mode, uncomment the next line.
# os.environ["TRANSFORMERS_OFFLINE"] = "1"

# Authenticate with Hugging Face to mitigate rate limiting
login(token=hf_api_token)

# Configure Generative AI and Pinecone with secure keys
genai.configure(api_key=genai_api_key)
pc = Pinecone(api_key=pinecone_api_key)

# Replace with your actual index name
index_name = "multilingual-e5-large"
index = pc.Index(index_name)

# ------------------------------
# Load Sentence Transformer with Exponential Backoff
# ------------------------------

def load_model_with_retries(model_name, retries=5):
    for i in range(retries):
        try:
            # Pass the authentication token to the SentenceTransformer
            embedder = SentenceTransformer(model_name, use_auth_token=hf_api_token)
            return embedder
        except HTTPError as e:
            if e.response is not None and e.response.status_code == 429:
                wait_time = 2 ** i  # Exponential backoff: 1, 2, 4, 8, ...
                st.warning(f"Rate limited by Hugging Face API. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e
    raise Exception("Failed to load the model after several retries.")

# Load the sentence transformer model for embedding.
model_name = 'sentence-transformers/all-mpnet-base-v2'
embedder = load_model_with_retries(model_name)

# ------------------------------
# Utility Functions
# ------------------------------

def extract_text_from_pdf(pdf_file):
    """Extract text from each page of a PDF file using pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def store_document_in_pinecone(doc_text):
    """Split document text into sentences, get embeddings, and upsert into Pinecone."""
    # Split text into smaller chunks for embedding
    sentences = doc_text.split('. ')
    embeddings = embedder.encode(sentences)
    
    # Store in Pinecone: each sentence is indexed separately
    for i, emb in enumerate(embeddings):
        index.upsert([(f"sentence-{i}", emb, {'text': sentences[i]})])

def retrieve_relevant_chunks(query, top_k=5):
    """Retrieve the most relevant text chunks from Pinecone based on the query."""
    query_embedding = embedder.encode([query])
    results = index.query(vector=query_embedding.tolist(), top_k=top_k, include_metadata=True)
    relevant_chunks = [match['metadata']['text'] for match in results.get('matches', [])]
    return " ".join(relevant_chunks)

def summarize_text(text):
    """Generate a summary of the provided text using Gemini-pro API."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([f"Please summarize the following text:\n\n{text}"])
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

def question_text(retrieved_text, question):
    """Answer a question based on the retrieved text using Gemini-pro API."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([
            f"Answer the following question based on the provided text:\n\nText: {retrieved_text}\n\nQuestion: {question}"
        ])
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# ------------------------------
# Streamlit App
# ------------------------------

def main():
    st.title("RAG-based PDF QA Bot with Gemini-pro")
    
    # Upload a PDF file
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        text = extract_text_from_pdf(uploaded_file)
        
        # Store the document embeddings in Pinecone
        store_document_in_pinecone(text)
        
        # Display the extracted text (first 500 characters)
        display_text = text[:500] + ('...' if len(text) > 500 else '')
        st.subheader("Extracted Text")
        st.text_area("Text from PDF", display_text, height=300)

        # Get a summary of the text
        if st.button("Get Summary"):
            summary = summarize_text(text)
            st.subheader("Summary")
            st.write(summary)

        # Provide an interface to ask a question
        question = st.text_input("Enter your question about the text")
        if st.button("Get Answer"):
            if question:
                # Retrieve relevant chunks from Pinecone based on the question
                relevant_text = retrieve_relevant_chunks(question)
                
                # Get the answer from Gemini-pro using the retrieved text
                answer = question_text(relevant_text, question)
                
                st.subheader("Retrieved Text")
                st.write(relevant_text)
                
                st.subheader("Answer")
                st.write(answer)
            else:
                st.warning("Please enter a question to get an answer.")

if __name__ == "__main__":
    main()
