# Agentic Research Assistant

## What this project is
- A multtiAgent orchestration (planner, synthesis, evaluator, supervisor) that build and validate research-style answers.
- Entrypoint: `app.py` which creates Agent instances, runs a planning→synthesis→evaluation workflow, writes outputs to `final_response.txt`/`final_response2.txt`, and logs per-agent outputs to `logs/`.

## High-level architecture
- `main/` — core agent wiring:
  - `agent.py` — Agent wrapper building langgraph StateGraph and invoking LLMs.
  - `model.py` — LLM factory (`get_llm`) using `langchain_openai.ChatOpenAI`.
  - `tools.py` — exposes LangChain-style tools that call services and other agents.
  - `config.py` — pydantic `Settings` reading `.env` for secrets.
- `services/` — concrete integrations and helpers (search, scraping, Qdrant, output validation, prompts).
- `scripts/` — ingestion/embedding helpers used by services.

## Quick run (development)
1. Create a virtual environment and activate it
2. Install dependencies (project has no `rqts.txt`; install required libraries used in code)
3. Create a `.env` file in the project root with these environment variables:

```
OPENAI_API_KEY=sk-...
EXA_API_KEY=...
qdrant_url=http://localhost:6333
```

4. Run the app ( run the ingestors inside the scripts if data is avaialble):

```powershell
python app.py
```

Outputs:
- `final_response.txt`, `final_response2.txt` contain the main outputs.
- `logs/` will include per-agent JSON outputs.