#!/bin/bash

# Docker环境中的Allure修复脚本
# 用于解决pytest --alluredir参数不被识别的问题

echo "🔧 Docker环境Allure修复工具"
echo "================================"

# 检查当前环境
echo "📋 环境信息:"
echo "  当前目录: $(pwd)"
echo "  Python版本: $(python3 --version)"
echo "  Pytest版本: $(pytest --version)"

# 检查虚拟环境
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ 虚拟环境已激活: $VIRTUAL_ENV"
else
    echo "❌ 虚拟环境未激活"
    echo "请先激活虚拟环境:"
    echo "  source venv/bin/activate"
    exit 1
fi

# 安装allure-pytest插件
echo ""
echo "📦 安装allure-pytest插件..."
pip install allure-pytest

# 验证安装
echo ""
echo "🔍 验证安装..."
python3 -c "import allure; print(f'Allure版本: {allure.__version__}')"

# 检查pytest插件
echo ""
echo "📋 Pytest插件列表:"
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
    else
        echo "❌ 没有找到JSON文件"
    fi
else
    echo "❌ ALLURE-RESULTS目录不存在"
fi

echo ""
echo "🎉 修复完成！" 