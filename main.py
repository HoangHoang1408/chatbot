from langgraph.graph import END, START, StateGraph

from chatbot.custom_tools import get_current_weather
from chatbot.nodes import ChatBotNode, InternalState, ToolExecutionNode
from chatbot.utils import route_tools

tool_list = [get_current_weather]

graph_builder = StateGraph(InternalState)
graph_builder.add_node("chatbot", ChatBotNode(tool_list=tool_list))
graph_builder.add_edge(START, "chatbot")
graph_builder.add_node("tools", ToolExecutionNode(tool_list=tool_list))
graph_builder.add_conditional_edges(
    "chatbot", route_tools, {"tools": "tools", END: END}
)
graph_builder.add_edge("tools", "chatbot")
graph = graph_builder.compile()

for event in graph.stream(
    {"messages": [{"role": "user", "content": "how is the weather at new york?"}]}
):
    print(event)
