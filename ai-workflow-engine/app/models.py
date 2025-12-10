from pydantic import BaseModel
from typing import Dict, List, Any, Optional


class NodeConfig(BaseModel):
    """
    A single node in the graph.
    - id: unique identifier inside this graph (e.g., "split", "summarize")
    - tool_name: name of the tool in TOOL_REGISTRY
    """
    id: str
    tool_name: str


class GraphConfig(BaseModel):
    """
    Represents the whole graph / workflow.
    - id: graph identifier
    - nodes: list of NodeConfig
    - edges: mapping from node_id -> next node_id (default transitions)
    - start_node: node_id to start execution from
    """
    id: str
    nodes: List[NodeConfig]
    edges: Dict[str, str]
    start_node: str


class RunRequest(BaseModel):
    """
    Input body for /graph/run endpoint.
    """
    graph_id: str
    initial_state: Dict[str, Any]


class RunLogEntry(BaseModel):
    """
    For returning logs of each step.
    """
    step: int
    node: str
    tool: str
    before: Dict[str, Any]
    after: Dict[str, Any]


class RunResponse(BaseModel):
    """
    Response for /graph/run.
    """
    run_id: str
    final_state: Dict[str, Any]
    log: List[RunLogEntry]


class GraphCreateResponse(BaseModel):
    """
    Response for /graph/create.
    """
    graph_id: str
    message: str


class StateResponse(BaseModel):
    """
    Response for /graph/state/{run_id}.
    """
    run_id: str
    state: Dict[str, Any]
    log: List[RunLogEntry]
