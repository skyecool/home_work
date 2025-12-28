#!/bin/bash

# 基于大模型的自然语言转SQL查询工具 - 一键部署脚本（macOS/Linux）

set -e

echo "=================================================="
echo "基于大模型的自然语言转SQL查询工具 - 一键部署"
echo "=================================================="

# 创建应用目录
APP_DIR="$(pwd)/sql_gen_assistant"
echo "创建应用目录: $APP_DIR"
mkdir -p "$APP_DIR"

# 复制项目文件
echo "复制项目文件..."
cp -r "../src" "$APP_DIR/"
cp -r "../docs" "$APP_DIR/"
cp "../seed_books.py" "$APP_DIR/"
cp "../requirements.txt" "$APP_DIR/"
cp "../.env.example" "$APP_DIR/"
cp "../.gitignore" "$APP_DIR/"

# 进入应用目录
cd "$APP_DIR"

# 检查Python版本
echo "检查Python版本..."
python3 --version

# 验证Python版本是否符合要求
PYTHON_VERSION=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
MIN_VERSION="3.9"

if [ "$(printf '%s\n' "$MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$MIN_VERSION" ]; then
    echo "警告：Python版本 $PYTHON_VERSION 低于推荐版本 $MIN_VERSION"
    echo "某些依赖可能无法正常安装或运行"
    read -p "是否继续？(y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 创建虚拟环境
echo "创建虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "升级pip..."
pip install --upgrade pip

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 创建.env文件
echo "创建环境变量配置文件..."
cp .env.example .env

# 执行预录入脚本
echo "执行预录入脚本，录入100本经典高中、大学图书..."
python seed_books.py

# 退出虚拟环境
deactivate

echo "=================================================="
echo "部署完成！"
echo "=================================================="
echo "下一步："
echo "1. 编辑环境变量配置文件: $APP_DIR/.env"
echo "2. 运行启动脚本: ./run.sh"
echo "3. 通过浏览器访问: http://localhost:8505"
echo ""
echo "如果需要配置API密钥，请编辑.env文件："
echo "- DeepSeek API: DEEPSEEK_API_KEY=your_deepseek_api_key"
echo "- 智谱AI API: ZHIPU_API_KEY=your_zhipu_api_key"
echo ""
echo "=================================================="