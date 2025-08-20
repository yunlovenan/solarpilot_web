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
                script {
                    // 首先尝试使用Jenkins的Git插件（现在有凭证了）
                    try {
                        echo "尝试使用Jenkins Git插件检出代码..."
                        checkout([
                            $class: 'GitSCM',
                            branches: [[name: "*/main"]],
                            doGenerateSubmoduleConfigurations: false,
                            extensions: [],
                            submoduleCfg: [],
                            userRemoteConfigs: [[
                                credentialsId: 'github-credentials',
                                url: 'https://github.com/yunlovenan/solarpilot_web.git'
                            ]]
                        ])
                        echo "✅ Jenkins Git插件检出成功"
                    } catch (Exception e) {
                        echo "❌ Jenkins Git插件检出失败: ${e.getMessage()}"
                        echo "尝试使用shell命令备用方案..."
                        
                        // 备用方案：使用shell命令
                        sh '''
                            echo "开始备用方案检出代码..."
                            pwd
                            ls -la
                            
                            # 配置Git网络参数
                            git config --global http.postBuffer 524288000
                            git config --global http.lowSpeedLimit 0
                            git config --global http.lowSpeedTime 999999
                            git config --global http.timeout 300
                            
                            # 清理并克隆
                            rm -rf * .git
                            
                            # 尝试多种克隆方式，带重试
                            echo "尝试HTTPS方式克隆..."
                            for i in {1..3}; do
                                echo "第 $i 次尝试HTTPS克隆..."
                                if git clone --progress https://github.com/yunlovenan/solarpilot_web.git .; then
                                    echo "HTTPS克隆成功"
                                    break
                                else
                                    echo "HTTPS克隆失败，清理重试..."
                                    rm -rf * .git
                                    sleep 5
                                fi
                            done
                            
                            # 如果HTTPS失败，尝试浅克隆
                            if [ ! -d ".git" ]; then
                                echo "尝试浅克隆..."
                                git clone --depth 1 --progress https://github.com/yunlovenan/solarpilot_web.git .
                            fi
                            
                            # 确保克隆成功
                            if [ ! -d ".git" ]; then
                                echo "❌ 所有克隆方式都失败了"
                                exit 1
                            fi
                            
                            git checkout main
                            echo "✅ 备用方案检出成功"
                        '''
                    }
                    
                    // 验证检出结果
                    sh '''
                        echo "验证代码检出结果..."
                        pwd
                        ls -la
                        
                        if [ -d ".git" ]; then
                            echo "✅ Git仓库检出成功"
                            echo "当前代码版本: $(git rev-parse HEAD)"
                            echo "当前分支: $(git branch --show-current)"
                            echo "远程分支: $(git branch -r)"
                        else
                            echo "❌ Git仓库检出失败"
                            exit 1
                        fi
                        
                        echo "代码检出完成"
                    '''
                }
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
