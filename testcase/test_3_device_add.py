import pytest
from data.case_data import SiteCase
from common.handle_logging import log
from page.page_login import LoginPage
from page.page_index import IndexPage
from page.page_device import DevicePage
from selenium import webdriver
import allure
import time
import json
from testcase.conftest import cases,excel
from common.handle_sql import HandleMysql
from selenium.webdriver import Chrome
from common.handle_config import conf
from common.handle_data import EnvData

# 延迟创建数据库连接，避免导入时就连接数据库
def get_db():
    try:
        return HandleMysql()
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None
@pytest.fixture(scope='class')
def device_fixture(driver):
    """添加设备的前置后置"""
    # 前置条件
    log.info("设备的用例执行开始")
    driver.implicitly_wait(10)
    
    # # 检查登录状态，如果未登录则进行登录
    # current_url = driver.current_url
    # print(f"当前页面URL: {current_url}")
    
    # # 更智能的登录检测
    # if '/account/login' in current_url:
    #     print("检测到登录页面，进行登录...")
    #     login_page = LoginPage(driver)
    #     login_page.login(user=conf.get('test_data', 'username'), pwd=conf.get('test_data', 'pwd'))
    #     time.sleep(3)  # 等待登录完成
    # else:
    #     print("已登录状态，继续执行...")
    #     # 如果不在登录页面，尝试导航到主页面
    #     try:
    #         driver.get("https://solar-tst.eiot6.com")
    #         time.sleep(3)
    #     except Exception as e:
    #         print(f"导航到主页面失败: {e}")
    
    # 创建设备管理对象
    device_page = DevicePage(driver)
    # # 点击菜单到添加设备入口
    # device_page.click_to_add_device()

    yield device_page
    # 后置条件
    log.info("设备的用例执行完毕")
@allure.epic('Solar系统')
@allure.feature('设备管理')
@allure.story('设备添加')
class TestDeviceAdd:
    """测试设备添加"""
    
    device_case_data = [{"zigbee_sn":"GW1123C21122"}]
    
    @allure.title('正常添加设备')
    @allure.description('测试正常添加设备功能')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", device_case_data)
    def test_device_add_pass(self, case, device_fixture):
        """测试设备添加成功"""
        with allure.step("准备测试数据"):
            device_page = device_fixture
            # 进行添加设备的操作（sn、imei唯一）
            case['gateway_name'] = 'gateway_'+str(int(time.time() * 1000))
            print(f"测试数据: {case}")
        
        with allure.step("执行设备添加"):
            try:
                device_page.device_add(case['zigbee_sn'], case['gateway_name'])
                print("设备添加操作完成")
            except Exception as e:
                allure.attach(f"设备添加失败: {str(e)}", "错误信息", allure.attachment_type.TEXT)
                raise e
        
        with allure.step("校验设备添加结果"):
            try:
                # 校验设备添加(通过页面列表查询校验)
                res = device_fixture.device_add_check(case['gateway_name'])
                print(f"查询结果: {res}")
                allure.attach(f"查询结果: {res}", "查询结果", allure.attachment_type.TEXT)
                
                # 断言用例执行是否通过
                assert case['gateway_name'] in res, f"设备名称 {case['gateway_name']} 未在结果中找到"
                
                log.info("用例执行通过")
                excel.write_data(5,7,json.dumps(case))
                setattr(EnvData,"device_sn",case['zigbee_sn'])
                setattr(EnvData,"device_name",case['gateway_name'])
                
                allure.attach(f"设备添加成功: {case['gateway_name']}", "成功信息", allure.attachment_type.TEXT)
                
            except AssertionError as e:
                log.error("用例执行失败")
                log.exception(e)
                allure.attach(f"断言失败: {str(e)}", "失败信息", allure.attachment_type.TEXT)
                raise e
            except Exception as e:
                log.error(f"校验过程发生异常: {e}")
                allure.attach(f"校验异常: {str(e)}", "异常信息", allure.attachment_type.TEXT)
                raise e
            #setattr(EnvData, "detectorId", res['id'])


