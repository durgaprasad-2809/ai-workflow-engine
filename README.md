# AI Workflow Engine – Assignment Implementation

```python
"""
AI WORKFLOW ENGINE – IMPLEMENTATION DETAILS

This engine executes workflows defined as a graph of nodes.
Each node calls a registered tool function.
State is a shared mutable dictionary passed through tools.

Core Features Implemented:
--------------------------------
1. Tool Registry
2. Graph Execution Engine
3. Sequential Execution (via edges)
4. Branching (via state["next_node"])
5. Looping (via repeated next_node assignment)
6. Step Logging (before & after state snapshots)
7. REST API Endpoints (FastAPI)
8. Summarization Workflow (Option B)

Directory Structure:
--------------------------------
ai-workflow-engine/
├─ app/
│  ├─ __init__.py           # makes 'app' package importable
│  ├─ main.py               # FastAPI endpoints
│  ├─ models.py             # Graph, Node, Run models (Pydantic)
│  ├─ engine.py             # core graph execution engine
│  ├─ tools.py              # tool registry + summarization tools
│  ├─ storage.py            # in-memory graph + run storage
├─ examples/
│  ├─ summary_workflow.json # workflow definition for Option B
├─ requirements.txt          # dependencies
├─ README.md

------------------------------------------------------------------------------
TOOLS IMPLEMENTED (Option B)
------------------------------------------------------------------------------

@register_tool("split_text")
def split_text(state):
    """
    Splits input text into chunks.
    Inputs:
        state["text"]  – long string
        state["chunk_size"] – optional, default 200 chars
    Outputs:
        state["chunks"] – list of text chunks
    """

@register_tool("generate_summaries")
def generate_summaries(state):
    """
    Summarizes each chunk by taking the first N words.
    Inputs:
        state["chunks"]
        state["max_words_per_chunk"] – default 30
    Outputs:
        state["summaries"] – mini summaries list
    """

@register_tool("merge_summaries")
def merge_summaries(state):
    """
    merges all small summaries into a single summary.
    Output:
        state["final_summary"]
    """

@register_tool("refine_summary")
def refine_summary(state):
    """
    Trims final summary until it fits 'max_length' words.
    Demonstrates looping:
        if too long → state["next_node"] = "refine_summary_node"
        else → state["next_node"] = "END"
    Output:
        state["final_summary"]
    """

------------------------------------------------------------------------------
GRAPH EXECUTION ENGINE (engine.py)
------------------------------------------------------------------------------

def run_graph(graph, initial_state):
    """
    - Starts at graph.start_node
    - Executes the tool mapped to each node
    - Tracks before/after states in log
    - Uses state["next_node"] for branching OR follows graph.edges
    - Stops when:
        • "END" is encountered
        • no outgoing edge exists
        • max_steps exceeded
    Returns:
        run_id, final_state, detailed log
    """

------------------------------------------------------------------------------
FASTAPI ENDPOINTS IMPLEMENTED (main.py)
------------------------------------------------------------------------------

POST /graph/create
    - Stores graph definition in memory.

POST /graph/run
    - Executes a stored graph using given initial_state.
    - Returns:
        run_id,
        final_state,
        execution log (step-by-step)

GET /graph/state/{run_id}
    - Retrieves final state + log for any previous run.

------------------------------------------------------------------------------
EXAMPLE WORKFLOW JSON (summary_workflow.json)
------------------------------------------------------------------------------

{
  "id": "summary_workflow",
  "start_node": "split",
  "nodes": [
    { "id": "split", "tool_name": "split_text" },
    { "id": "summarize", "tool_name": "generate_summaries" },
    { "id": "merge", "tool_name": "merge_summaries" },
    { "id": "refine_summary_node", "tool_name": "refine_summary" }
  ],
  "edges": {
    "split": "summarize",
    "summarize": "merge",
    "merge": "refine_summary_node"
  }
}

------------------------------------------------------------------------------
RUN REQUEST EXAMPLE
------------------------------------------------------------------------------

{
  "graph_id": "summary_workflow",
  "initial_state": {
    "text": "Your long text goes here...",
    "chunk_size": 200,
    "max_words_per_chunk": 30,
    "max_length": 50
  }
}

------------------------------------------------------------------------------
RESULT
------------------------------------------------------------------------------
final_state:
    contains final refined summary
log:
    contains list of {step, node, tool, before, after}

------------------------------------------------------------------------------
HOW TO RUN LOCALLY
------------------------------------------------------------------------------

pip install -r requirements.txt
uvicorn app.main:app --reload

Open:
http://127.0.0.1:8000/docs

------------------------------------------------------------------------------
END OF IMPLEMENTATION NOTES
------------------------------------------------------------------------------
"""
