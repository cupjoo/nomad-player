from bs4 import BeautifulSoup
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        
    def scrap_list(self, seq):
        try:
            melon_link='https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm'
            melon_link+='?plylstSeq='+seq
            self.driver.get(melon_link)
            self.driver.get_screenshot_as_file('melon.png')
        except:
            print('failed to load playlist')
            self.shutdown()
    
    def login(self, email, password):
        try:
            # 벅스 아이디 로그인
            self.driver.get('https://music.bugs.co.kr/')
            self.driver.find_element_by_id('loginHeader').click()
            self.driver.find_element_by_id('to_bugs_login').click()
            self.driver.find_element_by_id('user_id').send_keys(email)
            self.driver.find_element_by_id('passwd').send_keys(password)
            self.driver.find_element_by_xpath('//*[@id="frmLoginLayer"]/div/div/button').click()
            self.driver.find_element_by_xpath('//*[@id="frmLoginLayer"]/div/div/button').click()
        except:
            print('failed to login in')
            self.shutdown()
    
    def add_playlist(self):
        plist = ['painkiller']
        for song in plist:
            try:
                self.driver.find_element_by_id('headerSearchInput').clear()
                self.driver.find_element_by_id('headerSearchInput').send_keys(song)
                self.driver.find_element_by_id('hederSearchFormButton').click()
                soup = bs4(self.driver.page_source, 'html.parser')
                print(self.driver.find_element_by_xpath('//*[@id="DEFAULT0"]/table/tbody/tr[1]/td[8]/a')
                      .get_attribute("onclick"))
                # self.driver.get_screenshot_as_file('bugs.png')
            except:
                print('failed to add playlist')
                self.shutdown()
    
    def shutdown(self):
        self.driver.close()

migrator = Migrator()
#migrator.scrap_list('466034240')
migrator.login('', '')
migrator.add_playlist()
migrator.shutdown()