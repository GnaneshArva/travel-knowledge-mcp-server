# Enterprise Travel Knowledge MCP Server (`travel-knowledge-mcp-server`)

An enterprise-grade Model Context Protocol (MCP) Server for Knowledge Retrieval (RAG) built with Python 3.12+, **FastMCP** (Official MCP SDK), Pydantic v2, and Clean Architecture principles.

---

## 📌 Project Overview

`travel-knowledge-mcp-server` serves as a dedicated Knowledge Retrieval microservice in the Travel Planner ecosystem. It exposes RAG capabilities over the Model Context Protocol (MCP) to AI models, LLM agents (such as OpenAI Agents SDK, Claude Desktop, or custom MCP clients), and external services.

> [!IMPORTANT]
> **Separation of Concerns**: This server is strictly responsible for **Knowledge Retrieval**. It does **NOT** ingest, chunk, embed, or mutate vector database collections. Document indexing and embedding pipeline ingestion are owned separately by `travel-knowledge-ingestion`.

---

## 🏗 Enterprise Architecture

This project is designed using **Clean Architecture** and SOLID design principles, emphasizing decoupling and extensibility over monolithic database queries.

```
                      travel-knowledge-ingestion
                                  │
                                  ▼
                         ChromaDB Persistent Store
                                  ▲
                                  │
                     travel-knowledge-mcp-server
                                  │
                                  ▼
                        MCP Clients / AI Agents
```

### High-Level Architectural Highlights:
1. **Clean Architecture Layering**: Strict boundary separating protocol handlers (MCP Tools/Resources/Prompts), Business Logic (`KnowledgeService`), Orchestration (`KnowledgeRetrievalPipeline`), and Infrastructure/Strategies.
2. **Strategy Pattern**: Interchangeable algorithms for Query Processing, Vector Storage, Retrieval Logic, Reranking, and Embedding Providers.
3. **Factory Pattern**: Runtime selection and instantiation of strategies driven by environment configuration without changing source code.
4. **Dependency Injection**: Centralized Composition Root (`app/container.py`) instantiates dependencies and injects them into pipeline and domain services.
5. **DTO Contracts**: Strong schema validation using Pydantic v2 for all MCP tool requests and responses.

---

## 📁 Directory Structure

```
travel-knowledge-mcp-server/
│
├── app/
│   ├── main.py                          # Application entry point & FastMCP server setup
│   ├── container.py                     # Dependency Injection Container & Composition Root
│   │
│   ├── config/                          # Configuration & Environment settings
│   │   ├── __init__.py
│   │   └── settings.py
│   │
│   ├── dto/                             # Pydantic v2 DTO contracts
│   │   ├── __init__.py
│   │   ├── request.py                   # KnowledgeSearchRequest
│   │   ├── document.py                  # RetrievedDocumentDto, CitationDto
│   │   └── response.py                  # KnowledgeSearchResponse, KnowledgeResultDto
│   │
│   ├── interfaces/                      # Strategy & Provider Abstract Base Classes
│   │   ├── __init__.py
│   │   ├── query_strategy.py            # QueryProcessingStrategy
│   │   ├── retrieval_strategy.py        # RetrievalStrategy
│   │   ├── vectorstore_strategy.py      # VectorStoreStrategy
│   │   ├── reranking_strategy.py        # RerankingStrategy
│   │   └── embedding_provider.py        # EmbeddingProvider
│   │
│   ├── strategies/                      # Pluggable concrete strategy implementations
│   │   ├── __init__.py
│   │   ├── query/
│   │   │   ├── __init__.py
│   │   │   └── default_query_strategy.py
│   │   ├── retrieval/
│   │   │   ├── __init__.py
│   │   │   └── vector_similarity_strategy.py
│   │   ├── vectorstore/
│   │   │   ├── __init__.py
│   │   │   └── chroma_vectorstore_strategy.py
│   │   └── reranking/
│   │       ├── __init__.py
│   │       └── no_op_reranking_strategy.py
│   │
│   ├── implementations/                 # External service & embedding implementations
│   │   ├── __init__.py
│   │   └── embedding/
│   │       ├── __init__.py
│   │       └── sentence_transformer_provider.py
│   │
│   ├── factories/                       # Strategy & Provider Factories
│   │   ├── __init__.py
│   │   ├── query_factory.py
│   │   ├── retrieval_factory.py
│   │   ├── vectorstore_factory.py
│   │   ├── reranking_factory.py
│   │   └── embedding_factory.py
│   │
│   ├── pipeline/                        # Modular RAG Retrieval Pipeline
│   │   ├── __init__.py
│   │   └── knowledge_pipeline.py
│   │
│   ├── services/                        # Domain Business Logic
│   │   ├── __init__.py
│   │   └── knowledge_service.py
│   │
│   ├── tools/                           # MCP Tools Layer
│   │   ├── __init__.py
│   │   └── knowledge_tools.py
│   │
│   ├── resources/                       # MCP Resources Layer
│   │   ├── __init__.py
│   │   └── knowledge_resources.py
│   │
│   ├── prompts/                         # MCP Prompt Templates Layer
│   │   ├── __init__.py
│   │   └── knowledge_prompts.py
│   │
│   └── utils/                           # Shared Utilities & Logger
│       ├── __init__.py
│       └── logger.py
│
├── pyproject.toml                       # Dependencies & Project Metadata (uv compatible)
├── README.md                            # Comprehensive Architectural Documentation
└── .env.example                         # Environment configuration sample
```

