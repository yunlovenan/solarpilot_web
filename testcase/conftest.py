


from selenium import webdriver
from selenium.webdriver import Chrome

import pytest

from common.handle_config import conf
from common.handle_logging import log
from common.local_browser import local_chrome_manager
from page.page_index import IndexPage
from page.page_login import LoginPage
from page.page_antena import AntenaPage
from page.page_site import SitePage
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_data import get_standard_data
#from common.handle_sql import HandleMysql
import os
import time

excel = HandleExcel(os.path.join(DATA_DIR, "cases.xlsx"), "main_stream")
cases = excel.read_data()


class EnvData:
    pass


@pytest.fixture(scope='class')
def antenna_fixture(driver):
    """天线的前置后置"""
    # 前置条件
    log.info("天线的用例执行开始")
    # driver = Chrome()
    driver.implicitly_wait(10)
    # 创建登录页面
    # login_page = LoginPage(driver)
    # # # 登录
    # login_page.login(user=conf.get('test_data', 'username'), pwd=conf.get('test_data', 'pwd'))
    # 创建天线管理对象
    antenna_page = AntenaPage(driver)
    yield antenna_page
    # 后置条件
    time.sleep(2)
  #  driver.quit()
    log.info("天线的用例执行完毕")

@pytest.fixture(scope='class')
def site_fixture(driver):
    """添加站点的前置后置"""
    # 前置条件
    log.info("站点的用例执行开始")
    driver.implicitly_wait(10)
    
    # 检查登录状态，如果未登录则进行登录
    current_url = driver.current_url
    print(f"当前页面URL: {current_url}")
    
    # 更智能的登录检测
    if '/account/login' in current_url:
        print("检测到登录页面，进行登录...")
        from page.page_login import LoginPage
        from common.handle_config import conf
        login_page = LoginPage(driver)
        login_page.login(user=conf.get('test_data', 'username'), pwd=conf.get('test_data', 'pwd'))
        time.sleep(3)  # 等待登录完成
    else:
        print("已登录状态，继续执行...")
        # 如果不在登录页面，尝试导航到主页面
        try:
            driver.get("https://solar-tst.eiot6.com")
            time.sleep(3)
        except Exception as e:
            print(f"导航到主页面失败: {e}")
    
    # 创建站点管理对象
    site_page = SitePage(driver)
    
    yield site_page
    # 后置条件
    log.info("站点的用例执行完毕")



@pytest.fixture()
def get_standard_data_fixture():
    """获取标准数据"""
    # 前置条件
    log.info("开始获取标准数据")
    pre_site,pre_antena,pre_antena_param,pre_antena_bands = get_standard_data()
    yield pre_site,pre_antena,pre_antena_param,pre_antena_bands
    log.info("结束获取标准数据")
    




# def browser():
#     if conf.getboolean('env', "headless"):
#         """设置浏览启动的选项：无头模式"""
#         opt = webdriver.ChromeOptions()
#     #    opt.add_argument("--headless")
#         return opt
#     else:
#         return None



