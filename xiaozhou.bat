@echo off
chcp 65001 >nul 2>&1  :: 可选：解决中文乱码问题
:: 获取当前bat文件所在的目录（自动适配任意路径）
set "CURRENT_DIR=%~dp0"
:: 拼接python脚本的路径（bat同目录下的main.py）
set "PY_SCRIPT=%CURRENT_DIR%main.py"
:: 拼接虚拟环境python.exe的路径（bat同目录下的.venv/Scripts/python.exe）
set "PY_EXE=%CURRENT_DIR%.venv\Scripts\python.exe"

:: 检查python解释器是否存在，增强容错性
if not exist "%PY_EXE%" (
    echo 错误：未找到Python解释器，请检查虚拟环境路径是否正确！
    echo 预期路径：%PY_EXE%
    pause
    exit /b 1
)

:: 检查python脚本是否存在
if not exist "%PY_SCRIPT%" (
    echo 错误：未找到main.py脚本！
    echo 预期路径：%PY_SCRIPT%
    pause
    exit /b 1
)

:: 执行python脚本并传递所有参数
"%PY_EXE%" "%PY_SCRIPT%" %*

:: 可选：执行完不自动关闭窗口（调试用，发布时可删除）
:: pause