# Streamlit LangChain Chatbot for SQL Data Exploration

## Project Overview
This project demonstrates the development of a **Streamlit chatbot** integrated with **LangChain** and **OpenAI GPT-4**, enabling natural language interaction with a SQL database. Users can ask questions in plain language, and the chatbot generates SQL queries, retrieves relevant data, and dynamically produces visualizations using Python libraries such as **Matplotlib** or **Plotly**.

No more manual filtering or complex SQL commands—just ask, and the bot provides intelligent, insightful, visual answers in seconds.

---

## System Architecture
The architecture of the Streamlit LangChain Chatbot consists of a SQL Agent for query generation, a Python Agent for visualization, and a Streamlit interface for interactive chat.  

![System Architecture](imgs/image.png)  
*Figure: System Architecture Overview*

---

## Demo
Here is an example of the chatbot in action, showing a user query, SQL generation, and resulting visualization.  

![Chatbot Demo](imgs/demo.png)  
*Figure: Chatbot Demo with Query and Visualization*

---

## Key Features
- **Natural Language to SQL:** Users input questions in plain English, and the chatbot translates them into optimized SQL queries.  
- **Dynamic Visualization:** Automatically generates Python code to create charts and graphs from query results.  
- **Interactive Streamlit Interface:** Provides a user-friendly, real-time chat interface.  
- **Memory & Guardrails:** Maintains conversation context and ensures safe, relevant outputs.
