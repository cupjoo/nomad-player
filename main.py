import platform
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Migrator:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless = True
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('window-size=1920x1080')
        driver_path = '../chromedriver'
        if "Windows" in platform.platform():
            chrome_options.add_argument('--headless')
            driver_path += '.exe'
        self.driver = webdriver.Chrome(driver_path, options=chrome_options)
        self.driver.implicitly_wait(3)

    def scrap_list(self, seq):
        try:
            melon_link = 'https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm'
            melon_link += '?plylstSeq=' + seq
            self.driver.get(melon_link)
            self.driver.get_screenshot_as_file('melon.png')
            print('scrap successed')
        except:
            self.shutdown('failed to load playlist')

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
            WebDriverWait(self.driver, 5)\
                .until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginHeader"]/a[1]')))
            print('login successed')
        except:
            self.shutdown('failed to login in')

    def add_playlist(self):
        plist = ['painkiller']
        for song in plist:
            try:
                self.driver.find_element_by_id('headerSearchInput').clear()
                self.driver.find_element_by_id('headerSearchInput').send_keys(song)
                self.driver.find_element_by_id('hederSearchFormButton').click()
                self.driver.find_element_by_xpath('//*[@id="DEFAULT0"]/table/tbody/tr[1]/td[8]/a').click()
                WebDriverWait(self.driver, 2)\
                    .until(EC.presence_of_element_located((By.XPATH, '//*[@id="track2playlist"]')))
                self.driver.get_screenshot_as_file('bugs.png')
            except:
                self.shutdown('failed to add playlist')

    def shutdown(self, msg):
        print(msg)
        self.driver.get_screenshot_as_file('fails.png')
        self.driver.close()
        sys.exit()


migrator = Migrator()
# migrator.scrap_list('466034240')
migrator.login('cupjoo@naver.com', 'chl010177@')
migrator.add_playlist()
migrator.shutdown('migration successed!')
