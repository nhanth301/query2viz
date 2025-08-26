from src.graph.nodes import sql_node, code_node
from langgraph.graph import StateGraph, END, START 
from src.graph.schema import GraphInput, GraphOutput, GraphState

def build():
    graph = StateGraph(GraphState, input_schema=GraphInput, output_schema=GraphOutput)
    graph.add_node('sql',sql_node)
    graph.add_node('code',code_node)
    graph.add_edge(START,'sql')
    graph.add_edge('sql','code')
    graph.add_edge('code',END)
    graph = graph.compile()
    return graph 