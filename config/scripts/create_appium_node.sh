#!/bin/bash

echo "🚀 自动创建Appium节点脚本"
echo "=========================="

# 检查Jenkins是否运行
echo "📊 检查Jenkins状态..."
if ! curl -s http://localhost:8080/ > /dev/null; then
    echo "❌ Jenkins未运行，请先启动Jenkins"
    exit 1
fi
echo "✅ Jenkins正在运行"

# 下载Jenkins CLI
echo ""
echo "📥 下载Jenkins CLI..."
if [ ! -f "jenkins-cli.jar" ]; then
    curl -sO http://localhost:8080/jnlpJars/jenkins-cli.jar
    if [ $? -eq 0 ]; then
        echo "✅ Jenkins CLI下载成功"
    else
        echo "❌ Jenkins CLI下载失败"
        exit 1
    fi
else
    echo "✅ Jenkins CLI已存在"
fi

# 检查CLI文件
echo "📁 检查CLI文件..."
ls -la jenkins-cli.jar

# 创建Appium节点
echo ""
echo "🔧 创建Appium节点..."
if [ -f "config/scripts/appium-node-config.xml" ]; then
    echo "使用配置文件创建节点..."
    java -jar jenkins-cli.jar -s http://localhost:8080/ create-node appium-node < config/scripts/appium-node-config.xml
    
    if [ $? -eq 0 ]; then
        echo "✅ Appium节点创建成功！"
        echo ""
        echo "📋 节点信息:"
        echo "名称: appium-node"
        echo "标签: appium, mobile, android, ios"
        echo "执行器: 2"
        echo "工作目录: /appium/workspace"
        echo ""
        echo "🔗 查看节点: http://localhost:8080/computer/"
        echo ""
        echo "📱 启动Appium Agent:"
        echo "1. 在Jenkins中点击 'appium-node'"
        echo "2. 点击 'Launch agent' 或复制启动命令"
        echo "3. 使用提供的secret启动agent"
    else
        echo "❌ 节点创建失败，可能需要认证"
        echo ""
        echo "💡 手动创建方法:"
        echo "1. 访问: http://localhost:8080/computer/"
        echo "2. 点击 'New Node'"
        echo "3. 按配置创建节点"
    fi
else
    echo "❌ 配置文件不存在: config/scripts/appium-node-config.xml"
    exit 1
fi

echo ""
echo "🎯 下一步操作:"
echo "=========================="
echo "1. 在Jenkins中查看新创建的节点"
echo "2. 启动Appium Agent"
echo "3. 配置移动设备连接"
echo "4. 运行移动测试任务"
