import requests
import csv
from lxml import html


sites = [
    "https://en.tripadvisor.com.hk/Hotel_Review-g294217-d304490-Reviews-or{}-The_Langham_Hong_Kong-Hong_Kong.html",
]

xpath_review = "//div[contains(@class, 'review-container')]"
xpath_rating = "div/div/div/div/div/div/div/span"
xpath_comment = "div/div/div/div/div/div/div/div/p"


list_all = []
err_count = 0
max_comment = 1400
for site in sites:
    idx_page = 0
    site_name = "Langham"

    while True:
        page_num = idx_page * 5
        if page_num > max_comment:
            break
        url_page = site.format(page_num)
        print("Start processing site {}".format(url_page))
        r = requests.get(url_page)
        # r = requests.get(url_page, allow_redirects=False)

        if r.status_code > 400:
            print("Page not valid {}".format(url_page))
            continue
        else:
            print(r.text)
            root = html.fromstring(r.text)
            list_reviews = list(root.xpath(xpath_review))
            print("Number of reviews: {}".format(len(list_reviews)))
            for elm_review in list_reviews:
                list_row = []

                try:
                    print("Site Name: {}".format(site_name))
                    comment = ""
                    for comment_paragraph in elm_review.xpath(xpath_comment):
                        if comment_paragraph.text:
                            comment += " " + comment_paragraph.text.replace("\n", " ").replace("\r", " ")
                    print("Comment: {}".format(comment))

                    rating = None
                    for elm_rating in elm_review.xpath(xpath_rating):
                        for attrib, value in elm_rating.attrib.items():
                            if attrib == "class" and value.startswith("ui_bubble_rating"):
                                rating = str(value)[-2:-1]
                                print("Rating: {}".format(rating))
                                break

                    if site_name and comment and rating:
                        list_row.append(site_name)
                        list_row.append(comment)
                        list_row.append(rating)
                        list_all.append(list_row)

                except Exception as e:
                    print("Error found in pasre html")
                    err_count += 1
            idx_page += 1


with open("out.csv", "w", encoding="utf-8", newline="") as stream:
    writer = csv.writer(stream, quoting=csv.QUOTE_ALL)
    for row in list_all:
        writer.writerow(row)

print("Error count: {}".format(err_count))
print("Program end")