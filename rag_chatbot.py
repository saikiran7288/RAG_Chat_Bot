from transformers import pipeline, logging
import chromadb
from sentence_transformers import SentenceTransformer
from embed_store import create_vector_store
from  data_preprocessing import chunk_pdf , extract_text_from_pdf, clean_text
# Suppress unnecessary warnings
logging.set_verbosity_error()

class RAGChatbot:
    def __init__(self, vector_db):
        self.vector_db = vector_db
        self.llm = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",  # Use flan-t5-base for better performance
            device=-1,  # Force CPU usage
            max_length=300,  # Limit response length
            do_sample=True,  # Enable sampling for diverse responses
            temperature=0.7,  # Control randomness
            num_beams=3,  # Use beam search for better quality
            no_repeat_ngram_size=2  # Prevent repetition
        )
        self.embedding_model = SentenceTransformer(
            "sentence-transformers/multi-qa-MiniLM-L6-cos-v1",
            device="cpu"
        )

    def retrieve_chunks(self, query, top_k=5):
        """Retrieve relevant text chunks from vector DB"""
        try:
            query_embedding = self.embedding_model.encode(query).tolist()
            results = self.vector_db.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            print(f"Retrieval error: {str(e)}")
            return []

    def generate_response(self, query):
        """Generate final answer using retrieved context"""
        try:
            # Retrieve relevant chunks
            context_chunks = self.retrieve_chunks(query)
            
            if not context_chunks:
                return "No relevant information found in documents."
                
            # Combine chunks into context
            context = "\n".join([c for c in context_chunks if c.strip()])
            
            # Create LLM prompt
            prompt = f"""Answer the question in detail using ONLY this context. If unsure, say "I don't know".

            Context:
            {context}

            Question: {query}
            Answer in 3-5 sentences:"""
            
            # Generate response
            response = self.llm(prompt)[0]['generated_text']
            return response.strip()
            
        except Exception as e:
            print(f"Critical error: {str(e)}")
            return "Sorry, I encountered an error processing your request."

# Initialize the full pipeline
if __name__ == "__main__":

    pdf_file = r"C:\Users\ksaik\OneDrive\Desktop\Rag_Chatbot\Data.pdf"
    # 1. Process PDF and create vector store
    
    chunks = chunk_pdf(pdf_file)
    if not chunks:
        raise ValueError("No text extracted from PDF - check your document")
    
    vector_store = create_vector_store(chunks)
    
    # 2. Initialize RAG chatbot
    rag_bot = RAGChatbot(vector_store)
    
    # 3. Example usage
    query = input("Enter your question: ")
    response = rag_bot.generate_response(query)
    
    print("\n" + "="*50)
    print(f"Question: {query}")
    print(f"Answer: {response}")
    print("="*50 + "\n")