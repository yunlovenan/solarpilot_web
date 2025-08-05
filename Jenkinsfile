pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.13'
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
                    // 安装Python依赖
                    sh '''
                        python3 -m pip install --upgrade pip
                        python3 -m pip install -r requirements.txt
                    '''
                    
                    // 安装Chrome和ChromeDriver（如果需要）
                    sh '''
                        # 检查Chrome是否已安装
                        if ! command -v google-chrome &> /dev/null; then
                            echo "安装Chrome浏览器..."
                            # 这里可以根据系统添加Chrome安装命令
                        fi
                        
                        # 检查ChromeDriver是否已安装
                        if ! command -v chromedriver &> /dev/null; then
                            echo "安装ChromeDriver..."
                            # 这里可以根据系统添加ChromeDriver安装命令
                        fi
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
                        python3 jenkins_run.py
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
                    archiveArtifacts artifacts: 'test_reports/*.html', fingerprint: true
                    archiveArtifacts artifacts: 'allure_report/**/*', fingerprint: true
                    archiveArtifacts artifacts: 'result/logs/*.log', fingerprint: true
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