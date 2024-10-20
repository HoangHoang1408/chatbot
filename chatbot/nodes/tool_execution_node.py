from .graph_state import InternalState


class ToolExecutionNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tool_list: list) -> None:
        self.tools_by_name = {tool.__name__: tool for tool in tool_list}

    def __call__(self, state: InternalState):
        print("hellohello")
        print(state)
        if messages := state.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        messages = []
        for tool_call in message["tool_calls"]:
            tool_name = tool_call["function"]["name"]
            excution_result = self.tools_by_name[tool_name](
                **tool_call["function"]["arguments"]
            )
            message = {"role": "tool", "name": tool_name, "content": excution_result}
            messages.append(message)
        return {"messages": messages}
