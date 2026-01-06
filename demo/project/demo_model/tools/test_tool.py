import sqlite3
from agentscope.message import TextBlock
from agentscope.tool import ToolResponse

def insert_task(task:dict):
    """
    向tasks数据表中插入数据
    
    :param task: 插入的数据
    :type task: dict
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