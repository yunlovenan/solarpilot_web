#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Allure配置检查脚本
用于诊断Allure报告问题
"""

import os
import subprocess
import json
from pathlib import Path

def check_allure_installation():
    """检查Allure安装"""
    print("🔍 检查Allure安装...")
    
    try:
        result = subprocess.run(['allure', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Allure已安装: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Allure未安装或不可用")
        return False

def check_test_results():
    """检查测试结果文件"""
    print("\n🔍 检查测试结果文件...")
    
    allure_results_dir = Path('allure-results')
    if not allure_results_dir.exists():
        print("❌ allure-results目录不存在")
        return False
    
    # 查找JSON文件
    json_files = list(allure_results_dir.glob('*.json'))
    print(f"找到 {len(json_files)} 个JSON文件")
    
    if not json_files:
        print("❌ 没有找到测试结果JSON文件")
        return False
    
    # 检查每个JSON文件
    for json_file in json_files:
        print(f"📄 检查文件: {json_file.name}")
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"  - 文件大小: {len(data)} 字节")
                if 'name' in data:
                    print(f"  - 测试名称: {data['name']}")
                if 'status' in data:
                    print(f"  - 测试状态: {data['status']}")
                if 'start' in data and 'stop' in data:
                    duration = data['stop'] - data['start']
                    print(f"  - 执行时间: {duration}ms")
        except Exception as e:
            print(f"  - 解析失败: {e}")
    
    return True

def main():
    """主函数"""
    print("🔍 Allure配置检查工具")
    print("=" * 50)
    
    # 检查Allure安装
    allure_installed = check_allure_installation()
    
    # 检查测试结果
    results_exist = check_test_results()
    
    # 总结
    print("\n📋 检查总结:")
    print(f"  Allure安装: {'✅' if allure_installed else '❌'}")
    print(f"  测试结果: {'✅' if results_exist else '❌'}")

if __name__ == '__main__':
    main() 