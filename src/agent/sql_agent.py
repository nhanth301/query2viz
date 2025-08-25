from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain_core.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.prompt import SQL_FUNCTIONS_SUFFIX
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
load_dotenv()

sql_db = SQLDatabase.from_uri("mysql+pymysql://root:123456@localhost:3306/ecommerce")

class SQLQueryEngine:
    """
    A class representing an SQL query engine.

    Attributes:
        llm (ChatOpenAI): An instance of ChatOpenAI used for natural language processing.
        toolkit (SQLDatabaseToolkit): An SQL database toolkit instance.
        context (dict): Contextual information obtained from the SQL database toolkit.
        tools (list): List of tools available for SQL query execution.
        prompt (ChatPromptTemplate): The prompt used for interactions with the SQL query engine.
        agent_executor (AgentExecutor): An executor for the SQL query engine's agent.
    """
    def __init__(self, model_name, db):
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.toolkit = SQLDatabaseToolkit(db=db, llm=self.llm)
        self.context = self.toolkit.get_context()
        self.tools = self.toolkit.get_tools()
        self.prompt = None
        self.agent_executor = None
        self.set_prompt()
        self.initialize_agent()
        
    def set_prompt(self):
        messages = [
            HumanMessagePromptTemplate.from_template("{input}"),
            AIMessage(content=SQL_FUNCTIONS_SUFFIX),
            MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        self.prompt = ChatPromptTemplate.from_messages(messages)
        self.prompt = self.prompt.partial(**self.context)
        
    def initialize_agent(self):
        agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.toolkit.get_tools(),
            verbose=True,
        )
        
    def get_query_data(self, query):
        return self.agent_executor.invoke({"input": query})['output']

if __name__ == '__main__':
    engine = SQLQueryEngine('gpt-4o-mini',sql_db)
    output = engine.get_query_data('Number of orders per country in 2022?')
    print("========")
    print(output)
