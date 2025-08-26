from src.agent.code_agent import PythonDashboardEngine
from src.agent.sql_agent import SQLQueryEngine
from langchain_community.utilities import SQLDatabase
from src.graph.schema import GraphInput, GraphOutput, GraphState
sql_db = SQLDatabase.from_uri("mysql+pymysql://root:123456@localhost:3306/ecommerce")

sql_agent = SQLQueryEngine('gpt-4o-mini',sql_db)
code_agent = PythonDashboardEngine('gpt-4o-mini')

def sql_node(state: GraphInput) -> GraphState:
    output = sql_agent.get_query_data(state['query'])
    return {'data': output}

def code_node(state: GraphState) -> GraphOutput:
    output = code_agent.get_output(state['data'])
    return {'answer': output}


