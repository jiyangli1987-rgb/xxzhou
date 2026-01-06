from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import create_agent
import os
import asyncio

from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_mcp_adapters.client import MultiServerMCPClient

async def main():
    # 加载环境变量（包含API密钥等配置信息）
    load_dotenv()

    # 初始化文件操作工具集
    toolkit = FileManagementToolkit(root_dir="D:/test/ai_data")
    # 获取工具列表
    tools = toolkit.get_tools()


    client = MultiServerMCPClient(
        {
            "amap-maps": {
                "transport": "sse",
                "url": "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/sse",
                "headers": {
                "Authorization": "Bearer " + os.getenv("ALI_API_KEY")
                }
            }
        }
    )

    tools.extend(await client.get_tools())

    # 使用环境变量中的配置信息初始化大模型
    model = ChatOpenAI(
        model=os.getenv("DEEPSEEK_MODEL"),
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_API_BASE"),
    )

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt="""
        帮用户规划自驾游攻略路线，给用户提供路程涉及到的天气信息，并在饭店提供指定餐厅，目的地要安排酒店。其他要求根据用户的要求执行。
        生成html版的攻略介绍，页面要美观。  
    """,
    )

    prompt = "我11月11日向从长春到北京自驾游"

    response = await agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})

    print(response["messages"][-1].content)

asyncio.run(main())