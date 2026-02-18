from typing import Optional, TypedDict , List
from langchain_core.messages import BaseMessage
from typing_extensions import Annotated, Sequence
from langgraph.graph.message import add_messages
from pydantic import BaseModel

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage] , add_messages]

class SupervisorSchema(BaseModel):
    final_report : str
    final_evaluation : str

class PlannerOutputSchema(BaseModel):
    plan : List[dict]

class SynthesisOutputSchema(BaseModel):
    answer : str
    references : Optional[List[dict]]

class EvaluationOutputSchema(BaseModel):
    evaluation : dict

    