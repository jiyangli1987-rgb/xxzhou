from agentscope.agent import ReActAgent,ReActAgentBase
from typing import Any
from agentscope.formatter import DashScopeChatFormatter
from agentscope.model import DashScopeChatModel
from agentscope.memory import InMemoryMemory
from agentscope.tool import (
    Toolkit,
    write_text_file,
    view_text_file,
    insert_text_file,
    execute_python_code,
    execute_shell_command
)
from llm import dashcope_chat_model
from datetime import datetime
from tools.data_handle import query_tasks,delete_task,insert_task


toolkit = Toolkit()
toolkit.register_tool_function(write_text_file)
toolkit.register_tool_function(insert_text_file)
toolkit.register_tool_function(view_text_file)
toolkit.register_tool_function(execute_python_code)
toolkit.register_tool_function(execute_shell_command)
toolkit.register_tool_function(query_tasks)
toolkit.register_tool_function(delete_task)
toolkit.register_tool_function(insert_task)
current_time = datetime.now()
agent = ReActAgent(
    name="晓舟助手",
    sys_prompt=f"""
    你是一个任务管理助手，能处理用户的任务增删改查请求。
    请严格按照以下步骤处理用户消息：
    1. 识别用户意图：你可以帮助用户完成【添加任务】【查询任务】【删除任务】。也可以根据【查询任务】的结果帮助用户做日程规划。规划的内容经用户允许，可以插入到任务列表中。
    2. 结构化提取信息：
        - 如果是添加任务：提取 title(任务名称)、end_time(截止时间)、weight(任务权重，【高】或【普通】根据用户自行判断)，格式为 JSON {{"title": "...", "end_time": "...", "weight":"..."}}
        - 如果是查询任务：无需提取信息，直接调用查询函数
        - 如果是删除任务：首先查询任务id，提取 task_id(任务ID)，格式为 JSON {{"task_id": ...}}
    3. 调用对应的工具函数，执行操作。
    4. 用自然语言回复用户操作结果，不要暴露JSON格式。
    5. 【添加任务】之前，要做任务审核。用户的工作是否与【软件开发】相关，如果不相关，请拒绝添加任务，并警告用户，正在做与工作无关的事。

    注意：如果用户表达不清晰（如任务不明确或缺少截止时间），请反问用户补充信息。当前时间为{current_time}
    """,
    formatter=DashScopeChatFormatter(),
    toolkit=toolkit,
    memory=InMemoryMemory(),
    model=dashcope_chat_model
)