#!/bin/bash

# Jenkins Shell脚本 - 调用Python脚本运行测试

echo "🚀 开始Jenkins构建..."
echo "📁 当前目录: $(pwd)"
echo "📋 文件列表:"
ls -la

# 显示Python版本
echo "🐍 Python版本:"
python3 --version

# 运行我们的Python脚本
echo "🔧 运行Python脚本..."
python3 jenkins_run.py

# 检查退出码
if [ $? -eq 0 ]; then
    echo "✅ Jenkins构建成功"
    exit 0
else
    echo "❌ Jenkins构建失败"
    exit 1
fi 