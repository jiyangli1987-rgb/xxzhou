from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# 加载环境变量
load_dotenv()

# 初始化模型（确保模型支持流式，DeepSeek 支持）
model = ChatOpenAI(
    model=os.getenv("DEEPSEEK_MODEL"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_API_BASE"),
    temperature=0.7,  # 可选：调整随机性
    streaming=True,    # 显式开启流式（部分模型需显式声明，可选）
)

# 创建智能体（工具为空时，本质是纯对话模型）
agent = create_agent(
    model=model,
    tools=[],
    system_prompt="你是一个作文助手，按用户要求完成1000字作文，语言流畅自然。",  # 补充系统提示
    checkpointer=InMemorySaver(),
)

# 输入提示
prompt = "帮我写一篇1000字的作文，随意写点什么都行。"

# 流式调用智能体（关键：stream_mode="updates" 更适合增量拼接）
stream = agent.stream(
    input={
        "messages": [{"role": "user", "content": prompt}]
    },
    config={
        "configurable": {"thread_id": "1"},  # 会话ID，用于记忆
        "stream_mode": "updates",  # 增量更新模式（推荐）：只返回新增的内容片段
    }
)

# 拼接并打印流式内容
full_content = ""
print("作文流式输出：")
print("=" * 50)

for chunk in stream:
    # 解析 chunk：智能体输出的结构是 {"messages": [最新消息]}
    if "messages" in chunk and len(chunk["messages"]) > 0:
        # 获取最新消息的 content（增量片段）
        latest_msg = chunk["messages"][-1]
        if latest_msg["role"] == "assistant" and "content" in latest_msg:
            delta = latest_msg["content"][len(full_content):]  # 提取新增片段（避免重复）
            if delta:  # 只打印非空增量
                print(delta, end="", flush=True)  # end="" 不换行，flush=True 强制实时输出
                full_content = latest_msg["content"]  # 更新完整内容

print("\n" + "=" * 50)
print(f"\n作文总字数：{len(full_content)} 字")