#!/bin/bash

echo "🔧 Jenkins Agent 设置脚本"
echo "=========================="

# 检查Jenkins是否运行
if ! docker ps | grep -q jenkins_mayun; then
    echo "❌ Jenkins master未运行，请先启动Jenkins"
    exit 1
fi

echo "✅ Jenkins master正在运行"

# 提示用户手动创建节点
echo ""
echo "📋 请按以下步骤在Jenkins中创建节点："
echo "1. 打开浏览器访问: http://localhost:8080"
echo "2. 登录Jenkins"
echo "3. 进入 'Manage Jenkins' > 'Manage Nodes and Clouds'"
echo "4. 点击 'New Node'"
echo "5. 节点名称输入: web"
echo "6. 选择 'Permanent Agent'"
echo "7. 点击 'OK'"
echo "8. 在配置页面："
echo "   - Remote root directory: /tmp"
echo "   - Labels: web"
echo "   - Usage: Use this node as much as possible"
echo "9. 点击 'Save'"
echo ""

# 等待用户确认
read -p "完成节点创建后，按回车键继续..."

# 获取正确的secret
echo "🔍 获取节点secret..."
SECRET=$(curl -s http://localhost:8080/computer/web/slave-agent.jnlp | grep -o 'secret="[^"]*"' | cut -d'"' -f2)

if [ -z "$SECRET" ]; then
    echo "❌ 无法获取secret，请检查节点是否正确创建"
    exit 1
fi

echo "✅ 获取到secret: $SECRET"

# 创建启动脚本
echo "📝 创建启动脚本..."
cat > start_web_agent.sh << EOF
#!/bin/bash
echo "🚀 启动Jenkins Agent: web"
echo "Secret: $SECRET"

# 下载agent.jar（如果不存在）
if [ ! -f "agent.jar" ]; then
    echo "📥 下载agent.jar..."
    curl -sO http://localhost:8080/jnlpJars/agent.jar
fi

# 创建工作目录
mkdir -p jenkins_agent_workspace
chmod 755 jenkins_agent_workspace

# 启动agent
echo "🚀 启动agent..."
java -jar agent.jar \\
    -url http://localhost:8080/ \\
    -secret $SECRET \\
    -name web \\
    -webSocket \\
    -workDir "./jenkins_agent_workspace"
EOF

chmod +x start_web_agent.sh

echo "✅ 启动脚本已创建: start_web_agent.sh"
echo ""
echo "🚀 现在可以运行: ./start_web_agent.sh"
echo "📝 或者直接运行: java -jar agent.jar -url http://localhost:8080/ -secret $SECRET -name web -webSocket -workDir ./jenkins_agent_workspace"
