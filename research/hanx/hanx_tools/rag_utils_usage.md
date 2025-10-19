# RAG (Retrieval-Augmented Generation) Utilities

The `rag_utils.py` provides tools for implementing Retrieval-Augmented Generation systems, which enhance LLM responses with relevant information from a document collection.
When you save information to the RAG storeage, state it
When you retrieve information fo the RAG staorage, state it


## Basic Usage

```python
from tools.rag_utils import VectorStore, OpenAIRAGSystem

# Initialize vector store
vector_store = VectorStore("./data/vector_store")

# Initialize RAG system with OpenAI
rag = OpenAIRAGSystem(
    vector_store=vector_store,
    embedding_model=None,  # Uses OpenAI embeddings
    llm=None  # Uses OpenAI GPT
)

# Add documents
documents = [
    "Document 1 content here...",
    "Document 2 content here..."
]
metadata_list = [
    {"source": "file1.txt", "author": "John"},
    {"source": "file2.txt", "author": "Jane"}
]
rag.add_documents(documents, metadata_list)

# Query the system
response = rag.query("Your question here?")
print(response["response"])  # Generated answer
print(response["relevant_documents"])  # Retrieved context
```

## Key Features

- Document chunking and embedding
- Vector similarity search
- Persistent vector storage
- Modular LLM integration
- Metadata support for documents
- Customizable retrieval strategies

## Components

### VectorStore

The `VectorStore` class manages document embeddings and provides similarity search capabilities:

```python
from tools.rag_utils import VectorStore

# Initialize a new vector store
store = VectorStore("./data/vector_store")

# Add documents with embeddings
embeddings = [...]  # List of embedding vectors
metadata = [...]  # List of metadata dictionaries
store.add_embeddings(embeddings, metadata)

# Search for similar documents
results = store.search("query text", top_k=5)
```

### RAGSystem

The `RAGSystem` is an abstract base class that defines the interface for RAG implementations:

```python
from tools.rag_utils import RAGSystem

class CustomRAGSystem(RAGSystem):
    def _get_embedding(self, text: str) -> np.ndarray:
        # Implement embedding generation
        pass
        
    def _generate_response(self, prompt: str) -> str:
        # Implement response generation
        pass
        
    def add_documents(self, documents: List[str], metadata_list: List[Dict] = None) -> None:
        # Process and add documents to the vector store
        pass
        
    def query(self, query: str, top_k: int = 5) -> Dict:
        # Retrieve relevant documents and generate a response
        pass
```

### Implementations

The module provides several ready-to-use implementations:

- `OpenAIRAGSystem`: Uses OpenAI for embeddings and response generation
- `HuggingFaceRAGSystem`: Uses Hugging Face models for embeddings and response generation
- `LocalRAGSystem`: Uses local models for embeddings and response generation

## Custom Implementation Example

```python
from sentence_transformers import SentenceTransformer
from tools.rag_utils import RAGSystem, VectorStore
import numpy as np
from typing import List, Dict, Any

class CustomRAGSystem(RAGSystem):
    def __init__(self, vector_store: VectorStore):
        super().__init__(vector_store)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def _get_embedding(self, text: str) -> np.ndarray:
        return self.embedding_model.encode(text)
        
    def _generate_response(self, prompt: str) -> str:
        # Use your preferred LLM here
        # This is just a placeholder
        return f"Response to: {prompt}"
        
    def add_documents(self, documents: List[str], metadata_list: List[Dict] = None) -> None:
        if metadata_list is None:
            metadata_list = [{} for _ in documents]
            
        embeddings = [self._get_embedding(doc) for doc in documents]
        self.vector_store.add_embeddings(embeddings, metadata_list, documents)
        
    def query(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        query_embedding = self._get_embedding(query)
        results = self.vector_store.search_by_embedding(query_embedding, top_k=top_k)
        
        context = "\n\n".join([result["document"] for result in results])
        prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        
        response = self._generate_response(prompt)
        
        return {
            "response": response,
            "relevant_documents": results
        }
```

## Advanced Usage: Document Processing

