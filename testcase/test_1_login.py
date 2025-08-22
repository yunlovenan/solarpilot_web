import pytest
from data.case_data import LoginCase
from common.handle_logging import log
from page.page_login import LoginPage
from page.page_index import IndexPage
from selenium import webdriver
import allure
import os
import json
from common.handle_path import DATA_DIR
from common.handle_excel import HandleExcel
from testcase.conftest import cases
import time

def save_cookies(driver, cookies_file="../solar_cookies.json"):
    """保存cookies到文件"""
    try:
        cookies = driver.get_cookies()
        with open(cookies_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        print(f"✅ 成功保存 {len(cookies)} 个cookies到文件: {cookies_file}")
        return True
    except Exception as e:
        print(f"❌ 保存cookies失败: {e}")
        return False

@pytest.fixture(scope='class')
def login_fixture(driver):
    """登录功能的前置后置"""
    # 前置条件
    log.info("开始执行登录的用例")
    
    # # 清除所有cookies，确保是全新登录
    # print("清除所有cookies，准备进行登录测试...")
    # driver.delete_all_cookies()
    
    # 跳转到登录页面
    driver.get("https://solar-tst.eiot6.com/account/login")
    time.sleep(2)

    login_page = LoginPage(driver)
    index_page = IndexPage(driver)
    yield login_page, index_page
    
    # 后置条件：登录成功后保存cookies
    try:
        current_url = driver.current_url
        if 'login' not in current_url and 'account' not in current_url:
            print("检测到登录成功，正在保存cookies...")
            if save_cookies(driver):
                print("✅ cookies已保存，后续用例可使用cookies登录")
            else:
                print("⚠️ cookies保存失败")
        else:
            print("⚠️ 登录可能失败，不保存cookies")
    except Exception as e:
        print(f"❌ 保存cookies时出错: {e}")
    
    time.sleep(2)
    log.info("登录的用例执行完毕")
    
    
@allure.epic('Solar系统')
@allure.feature('登录模块')
@allure.story('用户登录')
class TestLogin:
    """测试登录"""
    login_case_data = []
    login_case_data.append(eval(cases[0]['data'])) #读取excel中的数据
    
    @allure.title('正确用户名密码登录成功')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description('使用正确的用户名和密码进行登录测试')
    @pytest.mark.parametrize("case", login_case_data)
    def test_login_pass(self, case, login_fixture):
        """测试正确用户名密码登录"""
        with allure.step("准备登录数据"):
            print(case)
            allure.attach(str(case), "测试数据", allure.attachment_type.TEXT)
        
        with allure.step("执行登录操作"):
            login_page, index_page = login_fixture
            
            # 强制访问登录页面，确保在正确的页面上
            driver = login_page.driver
            current_url = driver.current_url
            print(f"当前页面URL: {current_url}")
            
            # 检查是否在真正的登录页面
            if not current_url.startswith('https://solar-tst.eiot6.com/account/login'):
                print(f"当前页面不是登录页面，强制跳转到登录页面...")
                print(f"当前URL: {current_url}")
                
                # 清除cookies，防止自动重定向
                print("清除cookies，防止自动重定向...")
                driver.delete_all_cookies()
                
                # 访问登录页面
                driver.get("https://solar-tst.eiot6.com/account/login")
                time.sleep(5)  # 等待页面完全加载
                
                # 再次检查是否成功跳转
                current_url = driver.current_url
                print(f"跳转后的URL: {current_url}")
                
                # 如果还是不在登录页面，再次尝试
                if not current_url.startswith('https://solar-tst.eiot6.com/account/login'):
                    print(f"⚠️ 跳转失败，再次尝试...")
                    driver.get("https://solar-tst.eiot6.com/account/login")
                    time.sleep(5)
                    current_url = driver.current_url
                    print(f"第二次尝试后的URL: {current_url}")
            
            # 确保在登录页面
            if current_url.startswith('https://solar-tst.eiot6.com/account/login'):
                print("✅ 成功进入登录页面，开始执行登录操作")
                # 进行登录的操作
                login_page.login(case['username'], case['password'])
            else:
                print(f"❌ 无法进入登录页面，当前URL: {current_url}")
                raise Exception(f"无法进入登录页面，当前URL: {current_url}")
        
        with allure.step("获取登录结果"):
            # 获取登录之后的用户信息
            res = index_page.get_my_user_info()
            allure.attach(res, "登录结果", allure.attachment_type.TEXT)
        
        with allure.step("验证登录结果"):
            # 断言用例执行是否通过
            try:
                assert '登录成功' == res
                allure.attach("登录成功", "断言结果", allure.attachment_type.TEXT)
            except AssertionError as e:
                log.error("用例执行失败")
                log.exception(e)
                allure.attach(str(e), "断言失败", allure.attachment_type.TEXT)
                raise e
            else:
                log.info("用例执行通过")
                allure.attach("测试通过", "测试结果", allure.attachment_type.TEXT)
    
    @pytest.mark.skip
    @allure.title('错误用户名密码登录失败')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description('使用错误的用户名和密码进行登录测试')
    @pytest.mark.parametrize('case', LoginCase.error_case_data)
    def test_login_error_case(self, case, login_fixture):
        """异常用例，窗口上有提示"""
        with allure.step("准备错误登录数据"):
            allure.attach(str(case), "错误测试数据", allure.attachment_type.TEXT)
        
        with allure.step("执行错误登录操作"):
            login_page, index_page = login_fixture
            # 刷新页面
            login_page.page_refresh()
            # 执行登录操作
            login_page.login(case['username'], case['password'])
        
        with allure.step("获取错误提示信息"):
            # 获取实际提示结果
            result = login_page.get_error_info()
            allure.attach(result, "错误提示", allure.attachment_type.TEXT)
        
        with allure.step("验证错误提示"):
            # 断言
            try:
                assert case['expected'] == result
                allure.attach("错误提示正确", "断言结果", allure.attachment_type.TEXT)
            except AssertionError as e:
                log.error("用例执行失败")
                log.exception(e)
                allure.attach(str(e), "断言失败", allure.attachment_type.TEXT)
                raise e
            else:
                log.info("用例执行通过")
                allure.attach("测试通过", "测试结果", allure.attachment_type.TEXT)
