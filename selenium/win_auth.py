from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def win_auth(url, username, password):
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(3)
    driver.switch_to.alert.send_keys(username + Keys.TAB + password)
    time.sleep(0.5)
    driver.switch_to.alert.accept()
    time.sleep(3)

    links = driver.find_elements_by_xpath(".//a")
    for counter, link in enumerate(links):
        print("[{0}] Url: {1} [{2}]".format(counter, link.get_attribute("href"), link.text))

    driver.close()


if __name__ == "__main__":
    firefox_exe_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    phantomjs_exe_path = r"C:\phantomjs-2.1.1-windows\bin\phantomjs.exe"
    username = "crawler"
    password = "Linkpower2016"
    url = "http://192.168.11.182:8002/about.html"

    win_auth(url, username, password)