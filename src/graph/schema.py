from typing import TypedDict, List

class GraphInput(TypedDict):
    query: str 

class GraphOutput(TypedDict):
    answer: str 

class GraphState(TypedDict):
    query: str 
    data: str 
    answer: str 