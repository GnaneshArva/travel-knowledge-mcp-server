# Step-by-Step Execution Architecture (`travel-knowledge-mcp-server`)

## Purpose
`travel-knowledge-mcp-server` is an enterprise Model Context Protocol (MCP) server dedicated to vector-based Knowledge Retrieval (RAG). It exposes document search, travel guide retrieval, and visa/weather advisory queries over MCP to AI models and agents.

---

## Step-by-Step RAG Retrieval Flow

```
MCP Client ──► [1. Tool Invocation] ──► [2. Query Pre-Processing] ──► [3. Dense Embedding] ──► [4. ChromaDB Similarity Search] ──► [5. Reranking Strategy] ──► MCP Response
```

### Step 1: MCP Tool Invocation (`search_knowledge`)
- Receives `KnowledgeSearchRequest` DTO via MCP tool `search_knowledge` containing query text, destination filter, and top-k count.

### Step 2: Query Pre-Processing Strategy
- `QueryProcessingStrategy` cleans, normalizes, and expands query keywords.

### Step 3: Dense Embedding Computation
- `SentenceTransformerEmbeddingStrategy` generates vector embeddings for query text.

### Step 4: ChromaDB Similarity Vector Search
- `ChromaVectorStoreStrategy` performs cosine similarity search against persistent ChromaDB collections (created by `travel-knowledge-ingestion`).
- Retrieves top matching document chunks and metadata.

### Step 5: Cross-Encoder Reranking Strategy
- `RerankingStrategy` reranks candidate chunks to maximize semantic relevance to the prompt.

### Step 6: Response Assembly & Citation Building
- Assembles `KnowledgeSearchResponse` DTO containing context passages, similarity scores, and citation source IDs.
- Returns formatted payload to MCP agent.
