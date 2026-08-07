# travel-knowledge-mcp-server Handbook

## Universal Rules
- **Git Push Approval Rule**: NEVER run `git push` automatically. Always present implemented changes and unit test verification results, and wait for explicit user confirmation before executing any `git push` command.
- **Python Virtualenv Path**: All unit tests must be executed using:
  `/Users/gnanesh_arva/Downloads/travel-planner-v2/travel-agent-service/.venv/bin/pytest`

## Repository Standards
- **Port**: `8003` (Default)
- **Role**: FastMCP Knowledge RAG Server providing destination guides, MMR re-ranking, token context compression, and citation linking.

## Relevant Task Playbooks (`skills/`)
- `mcp-tools-management`: FastMCP tool execution, memory, and knowledge server operations.
