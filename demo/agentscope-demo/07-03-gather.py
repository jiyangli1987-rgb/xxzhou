# -*- coding: utf-8 -*-
"""并行多视角讨论系统示例"""
import asyncio
from datetime import datetime
from typing import Any

import numpy as np

from agentscope.agent import AgentBase
from agentscope.message import Msg
from agentscope.pipeline import fanout_pipeline


class ExampleAgent(AgentBase):
    """用于记录时间的示例智能体"""

    def __init__(self, name: str) -> None:
        """示例智能体的构造函数

        参数:
            name (`str`):
                智能体名称
        """
        super().__init__()
        self.name = name

    async def reply(self, *args: Any, **kwargs: Any) -> Msg:
        """示例智能体的回复函数（核心执行逻辑）"""
        # 记录开始时间
        start_time = datetime.now()
        await self.print(
            Msg(
                self.name,
                f"开始执行于 {start_time.strftime('%H:%M:%S.%f')}",
                "assistant",  # 角色标识保留框架约定
            ),
        )

        # 随机休眠一段时间（模拟任务执行）
        await asyncio.sleep(np.random.choice([2, 3, 4]))

        end_time = datetime.now()
        msg = Msg(
            self.name,
            f"执行完成于 {end_time.strftime('%H:%M:%S.%f')}",
            "user",  # 角色标识保留框架约定
            # 添加元数据用于演示
            metadata={
                "time": (end_time - start_time).total_seconds(),
            },
        )
        await self.print(msg)
        return msg

    async def handle_interrupt(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Msg:
        """本示例中暂不实现该函数，因为不会使用中断功能"""

    async def observe(self, *args: Any, **kwargs: Any) -> None:
        """与handle_interrupt函数类似，此处留空不实现"""


async def main() -> None:
    """并发示例的主入口函数"""
    alice = ExampleAgent("爱丽丝")
    bob = ExampleAgent("鲍勃")
    chalice = ExampleAgent("查理斯")

    print("使用 'asyncio.gather' 并发运行多个智能体：")
    futures = [alice(), bob(), chalice()]

    await asyncio.gather(*futures)

    print("\n\n使用扇出流水线（fanout_pipeline）并发运行多个智能体：")
    collected_res = await fanout_pipeline(
        agents=[alice, bob, chalice],
        enable_gather=True,
    )
    # 打印收集到的结果
    print("\n\n各智能体的执行耗时：")
    for res in collected_res:
        print(f"{res.name}: {res.metadata['time']} 秒")

    print("\n平均执行耗时：")
    avg_time = np.mean([res.metadata["time"] for res in collected_res])
    print(f"{avg_time} 秒")


asyncio.run(main())