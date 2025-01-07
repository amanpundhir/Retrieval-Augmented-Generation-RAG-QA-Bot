# Retrieval-Augmented Generation (RAG) QA Bot

This project implements a **Retrieval-Augmented Generation (RAG)** model for a Question Answering (QA) bot. The bot allows users to upload PDF documents, ask questions, and receive coherent, contextually relevant answers using both retrieval from the document and generative AI models.

## Project Overview

The project has two main components:

1. **RAG Model for Question Answering**:
   - The backend utilizes **Pinecone** as a vector database for storing document embeddings.
   - A generative model from **Google's Generative AI** is used to generate coherent responses based on the retrieved document information.
   
2. **Interactive QA Bot Interface**:
   - The frontend is built using **Streamlit**, allowing users to upload PDF files, ask questions, and view the bot's responses in real time.
   - The bot retrieves the most relevant document segments from the vector database and generates a response.
   
You can test the deployed version of the app [here](https://retrieval-augmented-generation-rag-app-bot-jamvhl5p9kkp4eexk9b.streamlit.app/).

---

## Features

- Upload PDF documents for processing.
- Ask questions based on the document content.
- Real-time retrieval of relevant document segments using **Pinecone**.
- Generative answers using **Google's Generative AI** model.
- Fully containerized with Docker for easy deployment.

---

## Setup Instructions


## Running the Application Locally
- Clone the repository:

```bash

git clone https://github.com/amanpundhir/genai_assessment.git
```
```bash
cd genai_assessment
```
## Requirements

To run this project locally, you'll need to install the required Python packages. The dependencies are listed in the `requirements.txt` file.

```bash
pip install -r requirements.txt
```
## Configuration

Before running the application, you'll need to configure your API keys. The application uses the following APIs:

- **Pinecone**: For vector database functionalities.
- **Google's Generative AI**: For generating responses to queries.

### Steps to get your FREE api keys & Replace API Keys:

1. **Obtain Your API Keys**:
   - **Pinecone API Key**:
     - Sign up at [Pinecone](https://www.pinecone.io/) and create a new project.
     - Once your project is created, navigate to the API keys section in your dashboard to find your API key.

   - **Google Generative AI API Key**:
     - Go to the [Google Gen AI Studio](https://cloud.google.com/generative-ai).
     - Sign in with your Google account and create a new project.
     - Once your project is set up, you will receive your API key directly in the studio interface.
     - Copy the API key provided for use in your application.

2. **Update Your API Keys in the Code**:
   - Open the `app.py` file in your project directory.
   - Locate the lines where the API keys are defined. They will look something like this:

   ```python
   PINECONE_API_KEY = "your_pinecone_api_key"
   GOOGLE_API_KEY = "your_google_api_key"
   ```
   - Update them with you api keys

## Pinecone Index Configuration

To use the Pinecone vector database, you'll need to create an index with the following specifications:

### Steps to Create a Pinecone Index:

1. **Sign in to your Pinecone account** at [Pinecone](https://www.pinecone.io/).
2. **Create a new index** with the following parameters:
   - **Index Name**: Choose a name for your index (e.g., `multilingual-e5-large`).
   - **Metric**: `cosine`
   - **Dimensions**: `768`
   - **Type**: `Serverless`
   - **Cloud**: `AWS`
   - **AWS Region**: `us-east-1`

3. Once the index is created, note the index name and other configuration details.

### Updating the Code

After creating your Pinecone index, you need to update the `app.py` file to reflect the new index name.

1. Open the `app.py` file in your project directory.
2. Locate the section where the index is defined. It will look similar to this:

   ```python
   index_name = "multilingual-e5-large"  # Replace with your actual index name
   index = pc.Index("multilingual-e5-large")  # Replace with your actual index name

## Docker Deployment
- This project is fully containerized. You can use the Dockerfile to build and run the application in a Docker container

## Run the Docker container:

```bash
docker build -t streamlit-qa-bot .
docker run -p 8501:8501 streamlit-qa-bot
```
## Access the app:

- The app will be available at http://localhost:8501 in your browser.
---

## Troubleshooting

If you encounter issues when running the Docker container, here is the error I got and its solution:

### **Error: Container not running**
If you receive an error indicating that the container is not running, ensure that you have successfully built the image before running it. You can check the status of your containers with:

```bash
docker ps 
```
- If you get the output like this :
```bash
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```
- It means the container is not working
- To fix this run this command :
```bash
docker start container id   # replace 'container id' with your container id which can be found in your docker container it should look somethig like this : 688decb3cc74

```
- Verify if the Container is Running After starting, check if the container is running by running the docker ps command again:

```bash
docker ps
```
- Now you should get the output like this :
```bash
CONTAINER ID   IMAGE              COMMAND                  CREATED             STATUS          PORTS                    NAMES
688decb3cc74   streamlit-qa-bot   "streamlit run app.p…"   About an hour ago   Up 22 seconds   0.0.0.0:8501->8501/tcp   zen_tu
```
- Your container is now running, and the port 8501 is mapped correctly. You should be able to access the Streamlit app at:

```bash
http://localhost:8501
```
- Open this URL in your browser, and the app should be displayed.

---

## How the System Works
- Document Upload: Users upload PDF documents via the Streamlit interface.
- Embedding Creation: The content of the document is transformed into embeddings using Sentence Transformers and stored in Pinecone, a vector database.
- Query Handling: When a user asks a question, the bot retrieves the most relevant sections from the document using similarity search on the embeddings.
- Answer Generation: The bot then uses Google's Generative AI to generate a coherent response based on the retrieved segments.
---


### Developed by Amankumar Pundhir 
### Contact :[Email Me](https://mail.google.com/mail/?view=cm&fs=1&to=amanpundhir2003@gmail.com)

