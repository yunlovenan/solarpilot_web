#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jenkins专用测试运行脚本
用于在Jenkins CI/CD环境中运行自动化测试
"""

import os
import sys
import subprocess
import shutil
import time
from pathlib import Path

def setup_environment():
    """设置测试环境"""
    print("🔧 设置测试环境...")
    
    # 设置环境变量
    os.environ['DISPLAY'] = ':99'
    os.environ['CHROME_HEADLESS'] = 'true'
    os.environ['JENKINS_URL'] = 'true'  # 标识在Jenkins环境中运行
    
    # 创建必要的目录
    directories = ['result/logs', 'result/error_image', 'allure_report', 'test_reports']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ 环境设置完成")

def clear_previous_results():
    """清理之前的测试结果"""
    print("🧹 清理之前的测试结果...")
    
    # 清理Allure结果
    allure_dirs = ['allure', 'allure_report']
    for dir_name in allure_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ 已清理 {dir_name}")
    
    # 清理JUnit XML
    if os.path.exists('junit.xml'):
        os.remove('junit.xml')
        print("✅ 已清理 junit.xml")
    
    print("✅ 清理完成")

def install_dependencies():
    """安装Python依赖"""
    print("📦 安装Python依赖...")
    
    try:
        # 升级pip
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      check=True, capture_output=True, text=True)
        print("✅ pip升级完成")
        
        # 安装依赖
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("✅ 依赖安装完成")
        
        # 验证pytest安装
        result = subprocess.run([sys.executable, '-m', 'pytest', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ pytest版本: {result.stdout.strip()}")
        else:
            print("❌ pytest安装验证失败")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False
    
    return True

def run_tests():
    """运行测试"""
    print("🚀 开始运行测试...")
    
    # 构建pytest命令
    pytest_args = [
        sys.executable, '-m', 'pytest',
        'testcase/',
        '-v',
        '--alluredir=allure_report',
        '--junitxml=junit.xml',
        '--tb=short',
        '--maxfail=5'  # 最多失败5个测试就停止
    ]
    
    print(f"执行命令: {' '.join(pytest_args)}")
    
    try:
        # 运行测试
        result = subprocess.run(pytest_args, capture_output=True, text=True)
        
        # 输出测试结果
        if result.stdout:
            print("📋 测试输出:")
            print(result.stdout)
        
        if result.stderr:
            print("⚠️ 测试错误:")
            print(result.stderr)
        
        print(f"测试退出码: {result.returncode}")
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 测试执行失败: {e}")
        return False

def generate_reports():
    """生成测试报告"""
    print("📊 生成测试报告...")
    
    try:
        # 生成Allure报告
        allure_cmd = ['allure', 'generate', 'allure_report', '--clean']
        result = subprocess.run(allure_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Allure报告生成成功")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Allure报告生成失败")
            if result.stderr:
                print(result.stderr)
                
    except FileNotFoundError:
        print("⚠️ Allure未安装，跳过报告生成")
    except Exception as e:
        print(f"❌ 报告生成失败: {e}")

def main():
    """主函数"""
    print("=" * 50)
    print("🚀 Jenkins测试运行器启动")
    print("=" * 50)
    
    # 记录开始时间
    start_time = time.time()
    
    try:
        # 1. 设置环境
        setup_environment()
        
        # 2. 清理之前的结果
        clear_previous_results()
        
        # 3. 安装依赖
        if not install_dependencies():
            print("❌ 依赖安装失败，退出")
            sys.exit(1)
        
        # 4. 运行测试
        test_success = run_tests()
        
        # 5. 生成报告
        generate_reports()
        
        # 计算运行时间
        end_time = time.time()
        duration = end_time - start_time
        
        print("=" * 50)
        print(f"⏱️ 总运行时间: {duration:.2f}秒")
        
        if test_success:
            print("✅ 测试运行完成")
            sys.exit(0)
        else:
            print("❌ 测试运行失败")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断测试")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 运行过程中发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 