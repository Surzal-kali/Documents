import os
import ollama
from typing import List

try:
    import numpy as np
    from sentence_transformers import SentenceTransformer 
except ImportError as e:
    raise ImportError(
        "Missing dependencies. Run: pip install ollama numpy sentence-transformers"
    ) from e

class KnowledgeAssistant:
    """
    A minimalist RAG (Retrieval-Augmented Generation) system 
    designed for the MainGit toolkit to query local markdown notes.
    """
    def __init__(self, notes_path: str = "Documents/Exploit_Notes"):
        self.notes_path = notes_path
        # Using a small, high-performance model for embedding. 
        # This runs entirely on your machine.
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.index: List[str] = []
        self.metadata: List[str] = []
        self._initialized = False

    def initialize(self):
        """Crawls the Exploit_Notes directory and prepares the vector index."""
        if not os.path.exists(self.notes_path):
            print(f"Warning: Path {self.notes_path} not found.")
            return

        files = [f for f in os.listdir(self.notes_path) if f.endswith('.md')]
        
        for file_name in files:
            path = os.path.join(self.notes_path, file_name)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Basic chunking: if a note is very long, it could be split here.
                self.index.append(content)
                self.metadata.append(file_name)
        
        if self.index:
            # Convert text to vectors for similarity searching
            self.embeddings = self.embedder.encode(self.index)
            self._initialized = True
            print(f"Successfully indexed {len(self.index)} files from {self.notes_path}")

    def ask(self, query: str) -> str:
        """The primary method used in the REPL to query your notes."""
        if not self._initialized:
            self.initialize()

        # 1. Convert user query into a vector
        query_vec = self.embedder.encode([query])[0]

        # 2. Find top similarity indices using dot product
        # This finds the most relevant notes based on your question context
        if len(self.embeddings) > 0:
            similarities = np.dot(self.embeddings, query_vec)
            top_indices = np.argsort(similarities)[-3:][::-1] # Get top 3 chunks
        else:
            top_indices = []

        # 3. Collect relevant content (The "Retrieval" step)
        context_parts = []
        for idx in top_indices:
            source = self.metadata[idx]
            content = self.index[idx]
            context_parts.append(f"--- Source: {source} ---\n{content}")
        
        context_block = "\n\n".join(context_parts)

        # 4. Generate response via Ollama (The "Generation" step)
        # We use a system prompt to force the LLM to stay in 'Expert' mode.
        prompt = f"""You are an expert cybersecurity assistant helping a researcher using the MainGit toolkit.
Use the following excerpts from internal notes to answer the user request. 
If the information is not in the notes, tell them what you know generally but mention it isn't in your specific documentation.

CONTEXT FROM NOTES:
{context_block}

USER REQUEST: {query}

ANSWER:"""

        try:
            response = ollama.generate(model='llama3', prompt=prompt)
            return response['response']
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}. Ensure 'ollama serve' is running."

#this....this isn't necessary anymore. we can just have a single instance of this that the REPL calls. no need for a class method. i mean, open web ui synthesizes the collection, and i can point out exact books in visual studio code when we work here. 
_assistant = KnowledgeAssistant()

def ask_notes(query: str) -> str:
    """
    REPL command to query your local exploit notes and documentation
    via a local LLM instance.
    """
    return _assistant.ask(query)

