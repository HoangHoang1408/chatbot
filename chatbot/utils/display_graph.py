from io import BytesIO

from PIL import Image


def display_graph(graph):
    img = Image.open(BytesIO(graph.get_graph().draw_mermaid_png()))
    img.show()
