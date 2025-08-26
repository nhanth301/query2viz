from src.graph.build_graph import build
import re
import matplotlib.pyplot as plt
import streamlit as st

if __name__ == "__main__":
    graph = build()
    plt.show = lambda *a, **k: None
    output = graph.invoke({'query': 'Number of orders in 2024 per country?'})
    fig, ax = plt.subplots()
    local_vars = {
    'plt': plt,
    'fig': fig,
    'ax': ax
    }
    exec(output['answer'].replace('python','').replace('```',''),globals(),local_vars)
    st.pyplot(fig)


    
