# Jenkins 本地Chrome测试配置

## 概述

本项目支持在Jenkins环境中使用本地Chrome浏览器进行自动化测试，具有以下特性：

- **自动环境检测**: 自动识别本地环境和Jenkins环境
- **智能模式切换**: 本地环境使用有头模式，Jenkins环境使用无头模式
- **性能优化**: 针对不同环境提供最优的Chrome配置

## 环境要求

### Jenkins Agent 要求

1. **操作系统**: Linux/Ubuntu (推荐) 或 macOS
2. **Python**: 3.8+ 
3. **Chrome**: 最新稳定版本
4. **ChromeDriver**: 与Chrome版本匹配

### 安装步骤

#### 1. 安装Chrome

```bash
# Ubuntu/Debian
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update
sudo apt-get install google-chrome-stable

# CentOS/RHEL
sudo yum install -y google-chrome-stable
```

#### 2. 安装ChromeDriver

```bash
# 下载ChromeDriver
wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE
CHROME_VERSION=$(cat LATEST_RELEASE)
wget https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip

# 解压并安装
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

# 验证安装
chromedriver --version
```

#### 3. 安装Python依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装项目依赖
pip install -r requirements.txt
```

## 配置说明

### 环境变量检测

系统会自动检测以下Jenkins环境变量：

- `JENKINS_URL`: Jenkins服务器URL
- `BUILD_NUMBER`: 构建编号
- `BUILD_ID`: 构建ID
- `WORKSPACE`: 工作空间路径
- `JOB_NAME`: 任务名称

### 模式说明

#### 有头模式 (本地环境)
- 显示浏览器窗口
- 便于调试和观察
- 适合本地开发和测试

#### 无头模式 (Jenkins环境)
- 浏览器在后台运行
- 不显示窗口，节省资源
- 适合CI/CD环境

## 使用方法

### 1. 在Jenkins中创建Pipeline任务

1. 创建新的Pipeline任务
2. 选择"Pipeline script from SCM"
3. 配置Git仓库信息
4. 指定Jenkinsfile路径: `config/jenkins/Jenkinsfile.local_chrome`

### 2. 运行测试

Pipeline会自动：
1. 检测环境
2. 安装依赖
3. 选择合适的Chrome模式
4. 执行测试
5. 生成报告

### 3. 查看结果

- **测试结果**: Jenkins JUnit插件
- **HTML报告**: 项目内置测试报告
- **Allure报告**: 详细的测试分析报告

## 故障排除

### 常见问题

#### 1. Chrome启动失败

```bash
# 检查Chrome安装
google-chrome --version

# 检查ChromeDriver版本
chromedriver --version

# 检查权限
ls -la /usr/local/bin/chromedriver
```

#### 2. 无头模式问题

```bash
# 检查环境变量
env | grep -i jenkins

# 手动设置环境变量测试
export JENKINS_URL=http://localhost:8080
export BUILD_NUMBER=123
python3 -c "from common.local_browser import local_chrome_manager; print(local_chrome_manager.is_jenkins)"
```

#### 3. 权限问题

```bash
# 确保ChromeDriver可执行
sudo chmod +x /usr/local/bin/chromedriver

# 检查用户权限
whoami
groups
```

### 调试技巧

1. **查看日志**: 检查Jenkins控制台输出
2. **环境检查**: 在Pipeline中添加环境信息输出
3. **手动测试**: 在Jenkins Agent上手动运行测试命令

## 性能优化

### 无头模式优化

- 禁用图片加载: `--disable-images`
- 禁用JavaScript: `--disable-javascript` (如果不需要)
- 禁用CSS: `--disable-css` (如果不需要)
- 禁用GPU: `--disable-gpu`

### 资源管理

- 设置合理的超时时间
- 及时清理浏览器实例
- 使用虚拟环境隔离依赖

## 扩展功能

### 1. 多浏览器支持

可以扩展支持Firefox、Safari等浏览器

### 2. 并行测试

使用pytest-xdist进行并行测试执行

### 3. 测试报告集成

集成Allure、HTMLTestRunner等报告工具

## 联系支持

如有问题，请检查：
1. 环境配置是否正确
2. 依赖版本是否匹配
3. 权限设置是否合适
4. 日志输出中的错误信息
