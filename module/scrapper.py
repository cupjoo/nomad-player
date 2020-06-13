from abc import ABCMeta, abstractmethod

from bs4 import BeautifulSoup

from module.utils import shutdown, get_driver, bugs_login


class Scrapper(metaclass=ABCMeta):
    def __init__(self, email=None, pw=None):
        self.driver = get_driver()
        self.email = email
        self.pw = pw

    @abstractmethod
    def scrap_page(self):
        pass

    @abstractmethod
    def scrap(self, psrno):
        pass


class MelonScrapper(Scrapper):
    def __init__(self, email=None, pw=None):
        print('No login is required for Melon Scrapper')
        super().__init__()

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