# Step-by-Step Execution Architecture (`travel-knowledge-mcp-server`)

## Purpose
`travel-knowledge-mcp-server` is an enterprise Model Context Protocol (MCP) server dedicated to vector-based Knowledge Retrieval (RAG). It exposes document search, travel guide retrieval, and visa/weather advisory queries over MCP to AI models and agents using 10 configurable RAG retrieval and query strategies.

---

## Step-by-Step RAG Retrieval Flow

```
MCP Client ──► [1. Tool Invocation] ──► [2. Query Strategy] ──► [3. Embedding Strategy] ──► [4. Retrieval Strategy] ──► [5. Reranking & Compression] ──► MCP Response
```

### Step 1: MCP Tool Invocation (`search_knowledge`)
- Receives `KnowledgeSearchRequest` DTO via FastMCP tool `search_knowledge` containing query text, destination filter, category, and limit.

### Step 2: Query Processing Strategy (`QueryStrategyFactory`)
Executes the configured query pre-processing strategy:
- **Default**: Normalizes and cleans whitespace.
- **`rewriting`** (`QueryRewritingStrategy`): Cleans text and expands domain synonyms (e.g. flight $\rightarrow$ airline, visa $\rightarrow$ entry requirements).
- **`hyde`** (`HyDEQueryStrategy`): Generates a hypothetical answer document for vector embedding matching.

### Step 3: Dense Vector Embedding Generation
- `EmbeddingFactory` invokes `SentenceTransformerEmbeddingStrategy` to generate vector embeddings for the query text.

### Step 4: Pluggable Retrieval Strategy Engine (`RetrievalStrategyFactory`)
Executes the configured retrieval strategy against ChromaDB vector storage:
- **`vector_similarity` / `semantic`** (`VectorSimilarityRetrievalStrategy`): Standard dense vector similarity search.
- **`hybrid`** (`HybridRetrievalStrategy`): Combines BM25 lexical keyword search + dense vector search via Reciprocal Rank Fusion (RRF).
- **`metadata`** (`MetadataFilteringRetrievalStrategy`): Enforces strict metadata pre-filtering (country, category, dates).
- **`multi_query`** (`MultiQueryRetrievalStrategy`): Generates query variations, searches candidates across all variations, and deduplicates.
- **`parent_child`** (`ParentChildRetrievalStrategy`): Searches granular child vector chunks, but resolves parent document content.
- **`compression`** (`ContextualCompressionRetrievalStrategy`): Trims and extracts relevant sentences from chunks to reduce prompt noise.
- **`agentic`** (`AgenticRetrievalStrategy`): Adaptive multi-step search that relaxes metadata filters if initial candidate yield is low.

### Step 5: Post-Processing & Reranking (`RerankingStrategyFactory`)
- `RerankingStrategy` executes cross-encoder relevance re-ordering over candidate chunks.

### Step 6: Response Assembly & Citation Building
- Assembles `KnowledgeSearchResponse` DTO containing context passages, similarity scores, and citation source IDs.
- Returns formatted payload to MCP client/agent.
