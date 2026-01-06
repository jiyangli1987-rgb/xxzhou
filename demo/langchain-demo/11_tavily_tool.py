import streamlit as st
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_tavily import TavilySearch

load_dotenv()

model = ChatOpenAI(
    model=os.getenv("DEEPSEEK_MODEL"),  
    api_key=os.getenv("DEEPSEEK_API_KEY"),  
    base_url=os.getenv("DEEPSEEK_API_BASE") 
)

tool = TavilySearch(
    max_results=5,  
    topic="news"    
)

agent = create_agent(
    model=model,
    tools=[tool],
    checkpointer=InMemorySaver()
)

st.title("信息搜索大师")

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = agent

# 显示对话历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("请输入您的问题……")

if prompt:
    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)

    
    with st.spinner("思考中..."):
        ai_response = st.session_state.agent.invoke({
            "messages":[
                {"role": "user", "content": prompt}
            ]
        },{"configurable": {"thread_id": "1"}})

        with st.chat_message("AI"):
            st.markdown(ai_response["messages"][-1].content)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_response["messages"][-1].content})