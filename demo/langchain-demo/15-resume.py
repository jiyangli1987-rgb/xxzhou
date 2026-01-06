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
    system_prompt="""帮用户生成简历，建立分为三部分：
    1. 个人信息：姓名、年龄、毕业院校等。
    2. 专业技能：根据用户要求的建立类型编写
    3. 工作经验：根据用户要求的具体情况进行扩展。
    将简历保存为本地的html格式文件，添加美观的样式。    
"""
)

prompt = "我是一个智能体开发工程师，今年35岁，毕业于北大，帮我写一份简历。"

response = agent.invoke({
            "messages":[
                {"role": "user", "content": prompt}
            ]
        })

print(response["messages"][-1].content)