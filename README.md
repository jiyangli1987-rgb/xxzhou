# 小小舟终端助手

## 一、快速上手

### 配置api key

首相将项目下载（或clone）到本地，然后在项目根目录下的`.env_demo`文件名修改为`.env`，再将自己的大模型`api_key`复制到对应的变量下。（当前项目默认使用千问大模型的api_key）

``` 
DEEPSEEK_API_KEY="sk-xxx"
QWEN_API_KEY="sk-xxx"
```

### 安装依赖

项目基于3.13.5开发，为了让系统可以顺利运行，推荐使用3.13.x系列版本。

推荐大家创建虚拟环境安装依赖和运行项目，创建虚拟环境的命令是

``` bash
python -m venv .venv
```

创建成功后，执行下面命令激活虚拟环境。

``` bash
.venv\Scripts\activate
```
然后执行下面的命令安装项目依赖。

``` bash
pip install agentscope dotenv
```

如果依赖速度较慢，可以使用国内镜像下载。

``` bash
pip install agentscope dotenv -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 配置环境变量

1. 右键「此电脑」→「属性」→「高级系统设置」→「环境变量」
2. 在「系统变量」的「Path」中，点击「新建」，粘贴项目所在目录。
3. 点击「确定」保存

如果环境变量重构，在终端中输入`xxzhou`命令，可以看到如下内容

``` bash
C:\Users\lenovo>xxzhou
只需要在xxzhou命令后输入您的要求即可。
例如：xxzhou <你要输入的内容>
示例1：xxzhou 下载视频，http……
示例2：xxzhou 图片1.png的内容是什么？
示例3：xxzhou 给1.png中的人物戴上一顶草帽。
示例4：xxzhou 分析这个PDF文件：document.pdf
示例5：xxzhou PDF文件report.pdf中都有哪些章节？
```

然后安装实例的交互方式，就实现可以【下载视频】【生成图片】【识别图片】【读取PDF文件】的功能了。

### 使用pyinstaller打包

``` bash
pip install pyinstaller
pyinstaller -F -n xxzhou --exclude-data .env:.env main.py
```

## 二、功能特性

### PDF文档识别

项目新增了PDF文档智能识别功能，支持：

- **文本提取**：自动提取PDF中的文字内容
- **图片识别**：识别PDF中的图片内容（使用Qwen视觉模型）
- **多页处理**：支持多页PDF文档，最多处理50页
- **智能分析**：根据用户的问题智能分析PDF内容

#### 使用方法

```bash
# 基本分析PDF内容
xxzhou 分析这个PDF文件：document.pdf

# 询问PDF中的特定信息
xxzhou PDF文件report.pdf中都有哪些章节？
xxzhou 提取invoice.pdf中的表格数据
xxzhou 总结research_paper.pdf的主要观点
```

#### 技术实现

- 使用PyMuPDF提取PDF文本和图片
- 结合Qwen视觉模型进行智能分析
- 支持中英文混合内容识别

## 三、股东群

对智能体开发感兴趣的小伙伴，欢迎加入晓舟的会员股东群，一起学习智能体开发。

![股东群](./images/xxzhouwx.jpg)