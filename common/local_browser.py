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
import shutil

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
        """检测当前平台的Chrome和ChromeDriver路径。
        优先级：环境变量 > 常见路径 > PATH 可执行文件。
        支持 Linux 上的 chromium/chromium-browser，以及 macOS 的 Google Chrome。
        """
        import platform

        def first_existing(candidates):
            for path in candidates:
                if path and os.path.exists(path):
                    return path
                # 支持可执行名，通过 PATH 解析
                if path and os.path.sep not in path:
                    found = shutil.which(path)
                    if found:
                        return found
            return None

        system = platform.system().lower()

        # 允许通过环境变量覆盖
        env_chrome = os.environ.get("CHROME_BIN") or os.environ.get("SE_CHROME_BINARY")
        env_chromedriver = os.environ.get("CHROMEDRIVER_PATH") or os.environ.get("WEBDRIVER_CHROME_DRIVER")

        if system == "darwin":  # macOS
            chrome_candidates = [
                env_chrome,
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "google-chrome",
                "chrome",
            ]
            driver_candidates = [
                env_chromedriver,
                "/opt/homebrew/bin/chromedriver",
                "/usr/local/bin/chromedriver",
                "chromedriver",
            ]
        elif system == "linux":  # Linux
            chrome_candidates = [
                env_chrome,
                "/usr/bin/google-chrome",
                "/usr/bin/chromium",
                "/usr/bin/chromium-browser",
                "/snap/bin/chromium",
                "google-chrome",
                "chromium",
                "chromium-browser",
            ]
            driver_candidates = [
                env_chromedriver,
                "/usr/bin/chromedriver",
                "/usr/lib/chromium/chromedriver",
                "/snap/bin/chromium.chromedriver",
                "chromedriver",
            ]
        elif system == "windows":  # Windows
            chrome_candidates = [
                env_chrome,
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            ]
            driver_candidates = [
                env_chromedriver,
                "C:\\chromedriver.exe",
            ]
        else:
            chrome_candidates = [env_chrome, "/usr/bin/google-chrome", "google-chrome"]
            driver_candidates = [env_chromedriver, "/usr/bin/chromedriver", "chromedriver"]

        chrome_path = first_existing(chrome_candidates) or chrome_candidates[0]
        chromedriver_path = first_existing(driver_candidates) or driver_candidates[0]

        log.info(f"🔍 检测到平台: {system}")
        log.info(f"🔍 Chrome路径候选: {chrome_path}")
        log.info(f"🔍 ChromeDriver路径候选: {chromedriver_path}")

        return chrome_path or "", chromedriver_path or ""
        
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
            if self.chrome_path and os.path.exists(self.chrome_path):
                chrome_options.binary_location = self.chrome_path
                log.info(f"✅ 使用本地Chrome: {self.chrome_path}")
            else:
                log.warning(f"⚠️ 本地Chrome路径不存在: {self.chrome_path}")
                log.info("🔄 将使用系统默认Chrome路径")
            
            # 创建Chrome服务 - 支持自动下载ChromeDriver
            if self.chromedriver_path and os.path.exists(self.chromedriver_path):
                service = Service(executable_path=self.chromedriver_path)
                log.info(f"✅ 使用本地ChromeDriver: {self.chromedriver_path}")
            else:
                log.warning(f"⚠️ 本地ChromeDriver路径不存在: {self.chromedriver_path}")
                # 在 aarch64 等平台，Selenium Manager 可能不支持。仅当找不到时再让它尝试。
                service = Service()  # 不指定路径，让Selenium Manager自动处理（若可用）
            
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
            if self.chrome_path and os.path.exists(self.chrome_path):
                chrome_options.binary_location = self.chrome_path
                log.info(f"✅ 使用本地Chrome: {self.chrome_path}")
            else:
                log.warning(f"⚠️ 本地Chrome路径不存在: {self.chrome_path}")
                log.info("🔄 将使用系统默认Chrome路径")
            
            # 创建Chrome服务 - 支持自动下载ChromeDriver
            if self.chromedriver_path and os.path.exists(self.chromedriver_path):
                service = Service(executable_path=self.chromedriver_path)
                log.info(f"✅ 使用本地ChromeDriver: {self.chromedriver_path}")
            else:
                log.warning(f"⚠️ 本地ChromeDriver路径不存在: {self.chromedriver_path}")
                # 在 aarch64 等平台，Selenium Manager 可能不支持。仅当找不到时再让它尝试。
                service = Service()  # 不指定路径，让Selenium Manager自动处理（若可用）
            
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
