# 测试所有钩子的执行顺序

import asyncio
from typing import Any, Type
from json import load
from agentscope.agent import ReActAgent,ReActAgentBase,UserAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.model import DashScopeChatModel
from agentscope.tool import (
    Toolkit, 
    write_text_file,
    insert_text_file,
    view_text_file,
    execute_python_code,
    execute_shell_command    
)
import os,asyncio
from dotenv import load_dotenv
load_dotenv();

async def main():
    toolkit = Toolkit()
    toolkit.register_tool_function(write_text_file)
    toolkit.register_tool_function(insert_text_file)
    toolkit.register_tool_function(view_text_file)
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(execute_shell_command)

    agent = ReActAgent(
        name="简历助手",
        sys_prompt="你可以在d盘的temp_data目录下做文件操作。",
        model=DashScopeChatModel(
            model_name="qwen-max",
            api_key=os.getenv("QWEN_API_KEY"),
            stream=True
        ),
        formatter=DashScopeChatFormatter(),
        toolkit=toolkit
    )

    def instance_pre_reply_hook(
        self:ReActAgentBase,
        kwargs:dict[str,Any]
    ):
        print("~~~~post_acting~~~~~")
        print(kwargs)
        print("~~~~end~~~~~")
        return kwargs
    
    def instance_post_reply_hook(
        self:ReActAgentBase,
        kwargs:dict[str,Any],
        output:Any
    ):
        print("~~~~post_acting~~~~~")
        print(kwargs)
        print("~~~~end~~~~~")
        return output
    
    def instance_pre_reply_hook(
        self:ReActAgentBase,
        kwargs:dict[str,Any]
    ):
        print("~~~~pre_reply~~~~~")
        print(kwargs)
        print("~~~~end~~~~~")
        return kwargs
    
    def instance_post_reply_hook(
        self:ReActAgentBase,
        kwargs:dict[str,Any],
        output:Any
    ):
        print("~~~~post_reply~~~~~")
        print(kwargs)
        print("~~~~end~~~~~")
        return output
    
    def instance_pre_print_hook(
        self:ReActAgentBase,
        kwargs:dict[str,Any]
    ):
        print("~~~~pre_print~~~~~")
        print(kwargs)
        print("~~~~end~~~~~")
        return kwargs
    
    def instance_post_print_hook(
        self:ReActAgentBase,
        kwargs:dict[str,Any],
        output:Any
    ):
        print("~~~~post_print~~~~~")
        print(kwargs)
        print("~~~~end~~~~~")
        return output
    
    def instance_pre_observe_hook(
        self:ReActAgentBase,
        kwargs:dict[str,Any]
    ):
        print("~~~~pre_observe~~~~~")
        print(kwargs)
        print("~~~~end~~~~~")
        return kwargs
    
    def instance_post_observe_hook(
        self:ReActAgentBase,
        kwargs:dict[str,Any],
        output:Any
    ):
        print("~~~~post_observe~~~~~")
        print(kwargs)
        print("~~~~end~~~~~")
        return output
    
    def instance_pre_reasoning_hook(
        self:ReActAgentBase,
        kwargs:dict[str,Any]
    ):
        print("~~~~pre_reasoning~~~~~")
        print(kwargs)
        print("~~~~end~~~~~")
        return kwargs
    
    def instance_post_reasoning_hook(
        self:ReActAgentBase,
        kwargs:dict[str,Any],
        output:Any
    ):
        print("~~~~post_reasoning~~~~~")
        print(kwargs)
        print("~~~~end~~~~~")
        return output
    
    def instance_pre_acting_hook(
        self:ReActAgentBase,
        kwargs:dict[str,Any]
    ):
        print("~~~~pre_acting~~~~~")
        print(kwargs)
        print("~~~~end~~~~~")
        return kwargs
    
    def instance_post_acting_hook(
        self:ReActAgentBase,
        kwargs:dict[str,Any],
        output:Any
    ):
        print("~~~~post_acting~~~~~")
        print(kwargs)
        print("~~~~end~~~~~")
        return output

    
    agent.register_instance_hook(
        hook_type="pre_reply",
        hook_name="test_pre_reply",
        hook=instance_pre_reply_hook
    )

    agent.register_instance_hook(
        hook_type="post_reply",
        hook_name="test_post_reply",
        hook=instance_post_reply_hook
    )

    # agent.register_instance_hook(
    #     hook_type="pre_print",
    #     hook_name="test_pre_print",
    #     hook=instance_pre_print_hook
    # )

    # agent.register_instance_hook(
    #     hook_type="post_print",
    #     hook_name="test_post_print",
    #     hook=instance_post_print_hook
    # )

    agent.register_instance_hook(
        hook_type="pre_observe",
        hook_name="test_pre_observe",
        hook=instance_pre_observe_hook
    )

    agent.register_instance_hook(
        hook_type="post_observe",
        hook_name="test_post_observe",
        hook=instance_post_observe_hook
    )

    agent.register_instance_hook(
        hook_type="pre_reasoning",
        hook_name="test_pre_reasoning",
        hook=instance_pre_reasoning_hook
    )

    agent.register_instance_hook(
        hook_type="post_reasoning",
        hook_name="test_post_reasoning",
        hook=instance_post_reasoning_hook
    )

    agent.register_instance_hook(
        hook_type="pre_acting",
        hook_name="test_pre_acting",
        hook=instance_pre_acting_hook
    )

    agent.register_instance_hook(
        hook_type="post_acting",
        hook_name="test_post_acting",
        hook=instance_post_acting_hook
    )

    


    user = UserAgent(name="晓舟")

    msg = None

    while True:
        msg = await agent(msg)
        msg = await user(msg)

asyncio.run(main())
