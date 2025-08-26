from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_experimental.tools import PythonREPLTool
from langchain import hub
import subprocess
from dotenv import load_dotenv
import seaborn as sns
load_dotenv()

class PythonDashboardEngine:
    """
    A Python dashboard engine using LLM to generate Python code for plotting data.

    Attributes:
        llm (ChatOpenAI): The language model used for code generation.
        tools (list): Tools available for the agent (e.g., Python REPL).
        instructions (str): Instructions guiding the behavior of the agent.
        prompt (Any): The Chat Prompt template used by the agent.
        agent_executor (AgentExecutor): Executor to run the agent with tools.
    """

    def __init__(self, model_name: str) -> None:
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.tools = [PythonREPLTool()]

        self.instructions = """You are a Python code generation agent specialized in generating Python code for data visualization.
        Rules:
        1. Generate **Python code only**. Do not provide explanations or plain text.
        2. You have access to a Python REPL to validate your code:
        - If the code runs successfully on the first try, return it immediately.
        - Only attempt fixes if an error occurs.
        - Stop retrying after three iterations at most.
        3. Always wrap your final answer in a **Python code block** only.
        4. If no meaningful code can be written, return exactly:
        ```python
        print("No meaningful code")
        ```
        """

        base_prompt = hub.pull("langchain-ai/openai-functions-template")
        self.prompt = base_prompt.partial(instructions=self.instructions)
        self.agent_executor: AgentExecutor | None = None
        self.initialize_agent()

    def initialize_agent(self) -> None:
        """Initialize the OpenAI Functions agent with the Python REPL tool."""
        agent = create_openai_functions_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def get_output(self, query: str, max_iterations: int = 1) -> str:
        """Generate Python code for plotting based on a query."""

        import matplotlib.pyplot as plt
        plt.show = lambda *a, **k: None
        if not self.agent_executor:
            raise RuntimeError("AgentExecutor not initialized.")

        prompt_input = (
        "Write Python code to visualize the following data.\n"
        "Requirements:\n"
        "- Automatically select the most appropriate chart type (bar, line, scatter, pie, etc.) based on the data.\n"
        "- Use matplotlib or seaborn to improve clarity and style.\n"  # sửa dòng này
        "- Show data labels directly on bars, points, or slices.\n"
        "- Add clear axis labels, title, and legend if needed.\n"
        "- Format large numbers in a readable way (e.g., 1K, 1M).\n"
        "- Use consistent colors, styles, and spacing suitable for a business dashboard.\n"
        "- Avoid plotting multiple figures unnecessarily; keep only the final chart.\n\n"
        + query
    )

        output = self.agent_executor.invoke(
            {"input": prompt_input},
            max_iterations=max_iterations
        )
        return output['output']

    def parse_output(self, code_str: str) -> str:
        """Extract Python code from LLM output and wrap for Streamlit."""
        import matplotlib.pyplot as plt

        # Remove ```python blocks
        parts = code_str.split('```')
        python_code = ""
        for part in parts:
            if "python" in part:
                python_code = part.replace("python", "").strip()
        python_code = python_code.replace("plt.show()", "").strip()

        # Close previous figures to avoid duplicates
        wrapped_code = (
            "import streamlit as st\n"
            "import matplotlib.pyplot as plt\n"
            "st.title('E-commerce Company Insights')\n"
            "st.write('Here is our LLM-generated dashboard')\n"
            "plt.close('all')\n"
            f"{python_code}\n"
            "st.pyplot(plt.gcf())\n"
        )
        return wrapped_code

    def export_to_streamlit(self, code_str: str, filename: str = "app.py") -> None:
        """Write code to a Streamlit app file and launch it."""
        streamlit_code = self.parse_output(code_str)

        with open(filename, "w") as f:
            f.write(streamlit_code)

        # Run Streamlit app
        command = f"streamlit run {filename}"
        subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)


if __name__ == '__main__':
    engine = PythonDashboardEngine('gpt-4o-mini')
    output = engine.get_output("""Here are the number of orders per country in 2022:

- **Brasil**: 4005 orders
- **United States**: 6328 orders
- **Spain**: 1050 orders
- **Germany**: 1099 orders
- **France**: 1274 orders
- **China**: 9196 orders
- **Australia**: 590 orders
- **Colombia**: 7 orders
- **Japan**: 650 orders
- **South Korea**: 1551 orders
- **United Kingdom**: 1195 orders
- **Belgium**: 369 orders
- **Poland**: 58 orders
- **Austria**: 1 order

If you need any further analysis or information, feel free to ask!""")
    print(output)
    engine.export_to_streamlit(output)