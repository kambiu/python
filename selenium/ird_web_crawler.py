from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re


class config:
    # login
    url_login = "http://192.168.11.182:8002/"
    username = "crawler"
    password = "Linkpower2016"

    # crawling config
    url_start_page = "https://blog.scrapinghub.com/"
    depth = 1
    stay_domain = True


# global variable
firefox_driver = None


def is_file_link(link):
    check_string = link[link.rfind("/"):]
    pattern = r"\.(.+$)"
    r = re.findall(pattern, check_string)
    if r:
        if r[0].upper() in "HTML,JSP,PHP,ASPX":
            return False
        else:
            return True
    else:
        return False


def create_web_driver():
    global firefox_driver
    firefox_driver = webdriver.Firefox()


def get_login_session():
    global firefox_driver
    firefox_driver.get(config.url_login)
    time.sleep(3)
    firefox_driver.switch_to.alert.send_keys(config.username + Keys.TAB + config.password)
    time.sleep(0.5)
    firefox_driver.switch_to.alert.accept()
    time.sleep(3)
    firefox_driver.close()


def get_page_links(url):
    print("Getting page {}".format(url))
    ret_file = set()
    ret_page = set()

    try:
        firefox_driver.get(url)
        links = firefox_driver.find_elements_by_xpath(".//a")
        for link in links:
            url_link = link.get_attribute("href")
            if url_link is None:
                continue
            if is_file_link(url_link):
                ret_file.add(url_link)
            else:
                ret_page.add(url_link)
    except Exception as e:
        print("Warning: Exception found on page {}".format(url))

    return ret_file, ret_page


def crawl_pages(depth, file_links, pages_to_crawl, page_crawled):
    if depth == 0:
        return file_links
    else:
        new_depth_pages = set()
        total_pages = len(pages_to_crawl)
        for idx, page in enumerate(pages_to_crawl):
            url_files, url_pages = get_page_links(page)
            print("[{} - {}/{}] Found {} files and {} pages".format(depth, idx, total_pages, len(url_files), len(url_pages)))
            page_crawled.add(page)
            file_links = file_links.union(url_files)
            new_depth_pages = new_depth_pages.union(url_pages)

        new_depth_pages = new_depth_pages - page_crawled
        print("[{}] {} new pages".format(depth, len(new_depth_pages)))

        return crawl_pages(depth-1, file_links, new_depth_pages, page_crawled)


def main():
    try:
        create_web_driver()
        # get_login_session()
        links = crawl_pages(2, set(), [config.url_start_page], set())
        print("Number of file links: {}".format(len(links)))
    except Exception as e:
        print("Exception!!!\n{}\n------------".format(e))

        if firefox_driver:
            firefox_driver.close()

if __name__ == "__main__":
    main()