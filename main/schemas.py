from typing import TypedDict , List
from langchain_core import BaseMessage
from typing_extensions import Annotated, Sequence
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage] , add_messages]
