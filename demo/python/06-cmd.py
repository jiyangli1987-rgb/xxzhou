# pip install inquirer

import inquirer

def professional_choice():
    # 定义问题（选项）
    questions = [
        inquirer.List(
            'action',
            message="请选择你要执行的操作",
            choices=['查看系统信息', '计算两数之和', '退出程序'],
        ),
    ]
    
    while True:
        # 获取用户选择
        answers = inquirer.prompt(questions)
        choice = answers['action']
        
        # 执行对应逻辑
        if choice == '查看系统信息':
            print("\n=== 系统信息 ===")
            print("Python版本：3.x")
            print("操作系统：Windows/Linux/macOS")
        elif choice == '计算两数之和':
            print("\n=== 计算两数之和 ===")
            try:
                num1 = float(input("请输入第一个数："))
                num2 = float(input("请输入第二个数："))
                print(f"计算结果：{num1} + {num2} = {num1 + num2}")
            except ValueError:
                print("输入错误！请输入有效的数字")
        elif choice == '退出程序':
            print("程序已退出，再见！")
            break

# 运行函数
if __name__ == "__main__":
    professional_choice()