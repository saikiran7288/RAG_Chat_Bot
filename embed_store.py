import chromadb
from sentence_transformers import SentenceTransformer

def create_vector_store(chunks):
    chroma_client = chromadb.Client()
    
    try:
        collection = chroma_client.get_collection(name="rag_docs")
        print("Using existing collection: rag_docs")
    except Exception:
        collection = chroma_client.create_collection(name="rag_docs")
        print("Created new collection: rag_docs")
    
    if collection.get()["ids"]:
        collection.delete(ids=collection.get()["ids"])
        print("Cleared existing data in collection.")
    
    model = SentenceTransformer("sentence-transformers/multi-qa-MiniLM-L6-cos-v1")
    embeddings = model.encode(chunks)
    
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            documents=[chunk],
            embeddings=[embedding.tolist()],
            ids=[f"chunk_{i}"]
        )
    
    print(f"Stored {len(chunks)} chunks in ChromaDB.")
    return collection
