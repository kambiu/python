import requests
import csv
from lxml import html


travel_sites = [
    "https://www.consumeraffairs.com/travel/airbnb.html",
    "https://www.consumeraffairs.com/travel/trivago.html",
    "https://www.consumeraffairs.com/travel/tripadvisor.html",
    "https://www.consumeraffairs.com/travel/expedia_air_reservations.html",
    "https://www.consumeraffairs.com/travel/booking_com.html",
    "https://www.consumeraffairs.com/travel/hotelsdotcom.html",
]

page_option = "?page={}"
xpath_next_page = "//a[contains(@rel, 'next')]"
xpath_review = "//div[contains(@itemprop, 'reviews')]"
xpath_comment = "div/div/p"
xpath_rating = "div/div/div/meta[contains(@itemprop, 'ratingValue')]"

list_all = []
err_count = 0
for site in travel_sites:
    site_name = site[site.rfind("/") + 1:site.rfind(".")]
    print("Start processing site {}".format(site))
    page = 1
    while True:
        print("Page: {}".format(page))
        url_page = site + page_option.format(page)
        print("Check site {}".format(url_page))
        r = requests.get(url_page, allow_redirects=False)
        if r.status_code > 300:
            print("Page not valid {}".format(url_page))
            break
        else:
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
                            comment += " " + comment_paragraph.text
                    print("Comment: {}".format(comment))

                    rating = None
                    for elm_rating in elm_review.xpath(xpath_rating):
                        rating = elm_rating.attrib["content"]
                        print("Rating: {}".format(elm_rating.attrib["content"]))

                    if site_name and comment and rating:
                        list_row.append(site_name)
                        list_row.append(comment)
                        list_row.append(rating)
                        list_all.append(list_row)

                except Exception as e:
                    print("Error found in pasre html")
                    err_count += 1
            page += 1


with open("out2.csv", "w", encoding="utf-8", newline="") as stream:
    writer = csv.writer(stream, quoting=csv.QUOTE_ALL)
    for row in list_all:
        writer.writerow(row)

print("Error count: {}".format(err_count))
print("Program end")