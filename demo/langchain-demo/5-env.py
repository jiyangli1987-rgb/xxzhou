from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

print(os.getenv("DEEPSEEK_MODEL"))
print(os.getenv("DEEPSEEK_API_BASE"))
