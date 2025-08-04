
from selenium import webdriver
from selenium.webdriver import Chrome

import pytest

from common.handle_config import conf
from common.handle_logging import log
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
    """Web测试 - 使用Chrome driver"""
    import os
    import time
    import sys
    from selenium import webdriver
    
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
    
    print(f'------------open browser------------')
    print(f'当前测试文件: {current_test_file}')
    
    chromeOptions = webdriver.ChromeOptions()
    # 设定下载文件的保存目录，
    # 如果该目录不存在，将会自动创建
    prefs = {"download.default_directory": "E:\\testDownload"}
    # 将自定义设置添加到Chrome配置对象实例中
    chromeOptions.add_experimental_option("prefs", prefs)
    chromeOptions.add_argument("--ignore-certificate-errors")
    chromeOptions.add_argument('--unlimited-storage')
    # 添加代理绕过选项
    chromeOptions.add_argument('--no-proxy-server')
    chromeOptions.add_argument('--proxy-bypass-list=*')
    chromeOptions.add_argument('--disable-web-security')
    chromeOptions.add_argument('--allow-running-insecure-content')
    # 移除无头模式，让浏览器窗口可见
    chromeOptions.add_argument('--disable-gpu')
    chromeOptions.add_argument('--no-sandbox')
    chromeOptions.add_argument('--disable-dev-shm-usage')
    
    # 使用本地安装的ChromeDriver
    chrome_driver_path = "/opt/homebrew/bin/chromedriver"
    try:
        driver = webdriver.Chrome(service=webdriver.chrome.service.Service(chrome_driver_path), options=chromeOptions)
        driver.maximize_window()
        # chrome由于每次都打开设置页面，暂时没有找到关闭的方法，需要切换操作窗口(火狐浏览器不需要切换窗口)
        windows = driver.window_handles  # 获取所有窗口
        driver.switch_to.window(windows[-1])  # 切换到最新窗口
    except Exception as e:
        print(f"浏览器启动失败: {e}")
        # 如果Chrome启动失败，尝试使用无头模式
        chromeOptions.add_argument('--headless')
        driver = webdriver.Chrome(service=webdriver.chrome.service.Service(chrome_driver_path), options=chromeOptions)

    # 总是尝试使用cookies登录（除了明确指定不使用cookies的情况）
    print("尝试使用cookies登录...")
    # 自动加载 cookies 绕过登录
    try:
        import json
        cookies_file = "../solar_cookies.json"
        if os.path.exists(cookies_file):
            print("发现 cookies 文件，正在加载...")
            
            # 先访问主域名，确保cookies能正确设置
            driver.get("https://solar-tst.eiot6.com")
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
                    except Exception as e3:
                        print(f"❌ 方法3失败: {e3}")
                        
                except Exception as e:
                    print(f"❌ 处理cookie {i+1} 时出错: {e}")
            
            # 刷新页面并等待
            print("刷新页面...")
            driver.refresh()
            time.sleep(5)
            
            # 检查是否成功登录
            current_url = driver.current_url
            print(f"当前页面URL: {current_url}")
            
            if 'login' not in current_url:
                print("✅ Cookies 加载完成，已绕过登录")
            else:
                print("⚠️ Cookies 可能无效，需要手动登录")
        else:
            print("未找到 cookies 文件，需要手动登录")
    except Exception as e:
        print(f"加载 cookies 时出错: {e}")
    
    yield driver
    print('------------测试完成，保持浏览器打开------------')
    # 调试模式下不关闭浏览器，让用户可以看到结果
    # driver.quit()


