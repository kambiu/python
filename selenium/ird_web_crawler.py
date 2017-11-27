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
    # url_start_page = "http://192.168.11.182:8002/"
    url_start_page = "https://blog.scrapinghub.com/"
    depth = 2
    allow_domains = ["blog.scrapinghub.com", "192.168.11.182:8002"]

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
        content_type = session_requset.head(link).headers['content-type']
        if not "text/html" in content_type:
            return True
    except Exception as e:
        logging.warning("Exception in is_file_link {}. Reason:{}".format(link, e))

    return False



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
    try:
        global firefox_driver
        logging.info("Retrieve firefox login session")
        firefox_driver.get(config.url_login)
        time.sleep(3)
        firefox_driver.switch_to.alert.send_keys(config.username + Keys.TAB + config.password)
        time.sleep(0.5)
        firefox_driver.switch_to.alert.accept()
        time.sleep(1)
        # firefox_driver.close()

        logging.info("Retrieve request login session")
        global session_requset
        session_requset.get(config.url_login, auth=HttpNtlmAuth(config.username, config.password))
    except Exception as e:
        logging.exception("Found exception when retrieving login session. {}".format(str(e)))


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
    logging.info("Analyze links in page {}".format(url))
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


def ird_crawl_pages(depth, file_links, pages_to_crawl, page_skip):
    """
    Recursive function of crawl the webpage and its sub pages
    Args:
        depth (int): Maximum depth of the link to jump
        file_links (set str): All the file links found
        pages_to_crawl (set str): Pages to analyze
        page_skip (set str): Pages analyzed or pages which will not be analyzed like file
    Returns:
        set str: file links found
        set str: analyzed pages
        set str: accessed pages
    """

    if depth == 0:
        page_accessed = file_links.union(pages_to_crawl).union(page_skip)
        return file_links, page_skip, page_accessed
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
                            logging.info("{}{} Found file link {}".format(depth_message, page_message, link))
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
        logging.info("[{}] {} new pages found to analyze in next depth level".format(depth, len(new_depth_pages)))

        return ird_crawl_pages(depth - 1, file_links, new_depth_pages, page_skip)


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
    2. Create web driver and get login session
    3. Execute crawling process
    4. Display results
    """
    try:
        # 1
        log_setup()
        # 2
        create_web_driver()
        get_login_session()

        # 3
        start_time = time.time()
        files_found, pages_analyzed, pages_accessed = ird_crawl_pages(config.depth, set(), [config.url_start_page], set())
        end_time = time.time()

        # 4
        logging.info(">>>> Summary")
        logging.info(">> Depth {}".format(config.depth))
        logging.info(">> Time used (s): {}".format(end_time - start_time))
        logging.info(">> Number of page analyzed: {}".format(len(pages_analyzed)))
        logging.info(">> Number of links tracked: {}".format(len(pages_accessed)))
        logging.info(">> Number of file links found: {}".format(len(files_found)))
        logging.info(".>> List of files:\n    {}".format("\n    ".join(files_found)))

    except Exception as e:
        logging.exception(str(e))

    global firefox_driver
    if firefox_driver:
        logging.info("Closing firefox driver")
        firefox_driver.close()

    logging.info("Program End")

if __name__ == "__main__":
    main()