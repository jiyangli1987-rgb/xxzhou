import streamlit as st
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.agents import create_agent

# 加载环境变量（包含API密钥等配置信息）
load_dotenv()

model = ChatOpenAI(
    model=os.getenv("DEEPSEEK_MODEL"),  
    api_key=os.getenv("DEEPSEEK_API_KEY"),  
    base_url=os.getenv("DEEPSEEK_API_BASE") 
)

agent = create_agent(
    model=model,
    tools=[]
)

response = agent.invoke({
    "messages":[
        {"role": "user", "content": "你是谁？"}
    ]
})

print(response["messages"][-1].content)