#设置为session，全部用例执行一次
@pytest.fixture(scope='session')
def driver():
    """Web测试 - 使用远程Chrome driver连接到Selenium Grid"""
    import os
    import time
    import sys
    from selenium import webdriver
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    
    # 检测当前运行的测试文件
    current_test_file = None
    for arg in sys.argv:
        if arg.endswith('.py') and 'test_' in arg:
            current_test_file = arg.split('/')[-1] if '/' in arg else arg
            break
    
    # 如果通过sys.argv没有找到，尝试从pytest的收集信息中获取
    if not current_test_file:
        import inspect
        frame = inspect.currentframe()
        while frame:
            if 'test_' in str(frame.f_code.co_filename):
                current_test_file = frame.f_code.co_filename.split('/')[-1]
                break
            frame = frame.f_back
    
    print(f'------------open remote browser------------')
    print(f'当前测试文件: {current_test_file}')
    
    # 检查是否在Jenkins环境中运行
    is_jenkins = os.environ.get('JENKINS_URL') is not None or os.environ.get('BUILD_NUMBER') is not None
    
    # 直接使用本地Chrome浏览器
    print("🚀 正在启动本地Chrome浏览器...")
    try:
        driver = local_chrome_manager.create_local_driver()
        print("✅ 本地Chrome浏览器启动成功")
    except Exception as e:
        print(f"❌ 本地Chrome启动失败: {e}")
        raise e

    # 总是尝试使用cookies登录（除了明确指定不使用cookies的情况）
    print("尝试使用cookies登录...")
    # 自动加载 cookies 绕过登录
    try:
        import json
        cookies_file = "../solar_cookies.json"
        if os.path.exists(cookies_file):
            print("发现 cookies 文件，正在加载...")
            
            # 先访问主域名，确保cookies能正确设置
            print("正在访问目标应用页面...")
            try:
                driver.get("https://solar-tst.eiot6.com")
                print("等待页面完全加载...")
                time.sleep(10)  # 给更多时间加载
                
                # 等待页面完全加载
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.webdriver.common.by import By
                
                try:
                    # 等待页面标题出现
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.TAG_NAME, "title"))
                    )
                    print("页面标题元素已加载")
                    
                    # 检查页面是否正常加载
                    current_url = driver.current_url
                    print(f"页面加载完成，当前URL: {current_url}")
                    
                    # 检查页面标题
                    try:
                        page_title = driver.title
                        print(f"页面标题: {page_title}")
                        
                        # 检查页面内容
                        page_source_length = len(driver.page_source)
                        print(f"页面源码长度: {page_source_length}")
                        
                    except Exception as e:
                        print(f"无法获取页面信息: {e}")
                        
                except Exception as e:
                    print(f"页面加载超时: {e}")
                
            except Exception as e:
                print(f"页面访问失败: {e}")
                # 如果页面访问失败，尝试访问一个简单的页面
                print("尝试访问简单页面...")
                driver.get("https://www.baidu.com")
                time.sleep(3)
            
            with open(cookies_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            
            print(f"加载 {len(cookies)} 个cookies...")
            for i, cookie in enumerate(cookies):
                try:
                    # 尝试多种domain设置
                    original_domain = cookie.get('domain', '')
                    print(f"原始domain: {original_domain}")
                    
                    # 方法1：使用原始domain
                    try:
                        driver.add_cookie(cookie)
                        print(f"✅ 方法1成功添加cookie {i+1}: {cookie.get('name', 'unknown')} (domain: {cookie.get('domain', 'unknown')})")
                    except Exception as e1:
                        print(f"❌ 方法1失败: {e1}")
                    
                    # 方法2：修改domain为.solar-tst.eiot6.com
                    cookie_copy = cookie.copy()
                    if 'domain' in cookie_copy:
                        if cookie_copy['domain'] == '.eiot6.com':
                            cookie_copy['domain'] = '.solar-tst.eiot6.com'
                        elif cookie_copy['domain'] == 'eiot6.com':
                            cookie_copy['domain'] = 'solar-tst.eiot6.com'
                    try:
                        driver.add_cookie(cookie_copy)
                        print(f"✅ 方法2成功添加cookie {i+1}: {cookie_copy.get('name', 'unknown')} (domain: {cookie_copy.get('domain', 'unknown')})")
                    except Exception as e2:
                        print(f"❌ 方法2失败: {e2}")
                    
                    # 方法3：移除domain字段
                    cookie_copy2 = cookie.copy()
                    if 'domain' in cookie_copy2:
                        del cookie_copy2['domain']
                    try:
                        driver.add_cookie(cookie_copy2)
                        print(f"✅ 方法3成功添加cookie {i+1}: {cookie_copy2.get('name', 'unknown')} (无domain)")
                    except Exception as e2:
                        print(f"❌ 方法3失败: {e2}")
                        
                except Exception as e:
                    print(f"❌ 处理cookie {i+1} 时出错: {e}")
            
            # 刷新页面并等待
            print("刷新页面...")
            try:
                driver.refresh()
                time.sleep(5)
                
                # 检查是否成功登录
                current_url = driver.current_url
                print(f"当前页面URL: {current_url}")
                
                if 'login' not in current_url:
                    print("✅ Cookies 加载完成，已绕过登录")
                else:
                    print("⚠️ Cookies 可能无效，需要手动登录")
                    
            except Exception as e:
                print(f"页面刷新失败: {e}")
                print("尝试重新访问页面...")
                try:
                    driver.get("https://solar-tst.eiot6.com")
                    time.sleep(5)
                except Exception as e2:
                    print(f"重新访问也失败: {e2}")
                    # 最后尝试访问百度
                    driver.get("https://www.baidu.com")
                    time.sleep(3)
        else:
            print("未找到 cookies 文件，需要手动登录")
    except Exception as e:
        print(f"加载 cookies 时出错: {e}")
    
    yield driver
    print('------------测试完成，保持浏览器打开------------')
    print("📺 您可以通过 http://localhost:7900 继续查看浏览器状态")
    # 调试模式下不关闭浏览器，让用户可以看到结果
    # driver.quit()