---

## 🔄 Knowledge Retrieval Pipeline

The retrieval workflow follows a stage-based pipeline pattern where each stage invokes independent strategies:

```
  User Query
      │
      ▼
┌───────────────────────────────────────┐
│ 1. Query Processing Strategy         │  --> Default, HyDE, Query Rewrite, Multi-Query
└───────────────────────────────────────┘
      │
      ▼
┌───────────────────────────────────────┐
│ 2. Embedding Provider                │  --> Sentence Transformers, OpenAI, Voyage, Gemini
└───────────────────────────────────────┘
      │
      ▼
┌───────────────────────────────────────┐
│ 3. Retrieval Strategy                 │  --> Vector Similarity, Hybrid Search, Parent-Doc
└───────────────────────────────────────┘
      │
      ▼
┌───────────────────────────────────────┐
│ 4. Vector Store Strategy              │  --> ChromaDB, Qdrant, Pinecone, PgVector
└───────────────────────────────────────┘
      │
      ▼
┌───────────────────────────────────────┐
│ 5. Reranking Strategy                 │  --> No-Op, Cross-Encoder, Cohere Rerank, RRF
└───────────────────────────────────────┘
      │
      ▼
┌───────────────────────────────────────┐
│ 6. Response DTO & Citations           │  --> KnowledgeSearchResponse DTO
└───────────────────────────────────────┘
```

---

## 🧩 Design Patterns & Extensibility

### 1. Strategy Pattern

Each core operational phase of RAG is defined as an abstract interface:

- **`QueryProcessingStrategy`**: Pre-processes and transforms queries.
  - *Implemented*: `DefaultQueryProcessingStrategy`
  - *Extensible for*: `HyDEStrategy`, `QueryRewriteStrategy`, `MultiQueryGenerationStrategy`, `QueryExpansionStrategy`
- **`EmbeddingProvider`**: Embeds text queries into vector space.
  - *Implemented*: `SentenceTransformerEmbeddingProvider` (`all-MiniLM-L6-v2`)
  - *Extensible for*: `OpenAIEmbeddingProvider`, `VoyageEmbeddingProvider`, `GeminiEmbeddingProvider`
- **`VectorStoreStrategy`**: Performs low-level vector queries against backend stores.
  - *Implemented*: `ChromaVectorStoreStrategy`
  - *Extensible for*: `PineconeVectorStoreStrategy`, `QdrantVectorStoreStrategy`, `PgVectorStrategy`, `WeaviateVectorStoreStrategy`
- **`RetrievalStrategy`**: High-level retrieval algorithm decoupled from vendor APIs.
  - *Implemented*: `VectorSimilarityRetrievalStrategy`
  - *Extensible for*: `HybridRetrievalStrategy`, `MetadataFilteredRetrievalStrategy`, `ParentDocumentRetrievalStrategy`, `GraphRetrievalStrategy`
- **`RerankingStrategy`**: Reranks retrieved candidate documents.
  - *Implemented*: `NoOpRerankingStrategy`
  - *Extensible for*: `CrossEncoderRerankingStrategy`, `CohereRerankingStrategy`, `VoyageRerankingStrategy`, `ReciprocalRankFusionStrategy`

