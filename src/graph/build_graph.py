from src.graph.nodes import sql_node, code_node, greeting, router, answer_node
from langgraph.graph import StateGraph, END, START 
from src.graph.schema import GraphInput, GraphOutput, GraphState
from langgraph.checkpoint.memory import MemorySaver

def build():
    memory = MemorySaver()
    graph = StateGraph(GraphState, input_schema=GraphInput, output_schema=GraphOutput)
    graph.add_node('sql',sql_node)
    graph.add_node('code',code_node)
    graph.add_node('greeting',greeting)
    graph.add_node('answer',answer_node)
    graph.add_edge(START,'greeting')
    graph.add_conditional_edges('greeting',router, {'sql': 'sql', 'end': END})
    graph.add_edge('sql','code')
    graph.add_edge('code','answer')
    graph.add_edge('answer',END)
    graph = graph.compile()
    return graph    