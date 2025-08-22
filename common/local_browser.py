#!/usr/bin/env python3
"""
本地Chrome浏览器管理器 - 支持自动检测环境
本地环境：有头模式（显示浏览器窗口）
Jenkins环境：无头模式（后台运行）
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from common.handle_logging import log

class LocalChromeManager:
    """本地Chrome浏览器管理器"""
    
    def __init__(self):
        # 根据平台自动检测Chrome和ChromeDriver路径
        self.chrome_path, self.chromedriver_path = self._detect_platform_paths()
        
        # 检测运行环境
        self.is_jenkins = self._detect_jenkins_environment()
        if self.is_jenkins:
            log.info("🔍 检测到Jenkins环境，将使用无头模式")
        else:
            log.info("🏠 检测到本地环境，将使用有头模式")
    
    def _detect_platform_paths(self):
        """检测当前平台的Chrome和ChromeDriver路径"""
        import platform
        
        system = platform.system().lower()
        
        if system == "darwin":  # macOS
            chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            chromedriver_path = "/opt/homebrew/bin/chromedriver"
        elif system == "linux":  # Linux
            chrome_path = "/usr/bin/google-chrome"  # 标准Linux Chrome路径
            chromedriver_path = "/usr/bin/chromedriver"  # 标准Linux ChromeDriver路径
        elif system == "windows":  # Windows
            chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            chromedriver_path = "C:\\chromedriver.exe"
        else:
            chrome_path = "/usr/bin/google-chrome"
            chromedriver_path = "/usr/bin/chromedriver"
        
        log.info(f"🔍 检测到平台: {system}")
        log.info(f"🔍 Chrome路径: {chrome_path}")
        log.info(f"🔍 ChromeDriver路径: {chromedriver_path}")
        
        return chrome_path, chromedriver_path
        
        # 检测运行环境
        self.is_jenkins = self._detect_jenkins_environment()
        if self.is_jenkins:
            log.info("🔍 检测到Jenkins环境，将使用无头模式")
        else:
            log.info("🏠 检测到本地环境，将使用有头模式")
    
    def _detect_jenkins_environment(self):
        """检测是否在Jenkins环境中运行"""
        jenkins_vars = [
            'JENKINS_URL',
            'BUILD_NUMBER', 
            'BUILD_ID',
            'WORKSPACE',
            'JOB_NAME'
        ]
        
        for var in jenkins_vars:
            if os.environ.get(var):
                return True
        return False
        
    def create_local_driver(self):
        """创建本地Chrome驱动 - 根据环境自动选择有头/无头模式"""
        try:
            if self.is_jenkins:
                log.info("🚀 正在启动无头Chrome浏览器（Jenkins环境）...")
                return self._create_headless_driver()
            else:
                log.info("🚀 正在启动有头Chrome浏览器（本地环境）...")
                return self._create_headed_driver()
            
        except Exception as e:
            log.error(f"❌ 本地Chrome启动失败: {e}")
            raise e
    
    def _create_headed_driver(self):
        """创建有头Chrome驱动（本地环境）"""
        try:
            # 创建Chrome选项 - 有头模式配置
            chrome_options = Options()
            
            # 基础选项
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--start-maximized')
            
            # 禁用缓存 - 解决304问题
            chrome_options.add_argument('--disable-application-cache')
            chrome_options.add_argument('--disk-cache-size=0')
            chrome_options.add_argument('--disable-cache')
            
            # 基本性能优化
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            
            # 设置Chrome二进制文件路径（仅在路径存在时设置）
            if os.path.exists(self.chrome_path):
                chrome_options.binary_location = self.chrome_path
                log.info(f"✅ 使用本地Chrome: {self.chrome_path}")
            else:
                log.warning(f"⚠️ 本地Chrome路径不存在: {self.chrome_path}")
                log.info("🔄 将使用系统默认Chrome路径")
            
            # 创建Chrome服务 - 支持自动下载ChromeDriver
            if os.path.exists(self.chromedriver_path):
                service = Service(executable_path=self.chromedriver_path)
                log.info(f"✅ 使用本地ChromeDriver: {self.chromedriver_path}")
            else:
                log.warning(f"⚠️ 本地ChromeDriver路径不存在: {self.chromedriver_path}")
                log.info("🔄 将使用Selenium Manager自动下载ChromeDriver")
                service = Service()  # 不指定路径，让Selenium Manager自动处理
            
            # 创建驱动
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # 设置超时
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            
            # 最大化窗口
            driver.maximize_window()
            
            log.info("✅ 有头Chrome浏览器启动成功")
            log.info(f"🌐 会话ID: {driver.session_id}")
            log.info("📺 有头模式：浏览器窗口可见，便于调试")
            
            return driver
            
        except Exception as e:
            log.error(f"❌ 有头Chrome启动失败: {e}")
            raise e
    
    def _create_headless_driver(self):
        """创建无头Chrome驱动（Jenkins环境）"""
        try:
            # 创建Chrome选项 - 无头模式配置
            chrome_options = Options()
            
            # 无头模式
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')  # 无头模式建议禁用GPU
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--remote-debugging-port=9222')  # 远程调试端口
            
            # 禁用缓存
            chrome_options.add_argument('--disable-application-cache')
            chrome_options.add_argument('--disk-cache-size=0')
            chrome_options.add_argument('--disable-cache')
            
            # 无头模式性能优化
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')  # 无头模式可以禁用图片
            # 注意：禁用JavaScript和CSS可能导致页面无法正常渲染，谨慎使用
            # chrome_options.add_argument('--disable-javascript')  # 如果不需要JS可以禁用
            # chrome_options.add_argument('--disable-css')  # 如果不需要样式可以禁用
            
            # 设置Chrome二进制文件路径（仅在路径存在时设置）
            if os.path.exists(self.chrome_path):
                chrome_options.binary_location = self.chrome_path
                log.info(f"✅ 使用本地Chrome: {self.chrome_path}")
            else:
                log.warning(f"⚠️ 本地Chrome路径不存在: {self.chrome_path}")
                log.info("🔄 将使用系统默认Chrome路径")
            
            # 创建Chrome服务 - 支持自动下载ChromeDriver
            if os.path.exists(self.chromedriver_path):
                service = Service(executable_path=self.chromedriver_path)
                log.info(f"✅ 使用本地ChromeDriver: {self.chromedriver_path}")
            else:
                log.warning(f"⚠️ 本地ChromeDriver路径不存在: {self.chromedriver_path}")
                log.info("🔄 将使用Selenium Manager自动下载ChromeDriver")
                service = Service()  # 不指定路径，让Selenium Manager自动处理
            
            # 创建驱动
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # 设置超时
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            
            log.info("✅ 无头Chrome浏览器启动成功")
            log.info(f"🌐 会话ID: {driver.session_id}")
            log.info("📺 无头模式：浏览器在后台运行，不显示窗口")
            
            return driver
            
        except Exception as e:
            log.error(f"❌ 无头Chrome启动失败: {e}")
            raise e

# 创建全局实例
local_chrome_manager = LocalChromeManager()
