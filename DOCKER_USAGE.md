# Docker环境中的Allure测试运行说明

## 问题分析

从你的终端输出可以看出：
1. ✅ `allure-pytest`插件已正确安装（显示`plugins: allure-pytest-2.15.0`）
2. ❌ 找不到测试文件：`ERROR: file or directory not found: testcase/test_1_login.py`
3. ❌ 当前在根目录`/`而不是项目目录

## 解决方案

### 方法1：使用自动修复脚本（推荐）

```bash
# 在Docker容器中执行
chmod +x docker_run_tests.sh
./docker_run_tests.sh
```

### 方法2：手动操作

```bash
# 1. 查找项目目录
find / -name "testcase" -type d 2>/dev/null

# 2. 切换到项目目录（通常是Jenkins工作目录）
cd /var/jenkins_home/workspace/solar_web

# 3. 检查文件
ls -la testcase/

# 4. 激活虚拟环境
source venv/bin/activate

# 5. 安装allure-pytest（如果还没安装）
pip install allure-pytest

# 6. 运行测试
python3 -m pytest testcase/test_minimal_allure.py -v --alluredir=ALLURE-RESULTS --junitxml=junit.xml --tb=short
```

### 方法3：使用Docker命令

```bash
# 进入Docker容器
docker exec -it --user root jenkins_mayun bash

# 切换到项目目录
cd /var/jenkins_home/workspace/solar_web

# 激活虚拟环境
source venv/bin/activate

# 运行测试
python3 -m pytest testcase/test_minimal_allure.py -v --alluredir=ALLURE-RESULTS --junitxml=junit.xml --tb=short
```

## 常见问题解决

### 问题1：找不到testcase目录
```bash
# 查找testcase目录
find / -name "testcase" -type d 2>/dev/null

# 或者查找项目文件
find / -name "*.py" -path "*/testcase/*" 2>/dev/null
```

### 问题2：虚拟环境未激活
```bash
# 检查虚拟环境
echo $VIRTUAL_ENV

# 激活虚拟环境
source venv/bin/activate

# 或者创建新的虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_docker.txt
```

### 问题3：allure-pytest未安装
```bash
# 安装allure-pytest
pip install allure-pytest

# 验证安装
python3 -c "import allure; print(f'Allure版本: {allure.__version__}')"
```

### 问题4：测试文件不存在
```bash
# 检查可用的测试文件
ls -la testcase/

# 运行存在的测试文件
python3 -m pytest testcase/test_1_login.py -v --alluredir=ALLURE-RESULTS --junitxml=junit.xml --tb=short
```

## 验证步骤

1. **检查环境**：
   ```bash
   pwd  # 应该在项目目录中
   ls -la testcase/  # 应该看到测试文件
   echo $VIRTUAL_ENV  # 应该显示虚拟环境路径
   ```

2. **运行测试**：
   ```bash
   python3 -m pytest testcase/test_minimal_allure.py -v --alluredir=ALLURE-RESULTS --junitxml=junit.xml --tb=short
   ```

3. **检查结果**：
   ```bash
   ls -la ALLURE-RESULTS/
   find ALLURE-RESULTS -name "*.json"
   ```

4. **生成报告**：
   ```bash
   allure generate ALLURE-RESULTS --clean -o allure-report
   ```

## 预期结果

成功运行后应该看到：
- ✅ 找到并运行测试文件
- ✅ 生成Allure结果文件
- ✅ 显示测试执行状态和结果
- ✅ 在`ALLURE-RESULTS`目录中生成JSON文件

## 故障排除

如果仍然有问题：

1. **检查Docker容器状态**：
   ```bash
   docker ps
   docker logs jenkins_mayun
   ```

2. **检查Jenkins工作目录**：
   ```bash
   ls -la /var/jenkins_home/workspace/
   ```

3. **重新进入容器**：
   ```bash
   docker exec -it --user root jenkins_mayun bash
   ```

按照这些步骤，应该能解决Docker环境中的Allure测试运行问题。 