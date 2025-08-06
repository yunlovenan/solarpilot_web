#!/usr/bin/env python3
"""
Jenkins运行脚本 - 修复Allure报告问题
"""

import os
import subprocess
import sys
import shutil

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"🔧 {description}")
    print(f"执行命令: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print(f"输出: {result.stdout}")
        if result.stderr:
            print(f"错误: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始Jenkins构建...")
    
    # 显示当前目录
    print(f"📁 当前目录: {os.getcwd()}")
    run_command("ls -la", "显示当前目录内容")
    
    # 显示Python版本
    run_command("python3 --version", "显示Python版本")
    
    # 创建虚拟环境
    if not run_command("python3 -m venv venv", "创建虚拟环境"):
        print("⚠️ 虚拟环境可能已存在")
    
    # 激活虚拟环境
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
    else:  # Linux/Mac
        activate_cmd = "source venv/bin/activate"
    
    # 安装依赖
    install_cmd = f"{activate_cmd} && python3 -m pip install --upgrade pip"
    run_command(install_cmd, "升级pip")
    
    install_cmd = f"{activate_cmd} && pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/"
    run_command(install_cmd, "安装项目依赖")
    
    # 清理旧的测试结果
    print("🧹 清理旧的测试结果...")
    for dir_name in ['allure-results', 'ALLURE-RESULTS', 'allure-report', 'allure_report']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ 删除目录: {dir_name}")
    
    # 创建测试结果目录
    os.makedirs('allure_report', exist_ok=True)
    os.makedirs('ALLURE-RESULTS', exist_ok=True)
    print("✅ 创建测试结果目录")
    
    # 运行测试
    test_cmd = f"{activate_cmd} && python3 -m pytest testcase/test_1_login.py -v --alluredir=allure_report --junitxml=junit.xml --tb=short --no-cov --verbose"
    if run_command(test_cmd, "运行测试"):
        print("✅ 测试运行成功")
    else:
        print("❌ 测试运行失败")
        return 1
    
    # 检查JUnit XML文件
    print("📋 检查JUnit XML文件...")
    if os.path.exists('junit.xml'):
        size = os.path.getsize('junit.xml')
        print(f"✅ junit.xml存在，大小: {size} 字节")
        
        # 显示XML内容预览
        try:
            with open('junit.xml', 'r', encoding='utf-8') as f:
                content = f.read()
                print("📄 XML内容预览:")
                print(content[:500] + "..." if len(content) > 500 else content)
        except Exception as e:
            print(f"❌ 读取XML文件失败: {e}")
    else:
        print("❌ junit.xml不存在")
        return 1
    
    # 检查测试结果
    print("📊 检查测试结果...")
    if os.path.exists('allure_report'):
        json_files = [f for f in os.listdir('allure_report') if f.endswith('.json')]
        print(f"✅ 找到 {len(json_files)} 个测试结果文件")
        for file in json_files:
            print(f"  📄 {file}")
    else:
        print("❌ allure_report目录不存在")
    
    # 复制测试结果到ALLURE-RESULTS
    print("📋 复制测试结果到ALLURE-RESULTS...")
    if os.path.exists('allure_report'):
        try:
            for item in os.listdir('allure_report'):
                src = os.path.join('allure_report', item)
                dst = os.path.join('ALLURE-RESULTS', item)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                elif os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
            print("✅ 测试结果已复制到ALLURE-RESULTS")
        except Exception as e:
            print(f"❌ 复制失败: {e}")
    
    # 检查ALLURE-RESULTS目录
    if os.path.exists('ALLURE-RESULTS'):
        json_files = [f for f in os.listdir('ALLURE-RESULTS') if f.endswith('.json')]
        print(f"✅ ALLURE-RESULTS目录包含 {len(json_files)} 个JSON文件")
        for file in json_files:
            print(f"  📄 {file}")
    else:
        print("❌ ALLURE-RESULTS目录不存在")
    
    # 生成Allure报告
    print("📊 生成Allure报告...")
    allure_cmd = "allure generate ALLURE-RESULTS --clean -o allure-report"
    if run_command(allure_cmd, "生成Allure报告"):
        print("✅ Allure报告生成成功")
        
        # 检查报告
        if os.path.exists('allure-report/index.html'):
            print("✅ allure-report/index.html存在")
            size = os.path.getsize('allure-report/index.html')
            print(f"📏 index.html大小: {size} 字节")
        else:
            print("❌ allure-report/index.html不存在")
    else:
        print("❌ Allure报告生成失败")
    
    print("🎉 Jenkins构建完成")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 