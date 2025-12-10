import uuid
from typing import Dict, Any, List

from .models import GraphConfig, RunLogEntry
from .tools import TOOL_REGISTRY


class RunResult:
    """
    Internal object used by the engine to return results.
    """
    def __init__(self, run_id: str, final_state: Dict[str, Any], log: List[Dict[str, Any]]):
        self.run_id = run_id
        self.final_state = final_state
        self.log = log


def run_graph(graph: GraphConfig, initial_state: Dict[str, Any]) -> RunResult:
    """
    Executes the graph starting from graph.start_node.
    Uses shared 'state' dict passed between nodes.
    Supports:
      - default edges (graph.edges)
      - branching/looping via state["next_node"] set by tools
    """
    run_id = str(uuid.uuid4())
    state: Dict[str, Any] = dict(initial_state)  # copy so we don't mutate caller's dict

    current_node_id = graph.start_node
    log: List[Dict[str, Any]] = []

    # Safety to avoid infinite loops
    max_steps = 100

    for step in range(max_steps):
        # Find the NodeConfig for the current node
        try:
            node = next(n for n in graph.nodes if n.id == current_node_id)
        except StopIteration:
            # Node id not found in graph.nodes -> stop
            break

        # Get the actual Python function for this node
        tool_fn = TOOL_REGISTRY.get(node.tool_name)
        if tool_fn is None:
            # Unknown tool -> stop
            break

        before = dict(state)  # snapshot before running
        state = tool_fn(state)  # run the tool
        after = dict(state)

        # Save log entry
        log.append({
            "step": step,
            "node": current_node_id,
            "tool": node.tool_name,
            "before": before,
            "after": after,
        })

        # Check if tool decided the next node dynamically
        next_node = state.pop("next_node", None)
        if next_node is not None:
            if next_node == "END":
                # End the graph
                break
            else:
                # Branch/loop to the given node id
                current_node_id = next_node
                continue

        # Otherwise follow default edge if exists
        if current_node_id in graph.edges:
            current_node_id = graph.edges[current_node_id]
        else:
            # No outgoing edge -> end of graph
            break

    return RunResult(run_id=run_id, final_state=state, log=log)
