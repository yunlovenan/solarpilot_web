# Jenkins Allure报告配置说明

## 问题描述
Jenkins构建成功，但Allure报告显示"ALLURE REPORT UNKNOWN"和"0 test cases"。

## 解决方案

### 1. Jenkins Allure插件配置

在Jenkins中配置Allure插件：

1. 进入 **Jenkins管理** → **全局工具配置**
2. 找到 **Allure Commandline** 部分
3. 添加新的Allure安装：
   - **名称**: Allure
   - **安装目录**: `/usr/local/bin/allure`
   - 勾选 **自动安装**

### 2. 项目配置

确保Jenkins项目配置中：

1. **构建后操作** → **Allure Report**
2. **Results path**: `allure-results`
3. **Report path**: `allure-report`

### 3. 目录结构

项目中的目录结构应该是：
```
solar_web/
├── allure-results/          # 测试结果（JSON文件）
├── allure-report/           # 生成的HTML报告
├── testcase/               # 测试用例
├── Jenkinsfile             # Jenkins流水线
└── jenkins_test_runner.py  # Jenkins测试运行器
```

### 4. 关键修复

#### 4.1 统一目录名称
- 测试结果目录：`allure-results`
- 报告目录：`allure-report`
- 归档目录：`allure-report/**/*`

#### 4.2 添加Allure插件后处理
在Jenkinsfile中添加：
```groovy
stage('Allure Report') {
    steps {
        echo '📊 生成Allure报告...'
        script {
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'allure-results']]
            ])
        }
    }
}
```

#### 4.3 专门的测试运行器
创建了`jenkins_test_runner.py`来：
- 设置Jenkins环境变量
- 清理旧的测试结果
- 运行测试并生成结果
- 生成Allure报告

### 5. 验证步骤

1. **检查测试结果文件**：
   ```bash
   ls -la allure-results/
   find allure-results -name "*.json"
   ```

2. **检查Allure报告**：
   ```bash
   ls -la allure-report/
   ```

3. **验证Jenkins插件**：
   - 确保Allure Jenkins Plugin已安装
   - 检查插件版本（推荐2.30.5+）

### 6. 常见问题

#### 6.1 报告显示"0 test cases"
- 检查`allure-results`目录是否有JSON文件
- 确认pytest正确生成了Allure结果
- 验证Allure插件配置

#### 6.2 报告显示"UNKNOWN"
- 检查Jenkins Allure插件配置
- 确认结果路径正确
- 验证Allure命令可用

#### 6.3 测试结果不显示
- 检查测试是否实际运行
- 确认测试生成了Allure结果
- 验证报告生成过程

### 7. 调试命令

```bash
# 检查Allure安装
allure --version

# 检查测试结果
ls -la allure-results/

# 手动生成报告
allure generate allure-results --clean -o allure-report

# 查看报告
allure serve allure-results
```

### 8. 配置检查清单

- [ ] Allure Jenkins Plugin已安装
- [ ] Allure Commandline工具已配置
- [ ] 项目构建后操作包含Allure Report
- [ ] 结果路径设置为`allure-results`
- [ ] Jenkinsfile包含Allure插件后处理步骤
- [ ] 测试正确生成Allure结果文件
- [ ] 目录名称统一（allure-results/allure-report）

按照以上配置，Allure报告应该能正确显示测试结果。 