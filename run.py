import pytest
import os
import sys
import shutil

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def clear_allure_results():
    """清空Allure报告目录"""
    allure_dir = "allure_report"
    if os.path.exists(allure_dir):
        try:
            shutil.rmtree(allure_dir)
            print(f"🗑️ 已清空Allure报告目录: {allure_dir}")
        except Exception as e:
            print(f"❌ 清空Allure报告目录失败: {e}")
    else:
        print(f"ℹ️ Allure报告目录不存在: {allure_dir}")

def run_tests():
    """运行Web自动化测试"""
    print("开始运行Web自动化测试")
    
    # 清空上次的Allure报告结果
    print("🧹 清理上次的测试结果...")
    clear_allure_results()
    
    # 运行Web测试
    pytest.main(['-s', '-v', '--alluredir=allure_report', 'testcase/test_1_login.py'])
    
    # 生成并打开Allure报告
    print("📊 生成Allure报告...")
    result = os.system('allure serve allure_report')
    
    if result == 0:
        print("✅ Allure报告生成成功")
    else:
        print("❌ Allure报告生成失败")

if __name__ == "__main__":
    run_tests()