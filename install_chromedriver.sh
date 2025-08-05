#!/bin/bash

# Jenkins ChromeDriver安装脚本
# 用于在Jenkins环境中安装和配置ChromeDriver

set -e  # 遇到错误立即退出

echo "🔧 开始安装ChromeDriver..."

# 检查Chrome是否安装
if ! command -v google-chrome &> /dev/null; then
    echo "❌ Chrome未安装，正在安装Chrome..."
    
    # 添加Google Chrome仓库
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
    
    # 更新包列表并安装Chrome
    sudo apt-get update
    sudo apt-get install -y google-chrome-stable
    
    echo "✅ Chrome安装完成"
else
    echo "✅ Chrome已安装: $(google-chrome --version)"
fi

# 检查ChromeDriver是否已安装
if command -v chromedriver &> /dev/null; then
    echo "✅ ChromeDriver已安装: $(chromedriver --version)"
    exit 0
fi

# 获取Chrome版本
CHROME_VERSION=$(google-chrome --version | grep -oE "[0-9]+\.[0-9]+\.[0-9]+")
echo "检测到Chrome版本: $CHROME_VERSION"

# 获取Chrome主版本号
MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d. -f1)
echo "Chrome主版本: $MAJOR_VERSION"

# 获取对应的ChromeDriver版本
echo "获取ChromeDriver版本..."
CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$MAJOR_VERSION")

if [ -z "$CHROMEDRIVER_VERSION" ]; then
    echo "❌ 无法获取ChromeDriver版本"
    exit 1
fi

echo "下载ChromeDriver版本: $CHROMEDRIVER_VERSION"

# 下载ChromeDriver
echo "下载ChromeDriver..."
wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"

# 解压并安装
echo "安装ChromeDriver..."
sudo unzip /tmp/chromedriver.zip -d /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

# 清理临时文件
rm /tmp/chromedriver.zip

# 验证安装
if command -v chromedriver &> /dev/null; then
    echo "✅ ChromeDriver安装成功: $(chromedriver --version)"
    
    # 测试ChromeDriver
    echo "测试ChromeDriver..."
    chromedriver --version
    
    echo "🎉 ChromeDriver安装和配置完成！"
else
    echo "❌ ChromeDriver安装失败"
    exit 1
fi 