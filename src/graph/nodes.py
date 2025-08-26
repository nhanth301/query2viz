from src.agent.code_agent import PythonDashboardEngine
from src.agent.sql_agent import SQLQueryEngine
from langchain_community.utilities import SQLDatabase
from src.graph.schema import GraphInput, GraphOutput, GraphState
from langchain.prompts import PromptTemplate
from src.graph.prompt import SUMMARIZE_PROMPT, ANWSWER_PROMPT
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
import json
load_dotenv()

sql_db = SQLDatabase.from_uri("mysql+pymysql://root:123456@localhost:3306/ecommerce")
sql_agent = SQLQueryEngine('gpt-4o-mini',sql_db)
code_agent = PythonDashboardEngine('gpt-4o-mini')
llm = ChatOpenAI(model='gpt-4o-mini',temperature=0)
creative_llm = ChatOpenAI(model='gpt-4o-mini',temperature=1.2)

def greeting(state: GraphInput) -> GraphState:
    prompt = PromptTemplate(
        template=SUMMARIZE_PROMPT,
        input_variables=["history", "user_input"]
    )
    user_input = state['messages'][-1]
    history = state['messages'][-5:-1]
    chain = LLMChain(llm=llm, prompt=prompt)
    output = chain.run(history=history, user_input=user_input)
    result = json.loads(output)
    print("="*10)
    print(result)
    print("="*10)
    if 'question' in result:
        return {'sql_query': result['question'], 'answer': None}
    else:
        return {'sql_query': None, 'answer': result['ask']}
    
def router(state: GraphState) -> GraphState:
    if state['sql_query']:
        return 'sql'
    else:
        return 'end'
        
    

def sql_node(state: GraphState) -> GraphState:
    output = sql_agent.get_query_data(state['sql_query'])
    return {'sql_result': output}

def code_node(state: GraphState) -> GraphState:
    output = code_agent.get_output(state['sql_result'])
    return {'code_result': output}

def answer_node(state: GraphState) -> GraphOutput:
    prompt = PromptTemplate(
        template=ANWSWER_PROMPT,
        input_variables=["user_query", "sql_result"]
    )
    chain = LLMChain(llm=creative_llm, prompt=prompt)
    output = chain.run(user_query=state['sql_query'],sql_result=state['sql_result'])
    return {'answer': output, 'code_result': state['code_result']}

