import argparse
from selenium import webdriver
import sys

""" config """
driver = None
phantomjs_exe_path = r"C:\phantomjs-2.1.1-windows\bin\phantomjs.exe"
google_search_url = r"https://www.google.com.hk/search?q={}"
num_print_results = 3
""" end config """


def get_info_from_google(keyword):
    # driver = webdriver.Chrome()
    driver = webdriver.PhantomJS(executable_path=phantomjs_exe_path)
    driver.set_window_size(1024, 768)  # optional
    driver.get(google_search_url.format(keyword))
    driver.save_screenshot('screen.png')  # save a screenshot to disk

    titles = driver.find_elements_by_xpath(".//div/h3/a")
    text_links = driver.find_elements_by_xpath(".//div/div/cite")
    summaries = driver.find_elements_by_xpath(".//div/span[contains(@class, 'st')]")

    # print("Counts titles: {},   text_links: {}   , summaries: {}".format(len(titles), len(text_links), len(summaries)))

    for i in range(num_print_results):
        print("#{}".format(i + 1))
        print("Title: {}".format(titles[i].text))
        print("Url: {}".format(text_links[i].text))
        print("Summary: {}".format(summaries[i].text))
        print("======")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", help="Search keywords with quotes")
    args = parser.parse_args()
    get_info_from_google(args.keyword)