import chromadb

# Initialize local vector database
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="rti_laws")

def retrieve_legal_context(query: str) -> str:
    """Queries ChromaDB for relevant legal acts based on user complaint."""
    results = collection.query(
        query_texts=[query],
        n_results=2 # Fetch top 2 most relevant document chunks
    )
    if not results["documents"]:
        return "No relevant legal context found."
    
    return "\n".join(results["documents"][0])