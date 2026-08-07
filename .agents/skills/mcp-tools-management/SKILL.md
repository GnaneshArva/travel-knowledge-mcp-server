---
name: mcp-tools-management
description: Operational playbook for managing FastMCP tools, memory, knowledge servers, circuit breakers, and pagination.
---

# FastMCP Tools Operational Playbook

This skill provides procedures for running and maintaining Model Context Protocol (MCP) servers in `travel-mcp-server`, `travel-memory-mcp-server`, and `travel-knowledge-mcp-server`.

## MCP Servers Overview

1. **`travel-mcp-server` (Port 8001)**:
   - Provides `search_flights`, `search_hotels`, `get_weather` tools via FastMCP.
   - Protected by `ToolCircuitBreaker` state machine (`CLOSED`, `OPEN`, `HALF-OPEN`).
   - Supports cursor & offset result pagination via `ToolResultPaginator`.

2. **`travel-memory-mcp-server` (Port 8002)**:
   - Provides user preference memory store and conversation history retrieval.
   - `HybridMemoryRetriever`: Combines BM25 keyword matching with Vector embedding search.

3. **`travel-knowledge-mcp-server` (Port 8003)**:
   - Provides RAG destination guide searches.
   - `MMRReranker`: Maximal Marginal Relevance diversity re-ranking.
