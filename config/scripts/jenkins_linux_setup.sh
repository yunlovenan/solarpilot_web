#!/bin/bash

# Jenkins Linux环境设置脚本
# 解决权限问题，自动安装Chrome和ChromeDriver

set -e  # 遇到错误立即退出

echo "🚀 开始设置Jenkins Linux环境..."

# 显示系统信息
echo "=== 系统信息 ==="
uname -a
echo "=== 当前用户 ==="
whoami
echo "=== 当前目录 ==="
pwd
echo "=== Python版本 ==="
python3 --version

# 检查是否有sudo权限
if sudo -n true 2>/dev/null; then
    echo "✅ 有sudo权限，可以安装系统包"
    HAS_SUDO=true
else
    echo "⚠️ 没有sudo权限，将使用其他方法"
    HAS_SUDO=false
fi

# 创建虚拟环境
echo "📦 创建Python虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 升级pip
echo "⬆️ 升级pip..."
python3 -m pip install --upgrade pip

# 安装Python依赖
echo "📚 安装Python依赖..."
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 尝试安装Chrome和ChromeDriver
if [ "$HAS_SUDO" = true ]; then
    echo "🔧 尝试安装Chrome和ChromeDriver..."
    
    # 更新包列表
    sudo apt-get update || echo "⚠️ apt-get update失败，继续..."
    
    # 尝试安装Chrome
    if ! command -v google-chrome &> /dev/null; then
        echo "📥 安装Chrome..."
        sudo apt-get install -y google-chrome-stable || echo "⚠️ Chrome安装失败"
    else
        echo "✅ Chrome已安装: $(google-chrome --version)"
    fi
    
    # 尝试安装ChromeDriver
    if ! command -v chromedriver &> /dev/null; then
        echo "📥 安装ChromeDriver..."
        sudo apt-get install -y chromium-chromedriver || echo "⚠️ ChromeDriver安装失败"
    else
        echo "✅ ChromeDriver已安装: $(chromedriver --version)"
    fi
else
    echo "⚠️ 无sudo权限，跳过系统包安装"
fi

# 检查Chrome和ChromeDriver状态
echo "🔍 检查Chrome状态..."
if command -v google-chrome &> /dev/null; then
    echo "✅ Chrome可用: $(google-chrome --version)"
else
    echo "❌ Chrome不可用"
fi

echo "🔍 检查ChromeDriver状态..."
if command -v chromedriver &> /dev/null; then
    echo "✅ ChromeDriver可用: $(chromedriver --version)"
else
    echo "❌ ChromeDriver不可用"
fi

# 清理旧的测试结果
echo "🧹 清理旧的测试结果..."
rm -rf ALLURE-RESULTS junit.xml allure-report allure_report

# 显示环境变量
echo "=== Jenkins环境变量 ==="
env | grep -E "(JENKINS|BUILD|WORKSPACE|JOB)" || echo "未设置Jenkins环境变量"

echo "✅ 环境设置完成！"
echo "💡 提示：如果没有Chrome/ChromeDriver，Selenium Manager会自动下载"
