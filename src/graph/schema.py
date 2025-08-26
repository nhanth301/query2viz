from typing import TypedDict, List, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from typing import Optional

class GraphInput(TypedDict):
    messages: list[AnyMessage]

class GraphOutput(TypedDict):
    answer: str 
    code_result: str

class GraphState(TypedDict):
    messages: list[AnyMessage]
    sql_query: str
    sql_result: str 
    code_result: str 
    answer: str 


