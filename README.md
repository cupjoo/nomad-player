## Bugs Migrator

Simple playlist migrator app from Melon to Bugs with crawling.

### Prerequisites
Before running the app, the `chrome browser` and `chrome driver` with same version is needed. Recommended driver version is [79.0.3945.36](https://chromedriver.storage.googleapis.com/index.html?path=79.0.3945.36/).

Check the version of chrome browser with following command.
```bash
google-chrome --version
```

### Run app
```bash
$ git clone https://github.com/cupjoo/bugs-migrator.git
$ virtualenv venv && . venv/bin/activate
$ cd bugs-migrator
$ pip install -r requirements/requirement.txt
$ python main.py
```