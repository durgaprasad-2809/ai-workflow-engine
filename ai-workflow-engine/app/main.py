from fastapi import FastAPI, HTTPException
from typing import Dict, Any, List

from .models import (
    GraphConfig,
    RunRequest,
    RunLogEntry,
    RunResponse,
    GraphCreateResponse,
    StateResponse,
)
from .engine import run_graph
from .storage import GRAPHS, RUNS

app = FastAPI(title="AI Workflow Engine", version="1.0.0")


@app.get("/")
def root():
    return {"message": "AI Workflow Engine is running"}


# ---------- Graph Endpoints ----------

@app.post("/graph/create", response_model=GraphCreateResponse)
def create_graph(graph: GraphConfig):
    """
    Creates or overwrites a graph in in-memory storage.
    """
    GRAPHS[graph.id] = graph
    return GraphCreateResponse(
        graph_id=graph.id,
        message="Graph created/updated successfully.",
    )


@app.post("/graph/run", response_model=RunResponse)
def run_graph_endpoint(req: RunRequest):
    """
    Runs a stored graph with the provided initial_state.
    """
    graph = GRAPHS.get(req.graph_id)
    if graph is None:
        raise HTTPException(status_code=404, detail="Graph not found")

    result = run_graph(graph, req.initial_state)

    # Convert raw log dicts to RunLogEntry for response model
    log_entries: List[RunLogEntry] = [
        RunLogEntry(**entry) for entry in result.log
    ]

    RUNS[result.run_id] = {
        "state": result.final_state,
        "log": log_entries,
    }

    return RunResponse(
        run_id=result.run_id,
        final_state=result.final_state,
        log=log_entries,
    )


@app.get("/graph/state/{run_id}", response_model=StateResponse)
def get_state(run_id: str):
    """
    Returns the final state and log for a given run_id.
    """
    run = RUNS.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="run_id not found")

    return StateResponse(
        run_id=run_id,
        state=run["state"],
        log=run["log"],
    )
