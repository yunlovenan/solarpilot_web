#!/bin/bash

echo "🔍 Jenkins节点管理脚本"
echo "=========================="

# 检查Jenkins是否运行
echo "📊 检查Jenkins状态..."
if ! curl -s http://localhost:8080/ > /dev/null; then
    echo "❌ Jenkins未运行，请先启动Jenkins"
    exit 1
fi
echo "✅ Jenkins正在运行"

# 查看现有节点
echo ""
echo "📋 查看现有节点..."
echo "方法1: 通过浏览器访问 http://localhost:8080/computer/"
echo "方法2: 通过Jenkins CLI (需要认证)"

# 尝试通过API获取节点信息（可能需要认证）
echo ""
echo "🔐 尝试获取节点信息..."
NODES_INFO=$(curl -s http://localhost:8080/computer/api/json 2>/dev/null)
if [[ $? -eq 0 && -n "$NODES_INFO" ]]; then
    echo "✅ 成功获取节点信息:"
    echo "$NODES_INFO" | python3 -m json.tool 2>/dev/null || echo "$NODES_INFO"
else
    echo "⚠️  需要认证才能访问API"
    echo "请在浏览器中访问: http://localhost:8080/computer/"
fi

echo ""
echo "🚀 创建Appium节点指南:"
echo "=========================="
echo "1. 打开浏览器访问: http://localhost:8080/"
echo "2. 点击左侧菜单 'Manage Jenkins' (管理Jenkins)"
echo "3. 点击 'Manage Nodes and Clouds' (管理节点和云)"
echo "4. 点击 'New Node' (新建节点)"
echo "5. 填写节点信息:"
echo "   - Name: appium-node"
echo "   - Type: Permanent Agent"
echo "   - Description: Appium移动测试节点"
echo "   - # of executors: 2"
echo "   - Remote root directory: /appium/workspace"
echo "   - Labels: appium, mobile, android, ios"
echo "   - Usage: Use this node as much as possible"
echo "   - Launch method: Launch agent by connecting it to the master"
echo "6. 点击 'Save' (保存)"
echo "7. 复制生成的secret和agent.jar下载命令"

echo ""
echo "📱 Appium节点配置建议:"
echo "=========================="
echo "- 标签: appium, mobile, android, ios"
echo "- 执行器数量: 2-4"
echo "- 远程目录: /appium/workspace"
echo "- 启动方式: 通过WebSocket连接到master"

echo ""
echo "🔧 自动化创建节点 (需要Jenkins CLI):"
echo "=========================="
echo "如果需要自动化创建，可以使用Jenkins CLI:"
echo "1. 安装Jenkins CLI: wget http://localhost:8080/jnlpJars/jenkins-cli.jar"
echo "2. 创建节点配置文件"
echo "3. 使用命令: java -jar jenkins-cli.jar -s http://localhost:8080/ create-node appium-node < node-config.xml"

echo ""
echo "📝 当前Jenkins信息:"
echo "=========================="
echo "URL: http://localhost:8080"
echo "端口: 8080 (HTTP), 50000 (Agent)"
echo "状态: 运行中"
echo ""
echo "💡 提示: 建议通过Web界面手动创建节点，这样更直观且不容易出错"
