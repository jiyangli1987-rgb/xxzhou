import asyncio
from asyncio import Queue

async def do_something(queue: Queue):
    """异步任务：向队列中放入结果（替代全局列表）"""
    await asyncio.sleep(3)
    await queue.put("a")  # 队列是异步安全的，无需担心并发问题
    await asyncio.sleep(3)
    await queue.put("b")
    await asyncio.sleep(3)
    await queue.put("c")
    return "over"

async def async_main():
    queue = Queue()
    # 创建任务并传入队列（解耦全局变量）
    my_task = asyncio.create_task(do_something(queue))
    
    # 同时等待任务完成和队列有数据
    while not my_task.done():
        try:
            # 非阻塞获取队列数据（超时 0.1s，避免死等）
            result = await asyncio.wait_for(queue.get(), timeout=0.1)
            yield result
        except asyncio.TimeoutError:
            continue  # 超时说明队列暂无数据，继续等待任务
    
    # return my_task.result()  # 返回任务最终结果

async def run():
    # 消费异步生成器
    async for res in async_main():
        print("产出结果:", res)
    # 打印任务最终返回值
    # print("任务完成:", await async_main())

if __name__ == "__main__":
    asyncio.run(run())