# AI Workflow Engine – Summarization Workflow (Assignment Implementation)

This repository contains a minimal **AI Workflow / Graph Engine** implemented using **Python + FastAPI**.

It is designed to satisfy the core requirements of the **AI Engineering Intern – Agentic Workflows** assignment:

- Represent workflows as a **graph** of nodes.
- Each node maps to a **tool** (Python function).
- A shared, mutable **state** dictionary is passed between nodes.
- Support for **sequential execution**, **branching**, and **looping**.
- Expose the engine over a **REST API**.

I have implemented **Case Study Option B – “Summarization + Refinement Workflow”** using this engine.

---

## 🔧 High-Level Design

### 1. Core Ideas

- **State**  
  A simple Python `dict` that carries all data across the workflow.
  Example (Option B):

  ```python
  {
    "text": "long input text...",
    "chunks": [],
    "summaries": [],
    "final_summary": "",
    "chunk_size": 200,
    "max_words_per_chunk": 30,
    "max_length": 100
  }
