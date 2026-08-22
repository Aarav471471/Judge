# Temporary RAG Bypass for Hackathon Speed

def retrieve_legal_context(query_text: str) -> str:
    """Mock retrieval function to bypass the 79MB download."""
    
    # We will just return a generic legal context for now so the AI still works
    return (
        "Under the Right to Information Act, 2005, citizens have the right to request "
        "information from any public authority. The authority must respond within 30 days."
    )