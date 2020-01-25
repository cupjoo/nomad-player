import platform
from multiprocessing import Pool
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_driver():
    driver_path = '../chromedriver'
    if "Windows" in platform.platform():
        driver_path += '.exe'
    driver = webdriver.Chrome(driver_path)
    driver.implicitly_wait(2)
    return driver


def shutdown(msg, driver=None):
    if driver is not None:
        driver.quit()
    print(msg)


class MelonScrapper:
    def __init__(self):
        self.driver = get_driver()

    def scrap_page(self, page=None):
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

    def scrap(self, psrno):
        try:
            self.driver.get('https://www.melon.com/mymusic/dj/mymusicdjplaylistview_inform.htm?plylstSeq=' + psrno)
            max_page = int(self.driver.find_element_by_xpath('//*[@id="conts"]/div[4]/div[1]/h5/span').text.strip('()'))
            max_page = int(max_page / 50) + (2 if max_page % 50 > 0 else 1)

            plist = [self.scrap_page()]
            for page_num in range(1, max_page):
                plist.append(self.scrap_page(page_num))

            with open('Playlist.txt', 'w', encoding="utf-8") as f:
                for song in plist:
                    f.write("%s\n" % song)
            f.close()
            print('Scrap Melon Playlist Successed')
        except:
            shutdown(msg='Failed to scrap Melon Playlist', driver=self.driver)


class BugsMigrator:
    def __init__(self, email, pw):
        self.email = email
        self.pw = pw
        self.failure_list = []

    def read_playlist(self):
        try:
            with open('Playlist.txt', 'r', encoding="utf-8") as f:
                plist = f.readlines()
                f.close()
                return plist
        except FileNotFoundError:
            shutdown(msg='Failed to load local playlist')

    def login(self, driver):
        success = True
        try:
            # login with bugs account
            driver.get('https://music.bugs.co.kr/')
            driver.find_element_by_id('loginHeader').click()
            driver.find_element_by_id('to_bugs_login').click()
            driver.find_element_by_id('user_id').send_keys(self.email)
            driver.find_element_by_id('passwd').send_keys(self.pw)
            driver.find_element_by_xpath('//*[@id="frmLoginLayer"]/div/div/button').click()
            driver.find_element_by_xpath('//*[@id="frmLoginLayer"]/div/div/button').click()
            WebDriverWait(driver, 3) \
                .until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginHeader"]/a[1]')))
            print('Bugs Login Successed')
        except NoSuchElementException:
            success = False
            shutdown(msg='Failed to Bugs Login', driver=driver)
        finally:
            return success

    def add_playlist(self, plist):
        driver = get_driver()
        success = self.login(driver)
        WebDriverWait(driver, 3) \
            .until(EC.presence_of_element_located((By.ID, 'headerSearchInput')))

        if success:
            for song in plist:
                # search song info
                driver.find_element_by_id('headerSearchInput').clear()
                driver.find_element_by_id('headerSearchInput').send_keys(song)
                driver.find_element_by_id('hederSearchFormButton').click()

                try:
                    driver.find_element_by_id('DEFAULT0')
                    # add song to first playlist
                    driver.find_element_by_xpath('//*[@id="DEFAULT0"]/table/tbody/tr[1]/td[8]/a').click()
                    driver.find_element_by_xpath('//*[@id="track2playlistScrollArea"]/div/div/ul/li[2]/a').click()
                    driver.find_element_by_xpath('//*[@id="bugsAlert"]/section/p/button').click()
                except NoSuchElementException:
                    # add failure playlist
                    self.failure_list.append(song)
                    pass

        self.save_failure(plist=None if success else plist)
        print('Add Playlist to Bugs Successed')

    def save_failure(self, plist=None):
        with open('Failure_list.txt', 'a', encoding="utf-8") as f:
            if plist is not None:
                for song in plist:
                    f.write("%s" % song)
            for song in self.failure_list:
                f.write("%s" % song)

    def migrate(self):
        # add playlist with multiprocessing
        process_num = 4
        plist = self.read_playlist()
        n = int(len(plist) / process_num + len(plist) % process_num)
        plist = [plist[i:i + n] for i in range(0, len(plist), n)]

        pool = Pool(processes=process_num)
        pool.map(self.add_playlist, plist)
        shutdown(msg='Migration Successed!')


if __name__ == '__main__':
    scrapper = MelonScrapper()
    scrapper.scrap(psrno='466034240')   # Playlist Serial Number
    migrator = BugsMigrator(email='sample@naver.com', pw='sample')    # Bugs Email / Password
    migrator.migrate()
