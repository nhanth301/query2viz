import streamlit as st
from src.graph.build_graph import build
from streamlit_chat import message
import matplotlib.pyplot as plt

graph = build()

st.set_page_config(
    page_title="Graph Chatbot AI", 
    page_icon="📊", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        padding: 0 2rem;
    }
    
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        max-width: 800px;
        margin: 0 auto;
    }
    
    .stChatMessage {
        max-width: 100%;
    }
    
    .chart-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 1rem;
    }
    
    .chart-container .stPyplot {
        max-width: 600px;
        width: 100%;
    }
    
    .stChatInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e0e6ed;
        padding: 12px 20px;
        font-size: 16px;
    }
    
    .stChatInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .chat-stats {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 1rem 0;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">📊 Graph Chatbot AI</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Intelligent AI assistant for creating charts and visualizations through natural conversation</p>', 
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.info("👋 **Welcome!** Ask me to create charts, analyze data, or visualize information. I can help you with various types of graphs including bar charts, line plots, scatter plots, and more!")

st.markdown('<div style="max-width: 800px; margin: 0 auto;">', unsafe_allow_html=True)
with st.sidebar:
    st.markdown("## 🚀 Quick Start Guide")
    st.markdown("""
    **Example requests:**
    - "Create a bar chart showing sales data"
    - "Plot a line graph of temperature changes"
    - "Generate a scatter plot for correlation analysis"
    - "Show me a pie chart of market share"
    """)
    
    st.markdown("## 🛠️ Features")
    st.markdown("""
    - ✨ Natural language chart creation
    - 📈 Multiple chart types supported
    - 🎨 Automatic styling and formatting
    - 💬 Interactive conversation history
    - 🔄 Real-time chart generation
    """)
    
    if st.button("🗑️ Clear Chat History", type="secondary"):
        st.session_state.messages = []
        st.rerun()

chat_container = st.container()

with chat_container:
    for i, msg in enumerate(st.session_state.messages):
        avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
        
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            
            if "code_result" in msg and msg["code_result"]:
                with st.expander("📊 View Chart Code", expanded=False):
                    st.code(msg["code_result"], language="python")
                
                try:
                    exec(msg["code_result"].replace('python','').replace('```',''), {"plt": plt})
                    fig = plt.gcf()  
                    st.pyplot(fig)
                    plt.clf()
                except Exception as e:
                    st.error(f"⚠️ Error rendering chart: {e}")

if prompt := st.chat_input("💬 Ask me to create a chart or analyze data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🧠 AI is thinking and generating your visualization..."):
            output = graph.invoke({"messages": st.session_state.messages})
            
        answer = output.get("answer", "")
        code_result = output.get("code_result")

        st.markdown(answer)

        if code_result:
            with st.expander("📊 View Generated Code", expanded=False):
                st.code(code_result, language="python")
            
            try:
                exec(code_result.replace('python','').replace('```',''), {"plt": plt})
                fig = plt.gcf()  
                st.pyplot(fig)
                plt.clf()
                st.success("✅ Chart generated successfully!")
            except Exception as e:
                st.error(f"⚠️ Error executing chart generation code: {e}")
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": answer, 
            "code_result": code_result
        })

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>🚀 Powered by AI Graph Generation Technology</div>", 
    unsafe_allow_html=True
)