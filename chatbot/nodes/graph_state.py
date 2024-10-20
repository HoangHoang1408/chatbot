import operator

from typing_extensions import Annotated, TypedDict


class InternalState(TypedDict):
    messages: Annotated[list, operator.add]
