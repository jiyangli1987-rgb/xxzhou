# 钩子函数的基本用法
import asyncio
from typing import Any, Type

from agentscope.agent import ReActAgentBase, AgentBase
from agentscope.message import Msg

class TestAgent(AgentBase):
    
    async def reply(self, msg:Msg):
        print("~~~~~~~~~~~~")
        return msg
    
def instance_pre_reply_hook(
        self:AgentBase,
        kwargs:dict[str,Any]
):
    msg = kwargs["msg"]
    msg.content += "[instance-pre-reply]"
    return {
        **kwargs,
        "msg":msg
    }

def cls_pre_reply_hook(
    self: AgentBase,
    kwargs: dict[str, Any],
) -> dict[str, Any]:
    """修改消息内容的前置回复钩子。"""
    msg = kwargs["msg"]
    msg.content += "[cls-pre-reply]"
    # 返回修改后的 kwargs
    return {
        **kwargs,
        "msg": msg,
    }
# 注册类钩子
TestAgent.register_class_hook(
    hook_type="pre_reply",
    hook_name="test_pre_reply",
    hook=cls_pre_reply_hook,
)

# 注册实例钩子
agent = TestAgent()
agent.register_instance_hook(
    hook_type="pre_reply",
    hook_name="test_pre_reply",
    hook=instance_pre_reply_hook,
)


async def example_test_hook() -> None:
    """测试钩子的示例函数。"""
    msg = Msg(
        name="user",
        content="你好，你知道我是谁吗？",
        role="user",
    )
    res = await agent(msg)
    print("响应内容：", res.content)
    TestAgent.clear_class_hooks()


asyncio.run(example_test_hook())