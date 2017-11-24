"""
Program dependencies
1. Python3
2. Python packages:
    2.1 selenium
    2.2 requests
    2.3 requests_ntlm
4. FireFox browser
5. Download geckodriver and put in environment variable from https://github.com/mozilla/geckodriver/releases
"""
import os
import time
import logging
from logging.handlers import RotatingFileHandler
import requests
from requests_ntlm import HttpNtlmAuth
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class config:
    # login
    url_login = "http://192.168.11.182:8002/"
    username = "crawler"
    password = "Linkpower2016"

    # crawling config
    url_start_page = "https://blog.scrapinghub.com/"
    depth = 2
    allow_domains = ["blog.scrapinghub.com"]

    # logging
    path_log_dir = "logs"
    path_log = "ird_web_crawler_%Y%m%d.log"
    max_bytes = 10485760 # 10MB 1024^2 * 10
    backup_count = 7


""" global variable """
# for analysis page source
firefox_driver = None
# for checking file format from headers
session_requset = None


def is_file_link(link):
    """
    Check if the url is file link or webpage link
    Args:
        link (str): Url to check if it contains file

    Returns:
        bool: False if it is webpage, otherwise False
    """
    try:
        content_type = requests.head(link).headers['content-type']
        if "text/html" in content_type:
            return False
    except Exception as e:
        logging.warning("Exception in is_file_link {}. Reason:{}".format(link, e))
        return False

    return True


def create_web_driver():
    """
    Function setup two global variables
    1 firefox_driver
    2 session_requset
    """
    logging.info("Create firefox driver")
    global firefox_driver
    firefox_driver = webdriver.Firefox()

    logging.info("Create requests session")
    global session_requset
    session_requset = requests.Session()


def get_login_session():
    """
    Function maintain a login session for two global variables
    1 firefox_driver
    2 session_requset
    """
    logging.info("Retrieve firefox login session")
    firefox_driver.get(config.url_login)
    time.sleep(3)
    firefox_driver.switch_to.alert.send_keys(config.username + Keys.TAB + config.password)
    time.sleep(0.5)
    firefox_driver.switch_to.alert.accept()
    time.sleep(3)
    firefox_driver.close()

    logging.info("Retrieve firefox login session")
    session_requset.get(config.url_login, auth=HttpNtlmAuth(config.username, config.password))


def is_link_valid(url):
    """
    Check if the link should be filtered.
    eg. to discard some pattern in url like
        Javascript file & style sheet
    Args:
        url (str): url to check

    Returns:
        bool: True if the link should not be filtered, otherise False
    """
    discard_pattern = [".CSS", ".JS"]
    for item in discard_pattern:
        if url.upper().endswith(item):
            logging.info("Discard invalid link {}".format(url))
            return False

    for domain in config.allow_domains:
        if domain.upper() in url.upper():
            return True
    else:
        return False


def reformat_link(url):
    """
    Remove the has tag to avoid crawling duplicate pages
    Args:
        url (str): link to reformat
    Returns:
        str: reformatted link
    """
    idx = url.rfind("#")
    if idx == -1:
        return url
    else:
        return url[:idx]


def selenium_get_page_links(url):
    """
    using selenium library & firefox and read the rendered html source
    Args:
        url (str): Link to get source and links

    Returns:
        list (str): all links in the source url
    """
    logging.info("Getting page {}".format(url))
    ret_links = set()

    try:
        firefox_driver.get(url)
        links = firefox_driver.find_elements_by_xpath(".//a")
        for link in links:
            url_link = link.get_attribute("href")
            if url_link:
                add_link = reformat_link(url_link)
                ret_links.add(add_link)
    except Exception as e:
        logging.warning("Exception found on page [{}]. Reason: {}".format(url, e))

    return ret_links


def crawl_pages(depth, file_links, pages_to_crawl, page_skip):
    """
    Recursive function of crawl the webpage and its sub pages
    Args:
        depth (int): Maximum depth of the link to jump
        file_links (list str): All the file links found
        pages_to_crawl (list str): Pages to analyze
        page_skip (list str): Pages analyzed or pages which will not be analyzed like file

    Returns:
        list str: file links found
        list str: analyzed pages
    """

    #TODO
    # add logic to avoid multiple checking of headers
    # now cannot pass previous depth checking pages

    if depth == 0:
        return file_links, page_skip
    else:
        new_depth_pages = set()
        total_pages = len(pages_to_crawl)
        for idx_page, page in enumerate(pages_to_crawl):
            depth_message = "[{}]-[{}/{}]".format(depth, idx_page + 1, total_pages)
            page_links = selenium_get_page_links(page)
            num_page_links = len(page_links)
            logging.info("{} Found {} link".format(depth_message, num_page_links))
            page_skip.add(page)

            url_files = set()
            # url_pages = set()

            for idx_link, link in enumerate(page_links):
                page_message = ">>[{}/{}]".format(idx_link + 1, num_page_links)
                if link in page_skip or link in new_depth_pages or link in pages_to_crawl:
                    continue
                else:
                    if is_link_valid(link):
                        if is_file_link(link):
                            logging.info("{} {} Found file link {}".format(depth_message, page_message, link))
                            url_files.add(link)
                            page_skip.add(link)
                        else:
                            logging.info("{} {} Found new web page {}".format(depth_message, page_message, link))
                            new_depth_pages.add(link)
                    else:
                        logging.info("Discard Invalid links {}".format(link))

            file_links = file_links.union(url_files)
            # new_depth_pages = new_depth_pages.union(url_pages)

        new_depth_pages = new_depth_pages - page_skip
        logging.info("[{}] {} new pages".format(depth, len(new_depth_pages)))

        return crawl_pages(depth - 1, file_links, new_depth_pages, page_skip)


def log_setup():
    """
    Setting logging module
    - create log directory
    - setup logging handlers
    """
    if config.path_log_dir:
        if not os.path.exists(config.path_log_dir):
            os.makedirs(config.path_log_dir)

    file_name_with_date = time.strftime(config.path_log)

    log_file_full_path = os.path.join(config.path_log_dir, file_name_with_date)

    logging.basicConfig(
        # format='%(asctime)s - %(levelname)s [%(filename)s] %(message)s'
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        level=logging.INFO,
        handlers=[
            RotatingFileHandler(log_file_full_path, maxBytes=config.max_bytes, backupCount=config.backup_count),
            # logging.FileHandler(log_file_full_path),
            logging.StreamHandler()
        ]
    )


def main():
    """
    Main Program
    Flow:
    1. Setup log
    2. Create web driver
    3. Get login session
    4. Execute crawling process
    5. Display results
    """
    try:
        log_setup()
        create_web_driver()
        # get_login_session()
        start_time = time.time()
        files, crawled_pages = crawl_pages(config.depth, set(), [config.url_start_page], set())
        end_time = time.time()

        logging.info(">>>> Summary")
        logging.info(">> Depth {}".format(config.depth))
        logging.info(">> Number of file links found: {}".format(len(files)))
        logging.info(">> Number of page analysed: {}".format(len(crawled_pages)))
        logging.info(">> Time used (s): {}".format(end_time - start_time))
        logging.info(">> List of files:\n>>>>{}\n".format("\n>>>> ".join(files)))

    except Exception as e:
        logging.exception(str(e))

    if firefox_driver:
        logging.info("Closing firefox driver")
        firefox_driver.close()

    logging.info("Program End")

if __name__ == "__main__":
    main()