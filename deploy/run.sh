#!/bin/bash

# 基于大模型的自然语言转SQL查询工具 - 启动脚本（macOS/Linux）

set -e

APP_DIR="$(pwd)/sql_gen_assistant"

# 检查应用目录是否存在
if [ ! -d "$APP_DIR" ]; then
    echo "错误：应用目录 $APP_DIR 不存在！"
    echo "请先运行部署脚本：./setup.sh"
    exit 1
fi

echo "=================================================="
echo "基于大模型的自然语言转SQL查询工具 - 启动脚本"
echo "=================================================="

# 进入应用目录
cd "$APP_DIR"

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 启动应用
echo "启动应用..."
echo "本地访问地址: http://localhost:8505"
echo "网络访问地址: http://$(hostname -I | awk '{print $1}'):8505"
echo "按 Ctrl+C 停止应用"
echo "=================================================="

streamlit run src/frontend/app.py --server.port 8505 --server.address 0.0.0.0