import streamlit as st
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 加载环境变量（包含API密钥等配置信息）
load_dotenv()

model = ChatOpenAI(
    model=os.getenv("DEEPSEEK_MODEL"),  
    api_key=os.getenv("DEEPSEEK_API_KEY"),  
    base_url=os.getenv("DEEPSEEK_API_BASE") 
)

st.title("聊天机器人")

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

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
        ai_response = model.invoke(prompt)
        with st.chat_message("AI"):
            st.markdown(ai_response.content)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_response.content})