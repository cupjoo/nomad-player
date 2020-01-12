import os
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
        self.driver.implicitly_wait(3)

    def scrap_1_page(self):
        # parse playlist
        plist = []
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        title = soup.select('#frm > div > table > tbody > tr > td:nth-child(5) > div > div > '
                            'div.ellipsis.rank01 > span > a')
        album = soup.select('#frm > div > table > tbody > tr > td:nth-child(6) > div > div > div > a')
        for i in range(len(title)):
            plist.append(title[i].text + ' ' + album[i].text)
        return plist

    def scrap_playlist(self, seq):
        playlist = []
        try:
            melon_link = 'https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm'
            self.driver.get(melon_link+'?plylstSeq='+seq)
            max_page = int(self.driver
                           .find_element_by_xpath('//*[@id="conts"]/div[4]/div[1]/h5/span')
                           .text.strip('()')
            )
            max_page = int(max_page/50) + (2 if max_page % 50 > 0 else 1)

            playlist.extend(self.scrap_1_page())
            for page_num in range(1, max_page):
                self.driver.execute_script("javascript:pageObj.sendPage('"+str(page_num*50+1)+"')")
                playlist.extend(self.scrap_1_page())

            # save playlist to local
            with open('Playlist.txt', 'w', encoding="utf-8") as f:
                for song in playlist:
                    f.write("%s\n" % song)
            print('Scrap Melon Playlist Successed')
        except:
            self.shutdown('Failed to scrap Melon Playlist')

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
            self.shutdown('Failed to Bugs Login')

    def add_playlist(self):
        try:
            with open('Playlist.txt', 'r', encoding="utf-8") as f:
                plist = f.readlines()
        except FileNotFoundError:
            self.shutdown('Failed to load local playlist')

        for song in plist:
            try:
                # search song info
                self.driver.find_element_by_id('headerSearchInput').clear()
                self.driver.find_element_by_id('headerSearchInput').send_keys(song)
                self.driver.find_element_by_id('hederSearchFormButton').click()
                WebDriverWait(self.driver, 2) \
                    .until(EC.presence_of_element_located((By.ID, 'DEFAULT0')))

                # add song to first playlist
                self.driver.find_element_by_xpath('//*[@id="DEFAULT0"]/table/tbody/tr[1]/td[8]/a').click()
                self.driver.find_element_by_xpath('//*[@id="track2playlistScrollArea"]/div/div/ul/li[2]/a').click()
                self.driver.find_element_by_xpath('//*[@id="bugsAlert"]/section/p/button').click()
            except NoSuchElementException:
                self.shutdown('Failed to add songs to Bugs Playlist')
        try:
            os.remove(r"Playlist.txt")
            print('Add Playlist to Bugs Successed')
        except OSError:
            self.shutdown('Failed to remove local playlist')

    def shutdown(self, msg):
        print(msg)
        self.driver.get_screenshot_as_file('fails.png')
        self.driver.close()
        sys.exit()


bugs_migrator = Migrator()
bugs_migrator.scrap_playlist('466034240')   # Playlist Serial Number
bugs_migrator.login('', '')                 # Bugs Account (Email) / Password
bugs_migrator.add_playlist()
bugs_migrator.shutdown('Migration Successed!')
