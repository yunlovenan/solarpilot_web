#!/bin/bash

echo "🚀 启动Jenkins Agent (简化版)..."

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未运行，请先启动Docker"
    exit 1
fi

# 检查Jenkins master是否运行
if ! docker ps | grep -q jenkins_mayun; then
    echo "⚠️  Jenkins master未运行，请先启动Jenkins"
    echo "   使用: docker start jenkins_mayun"
    exit 1
fi

echo "✅ Jenkins master正在运行"

# 检查agent.jar是否存在
if [ ! -f "../../agent.jar" ]; then
    echo "📥 下载Jenkins agent.jar..."
    cd ../..
    curl -sO http://localhost:8080/jnlpJars/agent.jar
    cd config/scripts
fi

# 创建Jenkins agent工作目录
echo "📁 创建Jenkins agent工作目录..."
cd ../..
mkdir -p jenkins_agent_simple_workspace
chmod 755 jenkins_agent_simple_workspace

# 启动Jenkins agent
echo "🚀 启动Jenkins agent..."
echo "Jenkins URL: http://localhost:8080"
echo "Agent Name: web"
echo "Work Directory: ./jenkins_agent_simple_workspace"
#创建节点后，修改secret即可
# 使用nohup在后台运行
nohup java -jar agent.jar \
    -url http://localhost:8080/ \
    -secret 6ff4d836bc146ac3fa99a2bc0f65256dad429f44a91a10ca942758d1ca40a372 \
    -name web \
    -webSocket \
    -workDir "./jenkins_agent_simple_workspace" \
    > jenkins_agent.log 2>&1 &

AGENT_PID=$!
echo "✅ Jenkins agent启动成功！PID: $AGENT_PID"
echo "📝 日志文件: jenkins_agent.log"
echo "🛑 停止agent: kill $AGENT_PID"
echo "📊 查看状态: ps aux | grep agent.jar"
