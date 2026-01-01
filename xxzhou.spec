# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 定义要打包的文件和目录
a = Analysis(
    ['main.py'],  # 主入口文件
    pathex=[],   # 额外的路径
    binaries=[],  # 二进制文件
    datas=[
        ('src', 'src'),  # 打包src目录到exe中
    ],  # 数据文件
    hiddenimports=[
        'agentscope',
        'src.agents.agent',
        'src.agents.image_reader',
        'src.agents.pdf_reader',
        'src.llm',
        'src.tools.download_video',
        'src.tools.create_image',
        'src.tools.image_reader',
        'src.tools.pdf_reader',
        'dotenv',
        'fitz',  # PyMuPDF
        'PIL',   # pillow
        'cv2',   # opencv-python
    ],  # 隐藏导入
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        '.env',  # 明确排除.env文件
    ],  # 要排除的模块
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='xxzhou',  # exe文件名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # 禁用UPX压缩以避免兼容性问题
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
