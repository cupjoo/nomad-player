import platform
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Migrator:
    def __init__(self):
        driver_path = '../chromedriver'
        if "Windows" in platform.platform():
            driver_path += '.exe'
        self.driver = webdriver.Chrome(driver_path)
        self.driver.implicitly_wait(2)
        self.failure_list = []

    def scrap_1_page(self, page=None):
        # parse page
        if page is not None:
            self.driver.execute_script("javascript:pageObj.sendPage('" + str(page * 50 + 1) + "')")
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        title = soup.select('#frm > div > table > tbody > tr > td:nth-child(5) > div > div > '
                            'div.ellipsis.rank01 > span > a')
        album = soup.select('#frm > div > table > tbody > tr > td:nth-child(6) > div > div > div > a')

        plist = []
        for i in range(len(title)):
            plist.append(title[i].text + ' ' + album[i].text)
        return plist

    def scrap_playlist(self, psrno):
        try:
            self.driver.get('https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=' + psrno)
            max_page = int(self.driver.find_element_by_xpath('//*[@id="conts"]/div[4]/div[1]/h5/span').text.strip('()'))
            max_page = int(max_page / 50) + (2 if max_page % 50 > 0 else 1)

            plist = [self.scrap_1_page()]
            for page_num in range(1, max_page):
                plist.append(self.scrap_1_page(page_num))

            with open('Playlist.txt', 'w', encoding="utf-8") as f:
                for song in plist:
                    f.write("%s\n" % song)
            f.close()
            print('Scrap Melon Playlist Successed')
        except:
            self.shutdown('Failed to scrap Melon Playlist', False)

    def read_playlist(self):
        try:
            with open('Playlist.txt', 'r', encoding="utf-8") as f:
                plist = f.readlines()
                f.close()
                return plist
        except FileNotFoundError:
            self.shutdown('Failed to load local playlist', False)

    def login(self, email, password):
        try:
            # login with bugs account
            self.driver.get('https://music.bugs.co.kr/')
            self.driver.find_element_by_id('loginHeader').click()
            self.driver.find_element_by_id('to_bugs_login').click()
            self.driver.find_element_by_id('user_id').send_keys(email)
            self.driver.find_element_by_id('passwd').send_keys(password)
            self.driver.find_element_by_xpath('//*[@id="frmLoginLayer"]/div/div/button').click()
            self.driver.find_element_by_xpath('//*[@id="frmLoginLayer"]/div/div/button').click()
            WebDriverWait(self.driver, 3) \
                .until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginHeader"]/a[1]')))
            print('Bugs Login Successed')
        except NoSuchElementException:
            self.shutdown('Failed to Bugs Login', False)

    def add_playlist(self, plist):
        WebDriverWait(self.driver, 3) \
            .until(EC.presence_of_element_located((By.ID, 'headerSearchInput')))
        for song in plist:
            # search song info
            self.driver.find_element_by_id('headerSearchInput').clear()
            self.driver.find_element_by_id('headerSearchInput').send_keys(song)
            self.driver.find_element_by_id('hederSearchFormButton').click()

            try:
                self.driver.find_element_by_id('DEFAULT0')
                # add song to first playlist
                self.driver.find_element_by_xpath('//*[@id="DEFAULT0"]/table/tbody/tr[1]/td[8]/a').click()
                self.driver.find_element_by_xpath('//*[@id="track2playlistScrollArea"]/div/div/ul/li[2]/a').click()
                self.driver.find_element_by_xpath('//*[@id="bugsAlert"]/section/p/button').click()
            except NoSuchElementException:
                # add failure playlist
                self.failure_list.append(song)
                pass
        print('Add Playlist to Bugs Successed')

    def shutdown(self, msg, flag):
        if not flag:
            self.driver.get_screenshot_as_file('fails.png')
        print(msg)

        # save failure playlist to local
        with open('Failure_list.txt', 'a', encoding="utf-8") as f:
            for song in self.failure_list:
                f.write("%s" % song)
        f.close()
        self.driver.close()
        sys.exit()

    def start(self, psrno=None, bid=None, pw=None, remainder=True):
        if psrno is not None:
            self.scrap_playlist(psrno)

        if all(info is not None for info in [bid, pw, remainder]):
            plist = self.read_playlist()
            
            # add playlist with n threads
            self.login(bid, pw)
            self.add_playlist(plist)
        self.shutdown('Migration Successed!', True)


if __name__ == '__main__':
    bugs_migrator = Migrator()
    bugs_migrator.start(
        psrno='466034240',  # Playlist Serial Number
        bid='sample@naver.com',  # Bugs Account (Email)
        pw='sample',  # Bugs Password
    )
