#!/bin/bash

# Docker环境设置脚本
# 用于在Docker容器中正确设置Allure环境

echo "🐳 Docker环境设置工具"
echo "========================"

# 检查是否在Docker容器中
if [ -f /.dockerenv ]; then
    echo "✅ 检测到Docker容器环境"
else
    echo "⚠️ 未检测到Docker容器环境"
fi

# 创建虚拟环境
echo ""
echo "📦 创建虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
echo ""
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo ""
echo "⬆️ 升级pip..."
pip install --upgrade pip

# 安装依赖
echo ""
echo "📦 安装Python依赖..."
pip install -r requirements_docker.txt

# 验证安装
echo ""
echo "🔍 验证安装..."
python3 -c "import pytest; print(f'Pytest版本: {pytest.__version__}')"
python3 -c "import allure; print(f'Allure版本: {allure.__version__}')"
python3 -c "import selenium; print(f'Selenium版本: {selenium.__version__}')"

# 检查pytest插件
echo ""
echo "📋 Pytest插件检查..."
pytest --version

# 测试allure参数
echo ""
echo "🧪 测试allure参数..."
pytest --help | grep -i allure || echo "allure参数不可用"

# 创建测试目录
echo ""
echo "📁 创建测试目录..."
mkdir -p ALLURE-RESULTS

# 运行测试
echo ""
echo "🚀 运行测试..."
python3 -m pytest testcase/test_minimal_allure.py -v --alluredir=ALLURE-RESULTS --tb=short

# 检查结果
echo ""
echo "📊 检查测试结果..."
if [ -d "ALLURE-RESULTS" ]; then
    echo "✅ ALLURE-RESULTS目录存在"
    ls -la ALLURE-RESULTS/
    
    json_files=$(find ALLURE-RESULTS -name "*.json" | wc -l)
    echo "📄 JSON文件数量: $json_files"
    
    if [ $json_files -gt 0 ]; then
        echo "📄 JSON文件列表:"
        find ALLURE-RESULTS -name "*.json" -exec basename {} \;
        
        echo "📄 第一个JSON文件内容预览:"
        first_json=$(find ALLURE-RESULTS -name "*.json" | head -1)
        if [ -n "$first_json" ]; then
            head -5 "$first_json"
        fi
    else
        echo "❌ 没有找到JSON文件"
    fi
else
    echo "❌ ALLURE-RESULTS目录不存在"
fi

echo ""
echo "🎉 Docker环境设置完成！"
echo ""
echo "💡 使用说明:"
echo "1. 激活虚拟环境: source venv/bin/activate"
echo "2. 运行测试: python3 -m pytest testcase/test_minimal_allure.py -v --alluredir=ALLURE-RESULTS"
echo "3. 生成报告: allure generate ALLURE-RESULTS --clean -o allure-report" 