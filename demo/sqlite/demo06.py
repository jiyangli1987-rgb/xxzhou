# filesystem:生成html简历

import asyncio
from json import load
from pydantic import BaseModel,Field
import sqlite3
from typing import Literal,Optional
from datetime import datetime
from agentscope.agent import ReActAgent,UserAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.model import DashScopeChatModel
from agentscope.tool import (
    Toolkit, 
    write_text_file,
    view_text_file,
    insert_text_file,
    execute_shell_command,
    execute_python_code,
    ToolResponse
)
import os,asyncio
from agentscope.message import Msg,TextBlock
from dotenv import load_dotenv
load_dotenv();

class DataModel(BaseModel):
    # 任务标题：必填 + 长度约束（避免空标题/超长标题）
    title: str = Field(
        ...,  # 表示必填（你的写法默认允许 None，建议显式必填）
        min_length=1,
        max_length=100,
        description="任务标题"
    )
    
    # 创建时间：支持字符串（如 ISO 格式）自动转 datetime，也可直接传 datetime
    created_at: datetime = Field(
        description="创建时间（支持格式：YYYY-MM-DD HH:MM:SS 或 ISO 格式，如 2025-12-18T14:30:00）"
    )
    
    # 截止时间：同上 + 必须晚于创建时间
    end_time: datetime = Field(
        description="截止时间（格式同创建时间，需晚于创建时间）"
    )
    
    # 权重：用 Literal 限定可选值（统一标准），比 str 更规范
    weight: Literal["高", "普通"] = Field(
        default="默认",  # 可选：设置默认值，无需手动传入
        description="权重（可选值：高/中/低/默认）"
    )


def insert_data(task_data: DataModel) -> Optional[int]:
    """
    插入示例数据（演示数据类型兼容性）
    :param task_data: 任务数据（符合 DataModel 结构）
    :return: 插入数据的主键 ID
    """
    conn = sqlite3.connect("task_db.sqlite3")
    cursor = conn.cursor()

    insert_sql = """
    INSERT INTO tasks (title, created_at, end_time, weight)
    VALUES (?, ?, ?, ?)
    """

    try:
        # 处理 datetime 类型（自动转换为 ISO 格式字符串，SQLite 可识别）
        params = (
            task_data["title"],
            task_data["created_at"].isoformat() if isinstance(task_data["created_at"], datetime) else task_data["created_at"],
            task_data["end_time"].isoformat() if isinstance(task_data["end_time"], datetime) else task_data["end_time"],
            task_data.get("weight", "默认")  # 使用默认值
        )

        cursor.execute(insert_sql, params)
        conn.commit()
        print(f"✅ 数据插入成功，主键 ID：{cursor.lastrowid}")
        # return cursor.lastrowid
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"✅ 数据插入成功，主键 ID：{cursor.lastrowid}",
                ),
            ]
        )
    except Exception as e:
        conn.rollback()
        print(f"❌ 数据插入失败：{str(e)}")
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"❌ 数据插入失败：{str(e)}",
                ),
            ]
        )
    finally:
        cursor.close()
        conn.close()

def select_data():
    """查询所有任务数据"""
    conn = sqlite3.connect("task_db.sqlite3")
    cursor = conn.cursor()

    sql = "select * from tasks;"

    cursor.execute(sql)

    tasks = cursor.fetchall();

    cursor.close()
    conn.close()

    return ToolResponse(
        content=[
            TextBlock(
                type="text",
                text=str(tasks),
            ),
        ]
    )

async def main():
    toolkit = Toolkit()
    toolkit.register_tool_function(write_text_file)
    toolkit.register_tool_function(view_text_file)
    toolkit.register_tool_function(insert_text_file)
    toolkit.register_tool_function(execute_shell_command)
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(insert_data)
    toolkit.register_tool_function(select_data)

    current_time = datetime.now()

    agent = ReActAgent(
        name="AI助手",
        sys_prompt=f"""
        你是一个AI任务管理助手，当接到任务的时候，将格式化的任务通过insert_data工具插入到数据库。
        当接收到查询任务的消息时，使用select_data工具查询所有任务。
        （当前时间是{current_time}）
        """,
        model=DashScopeChatModel(
            model_name="qwen-max",
            api_key=os.getenv("QWEN_API_KEY"),
            stream=True
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit
    )

    msg = Msg(
        name="user",
        role="user",
        content="看看我有那些任务要做。"
    )

    res = await agent(msg,structured_model=DataModel)

    print(res)

asyncio.run(main())
