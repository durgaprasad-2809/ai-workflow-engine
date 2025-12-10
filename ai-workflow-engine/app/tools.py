from typing import Callable, Dict, Any

# Registry: maps tool name -> Python function
TOOL_REGISTRY: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}


def register_tool(name: str):
    """
    Decorator to register a function as a tool in the registry.
    Each tool must take `state: dict` and return the updated state.
    """
    def decorator(func: Callable[[Dict[str, Any]], Dict[str, Any]]):
        TOOL_REGISTRY[name] = func
        return func
    return decorator


# ---------- Example / Debug Tool ----------

@register_tool("echo")
def echo_state(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simple tool for testing. Just sets 'echoed' to True.
    """
    state["echoed"] = True
    return state


# ---------- Option B: Summarization Workflow Tools ----------

@register_tool("split_text")
def split_text(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Splits the input text into chunks.
    Uses 'chunk_size' from state if present, else defaults to 200 characters.
    """
    text = state.get("text", "")
    chunk_size = int(state.get("chunk_size", 200))

    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    state["chunks"] = chunks
    return state


@register_tool("generate_summaries")
def generate_summaries(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    For each chunk, create a simple 'summary' by taking first N words.
    This is intentionally simple (no ML), as allowed by the assignment.
    """
    chunks = state.get("chunks", [])
    max_words_per_chunk = int(state.get("max_words_per_chunk", 30))

    summaries = []
    for chunk in chunks:
        words = chunk.split()
        small_summary = " ".join(words[:max_words_per_chunk])
        summaries.append(small_summary)

    state["summaries"] = summaries
    return state


@register_tool("merge_summaries")
def merge_summaries(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merges all small summaries into one large summary string.
    """
    summaries = state.get("summaries", [])
    final_summary = " ".join(summaries)
    state["final_summary"] = final_summary
    return state


@register_tool("refine_summary")
def refine_summary(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Refines/shortens the final summary until it fits within 'max_length' words.
    Demonstrates LOOPING: it may decide to:
      - loop back to the same node ("refine_summary_node"), or
      - end the graph by setting next_node = "END".
    """
    summary = state.get("final_summary", "")
    max_length = int(state.get("max_length", 100))

    words = summary.split()
    if len(words) > max_length:
        # Trim the summary
        trimmed = " ".join(words[:max_length])
        state["final_summary"] = trimmed
        # Tell the engine to loop on this same node again (if needed)
        state["next_node"] = "refine_summary_node"
    else:
        # We're done – signal the engine to end
        state["next_node"] = "END"

    return state
