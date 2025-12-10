# AI Workflow Engine

A minimal workflow/graph engine built with **Python + FastAPI** for executing agent-like pipelines.  
The system models a workflow as a **graph of nodes**, where each node is a registered tool function, and a **shared mutable state** is passed between them.

This project implements **Case Study Option B – Summarization + Refinement**, where text is:
1. Split into chunks  
2. Summarized chunk-wise  
3. Merged  
4. Refined in a loop until it fits a target length  

The engine supports:
- Sequential flow (via edges)  
- Branching (via `state["next_node"]`)  
- Looping (repeat same node until condition satisfied)  
- Step-level logging (before/after state)  

Run the server:
```bash
uvicorn app.main:app --reload
