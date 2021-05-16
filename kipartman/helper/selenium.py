import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as ui
import os
import pyvirtualdisplay

class Display(object):
    def __init__(self, virtual=True, *args, **kwargs):
        
        self.virtual = virtual
        self.driver = pyvirtualdisplay.Display(*args, **kwargs)
            
        if 'DISPLAY' in os.environ:
            self.display = os.environ["DISPLAY"]
        else:
            self.display = ':0'
        self.vdisplay = None
                    
    def __del__(self):
        if self.vdisplay is not None:
            self.driver.stop()

    def __enter__(self):
        if self.virtual and self.vdisplay is None:
            self.driver.start()
            self.vdisplay = self.driver.new_display_var
            
        if self.vdisplay is not None:
            os.environ["DISPLAY"] = self.vdisplay
        else:
            os.environ["DISPLAY"] = self.display

        return self
          
    def __exit__(self, *args):
        os.environ["DISPLAY"] = self.display


# Debug tools
# show sent headers: https://www.httpbin.org/headers
class Proxy(object):
    def __init__(self, http_proxy, https_proxy=None):
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy 
        
class Browser(object):
    def __init__(self, headless=False, proxy=None, bot_protection=False, vdisplay=False):
        self.headless = headless
        self.proxy = proxy
        self.bot_protection = bot_protection
        
        self.browser = None
    
        if vdisplay==True:
            self.display = Display(virtual=True, visible=False, size=(1920, 1080))
        else:
            self.display = Display(virtual=False)
        
        self.default_window = None
        self.windows = {}
        
    def __del__(self):
        self.close()

    def _is_alive(self):
        if self.browser is None:
            return False
        try:
            self.browser.window_handles
        except Exception as e:
            print(e)
            return False
#         if 'disconnected:' in self.browser.get_log('driver')[-1]['message']:
#             self.browser.quit()
#             return False
        return True
    
    def open_url(self, url, focus=False):
        print(f"browse {url}")
        self.create_browser()
        
        self.browser.get(url)

    def open_tab(self, url, name, focus=False):
        print(f"browse {url} in tab {name}")
        self.create_browser()
        
        if self.default_window is None:
            self.browser.get(url)
            self.default_window = self.browser.current_window_handle
            self.windows[name] = self.default_window
        else:
            window = None
            if name in self.windows:
                window = self.windows[name]
            if window is not None:
                try:
                    self.browser.switch_to.window(window)
                    self.browser.get(url)
                except:
                    del self.windows[name]
                    window = None
            
            if window is None:
                self.browser.execute_script(f"window.open('{url}', '_blank');")
                self.windows[name] = self.browser.current_window_handle
            
    def close_tab(self, name):
        if name in self.windows:
            try:
                window = self.windows[name]
                self.browser.switch_to.window(window)
                self.browser.driver.close()
            except:
                pass
            del self.windows[name]

    def close(self):
        if self.browser is not None:
            self.browser.quit()
        self.browser = None
            
class Firefox(Browser):
    # for bo detection
    # https://stackoverflow.com/questions/57122151/exclude-switches-in-firefox-webdriver-options
    
    def __init__(self, *args, **kwargs):
        super(Firefox, self).__init__(*args, **kwargs)

    def create_browser(self):
        if self._is_alive():
            return 

        self.default_window = None
        self.windows = {}

        options = FirefoxOptions()
        
        if self.headless==True:
            options.add_argument('--headless')
    #     options.add_argument('--private')

        profile = None
        if self.proxy is not None or self.bot_protection==True:
            profile = webdriver.FirefoxProfile()
        
#         if self.proxy is not None:
#             PROXY_HOST = "12.12.12.123"
#             PROXY_PORT = "1234"
#             profile.set_preference("network.proxy.type", 1)
#             profile.set_preference("network.proxy.http", PROXY_HOST)
#             profile.set_preference("network.proxy.http_port", int(PROXY_PORT))
        if self.bot_protection==True:
            # options for bot detection
            profile.set_preference("dom.webdriver.enabled", False)
            profile.set_preference('useAutomationExtension', False)
#             profile.set_preference('devtools.jsonview.enabled', False)
        
        if profile is not None:
            # open window / preferences
            profile.set_preference('browser.link.open_newwindow', 3)    # prefer tab
            profile.set_preference('browser.link.open_newwindow.restriction', 0)
        
            profile.update_preferences()
            desired = DesiredCapabilities.FIREFOX

            with self.display:        
                self.browser = webdriver.Firefox(options=options, firefox_profile=profile, desired_capabilities=desired)
        else:
            with self.display:        
                self.browser = webdriver.Firefox(options=options)
            
        self.browser.install_addon(os.path.abspath("resources/firefox/i_dont_care_about_cookies-3.2.9-an+fx.xpi"))
        self.browser.implicitly_wait(1) # poll every second when waiting for an element

#     def open_tab(self, url, name, activate=False):
#         # focus on last tab
#         self.browser.switch_to.window(self.browser.window_handles[len(self.browser.window_handles)-1])
#         # open a tab after
#         self.browser.execute_script("window.open('');")
#         # focus on it
#         self.browser.switch_to.window(self.browser.window_handles[len(self.browser.window_handles)-1])

# class Chrome(Browser):
#     # For bot detection
#     # https://stackoverflow.com/questions/56528631/is-there-a-version-of-selenium-webdriver-that-is-not-detectable/56529616#56529616
#     # https://stackoverflow.com/questions/59174899/what-is-the-difference-in-accessing-cloudflare-website-using-chromedriver-chrome
#     # https://blog.m157q.tw/posts/2020/09/11/bypass-cloudflare-detection-while-using-selenium-with-chromedriver/
# 
# 
#     def __init__(self, *args, **kwargs):
#         super(Chrome, self).__init__(*args, **kwargs)
# 
#     def create_browser(self):
#         if self.browser is not None:
#             return 
# 
#         # TODO the plugin i_dont_care_about_cookies does not work by default in incognito mode (in chrome://extensions can be activated manually) 
#         options = ChromeOptions()
#         
#         if self.headless==True:
#             options.add_argument('--headless')
#             
#         options.add_argument("--new-window")
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")
#         
#         # prevent bot detection
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option('useAutomationExtension', False)
#         options.add_argument("--disable-blink-features=AutomationControlled")
# 
#     #     options.add_argument('--incognito')
#         options.add_extension(os.path.abspath("resources/chrome/i_dont_care_about_cookies-3.2.9-an+fx.crx"));
#         options.add_argument('--user-data-dir=/home/seb/.config/google-chrome/Default')
#         
#         self.browser = webdriver.Chrome(options=options)
#         agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
#         self.browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": agent})
#         self.browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
# #         self.browser.implicitly_wait(1.) # poll every second when waiting for an element

class Opera(Browser):

    def __init__(self, *args, **kwargs):
        super(Opera, self).__init__(*args, **kwargs)

    def create_browser(self):
        if self.browser is not None:
            return 
        
        # TODO

class Edge(Browser):

    def __init__(self, *args, **kwargs):
        super(Edge, self).__init__(*args, **kwargs)


    def __init__(self, headless=False):
        pass

    def create_browser(self):
        if self.browser is not None:
            return 
        
        # TODO
