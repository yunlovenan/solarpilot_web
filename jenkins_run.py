#!/usr/bin/env python3
"""
Jenkins专用启动脚本
支持无头模式运行，适合CI/CD环境
"""

import pytest
import os
import sys
import shutil
import subprocess
import time

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def setup_jenkins_environment():
    """设置Jenkins环境"""
    print("🔧 设置Jenkins环境...")
    
    # 设置显示变量（用于无头模式）
    os.environ['DISPLAY'] = ':99'
    os.environ['CHROME_HEADLESS'] = 'true'
    
    # 创建必要的目录
    os.makedirs('allure_report', exist_ok=True)
    os.makedirs('test_reports', exist_ok=True)
    os.makedirs('result/logs', exist_ok=True)
    
    print("✅ Jenkins环境设置完成")

def clear_previous_results():
    """清空之前的测试结果"""
    print("🧹 清理之前的测试结果...")
    
    # 清空Allure报告目录
    allure_dir = "allure_report"
    if os.path.exists(allure_dir):
        try:
            shutil.rmtree(allure_dir)
            print(f"🗑️ 已清空Allure报告目录: {allure_dir}")
        except Exception as e:
            print(f"❌ 清空Allure报告目录失败: {e}")
    
    # 清空之前的JUnit XML文件
    junit_file = "junit.xml"
    if os.path.exists(junit_file):
        try:
            os.remove(junit_file)
            print(f"🗑️ 已删除JUnit XML文件: {junit_file}")
        except Exception as e:
            print(f"❌ 删除JUnit XML文件失败: {e}")

def run_tests():
    """运行Web自动化测试"""
    print("🚀 开始运行Web自动化测试")
    
    # 设置Jenkins环境
    setup_jenkins_environment()
    
    # 清理之前的结果
    clear_previous_results()
    
    # 运行测试用例
    test_files = [
        'testcase/test_1_login.py',
        'testcase/test_2_site_add.py', 
        'testcase/test_3_device_add.py'
    ]
    
    # 过滤存在的测试文件
    existing_tests = [f for f in test_files if os.path.exists(f)]
    
    if not existing_tests:
        print("⚠️ 没有找到可运行的测试文件")
        return False
    
    print(f"📋 找到 {len(existing_tests)} 个测试文件")
    
    # 构建pytest命令
    pytest_args = [
        'pytest',
        '-v',  # 详细输出
        '--tb=short',  # 简短的错误回溯
        '--alluredir=allure_report',  # Allure报告目录
        '--junitxml=junit.xml',  # JUnit XML报告
        '--capture=no',  # 显示print输出
        '--maxfail=3',  # 最多失败3个测试后停止
    ]
    
    # 添加测试文件
    pytest_args.extend(existing_tests)
    
    print(f"🔧 执行命令: {' '.join(pytest_args)}")
    
    try:
        # 运行pytest
        result = subprocess.run(pytest_args, capture_output=False, text=True)
        
        if result.returncode == 0:
            print("✅ 所有测试通过")
        else:
            print(f"⚠️ 测试完成，但有 {result.returncode} 个测试失败")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 运行测试时出错: {e}")
        return False

def generate_reports():
    """生成测试报告"""
    print("📊 生成测试报告...")
    
    # 生成Allure报告
    try:
        allure_cmd = ['allure', 'generate', 'allure_report', '--clean']
        result = subprocess.run(allure_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Allure报告生成成功")
        else:
            print(f"⚠️ Allure报告生成失败: {result.stderr}")
    except Exception as e:
        print(f"❌ 生成Allure报告时出错: {e}")
    
    # 检查JUnit XML文件
    if os.path.exists('junit.xml'):
        print("✅ JUnit XML报告已生成")
    else:
        print("⚠️ JUnit XML报告未生成")

def main():
    """主函数"""
    print("=" * 60)
    print("🤖 Jenkins自动化测试启动")
    print("=" * 60)
    
    # 记录开始时间
    start_time = time.time()
    
    # 运行测试
    success = run_tests()
    
    # 生成报告
    generate_reports()
    
    # 记录结束时间
    end_time = time.time()
    duration = end_time - start_time
    
    print("=" * 60)
    print(f"⏱️ 测试总耗时: {duration:.2f} 秒")
    print(f"📊 测试结果: {'✅ 成功' if success else '❌ 失败'}")
    print("=" * 60)
    
    # 返回适当的退出码
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 