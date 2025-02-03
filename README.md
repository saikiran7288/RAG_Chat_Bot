🧠 Retrieval-Augmented Generation (RAG) Chatbot

 📌 Overview
 
  The RAG Chatbot is an AI-powered chatbot that combines retrieval-based search and language model generation to provide accurate and context-aware responses. It     utilizes vector embeddings to store and retrieve relevant information from a vector database and stores chat history in a MySQL database. The chatbot is a  
  accessible via a Flask API with endpoints for chatting and retrieving conversation history.

🚀 Features

  ✅ Retrieval-Augmented Generation (RAG) – Combines retrieval and generation for enhanced responses.
  ✅ Vector-Based Semantic Search – Stores and retrieves relevant text chunks using Faiss / ChromaDB.
  ✅ Chat History Management – Stores past conversations in MySQL.
  ✅ Flask API – Simple RESTful interface for communication.
  ✅ Modular Design – Clean and scalable structure for easy modifications.





📂 Project Structure

 


🛠️ Setup & Installation

1️⃣ create virtual Environment
  
    conda create -p venv python==3.8
    conda activate venv/

2️⃣ Install Dependencies

    pip install -r requirements.txt

3️⃣ Set Up MySQL Database

  Start MySQL Server.
  Create a database and tables using schema.sql.
  Update .env file with database credentials.

4️⃣ Run the Chatbot

  python rag_chatbot.py


🔌 API Endpoints

  Method	Endpoint	Description
  POST	/chat	Accepts a JSON query and returns a generated response.
  GET	/history	Retrieves chat history from MySQL.\

🧪 Example Usage


    Chat Request
    json
    
    POST /chat
    {
      "query": "What is retrieval-augmented generation?"
    }
    Chat Response
    json
    Copy
    Edit
    {
      "response": "Retrieval-Augmented Generation (RAG) is a hybrid AI approach...",
      "retrieved_chunks": ["RAG combines retrieval and generation..."]
    }

📚 Technologies Used


  Programming Language: Python
  Framework: Flask
  Vector Database: ChromaDB
  Embeddings: sentence-transformers
  Database: MySQL
  Language Model: OpenAI API 




docker build -t rag_chatbot .
docker run -p 5000:5000 rag_chatbot
📜 License
This project is open-source under the MIT License.
