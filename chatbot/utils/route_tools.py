from langgraph.graph import END

from ..nodes.graph_state import InternalState


def route_tools(state: InternalState):
    if messages := state.get("messages", []):
        message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(message, "tool_calls") and len(message["tool_calls"]) > 0:
        return "tools"
    return END
