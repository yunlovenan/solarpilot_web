#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Allure报告修复脚本
用于诊断和修复Jenkins中的Allure报告问题
"""

import os
import sys
import subprocess
import json
import glob
from pathlib import Path

def check_allure_results():
    """检查Allure结果目录"""
    print("🔍 检查Allure结果目录...")
    
    allure_dirs = ['allure_report', 'allure-results']
    for dir_name in allure_dirs:
        if os.path.exists(dir_name):
            print(f"✅ 找到目录: {dir_name}")
            files = os.listdir(dir_name)
            print(f"   文件数量: {len(files)}")
            
            # 检查JSON文件
            json_files = glob.glob(f"{dir_name}/*.json")
            print(f"   JSON文件数量: {len(json_files)}")
            
            if json_files:
                print("   最新的JSON文件:")
                for json_file in json_files[:3]:
                    print(f"     - {json_file}")
                    
                    # 读取JSON内容
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            status = data.get('status', 'unknown')
                            name = data.get('name', 'unknown')
                            print(f"       状态: {status}, 名称: {name}")
                    except Exception as e:
                        print(f"       读取失败: {e}")
        else:
            print(f"❌ 目录不存在: {dir_name}")

def generate_test_results():
    """生成测试结果"""
    print("🚀 生成测试结果...")
    
    # 创建测试结果目录
    os.makedirs('allure-results', exist_ok=True)
    
    # 运行一个简单的测试
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest',
            'testcase/test_1_login.py::TestLogin::test_login_pass',
            '-v',
            '--alluredir=allure-results',
            '--tb=short'
        ], capture_output=True, text=True)
        
        print(f"测试退出码: {result.returncode}")
        if result.stdout:
            print("测试输出:")
            print(result.stdout)
        if result.stderr:
            print("测试错误:")
            print(result.stderr)
            
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 运行测试失败: {e}")
        return False

def generate_allure_report():
    """生成Allure报告"""
    print("📊 生成Allure报告...")
    
    try:
        # 检查allure命令
        result = subprocess.run(['allure', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Allure版本: {result.stdout.strip()}")
        else:
            print("❌ Allure未安装")
            return False
        
        # 生成报告
        result = subprocess.run([
            'allure', 'generate', 'allure-results', '--clean'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Allure报告生成成功")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ Allure报告生成失败")
            if result.stderr:
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 生成Allure报告失败: {e}")
        return False

def check_jenkins_environment():
    """检查Jenkins环境"""
    print("🔧 检查Jenkins环境...")
    
    jenkins_vars = [
        'JENKINS_URL',
        'BUILD_NUMBER',
        'WORKSPACE',
        'JOB_NAME'
    ]
    
    for var in jenkins_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: 未设置")
    
    # 检查当前目录
    print(f"当前工作目录: {os.getcwd()}")
    
    # 检查文件权限
    test_dirs = ['allure-results', 'allure_report']
    for dir_name in test_dirs:
        if os.path.exists(dir_name):
            try:
                test_file = os.path.join(dir_name, 'test_write.tmp')
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                print(f"✅ {dir_name} 目录可写")
            except Exception as e:
                print(f"❌ {dir_name} 目录不可写: {e}")

def main():
    """主函数"""
    print("=" * 50)
    print("🔧 Allure报告诊断和修复工具")
    print("=" * 50)
    
    # 1. 检查Jenkins环境
    check_jenkins_environment()
    print()
    
    # 2. 检查现有结果
    check_allure_results()
    print()
    
    # 3. 生成测试结果
    if generate_test_results():
        print("✅ 测试结果生成成功")
    else:
        print("❌ 测试结果生成失败")
        return
    print()
    
    # 4. 生成Allure报告
    if generate_allure_report():
        print("✅ Allure报告生成成功")
        
        # 检查生成的报告
        if os.path.exists('allure-report'):
            print("📁 报告目录内容:")
            for root, dirs, files in os.walk('allure-report'):
                level = root.replace('allure-report', '').count(os.sep)
                indent = ' ' * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files[:5]:  # 只显示前5个文件
                    print(f"{subindent}{file}")
                if len(files) > 5:
                    print(f"{subindent}... 还有 {len(files) - 5} 个文件")
    else:
        print("❌ Allure报告生成失败")
    
    print("=" * 50)
    print("🎉 诊断完成")

if __name__ == "__main__":
    main() 