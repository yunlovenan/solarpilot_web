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
    
    # 清除所有cookies，确保是全新登录
    print("清除所有cookies，准备进行登录测试...")
    driver.delete_all_cookies()
    
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
    
    
@allure.feature('登录流程')
@allure.description('登录界面功能测试')
class TestLogin:
    """测试登录"""
    login_case_data = []
    login_case_data.append(eval(cases[0]['data'])) #读取excel中的数据
    @allure.story('正确用户名密码登录')
    @allure.title('登录成功场景')
    @pytest.mark.parametrize("case", login_case_data)
    def test_login_pass(self, case, login_fixture):
        print(case)
        login_page, index_page = login_fixture
        # 进行登录的操作
        login_page.login(case['username'], case['password'])
        # 获取登录之后的用户信息
        res = index_page.get_my_user_info()
        # 断言用例执行是否通过
        try:
            assert '登录成功' == res
        except AssertionError as e:
            log.error("用例执行失败")
            log.exception(e)
            raise e
        else:
            log.info("用例执行通过")
            # 退出登录，重新访问登录页面
         #   index_page.click_quit()
            # 重新进入登录页面
          #  login_page.page_refresh()
    @pytest.mark.skip
    @allure.story('错误用户名密码登录')
    @allure.title('登录失败场景')
    @pytest.mark.parametrize('case', LoginCase.error_case_data)
    def test_login_error_case(self, case, login_fixture):
        """异常用例，窗口上有提示"""
        login_page, index_page = login_fixture
        # 刷新页面
        login_page.page_refresh()
        # 执行登录操作
        login_page.login(case['username'], case['password'])
        # 获取实际提示结果
        result = login_page.get_error_info()
        # 断言
        try:
            assert case['expected'] == result
        except AssertionError as e:
            log.error("用例执行失败")
            log.exception(e)
            raise e
        else:
            log.info("用例执行通过")
