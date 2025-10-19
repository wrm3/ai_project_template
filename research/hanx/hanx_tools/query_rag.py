"""
Universal script to query our RAG system.
"""
from rag_utils import VectorStore, OpenAIRAGSystem
import argparse
import json

def query_rag(query, vector_store_path="./data/vector_store", top_k=3, format_json=False):
    """Query the RAG system.
    
    Args:
        query: The query string
        vector_store_path: Path to the vector store
        top_k: Number of documents to retrieve
        format_json: Whether to format the output as JSON
        
    Returns:
        The response from the RAG system
    """
    # Initialize vector store and RAG system
    vector_store = VectorStore(vector_store_path)
    rag = OpenAIRAGSystem(vector_store=vector_store, embedding_model=None, llm=None)
    
    # Query the RAG system
    print(f"Query: {query}")
    response = rag.query(query, top_k=top_k)
    
    if format_json:
        print(json.dumps(response, indent=2))
    else:
        print(f"\nResponse from RAG system:\n{response['response']}")
        
        # Print retrieved documents
        print("\nRetrieved documents:")
        for i, doc in enumerate(response['relevant_documents']):
            print(f"\nDocument {i+1}:")
            print(f"Source: {doc['metadata'].get('source', 'Unknown')}")
            print(f"Title: {doc['metadata'].get('title', 'Unknown')}")
            content_snippet = doc['content'][:150] + "..." if len(doc['content']) > 150 else doc['content']
            print(f"Content snippet: {content_snippet}")
    
    return response

def main():
    parser = argparse.ArgumentParser(description="Query the RAG system")
    parser.add_argument("query", help="The query string")
    parser.add_argument("--vector-store", default="./data/vector_store", help="Path to vector store")
    parser.add_argument("--top-k", type=int, default=3, help="Number of documents to retrieve")
    parser.add_argument("--json", action="store_true", help="Format output as JSON")
    
    args = parser.parse_args()
    
    return query_rag(
        query=args.query,
        vector_store_path=args.vector_store,
        top_k=args.top_k,
        format_json=args.json
    )

if __name__ == "__main__":
    main() 