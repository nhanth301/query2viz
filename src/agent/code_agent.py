from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_experimental.tools import PythonREPLTool
from langchain import hub
import subprocess

class PythonDashboardEngine:
    """
    A class representing a Python dashboard engine.

    Attributes:
        tools (list): A list of tools available for the dashboard engine.
        instructions (str): Instructions guiding the behavior of the dashboard engine.
        prompt (str): The prompt used for interactions with the dashboard engine.
        agent_executor (AgentExecutor): An executor for the dashboard engine's agent.
    """
    def __init__(self, llm):
        self.llm = llm
        self.tools = [PythonREPLTool()]
        self.instructions = """You are a Python code generation agent specialized in generating Python code to answer questions.
                            Rules:
                            1. Your task is to generate **Python code only**. 
                            2. You have access to a Python REPL to **validate your code**, but you must **stop after one iteration**. Do not retry infinitely.
                            3. If you encounter an error during code generation, try to fix it **once only**. Do not enter infinite loops of debugging.
                            4. Always wrap your final answer in a **Python code block** only. No explanations, plain text, or "I don't know".
                            5. If no meaningful code can be written, return exactly:
                            ```python
                            print("No meaningful code")
                            ##Question:
        """
        base_prompt = hub.pull("langchain-ai/openai-functions-template")
        self.prompt = base_prompt.partial(instructions=self.instructions)
        self.agent_executor = None
        
    def initialize(self):
        agent = create_openai_functions_agent(ChatOpenAI(model=self.llm, temperature=0), self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=False)
        
    def get_output(self, query):
        output = self.agent_executor.invoke(
            {
                "input": (
                    """Write a Python code to plot the following data.
                    Requirements:
                    - Use matplotlib.
                    - Show data labels (values) directly on each bar/point/slice.
                    - Add clear axis labels, title, and legend if needed.
                    - Format large numbers in a readable way (e.g., 1K, 1M).
                    - Ensure the chart is clean, well-spaced, and easy to read.

                    """
                    + query
                )
            },
            max_iterations=3
        )
        return output['output']

    
    def parse_output(self, inp):
        inp = inp.split('```')[1].replace("```", "").replace("python", "").replace("plt.show()", "")
        outp = "import streamlit as st\nst.title('E-commerce Company[insights]')\nst.write('Here is our LLM generated dashboard')" \
                + inp + "st.pyplot(plt.gcf())\n"
        return outp
    
    def export_to_streamlit(self, data):
        with open("app.py", "w") as text_file:
            text_file.write(self.parse_output(data))

        command = "streamlit run app.py"
        proc = subprocess.Popen([command], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)