from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import create_agent
import os

from langchain_community.agent_toolkits import FileManagementToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import HumanInTheLoopMiddleware 
from langgraph.types import Command

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
    middleware=[
        HumanInTheLoopMiddleware( 
            interrupt_on={
                "write_file": True,  # All decisions (approve, edit, reject) allowed
                "execute_sql": {"allowed_decisions": ["approve", "reject"]},  # No editing allowed
                # Safe operation, no approval needed
                "read_data": False,
            },
            description_prefix="Tool execution pending approval",
        ),
    ],
    checkpointer=InMemorySaver()
)

config = {"configurable": {"thread_id": "1"}}

prompt = "创建空文件：abcd.txt"

response = agent.invoke({
            "messages":[
                {"role": "user", "content": prompt}
            ]
        },config)

print(response["messages"][-1].content)

print(response['__interrupt__'])

agent.invoke(
    Command( 
        # resume={"decisions": [{"type": "approve"}]}  #approve or "edit", "reject"
        resume={"decisions": [{
            "type": "reject",
            "message": "你不能操作这个目录。"
        }]}  
    ), 
    config=config # Same thread ID to resume the paused conversation
)