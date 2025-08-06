#!/bin/bash

# Docker容器中运行测试的脚本
# 解决文件路径和目录问题

echo "🐳 Docker测试运行工具"
echo "======================"

# 检查当前目录
echo "📋 当前环境:"
echo "  当前目录: $(pwd)"
echo "  当前用户: $(whoami)"
echo "  虚拟环境: $VIRTUAL_ENV"

# 查找项目目录
echo ""
echo "🔍 查找项目目录..."
if [ -d "/var/jenkins_home/workspace/solar_web" ]; then
    echo "✅ 找到Jenkins工作目录"
    cd /var/jenkins_home/workspace/solar_web
elif [ -d "/app" ]; then
    echo "✅ 找到应用目录"
    cd /app
elif [ -d "/workspace" ]; then
    echo "✅ 找到工作空间目录"
    cd /workspace
else
    echo "❌ 未找到项目目录，尝试查找..."
    find / -name "testcase" -type d 2>/dev/null | head -5
    echo "请手动切换到项目目录"
    exit 1
fi

echo "📁 切换到项目目录: $(pwd)"

# 检查项目文件
echo ""
echo "📁 检查项目文件..."
if [ -d "testcase" ]; then
    echo "✅ testcase目录存在"
    ls -la testcase/
else
    echo "❌ testcase目录不存在"
    echo "当前目录内容:"
    ls -la
    exit 1
fi

# 检查虚拟环境
echo ""
echo "🔧 检查虚拟环境..."
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ 虚拟环境已激活: $VIRTUAL_ENV"
else
    echo "⚠️ 虚拟环境未激活，尝试激活..."
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        echo "✅ 虚拟环境已激活"
    else
        echo "❌ 虚拟环境不存在，创建新的虚拟环境..."
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements_docker.txt
        echo "✅ 虚拟环境创建并激活完成"
    fi
fi

# 安装依赖
echo ""
echo "📦 检查依赖..."
python3 -c "import allure; print('✅ allure-pytest已安装')" 2>/dev/null || {
    echo "📦 安装allure-pytest..."
    pip install allure-pytest
}

# 清理旧结果
echo ""
echo "🧹 清理旧结果..."
rm -rf ALLURE-RESULTS allure-results allure-report
mkdir -p ALLURE-RESULTS

# 运行测试
echo ""
echo "🚀 运行测试..."
echo "测试文件检查:"
for test_file in testcase/test_minimal_allure.py testcase/test_simple_allure.py testcase/test_basic_allure.py testcase/test_1_login.py; do
    if [ -f "$test_file" ]; then
        echo "  ✅ $test_file 存在"
    else
        echo "  ❌ $test_file 不存在"
    fi
done

# 尝试运行不同的测试文件
if [ -f "testcase/test_minimal_allure.py" ]; then
    echo "运行 test_minimal_allure.py..."
    python3 -m pytest testcase/test_minimal_allure.py -v --alluredir=ALLURE-RESULTS --junitxml=junit.xml --tb=short
elif [ -f "testcase/test_simple_allure.py" ]; then
    echo "运行 test_simple_allure.py..."
    python3 -m pytest testcase/test_simple_allure.py -v --alluredir=ALLURE-RESULTS --junitxml=junit.xml --tb=short
elif [ -f "testcase/test_basic_allure.py" ]; then
    echo "运行 test_basic_allure.py..."
    python3 -m pytest testcase/test_basic_allure.py -v --alluredir=ALLURE-RESULTS --junitxml=junit.xml --tb=short
elif [ -f "testcase/test_1_login.py" ]; then
    echo "运行 test_1_login.py..."
    python3 -m pytest testcase/test_1_login.py -v --alluredir=ALLURE-RESULTS --junitxml=junit.xml --tb=short
else
    echo "❌ 没有找到可用的测试文件"
    echo "当前testcase目录内容:"
    ls -la testcase/
    exit 1
fi

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
echo "🎉 测试运行完成！" 