### 2. Factory Pattern

Factories (`QueryStrategyFactory`, `VectorStoreFactory`, `RetrievalStrategyFactory`, `RerankingStrategyFactory`, `EmbeddingFactory`) select and instantiate concrete strategy objects at runtime based on environment configuration.

### 3. Dependency Injection

Centralized dependency wiring in `app/container.py` ensures that `KnowledgeService` and `KnowledgeRetrievalPipeline` do not hardcode dependencies, enabling effortless unit testing and strategy swapping.

---

## 🔌 MCP Layer Specifications

### 🛠 MCP Tools

This MCP server exposes three tools:

| Tool Name | Description | Parameters | Return Type |
|---|---|---|---|
| `search_country_information` | Retrieve destination information, attractions, and cultural guidance. | `query`: str, `country`: str (optional), `limit`: int | `KnowledgeSearchResponse` |
| `search_visa_requirements` | Retrieve visa rules, passport requirements, and entry conditions. | `query`: str, `country`: str (optional), `limit`: int | `KnowledgeSearchResponse` |
| `search_travel_guidelines` | Retrieve general travel advisories, health rules, and safety tips. | `query`: str, `category`: str (optional), `limit`: int | `KnowledgeSearchResponse` |

### 📦 MCP Resources

| Resource URI | Name | Description |
|---|---|---|
| `knowledge://categories` | `knowledge-categories` | JSON list of available knowledge categories indexed in ChromaDB. |
| `knowledge://countries` | `supported-countries` | JSON list of supported countries with knowledge entries. |
| `knowledge://version` | `knowledge-version` | Knowledge base version and vector store connection metadata. |

### 💬 MCP Prompt Templates

| Template Name | Arguments | Description |
|---|---|---|
| `destination-guide` | `destination`, `duration`, `interests` | Generates a prompt for synthesizing a custom itinerary using retrieved knowledge. |
| `visa-summary` | `origin_country`, `destination_country`, `passport_type` | Generates a prompt for structured visa and entry requirement analysis. |
| `travel-advisor` | `query`, `target_audience` | Generates a prompt for travel advisory and safety planning. |

---

## ⚙️ Configuration & Environment Variables

Copy `.env.example` to `.env` to customize runtime settings:

```env
# Server Settings
HOST=0.0.0.0
PORT=8000

# Strategy Selection
VECTOR_STORE=chroma
RETRIEVAL_STRATEGY=vector_similarity
QUERY_STRATEGY=default
RERANKING_STRATEGY=no_op
EMBEDDING_PROVIDER=sentence-transformers

# Model Parameters
EMBEDDING_MODEL=all-MiniLM-L6-v2
TOP_K=5

# ChromaDB Connection
CHROMA_COLLECTION=travel_knowledge
CHROMA_PERSIST_DIRECTORY=../travel-knowledge-ingestion/chroma
```

---

## 🚀 Running the Server

### Prerequisites

Ensure Python 3.12+ and `uv` package manager are installed.

```bash
# Install dependencies using uv
uv sync

# Run the MCP Server
uv run python app/main.py
```

---

## 🧪 Example Client Interaction & Request Flow

### End-to-End Sequence:

1. **MCP Client** calls tool `search_visa_requirements(query="Schengen visa requirements", country="France")`.
2. **`knowledge_tools.py`** invokes `KnowledgeService.search_visa_requirements(...)`.
3. **`KnowledgeService`** constructs `KnowledgeSearchRequest` DTO and forwards to `KnowledgeRetrievalPipeline`.
4. **`KnowledgeRetrievalPipeline`**:
   - Runs `DefaultQueryProcessingStrategy` -> `"Schengen visa requirements"`.
   - Runs `SentenceTransformerEmbeddingProvider` -> `[0.012, -0.045, ...]`.
   - Runs `VectorSimilarityRetrievalStrategy` -> calls `ChromaVectorStoreStrategy.search(...)`.
   - Executes metadata filter `{"country": "France", "category": "visa"}` against persistent ChromaDB.
   - Runs `NoOpRerankingStrategy`.
5. **Response DTO** (`KnowledgeSearchResponse`) containing retrieved document chunks, metadata, and citation details is returned over MCP protocol.

---

## 📄 License

MIT License. Designed for Enterprise MCP RAG Reference Architecture.