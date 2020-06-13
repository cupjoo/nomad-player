from module.migrator import BugsMigrator, YoutubeMigrator
from module.scrapper import MelonScrapper, BugsScrapper


def scrap():
    # Bugs Scrapper
    # - No login required
    # - Scrap liked playlist
    #
    # scrapper = BugsScrapper(email='sample@naver.com', pw='sample')
    # scrapper.scrap()

    # Melon Scrapper
    # - Login required
    # - Scrap selected playlist with Serial Number (psrno)
    #
    scrapper = MelonScrapper()
    scrapper.scrap(psrno='466034240')


def migrate():
    # Bugs Migrator
    # - Login required
    # - Migrate Playlist from 'Playlist.txt' to 'liked playlist'
    #
    # migrator = BugsMigrator(email='sample@gmail.com', pw='sample')  # Bugs Email / Password
    # migrator.migrate()

    # Youtube Music Migrator
    # - Login required
    # - Migrate Playlist from 'Playlist.txt' to 'songs'
    #
    migrator = YoutubeMigrator(email='sample@gmail.com', pw='sample')
    migrator.migrate()


if __name__ == '__main__':
    scrap()
    migrate()
