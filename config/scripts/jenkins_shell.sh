#!/bin/bash

# Jenkins Shell脚本 - 修复测试结果趋势显示问题

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
    echo "✅ Python脚本执行成功"
else
    echo "❌ Python脚本执行失败"
    exit 1
fi

# 检查JUnit XML文件
echo "📋 检查JUnit XML文件..."
if [ -f "junit.xml" ]; then
    echo "✅ junit.xml存在"
    echo "文件大小: $(du -h junit.xml | cut -f1)"
    echo "文件内容预览:"
    head -20 junit.xml
else
    echo "❌ junit.xml不存在"
    exit 1
fi

# 检查Allure结果
echo "📊 检查Allure结果..."
if [ -d "ALLURE-RESULTS" ]; then
    echo "✅ ALLURE-RESULTS目录存在"
    json_count=$(find ALLURE-RESULTS -name "*.json" | wc -l)
    echo "JSON文件数量: $json_count"
else
    echo "❌ ALLURE-RESULTS目录不存在"
fi

echo "🎉 Jenkins构建完成" 