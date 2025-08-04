
import os
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from common.handle_logging import log
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.handle_path import ERROR_IMG

from selenium.webdriver import ActionChains

class BasePage:
    """把页面一些常见的功能操作全部封装到这里"""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def wait_element_visibility(self, locator, img_info, timeout=20, poll_frequency=0.5):
        """
        等待元素可见
        :param locator: 定位表达式
        :param img_info: 错误截图文件名
        :param timeout: 等待超时时间
        :param poll_frequency: 等待轮询时间
        :return:
        """
        # 等待元素之前获取当前的时间
        start_time = time.time()
        try:
            ele = WebDriverWait(self.driver, timeout, poll_frequency).until(
                EC.visibility_of_element_located(locator)
            )
        except Exception as e:
            # 输出日志
            log.error("元素--{}--等待可见超时".format(locator))
            log.exception(e)
            # 对当前页面进行截图
            self.save_scree_image(img_info)
            raise e
        else:
            # 元素等待出现之后，获取实际
            end_time = time.time()
            log.info("元素--{}--等待可见成功,等待时间{}秒".format(locator, end_time - start_time))
            return ele

    def wait_element_clickable(self, locator, img_info, timeout=30, poll_frequency=0.5):
        """
        等待元素可点击
        :param locator: 定位表达式
        :param img_info: 错误截图文件名
        :param timeout: 等待超时时间
        :param poll_frequency: 等待轮询时间
        :return:
        """
        # 等待元素之前获取当前的时间
        start_time = time.time()
        try:
            ele = WebDriverWait(self.driver, timeout, poll_frequency).until(
                EC.element_to_be_clickable(locator)
            )
        except Exception as e:
            # 输出日志
            log.error("元素--{}--等待可点击超时".format(locator))
            log.exception(e)
            # 对当前页面进行截图
            self.save_scree_image(img_info)
            raise e
        else:
            # 元素等待出现之后，获取实际
            end_time = time.time()
            log.info("元素--{}--可点击等待成功,等待时间{}秒".format(locator, end_time - start_time))
            return ele

    def wait_element_presence(self, locator, img_info, timeout=15, poll_frequency=0.5):
        """
        等待元素被加载
        :param locator: 定位表达式
        :param img_info: 错误截图文件名
        :param timeout: 等待超时时间
        :param poll_frequency: 等待轮询时间
        :return:
        """
        # 等待元素之前获取当前的时间
        start_time = time.time()
        try:
            ele = WebDriverWait(self.driver, timeout, poll_frequency).until(
                EC.presence_of_element_located(locator)
            )
        except Exception as e:
            # 输出日志
            log.error("元素--{}--等待被加载超时".format(locator))
            log.exception(e)
            # 对当前页面进行截图
            self.save_scree_image(img_info)
            raise e
        else:
            # 元素等待出现之后，获取实际
            end_time = time.time()
            log.info("元素--{}--加载等待成功,等待时间{}秒".format(locator, end_time - start_time))
            return ele

    def get_element_text(self, locator, img_info):
        """
        获取元素的文本
        :param locator: 元素定位表达式
        :param img_info: 错误截图信息
        :return:
        """
        try:
            text = self.driver.find_element(*locator).text
        except Exception as e:
            # 输出日志
            log.error("元素--{}--获取文本失败".format(locator))
            log.exception(e)
            # 对当前页面进行截图
            self.save_scree_image(img_info)
            raise e
        else:
            log.info("元素--{}--获取文本成功".format(locator))
            return text

    def get_element_attribute(self, locator, attr_name, img_info):
        """
        获取元素的文本"
        :param locator: 元素定位表达式
        :param attr_name: 属性名字
        :param img_info: 错误截图信息
        :return:
        """
        try:
            ele = self.driver.find_element(*locator)
            attr_value = ele.get_attribute(attr_name)
        except Exception as e:
            # 输出日志
            log.error("获取元素--{}--属性失败".format(locator))
            log.exception(e)
            # 对当前页面进行截图
            self.save_scree_image(img_info)
            raise e
        else:
            log.info("获取元素--{}--属性成功".format(locator))
            return attr_value

    def click_element(self, locator, img_info):
        """
        点击元素
        :param locator: 元素定位表达式
        :param img_info: 错误截图信息
        :return:
        """
        try:
            self.driver.find_element(*locator).click()
        except Exception as e:
            # 输出日志
            log.error("点击元素--{}--失败".format(locator))
            log.exception(e)
            # 对当前页面进行截图
            self.save_scree_image(img_info)
            raise e
        else:
            log.info("元素--{}--点击成功".format(locator))

    def input_text(self, locator, text_value, img_info):
        """
        文本内容输入
        :param locator: 元素定位表达式
        :param text_value: 输入的文本内容
        :param img_info: 错误截图信息
        :return:
        """
        try:
            
            self.driver.find_element(*locator).send_keys(text_value)
            
        except Exception as e:
            # 输出日志
            log.error("输入文本--{}--失败".format(locator))
            log.exception(e)
            # 对当前页面进行截图
            self.save_scree_image(img_info)
            raise e
        else:
            log.info("文本内容输入--{}--成功".format(locator))

    def get_element(self, locator, img_info):
        """
        获取元素
        :param locator: 元素定位表达式
        :param img_info: 错误截图信息
        :return:
        """
        try:
            ele = self.driver.find_element(*locator)
        except Exception as e:
            # 输出日志
            log.error("获取元素--{}--失败".format(locator))
            log.exception(e)
            # 对当前页面进行截图
            self.save_scree_image(img_info)
            raise e
        else:
            log.info("元素--{}--获取成功".format(locator))
            return ele

    def get_elements(self, locator, img_info):
        """
        获取元素
        :param locator: 元素定位表达式
        :param img_info: 错误截图信息
        :return:
        """
        try:
            eles = self.driver.find_elements(*locator)
        except Exception as e:
            # 输出日志
            log.error("获取元素--{}--失败".format(locator))
            log.exception(e)
            # 对当前页面进行截图
            self.save_scree_image(img_info)
            raise e
        else:
            log.info("元素--{}--获取成功".format(locator))
            return eles
    
    def save_scree_image(self, img_info):
        """
        对当前页面进行截图
        :param img_info: 错误截图信息
        :return:
        """
        start_time = time.time()
        filename = '{}_{}.png'.format(img_info, start_time)
        file_path = os.path.join(ERROR_IMG, filename)
        self.driver.save_screenshot(file_path)
        log.info("错误页面截图成功，图表保存的路径:{}".format(file_path))


    def js_focus_element(self,locator):
        '''js聚焦元素'''
        self.driver.execute_script("arguments[0].click();",locator)


    def js_remove_disable(self,locator):
        "删除输入框的disable属性"
        self.driver.execute_script('arguments[0].removeAttribute(\"disabled\")', locator)

    def move_to_element(self, locator):
        '''鼠标悬停操作'''
        ActionChains(self.driver).move_to_element(locator).perform()


    def arrow_down_enter_to_element(self):
        '''鼠标操作'''
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ARROW_DOWN)
        self.driver.implicitly_wait(5)
        actions.send_keys(Keys.ENTER)  # enter
        self.driver.implicitly_wait(5)
        actions.perform()

    def enter_to_element(self,locator,imginfo):
        """
        键盘enter
        :param locator: 元素定位表达式
        :param img_info: 错误截图信息
        :return:
        """

        self.get_element(locator,imginfo).send_keys(Keys.ENTER)


    def input_pic(self, locator,pic,img_info):
        '''上传图片'''
        try:
            self.driver.find_element(*locator).send_keys(pic)


        except Exception as e:
            # 输出日志
            log.error("获取元素--{}--失败".format(locator))
            log.exception(e)
            # 对当前页面进行截图
            self.save_scree_image(img_info)
            raise e
        else:
            log.info("元素--{}--获取成功".format(locator))


    def select_by_visibleText(self,locator,text,img_info):
        
        try:
            elementList  = self.driver.find_elements(locator)
            for element in elementList:
                element_text = element.text
                if element_text.__contains__(text) == True:
                    element.click()
                    break
        except Exception as e:
            # 输出日志
            log.error("获取元素--{}--失败".format(locator))
            log.exception(e)
            # 对当前页面进行截图
            self.save_scree_image(img_info)
            raise e
        else:

            log.info("元素--{}--获取成功".format(locator))

    def is_element_exist(self, locator, timeout=5):
        """
        检查元素是否存在
        :param locator: 元素定位表达式
        :param timeout: 等待超时时间
        :return: True/False
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except:
            return False

    def wait_for_element_exist(self, locator, timeout=10):
        """
        等待元素存在
        :param locator: 元素定位表达式
        :param timeout: 等待超时时间
        :return: 元素对象
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except Exception as e:
            log.error("元素--{}--等待存在超时".format(locator))
            log.exception(e)
            self.save_scree_image("等待元素存在失败")
            raise e