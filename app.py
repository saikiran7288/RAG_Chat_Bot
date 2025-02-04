from flask import Flask, render_template, request, jsonify
import pymysql
from rag_chatbot import RAGChatbot
from embed_store import create_vector_store
from data_preprocessing import chunk_pdf  # Ensure this is the correct import

# Initialize Flask app
app = Flask(__name__)

# MySQL connection function using PyMySQL
def create_db_connection():
    try:
        connection = pymysql.connect(
            host='localhost',
            database='rag_chatbot_db',
            user='root',
            password='enter your password'
        )
        print("Connected to MySQL")
        return connection
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None

# Function to store user question and bot response in MySQL
def store_question_response(connection, question, response):
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO chat_history (user_question, bot_response)
        VALUES (%s, %s)
        """
        values = (question, response)
        cursor.execute(query, values)
        connection.commit()
        print("Question and response stored in the database.")
    except pymysql.MySQLError as e:
        print(f"Error while inserting data: {e}")
        connection.rollback()

# Initialize RAG chatbot
def initialize_rag_bot():
    # Process the PDF and create chunks
    pdf_file = r"C:\Users\ksaik\OneDrive\Desktop\Rag_Chatbot\Data.pdf"
    chunks = chunk_pdf(pdf_file)
    if not chunks:
        raise ValueError("No text extracted from PDF - check your document")
    
    vector_store = create_vector_store(chunks)
    return RAGChatbot(vector_store)

rag_bot = initialize_rag_bot()

# Route to handle user input and provide response
@app.route('/')
@app.route('/')
def home():
    # Fetch previous chat history from MySQL
    connection = create_db_connection()
    chat_history = []
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT user_question, bot_response FROM chat_history ORDER BY id DESC LIMIT 10")
        chat_history = cursor.fetchall()
        connection.close()

    # Reverse chat history for correct order (oldest first)
    chat_history = chat_history[::-1]

    return render_template('index.html', chat_history=chat_history)



@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')  # Use JSON input
    
    # Get bot response from RAG chatbot
    bot_response = rag_bot.generate_response(user_question)
    
    # Store question and response in MySQL
    connection = create_db_connection()
    if connection:
        store_question_response(connection, user_question, bot_response)
        connection.close()
    
    return jsonify({'question': user_question, 'response': bot_response})

if __name__ == "__main__":
    app.run(debug=True)












