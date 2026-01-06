# -*- coding: utf-8 -*-
"""基于SQLite会话管理的示例主入口文件"""
import asyncio
import os

from sqlite_session import SqliteSession

from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.message import Msg
from agentscope.model import DashScopeChatModel

# SQLite数据库文件路径
SQLITE_PATH = "./session.db"


async def main(username: str, query: str) -> None:
    """创建智能体、从会话加载状态、与智能体对话，并将其状态保存至SQLite。

    参数:
        username (`str`):
            用于标识会话的用户名。
        query (`str`):
            用户输入的查询内容。
    """

    # 创建ReAct智能体
    agent = ReActAgent(
        name="星期五",  # 智能体名称（原friday译为星期五）
        sys_prompt="你是一名名为星期五的得力助手。",
        model=DashScopeChatModel(
            model_name="qwen-max",  # 模型名称保留原标识符
            api_key=os.environ["DASHSCOPE_API_KEY"],  # 环境变量保留原命名
        ),
        formatter=DashScopeChatFormatter(),
    )

    # 创建SQLite会话实例
    session = SqliteSession(SQLITE_PATH)

    # 根据指定键"friday_of_user"加载智能体状态
    # load_session_state方法支持加载多个状态模块（如多个智能体）
    await session.load_session_state(
        session_id=username,
        friday_of_user=agent,
    )

    # 与智能体对话，生成会话状态
    await agent(
        Msg("user", query, "user"),  # 角色标识保留框架约定
    )

    # 根据指定键"friday_of_user"保存智能体状态
    # 同样支持保存多个状态模块（例如多个智能体）
    await session.save_session_state(
        session_id=username,
        friday_of_user=agent,
    )


print("用户爱丽丝与智能体对话中...")
asyncio.run(main("alice", "美国的首都是什么？"))

print("用户鲍勃与智能体对话中...")
asyncio.run(main("bob", "中国的首都是什么？"))

print(
    "\n现在，恢复爱丽丝的会话，并询问她此前提出的问题相关信息。",
)
asyncio.run(
    main(
        "alice",
        "我之前问了你什么问题？你的回答是什么？我总共问了你多少个问题？",
    ),
)