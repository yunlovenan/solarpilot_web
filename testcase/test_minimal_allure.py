#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
最简化的Allure测试
用于验证Allure报告生成
"""

import pytest
import allure
import time

@allure.epic('最小测试')
@allure.feature('基础功能')
class TestMinimalAllure:
    """最小Allure测试"""
    
    @allure.title('最小成功测试')
    @allure.description('这是一个最小的成功测试')
    @allure.severity(allure.severity_level.NORMAL)
    def test_minimal_success(self):
        """最小成功测试"""
        print("开始执行最小成功测试")
        time.sleep(3)  # 确保有执行时间
        
        with allure.step("步骤1: 准备数据"):
            data = {"test": "value"}
            print(f"准备数据: {data}")
        
        with allure.step("步骤2: 执行操作"):
            result = len(data)
            print(f"执行操作，结果: {result}")
        
        with allure.step("步骤3: 验证结果"):
            assert result == 1, f"期望结果1，实际结果{result}"
            print("验证通过")
        
        print("最小成功测试完成")
    
    @allure.title('最小失败测试')
    @allure.description('这是一个最小的失败测试')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_minimal_failure(self):
        """最小失败测试"""
        print("开始执行最小失败测试")
        time.sleep(3)  # 确保有执行时间
        
        with allure.step("步骤1: 准备数据"):
            data = {"test": "value"}
            print(f"准备数据: {data}")
        
        with allure.step("步骤2: 执行操作"):
            result = len(data)
            print(f"执行操作，结果: {result}")
        
        with allure.step("步骤3: 验证结果"):
            # 故意让测试失败
            assert result == 999, f"期望结果999，实际结果{result}"
        
        print("最小失败测试完成") 