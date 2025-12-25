import sys,asyncio,os
from agents.agent import agent
from agentscope.message import Msg

async def main():
    if len(sys.argv) < 2:
        print("只需要在xxzhou命令后输入您的要求即可。")
        print("例如：xxzhou <你要输入的内容>")
        print("示例1：xxzhou 下载视频，http……")
        print("示例2：xxzhou 图片1.png的内容是什么？")
        print("示例3：xxzhou 给1.png中的人物戴上一顶草帽。")
        return  # 无参数时提示用法，直接退出
    
    # 拼接所有参数
    input_content = " ".join(sys.argv[1:])

    # 获取当前终端打开的目录路径
    current_dir = os.getcwd() 
    # 兼容 Windows 路径
    current_dir = os.path.abspath(current_dir)

    msg = Msg(
        name="user",
        role="user",
        content=input_content + f"当前目录为：{current_dir}"
    )

    res = await agent(msg)
    print(res.content[0]["text"])

if __name__ == "__main__":
    asyncio.run(main())