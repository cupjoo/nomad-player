from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urlencode

class Migrator:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        chrome_options.add_argument('--headless') 
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('window-size=1920x1080')
        self.driver = webdriver.Chrome('../chromedriver', options=chrome_options)
        self.driver.implicitly_wait(3)
        
    def crawl_list(self, seq):
        try:
            melon_link='https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm'
            melon_link+='?plylstSeq='+seq
            self.driver.get(melon_link)
            self.driver.get_screenshot_as_file('melon.png')
        except:
            self.shutdown()
    
    def add_playlist(self, email, password):
        try:
            # 벅스 아이디 로그인
            self.driver.get('https://music.bugs.co.kr/')
            self.driver.find_element_by_id('loginHeader').click()
            self.driver.find_element_by_id('to_bugs_login').click()
            self.driver.find_element_by_id('user_id').send_keys(email)
            self.driver.find_element_by_id('passwd').send_keys(password)
            self.driver.get_screenshot_as_file('bugs.png')
        except:
            self.shutdown()
    
    def shutdown(self):
        self.driver.close()

migrator = Migrator()
migrator.crawl_list('466034240')
migrator.add_playlist('id', 'pw')
migrator.shutdown()