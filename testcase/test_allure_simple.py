#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的Allure测试用例
用于验证Allure报告生成是否正常
"""

import pytest
import allure
import time

@allure.epic('Allure测试')
@allure.feature('基础功能')
@allure.story('简单测试')
class TestAllureSimple:
    """简单的Allure测试"""
    
    @allure.title('成功测试')
    @allure.description('这是一个成功的测试用例')
    @allure.severity(allure.severity_level.NORMAL)
    def test_success(self):
        """成功的测试"""
        with allure.step("步骤1: 准备数据"):
            data = {"name": "test", "value": 123}
            print(f"准备数据: {data}")
            allure.attach(str(data), "测试数据", allure.attachment_type.TEXT)
        
        with allure.step("步骤2: 执行操作"):
            result = data["value"] * 2
            print(f"计算结果: {result}")
            allure.attach(str(result), "计算结果", allure.attachment_type.TEXT)
        
        with allure.step("步骤3: 验证结果"):
            assert result == 246, f"期望结果246，实际结果{result}"
            print("测试通过")
            allure.attach("测试通过", "验证结果", allure.attachment_type.TEXT)
    
    @allure.title('失败测试')
    @allure.description('这是一个失败的测试用例')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_failure(self):
        """失败的测试"""
        with allure.step("步骤1: 准备数据"):
            data = {"name": "test", "value": 123}
            print(f"准备数据: {data}")
        
        with allure.step("步骤2: 执行操作"):
            result = data["value"] * 2
            print(f"计算结果: {result}")
        
        with allure.step("步骤3: 验证结果"):
            # 故意让测试失败
            assert result == 999, f"期望结果999，实际结果{result}"
    
    @allure.title('跳过测试')
    @allure.description('这是一个跳过的测试用例')
    @pytest.mark.skip(reason="暂时跳过此测试")
    def test_skip(self):
        """跳过的测试"""
        assert True
    
    @allure.title('参数化测试')
    @allure.description('参数化测试示例')
    @pytest.mark.parametrize("input_value,expected", [
        (1, 2),
        (2, 4),
        (3, 6)
    ])
    def test_parametrized(self, input_value, expected):
        """参数化测试"""
        with allure.step(f"测试输入值: {input_value}"):
            result = input_value * 2
            print(f"输入: {input_value}, 期望: {expected}, 实际: {result}")
            assert result == expected, f"期望{expected}，实际{result}" 