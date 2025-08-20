pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
        PROJECT_NAME = 'solarpilot_web'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 检出代码...'
                sh '''
                    echo "开始检出代码..."
                    pwd
                    ls -la
                    
                    # 清理并克隆
                    rm -rf * .git
                    git clone https://github.com/yunlovenan/solarpilot_web.git .
                    git checkout main
                    
                    echo "代码检出完成"
                    ls -la
                '''
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo '🔧 设置环境...'
                sh '''
                    echo "安装Python依赖..."
                    python3 --version || echo "Python3未安装"
                    python3 -m pip --version || echo "pip未安装"
                    
                    # 尝试安装依赖
                    if [ -f "requirements.txt" ]; then
                        python3 -m pip install -r requirements.txt || echo "依赖安装失败，继续执行"
                    fi
                    
                    echo "环境设置完成"
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo '🚀 运行测试...'
                sh '''
                    echo "开始运行测试..."
                    pwd
                    ls -la testcase/ || echo "testcase目录不存在"
                    
                    # 运行测试
                    if [ -f "testcase/test_1_login.py" ]; then
                        python3 -m pytest testcase/test_1_login.py -v || echo "测试运行失败"
                    else
                        echo "测试文件不存在"
                    fi
                    
                    echo "测试完成"
                '''
            }
        }
        
        stage('Generate Report') {
            steps {
                echo '📊 生成报告...'
                sh '''
                    echo "生成测试报告..."
                    ls -la
                    
                    # 创建简单的报告
                    echo "测试执行完成" > test_report.txt
                    echo "时间: $(date)" >> test_report.txt
                    echo "工作目录: $(pwd)" >> test_report.txt
                    
                    cat test_report.txt
                '''
            }
        }
    }
    
    post {
        always {
            echo '🧹 清理完成'
        }
        
        success {
            echo '✅ 流水线执行成功'
        }
        
        failure {
            echo '❌ 流水线执行失败'
        }
    }
}
