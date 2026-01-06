import asyncio
import time

# 定义协程函数，协程函数内可以使用await，await后面可以调用协程函数


# 调用协程函数，会创建协程对象
async def say_something(str,delay):
    await asyncio.sleep(delay)
    print(f"你好：{str}")
    return f"你好：{str}"

async def main():
    # await say_something("A",1)
    # await say_something("B",2)
    # await say_something("C",3)

    task1 = asyncio.create_task(say_something("A",1))
    task2 = asyncio.create_task(say_something("B",2))
    task3 = asyncio.create_task(say_something("C",3))

    result = await asyncio.gather(task1,task2,task3)

    print(result)


asyncio.run(main());