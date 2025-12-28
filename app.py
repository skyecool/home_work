#!/usr/bin/env python3
"""
应用入口脚本，用于启动Streamlit应用
"""

import sys
import os
import subprocess

# 确保在项目根目录下运行
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 启动Streamlit应用
cmd = [sys.executable, "-m", "streamlit", "run", "src/frontend/app.py"]
print(f"启动应用: {' '.join(cmd)}")

subprocess.run(cmd)
