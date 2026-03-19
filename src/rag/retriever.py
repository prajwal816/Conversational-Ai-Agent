import logging
import numpy as np

logger = logging.getLogger(__name__)

# Try importing FAISS and Sentence Transformers
try:
    import faiss
    from sentence_transformers import SentenceTransformer
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("FAISS or sentence_transformers not installed. Using mocked RAG.")

class RAGRetriever:
    def __init__(self, config: dict):
        self.model_name = config.get("rag", {}).get("embedding_model", "all-MiniLM-L6-v2")
        self.top_k = config.get("rag", {}).get("top_k", 2)
        
        self.documents = [
            "Our return policy allows returns within 30 days of purchase.",
            "Technical support is available 24/7 at support@example.com.",
            "You can upgrade your subscription from the account dashboard.",
            "The Conversational AI agent supports less than 100ms latency.",
            "Streaming ASR chunks audio into 100ms fragments."
        ]
        
        if FAISS_AVAILABLE:
            logger.info(f"Loading embeddings model {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            self.dimension = self.model.get_sentence_embedding_dimension()
            self.index = faiss.IndexFlatL2(self.dimension)
            
            # Populate index
            embeddings = self.model.encode(self.documents)
            self.index.add(np.array(embeddings).astype('float32'))
        else:
            self.model = None
            self.index = None

    def retrieve(self, query: str) -> list[str]:
        if not FAISS_AVAILABLE:
            # Fallback to simulated RAG
            logger.debug(f"Mocking RAG retrieval for query: {query}")
            return self.documents[:self.top_k]
            
        # Actual FAISS retrieval
        query_vector = self.model.encode([query]).astype('float32')
        distances, indices = self.index.search(query_vector, self.top_k)
        
        results = []
        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])
        return results
