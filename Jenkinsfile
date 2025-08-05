pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
        PROJECT_NAME = 'solar_web'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 检出代码...'
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo '🔧 设置环境...'
                script {
                    // 使用sudo权限安装系统依赖
                    sh '''
                        # 更新包管理器
                        sudo apt-get update || true
                        
                        # 安装Python3和pip（如果需要）
                        if ! command -v python3 &> /dev/null; then
                            sudo apt-get install -y python3 python3-pip
                        fi
                        
                        # 安装Chrome浏览器
                        if ! command -v google-chrome &> /dev/null; then
                            echo "安装Chrome浏览器..."
                            wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
                            echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
                            sudo apt-get update
                            sudo apt-get install -y google-chrome-stable
                        fi
                        
                        # 安装ChromeDriver
                        if ! command -v chromedriver &> /dev/null; then
                            echo "安装ChromeDriver..."
                            CHROME_VERSION=$(google-chrome --version | grep -oE "[0-9]+\\.[0-9]+\\.[0-9]+")
                            CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
                            wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
                            sudo unzip /tmp/chromedriver.zip -d /usr/local/bin/
                            sudo chmod +x /usr/local/bin/chromedriver
                            rm /tmp/chromedriver.zip
                        fi
                        
                        # 安装Allure
                        if ! command -v allure &> /dev/null; then
                            echo "安装Allure..."
                            curl -o allure-2.24.1.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.24.1/allure-commandline-2.24.1.tgz
                            sudo tar -zxvf allure-2.24.1.tgz -C /opt/
                            sudo ln -s /opt/allure-2.24.1/bin/allure /usr/local/bin/allure
                            rm allure-2.24.1.tgz
                        fi
                    '''
                    
                    // 安装Python依赖
                    sh '''
                        python3 -m pip install --upgrade pip
                        python3 -m pip install -r requirements.txt
                        
                        # 验证pytest安装
                        python3 -m pytest --version
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                echo '🚀 运行自动化测试...'
                script {
                    // 设置显示变量（用于无头模式）
                    env.DISPLAY = ':99'
                    env.CHROME_HEADLESS = 'true'
                    
                    // 运行测试
                    sh '''
                        # 使用python3 -m pytest确保命令可用
                        python3 -m pytest testcase/ -v --alluredir=allure_report --junitxml=junit.xml
                    '''
                }
            }
        }
        
        stage('Generate Reports') {
            steps {
                echo '📊 生成测试报告...'
                script {
                    // 生成Allure报告
                    sh '''
                        if command -v allure &> /dev/null; then
                            allure generate allure_report --clean
                        else
                            echo "Allure未安装，跳过报告生成"
                        fi
                    '''
                }
            }
        }
        
        stage('Archive Results') {
            steps {
                echo '📦 归档测试结果...'
                script {
                    // 归档测试报告
                    archiveArtifacts artifacts: 'junit.xml', fingerprint: true
                    archiveArtifacts artifacts: 'allure_report/**/*', fingerprint: true
                    archiveArtifacts artifacts: 'result/logs/*.log', fingerprint: true
                    archiveArtifacts artifacts: 'result/error_image/*.png', fingerprint: true
                }
            }
        }
    }
    
    post {
        always {
            echo '🧹 清理工作空间...'
            cleanWs()
        }
        
        success {
            echo '✅ 测试成功完成'
            script {
                // 可以在这里添加成功通知
                emailext (
                    subject: "✅ ${env.JOB_NAME} - 构建成功",
                    body: "构建 ${env.BUILD_NUMBER} 成功完成\n\n查看详情: ${env.BUILD_URL}",
                    to: "${env.BUILD_USER_EMAIL}"
                )
            }
        }
        
        failure {
            echo '❌ 测试失败'
            script {
                // 可以在这里添加失败通知
                emailext (
                    subject: "❌ ${env.JOB_NAME} - 构建失败",
                    body: "构建 ${env.BUILD_NUMBER} 失败\n\n查看详情: ${env.BUILD_URL}",
                    to: "${env.BUILD_USER_EMAIL}"
                )
            }
        }
        
        unstable {
            echo '⚠️ 测试不稳定'
        }
    }
} 