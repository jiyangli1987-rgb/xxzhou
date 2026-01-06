from email import message
from tabnanny import verbose
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.agents import create_agent
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain.tools import tool
import random
from langgraph.checkpoint.memory import InMemorySaver

@tool
def getRandomStudent():
    """随机获取一位学生的名字，不需要参数，当老师要点名的时候使用。"""
    index = random.randint(0,4)
    list = ["钢铁侠","蝙蝠侠","蜘蛛侠","超胆侠","超人"]
    return list[index];

# toolkit = FileManagementToolkit(
#     root_dir="D:/AIagent/data"
# )

# tools = toolkit.get_tools();

load_dotenv()

model = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

#创建智能体
agent = create_agent(
    model=model,
    tools=[getRandomStudent],
    checkpointer=InMemorySaver()
)

config = {
    "configurable":{"thread_id":1}
}

while True:
    prompt = input("用户：")
    response = agent.invoke({
        "messages":[
            {
                "role":"user",
                "content":prompt
            }
        ]
    },config);
    print("AI:" + response["messages"][-1].content);
    print("-"*60)