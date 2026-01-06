from pydantic import BaseModel,Field
from datetime import datetime
from typing import Literal
import sqlite3
from agentscope.message import TextBlock
from agentscope.tool import ToolResponse


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

def insert_task(task:DataModel):
    """
    向tasks数据表中插入数据
    
    :param task: 插入的数据
    :type task: DataModel
    """
    conn = sqlite3.connect("task_db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, created_at, end_time, weight) VALUES (?, ?, ?, ?)",
        (task["title"],task["created_at"],task["end_time"],task["weight"])
    )
    conn.commit()
    conn.close()
    return ToolResponse(
        content=[
            TextBlock(
                type="text",
                text=f"任务添加成功：{task["title"]}（截止时间：{task["end_time"]}）",
            ),
        ]
    )

def delete_task(task_id:int):
    """
    在tasks数据表中根据id删除数据
    
    :param id: 数据表中的任务id
    """
    conn = sqlite3.connect("task_db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return ToolResponse(
        content=[
            TextBlock(
                type="text",
                text="任务删除成功",
            ),
        ]
    )

def query_tasks():
        """查询所有任务"""
        conn = sqlite3.connect("task_db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, end_time, created_at,weight FROM tasks")
        tasks = cursor.fetchall()
        conn.close()
        res = ""
        if not tasks:
            res = "当前没有待办任务"
        res = "当前待办任务列表：\n"
        for task in tasks:
            res += f"- ID:{task[0]} | 任务：{task[1]} | 截止时间：{task[2]} | 状态：{task[3]}\n"
        return ToolResponse(
        content=[
            TextBlock(
                type="text",
                text=res,
            ),
        ]
    )