from module.migrator import BugsMigrator
from module.scrapper import MelonScrapper, BugsScrapper     # list of supporting scrapper

if __name__ == '__main__':
    scrapper = BugsScrapper(email='sample@gmail.com', pw='sample')
    # scrapper = MelonScrapper(email='sample@gmail.com', pw='sample')
    scrapper.scrap(psrno='466034240')   # Playlist Serial Number
    migrator = BugsMigrator(email='sample@naver.com', pw='sample')    # Bugs Email / Password
    migrator.migrate()
