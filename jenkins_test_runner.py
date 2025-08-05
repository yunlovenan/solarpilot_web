#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jenkins测试运行器
专门用于Jenkins环境的测试执行
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def setup_environment():
    """设置Jenkins环境"""
    print("🔧 设置Jenkins环境...")
    
    # 设置环境变量
    os.environ['DISPLAY'] = ':99'
    os.environ['CHROME_HEADLESS'] = 'true'
    os.environ['JENKINS_URL'] = 'true'
    
    print(f"环境变量设置完成:")
    print(f"  DISPLAY: {os.environ.get('DISPLAY')}")
    print(f"  CHROME_HEADLESS: {os.environ.get('CHROME_HEADLESS')}")
    print(f"  JENKINS_URL: {os.environ.get('JENKINS_URL')}")

def clean_results():
    """清理旧的测试结果"""
    print("🧹 清理旧的测试结果...")
    
    # 清理目录
    for dir_name in ['allure-results', 'allure-report', 'result/logs', 'result/error_image']:
        if os.path.exists(dir_name):
            import shutil
            shutil.rmtree(dir_name)
            print(f"  清理目录: {dir_name}")
    
    # 创建必要的目录
    os.makedirs('allure-results', exist_ok=True)
    os.makedirs('result/logs', exist_ok=True)
    os.makedirs('result/error_image', exist_ok=True)
    
    print("✅ 清理完成")

def run_tests():
    """运行测试"""
    print("🚀 开始运行测试...")
    
    # 检查pytest是否可用
    try:
        result = subprocess.run([sys.executable, '-m', 'pytest', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ pytest版本: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"❌ pytest不可用: {e}")
        return False
    
    # 运行测试
    test_command = [
        sys.executable, '-m', 'pytest',
        'testcase/test_allure_simple.py',  # 先运行简单测试
        '-v',
        '--alluredir=allure-results',
        '--junitxml=junit.xml',
        '--tb=short',
        '--capture=no'
    ]
    
    print(f"执行命令: {' '.join(test_command)}")
    
    try:
        result = subprocess.run(test_command, check=True)
        print("✅ 测试执行完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 测试执行失败: {e}")
        return False

def generate_allure_report():
    """生成Allure报告"""
    print("📊 生成Allure报告...")
    
    # 检查allure命令
    try:
        result = subprocess.run(['allure', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Allure版本: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Allure命令不可用，尝试安装...")
        install_allure()
    
    # 检查测试结果
    if not os.path.exists('allure-results'):
        print("❌ allure-results目录不存在")
        return False
    
    result_files = list(Path('allure-results').glob('*.json'))
    if not result_files:
        print("❌ 没有找到测试结果文件")
        return False
    
    print(f"✅ 找到 {len(result_files)} 个测试结果文件")
    
    # 生成报告
    try:
        subprocess.run(['allure', 'generate', 'allure-results', '--clean', '-o', 'allure-report'], 
                      check=True)
        print("✅ Allure报告生成成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Allure报告生成失败: {e}")
        return False

def install_allure():
    """安装Allure"""
    print("📦 安装Allure...")
    
    try:
        # 下载Allure
        subprocess.run([
            'curl', '-o', 'allure-2.24.1.tgz', '-Ls',
            'https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.24.1/allure-commandline-2.24.1.tgz'
        ], check=True)
        
        # 解压
        subprocess.run(['sudo', 'tar', '-zxvf', 'allure-2.24.1.tgz', '-C', '/opt/'], check=True)
        
        # 创建软链接
        subprocess.run(['sudo', 'ln', '-sf', '/opt/allure-2.24.1/bin/allure', '/usr/local/bin/allure'], check=True)
        
        # 清理
        os.remove('allure-2.24.1.tgz')
        
        print("✅ Allure安装成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ Allure安装失败: {e}")

def main():
    """主函数"""
    print("🚀 Jenkins测试运行器启动")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python版本: {sys.version}")
    
    # 设置环境
    setup_environment()
    
    # 清理结果
    clean_results()
    
    # 运行测试
    if not run_tests():
        print("❌ 测试运行失败")
        sys.exit(1)
    
    # 生成报告
    if not generate_allure_report():
        print("❌ 报告生成失败")
        sys.exit(1)
    
    print("✅ 所有任务完成")
    
    # 显示结果统计
    if os.path.exists('allure-results'):
        result_files = list(Path('allure-results').glob('*.json'))
        print(f"📊 测试结果统计: {len(result_files)} 个结果文件")
    
    if os.path.exists('allure-report'):
        print("📊 Allure报告已生成在 allure-report/ 目录")

if __name__ == '__main__':
    main() 