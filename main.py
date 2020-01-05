from selenium import webdriver

class Migrator:
    def add_playlist(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        chrome_options.add_argument('--headless') 
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('window-size=1920x1080')
        driver = webdriver.Chrome('../chromedriver', options=chrome_options)
        driver.implicitly_wait(3)

        driver.get('https://music.bugs.co.kr/')
        driver.get_screenshot_as_file('capture.png')

migrator = Migrator()
migrator.add_playlist()