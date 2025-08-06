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
                
                // 确保使用最新代码
                sh '''
                    git fetch origin
                    git checkout main
                    git pull origin main
                    echo "当前代码版本: $(git rev-parse HEAD)"
                    echo "当前分支: $(git branch --show-current)"
                    echo "远程分支: $(git branch -r)"
                    echo "文件列表:"
                    ls -la testcase/
                '''
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
                            echo "安装Python3..."
                            sudo apt-get install -y python3 python3-pip
                        fi
                        
                        # 验证Python3安装
                        python3 --version
                        python3 -m pip --version
                        
                        # 安装Chrome浏览器
                        if ! command -v google-chrome &> /dev/null; then
                            echo "安装Chrome浏览器..."
                            wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
                            echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
                            sudo apt-get update
                            sudo apt-get install -y google-chrome-stable
                        fi
                        
                        # 验证Chrome安装
                        google-chrome --version
                        
                        # 检查架构并安装ChromeDriver
                        ARCH=$(uname -m)
                        echo "检测到架构: $ARCH"
                        
                        if [ "$ARCH" = "aarch64" ]; then
                            echo "🔧 ARM64架构，安装ChromeDriver..."
                            
                            # 检查ChromeDriver是否已安装
                            if ! command -v chromedriver &> /dev/null; then
                                echo "📦 安装ChromeDriver..."
                                
                                # 检测Chrome版本
                                CHROME_VERSION=$(google-chrome --version | grep -oE "[0-9]+\\.[0-9]+\\.[0-9]+")
                                echo "检测到Chrome版本: $CHROME_VERSION"
                                
                                # 获取Chrome主版本号
                                MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d. -f1)
                                echo "Chrome主版本: $MAJOR_VERSION"
                                
                                # 获取对应的ChromeDriver版本
                                echo "获取ChromeDriver版本..."
                                CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$MAJOR_VERSION")
                                
                                if [ -n "$CHROMEDRIVER_VERSION" ]; then
                                    echo "下载ChromeDriver版本: $CHROMEDRIVER_VERSION"
                                    
                                    # 下载ChromeDriver
                                    echo "下载ChromeDriver..."
                                    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
                                    
                                    # 解压并安装
                                    echo "安装ChromeDriver..."
                                    sudo unzip /tmp/chromedriver.zip -d /usr/local/bin/
                                    sudo chmod +x /usr/local/bin/chromedriver
                                    rm /tmp/chromedriver.zip
                                    
                                    echo "✅ ChromeDriver安装完成: $(chromedriver --version)"
                                else
                                    echo "❌ 无法获取ChromeDriver版本"
                                    exit 1
                                fi
                            else
                                echo "✅ ChromeDriver已安装: $(chromedriver --version)"
                            fi
                        else
                            echo "✅ x86_64架构，使用Selenium Manager自动管理ChromeDriver"
                        fi
                    '''
                    
                    // 安装Python依赖
                    sh '''
                        echo "📦 安装Python依赖..."
                        
                        # 升级pip
                        python3 -m pip install --upgrade pip
                        echo "✅ pip升级完成"
                        
                        # 显示当前pip版本
                        python3 -m pip --version
                        
                        # 安装requirements.txt中的依赖
                        echo "安装项目依赖..."
                        python3 -m pip install -r requirements.txt
                        echo "✅ 项目依赖安装完成"
                        
                        # 单独安装pytest（确保安装成功）
                        echo "安装pytest..."
                        python3 -m pip install pytest==8.4.1
                        echo "✅ pytest安装完成"
                        
                        # 验证pytest安装
                        echo "验证pytest安装..."
                        python3 -m pytest --version
                        echo "✅ pytest验证成功"
                        
                        # 验证其他关键依赖
                        echo "验证其他依赖..."
                        python3 -c "import selenium; print(f'Selenium版本: {selenium.__version__}')"
                        python3 -c "import openpyxl; print('OpenPyXL安装成功')"
                        python3 -c "import pymysql; print('PyMySQL安装成功')"
                        python3 -c "import allure; print('Allure-pytest安装成功')"
                        echo "✅ 所有依赖验证完成"
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
                    env.JENKINS_URL = 'true'
                    env.BUILD_NUMBER = '1'
                    
                    // 运行测试
                    sh '''
                        echo "开始运行测试..."
                        echo "当前工作目录: $(pwd)"
                        echo "当前代码版本: $(git rev-parse HEAD)"
                        
                        # 显示pytest版本和位置
                        which python3
                        python3 -m pytest --version
                        
                        # 清理旧的测试结果
                        rm -rf allure-results ALLURE-RESULTS allure-report
                        mkdir -p ALLURE-RESULTS
                        
                        # 强制运行我们的最小测试
                        echo "强制运行test_minimal_allure.py..."
                        python3 -m pytest testcase/test_minimal_allure.py -v --alluredir=ALLURE-RESULTS --junitxml=junit.xml --tb=short --no-cov
                        
                        # 如果上面的测试不存在，运行简单测试
                        if [ ! -f "testcase/test_minimal_allure.py" ]; then
                            echo "test_minimal_allure.py不存在，运行test_simple_allure.py..."
                            python3 -m pytest testcase/test_simple_allure.py -v --alluredir=ALLURE-RESULTS --junitxml=junit.xml --tb=short --no-cov
                        fi
                        
                        # 如果上面的测试都不存在，运行基础测试
                        if [ ! -f "testcase/test_simple_allure.py" ]; then
                            echo "test_simple_allure.py不存在，运行test_basic_allure.py..."
                            python3 -m pytest testcase/test_basic_allure.py -v --alluredir=ALLURE-RESULTS --junitxml=junit.xml --tb=short --no-cov
                        fi
                        
                        echo "测试运行完成"
                        
                        # 检查生成的测试结果
                        echo "检查测试结果..."
                        ls -la ALLURE-RESULTS/ || echo "ALLURE-RESULTS目录不存在"
                        find ALLURE-RESULTS -name "*.json" | head -5
                        
                        # 显示测试结果统计
                        echo "测试结果统计:"
                        find ALLURE-RESULTS -name "*.json" | wc -l
                        
                        # 显示测试结果内容
                        echo "测试结果内容:"
                        for file in ALLURE-RESULTS/*.json; do
                            if [ -f "$file" ]; then
                                echo "文件: $file"
                                head -5 "$file"
                            fi
                        done
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
                        echo "生成Allure报告..."
                        
                        # 检查allure命令
                        if command -v allure &> /dev/null; then
                            echo "✅ Allure已安装: $(allure --version)"
                            
                            # 检查测试结果目录
                            if [ -d "ALLURE-RESULTS" ]; then
                                echo "✅ 找到测试结果目录"
                                ls -la ALLURE-RESULTS/
                                
                                # 生成Allure报告
                                allure generate ALLURE-RESULTS --clean -o allure-report
                                
                                if [ $? -eq 0 ]; then
                                    echo "✅ Allure报告生成成功"
                                    ls -la allure-report/
                                else
                                    echo "❌ Allure报告生成失败"
                                fi
                            else
                                echo "❌ 测试结果目录不存在"
                            fi
                        else
                            echo "❌ Allure未安装"
                            
                            # 尝试安装Allure
                            echo "尝试安装Allure..."
                            curl -o allure-2.24.1.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.24.1/allure-commandline-2.24.1.tgz
                            sudo tar -zxvf allure-2.24.1.tgz -C /opt/
                            sudo ln -s /opt/allure-2.24.1/bin/allure /usr/local/bin/allure
                            rm allure-2.24.1.tgz
                            
                                                            # 重新生成报告
                                if command -v allure &> /dev/null; then
                                    echo "✅ Allure安装成功，重新生成报告"
                                    allure generate ALLURE-RESULTS --clean -o allure-report
                                fi
                        fi
                        
                        # 检查生成的报告
                        if [ -d "allure-report" ]; then
                            echo "✅ 报告目录存在"
                            ls -la allure-report/
                            if [ -f "allure-report/index.html" ]; then
                                echo "✅ index.html存在"
                                echo "报告大小: $(du -sh allure-report/)"
                            else
                                echo "❌ index.html不存在"
                            fi
                        else
                            echo "❌ 报告目录不存在"
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
                    archiveArtifacts artifacts: 'allure-report/**/*', fingerprint: true
                    archiveArtifacts artifacts: 'result/logs/*.log', fingerprint: true
                    archiveArtifacts artifacts: 'result/error_image/*.png', fingerprint: true
                }
            }
        }
        
        stage('Allure Report') {
            steps {
                echo '📊 生成Allure报告...'
                script {
                    // 使用Allure插件生成报告
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'ALLURE-RESULTS']]
                    ])
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