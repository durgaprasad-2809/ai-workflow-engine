from typing import Dict, Any
from .models import GraphConfig, RunLogEntry

# All graphs stored here in memory: graph_id -> GraphConfig
GRAPHS: Dict[str, GraphConfig] = {}

# All run results stored here in memory: run_id -> {"state": ..., "log": [...]}
RUNS: Dict[str, Dict[str, Any]] = {}
