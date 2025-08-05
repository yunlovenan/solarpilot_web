#!/bin/bash

# Jenkins pytest安装脚本
# 用于在Jenkins环境中安装和配置pytest

set -e  # 遇到错误立即退出

echo "🔧 开始安装pytest和相关依赖..."

# 检查Python3是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装，正在安装..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
else
    echo "✅ Python3已安装: $(python3 --version)"
fi

# 检查pip是否安装
if ! command -v python3 -m pip &> /dev/null; then
    echo "❌ pip未安装，正在安装..."
    sudo apt-get install -y python3-pip
else
    echo "✅ pip已安装: $(python3 -m pip --version)"
fi

# 升级pip
echo "📦 升级pip..."
python3 -m pip install --upgrade pip

# 安装pytest
echo "📦 安装pytest..."
python3 -m pip install pytest==8.4.1

# 验证pytest安装
echo "🔍 验证pytest安装..."
if python3 -m pytest --version; then
    echo "✅ pytest安装成功"
else
    echo "❌ pytest安装失败"
    exit 1
fi

# 安装项目依赖
echo "📦 安装项目依赖..."
if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt
    echo "✅ 项目依赖安装完成"
else
    echo "⚠️ requirements.txt不存在，跳过项目依赖安装"
fi

# 验证关键依赖
echo "🔍 验证关键依赖..."
python3 -c "
import sys
print(f'Python版本: {sys.version}')

try:
    import pytest
    print(f'pytest版本: {pytest.__version__}')
except ImportError:
    print('❌ pytest导入失败')
    sys.exit(1)

try:
    import selenium
    print(f'Selenium版本: {selenium.__version__}')
except ImportError:
    print('⚠️ Selenium未安装')

try:
    import openpyxl
    print('OpenPyXL安装成功')
except ImportError:
    print('⚠️ OpenPyXL未安装')

try:
    import pymysql
    print('PyMySQL安装成功')
except ImportError:
    print('⚠️ PyMySQL未安装')

try:
    import allure
    print('Allure-pytest安装成功')
except ImportError:
    print('⚠️ Allure-pytest未安装')

print('✅ 依赖验证完成')
"

echo "🎉 pytest安装和配置完成！"
echo "📋 安装信息:"
echo "  - Python: $(python3 --version)"
echo "  - pip: $(python3 -m pip --version)"
echo "  - pytest: $(python3 -m pytest --version)"
echo "  - 工作目录: $(pwd)" 