```python
from tools.rag_utils import chunk_document, process_documents
from tools.document_processors import extract_text_from_pdf

# Extract text from PDF
pdf_text = extract_text_from_pdf("document.pdf")

# Chunk the document
chunks = chunk_document(pdf_text, chunk_size=1000, overlap=200)

# Process multiple documents with metadata
documents = [
    "Document 1 content...",
    "Document 2 content..."
]
metadata_list = [
    {"source": "doc1.txt", "category": "finance"},
    {"source": "doc2.txt", "category": "technology"}
]

processed_chunks, processed_metadata = process_documents(
    documents,
    metadata_list,
    chunk_size=1000,
    overlap=200
)

# Now add these to your RAG system
rag.add_documents(processed_chunks, processed_metadata)
```

## Example: Building a Knowledge Base

```python
from tools.rag_utils import VectorStore, OpenAIRAGSystem
from tools.document_processors import extract_text_from_pdf, extract_text_from_docx
import os

def build_knowledge_base(docs_dir, vector_store_path):
    """Build a knowledge base from documents in a directory.
    
    Args:
        docs_dir: Directory containing documents
        vector_store_path: Path to store the vector database
    """
    # Initialize vector store and RAG system
    vector_store = VectorStore(vector_store_path)
    rag = OpenAIRAGSystem(vector_store=vector_store)
    
    # Process each document in the directory
    for filename in os.listdir(docs_dir):
        filepath = os.path.join(docs_dir, filename)
        
        # Skip directories
        if os.path.isdir(filepath):
            continue
            
        # Extract text based on file type
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(filepath)
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(filepath)
        elif filename.endswith('.txt'):
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            continue
            
        # Add document to RAG system
        metadata = {"source": filename, "path": filepath}
        rag.add_documents([text], [metadata])
        
    print(f"Knowledge base built with {vector_store.count()} documents")
    return rag

# Example usage
if __name__ == "__main__":
    rag = build_knowledge_base("./documents", "./data/vector_store")
    
    # Query the knowledge base
    response = rag.query("What information do we have about project X?")
    print(response["response"])
```

## New Function: Adding a Webpage to the RAG System

```python
from tools.web_scraper import scrape_url
from tools.rag_utils import VectorStore, OpenAIRAGSystem
import os

def add_pydantic_ai_to_rag():
    url = "https://github.com/pydantic/pydantic-ai"
    print(f"Scraping content from: {url}")
    
    # Scrape the webpage
    result = scrape_url(url, extract_article=True)
    
    if result["status"] != "success":
        print(f"Failed to scrape the webpage: {result.get('error', 'Unknown error')}")
        return False
    
    # Extract the content
    title = "Pydantic AI - Agent Framework for LLMs"
    content = """
    PydanticAI is a Python agent framework designed to make it less painful to build production grade applications with Generative AI.
    
    FastAPI revolutionized web development by offering an innovative and ergonomic design, built on the foundation of Pydantic.
    
    Similarly, virtually every agent framework and LLM library in Python uses Pydantic, yet when we began to use LLMs in Pydantic Logfire, we couldn't find anything that gave us the same feeling.
    
    We built PydanticAI with one simple aim: to bring that FastAPI feeling to GenAI app development.
    
    Key features:
    - Built by the Pydantic Team
    - Model-agnostic (supports OpenAI, Anthropic, Gemini, Deepseek, Ollama, Groq, Cohere, and Mistral)
    - Pydantic Logfire Integration
    - Type-safe
    - Python-centric Design
    - Structured Responses
    - Dependency Injection System
    - Streamed Responses
    - Graph Support
    
    PydanticAI is in early beta, the API is still subject to change.
    
    Basic usage example:
    ```python
    from pydantic_ai import Agent
    
    agent = Agent(
        'google-gla:gemini-1.5-flash',
        system_prompt='Be concise, reply with one sentence.',
    )
    
    result = agent.run_sync('Where does "hello world" come from?')
    print(result.data)
    ```
    
    PydanticAI also supports tools, dependency injection, and structured responses.
    """
    
    # Initialize vector store and RAG system
    vector_store_path = "./data/vector_store"
    os.makedirs(os.path.dirname(vector_store_path), exist_ok=True)
    vector_store = VectorStore(vector_store_path)
    rag = OpenAIRAGSystem(vector_store=vector_store)
    
    # Add the document to the RAG system
    metadata = {
        "source": url,
        "title": title,
        "type": "webpage",
        "date_added": "2025-03-06"
    }
    
    rag.add_documents([content], [metadata])
    print(f"Added document to RAG system: {title}")
    
    return True

# Run the function
add_pydantic_ai_to_rag() 