#!/bin/bash
# ChatPPT 部署脚本

set -e

echo "开始部署 ChatPPT..."

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3"
    exit 1
fi

# 检查依赖
echo "检查依赖..."
pip install -r requirements.txt

# 检查环境变量
if [ -z "$OPENAI_API_KEY" ]; then
    echo "警告: OPENAI_API_KEY 环境变量未设置"
    read -p "请输入 OPENAI_API_KEY: " api_key
    export OPENAI_API_KEY=$api_key
fi

# 创建输出目录
mkdir -p outputs

# 启动服务
echo "启动 ChatPPT 服务..."
echo "服务将在 http://0.0.0.0:7860 启动"
echo "按 Ctrl+C 停止服务"

python3 src/gradio_server.py

