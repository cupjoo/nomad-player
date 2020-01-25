# Bugs Migrator

Simple playlist migrator app from Melon to Bugs with crawling.

## Screenshot

![screenshot.gif](docs/screenshot.gif)

## Release Note (Ver 2.0)
- Supports multiprocessing

## Prerequisites
This application will proceed in the following environment (Recommended).
- Python 3.7
- Chrome Driver [79.0.3945.36](https://chromedriver.storage.googleapis.com/index.html?path=79.0.3945.36/)

Before running the app, the `chrome browser` and `chrome driver` with same version is needed. Check the version of chrome browser with following command.
```bash
google-chrome --version
```

## Installation
Following commands run on Ubuntu 18.04. There are some variations on Windows.
```bash
$ git clone https://github.com/cupjoo/bugs-migrator.git
$ virtualenv venv && . venv/bin/activate
$ cd bugs-migrator
$ pip install -r requirements/requirement.txt
```

## How to run app
- Before run the app, fill the arguments with your bugs account and serial number of playlist.

![args.png](https://i.imgur.com/D90H1NB.png)

- Run 'main.py' with python3.
```bash
$ python main.py
```
- Then, the songs are added to at the top of the playlist you created in Bugs.

## Caution
Too many attempts to run the app in a short period of time can result in restricted access from the melon (maybe for about 10~20 minutes).
