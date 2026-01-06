from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import create_agent
import os

from langchain_community.agent_toolkits import FileManagementToolkit

# 初始化文件操作工具集
toolkit = FileManagementToolkit(
    root_dir = "D:/test/ai_data"
)
# 获取工具列表
tools = toolkit.get_tools()


# 加载环境变量（包含API密钥等配置信息）
load_dotenv()

# 使用环境变量中的配置信息初始化大模型
model = ChatOpenAI(
    model=os.getenv("DEEPSEEK_MODEL"),  
    api_key=os.getenv("DEEPSEEK_API_KEY"),  
    base_url=os.getenv("DEEPSEEK_API_BASE") 
)

agent = create_agent(
    model=model,
    tools=tools,
)

prompt = "创建10个txt文件，文件名为10个漫威的超级英雄，文件内容是对应英雄的一句话简介。"

response = agent.invoke({
            "messages":[
                {"role": "user", "content": prompt}
            ]
        })

print(response["messages"][-1].content)