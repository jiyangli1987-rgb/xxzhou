import os,sys
from dotenv import load_dotenv
from agentscope.model import DashScopeChatModel

load_dotenv()

def get_exe_dir():
    """获取exe所在目录（打包后/未打包都兼容）"""
    if getattr(sys, 'frozen', False):
        # 打包成exe后的运行环境
        return os.path.dirname(sys.executable)
    else:
        # 开发环境（main.py所在目录）
        return os.path.dirname(os.path.abspath(__file__))

def load_env_config():
    """加载外置.env配置"""
    exe_dir = get_exe_dir()
    env_path = os.path.join(exe_dir, '.env')
    
    # 检查.env是否存在
    if not os.path.exists(env_path):
        # 不存在则创建默认.env模板（提示用户填写API Key）
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write('API_KEY=请填写你的API密钥\n')
        print(f"⚠️  未找到配置文件，已在 {env_path} 创建默认.env模板，请填写API_KEY后重新运行！")
        sys.exit(1)
    
    # 加载.env配置
    load_dotenv(dotenv_path=env_path)
    api_key = os.getenv('QWEN_API_KEY')
    if not api_key or api_key == '请填写你的API密钥':
        print(f"⚠️  请在 {env_path} 中填写有效的API_KEY！")
        sys.exit(1)
    return api_key

class XXzhouModel():

    def __init__(self):

        self.dashcope_api_key = load_env_config()

    # qwen-max qwen3-vl-plus
    def get_dashscope_chat_model(self, model_name="qwen-max"):
        return DashScopeChatModel(
            model_name=model_name,
            api_key=self.dashcope_api_key,
            stream=True
        )
