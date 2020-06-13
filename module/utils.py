import platform
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def youtube_login(driver, email, pw):
    success = True
    try:
        driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27')
        driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
        driver.find_element_by_id('identifierId').send_keys(email)
        driver.find_element_by_id('identifierNext').click()
        sleep(3)
        driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(pw)
        driver.find_element_by_id('passwordNext').click()
        sleep(3)
        driver.get('https://music.youtube.com/')
        sleep(2)
    except NoSuchElementException:
        success = False
        shutdown(msg='Failed to Youtube Login', driver=driver)
    finally:
        return success


def bugs_login(driver, email, pw):
    success = True
    try:
        # login with bugs account
        driver.get('https://music.bugs.co.kr/')
        driver.find_element_by_id('loginHeader').click()
        driver.find_element_by_id('to_bugs_login').click()
        driver.find_element_by_id('user_id').send_keys(email)
        driver.find_element_by_id('passwd').send_keys(pw)
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
