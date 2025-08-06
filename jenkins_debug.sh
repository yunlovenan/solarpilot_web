#!/bin/bash

# Jenkins调试脚本
# 用于诊断Jenkins Allure问题

echo "🔍 Jenkins Allure调试工具"
echo "================================"

# 检查当前环境
echo "📋 环境信息:"
echo "  当前目录: $(pwd)"
echo "  Git版本: $(git rev-parse HEAD)"
echo "  当前分支: $(git branch --show-current)"
echo "  Python版本: $(python3 --version)"
echo "  Pytest版本: $(python3 -m pytest --version)"

# 检查测试文件
echo ""
echo "📁 测试文件检查:"
for test_file in testcase/test_minimal_allure.py testcase/test_simple_allure.py testcase/test_basic_allure.py; do
    if [ -f "$test_file" ]; then
        echo "  ✅ $test_file 存在"
    else
        echo "  ❌ $test_file 不存在"
    fi
done

# 清理旧结果
echo ""
echo "🧹 清理旧结果..."
rm -rf ALLURE-RESULTS allure-results allure-report
mkdir -p ALLURE-RESULTS

# 运行测试
echo ""
echo "🚀 运行测试..."
python3 -m pytest testcase/test_minimal_allure.py -v --alluredir=ALLURE-RESULTS --tb=short

# 检查结果
echo ""
echo "📊 检查测试结果..."
if [ -d "ALLURE-RESULTS" ]; then
    echo "  ✅ ALLURE-RESULTS目录存在"
    ls -la ALLURE-RESULTS/
    
    json_files=$(find ALLURE-RESULTS -name "*.json" | wc -l)
    echo "  📄 JSON文件数量: $json_files"
    
    if [ $json_files -gt 0 ]; then
        echo "  📄 JSON文件列表:"
        find ALLURE-RESULTS -name "*.json" -exec basename {} \;
        
        echo "  📄 第一个JSON文件内容预览:"
        first_json=$(find ALLURE-RESULTS -name "*.json" | head -1)
        if [ -n "$first_json" ]; then
            head -10 "$first_json"
        fi
    else
        echo "  ❌ 没有找到JSON文件"
    fi
else
    echo "  ❌ ALLURE-RESULTS目录不存在"
fi

# 生成报告
echo ""
echo "📊 生成Allure报告..."
if command -v allure &> /dev/null; then
    echo "  ✅ Allure已安装: $(allure --version)"
    
    if [ -d "ALLURE-RESULTS" ] && [ $(find ALLURE-RESULTS -name "*.json" | wc -l) -gt 0 ]; then
        allure generate ALLURE-RESULTS --clean -o allure-report
        
        if [ -d "allure-report" ]; then
            echo "  ✅ 报告生成成功"
            ls -la allure-report/
            
            if [ -f "allure-report/index.html" ]; then
                echo "  ✅ index.html存在"
                echo "  📏 报告大小: $(du -sh allure-report/)"
            else
                echo "  ❌ index.html不存在"
            fi
        else
            echo "  ❌ 报告生成失败"
        fi
    else
        echo "  ❌ 没有测试结果，无法生成报告"
    fi
else
    echo "  ❌ Allure未安装"
fi

echo ""
echo "🎉 调试完成！" 