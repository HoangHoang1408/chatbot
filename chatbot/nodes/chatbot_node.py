import json

from ..utils.together_get_completion import get_completion
from .graph_state import InternalState


def parse_chatbot_response(response):
    def try_parse_json(response):
        first = response.find("{")
        last = response.rfind("}")
        return json.loads(response[first : last + 1])

    message = {"role": "assistant"}
    try:
        function = try_parse_json(response)
        function["arguments"] = function["parameters"]
        del function["parameters"]
        message["tool_calls"] = [
            {
                "type": "function",
                "function": function,
            }
        ]
    except:
        message["content"] = response
    return {"messages": [message]}


class ChatBotNode:
    def __init__(self, tool_list):
        self.tool_list = tool_list

    def __call__(self, state: InternalState):
        response = get_completion(state["messages"], self.tool_list or None)
        return parse_chatbot_response(response)
