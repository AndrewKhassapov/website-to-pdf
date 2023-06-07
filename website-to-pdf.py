import pdfkit
import time
import requests
import os
from bs4 import BeautifulSoup

urls_to_parse = []


# Web crawler to get all linked urls from a website.
# @return list of urls
# TODO: Add recursion to get all urls from a website.
# TODO: Convert relative links to absolute links.
# @refer https://stackoverflow.com/questions/59347372/how-extract-all-urls-in-a-website-using-beautifulsoup
def get_url_list_from_site(homepage_url):
    reqs = requests.get(homepage_url)
    soup = BeautifulSoup(reqs.text, "html.parser")

    urls = []
    for link in soup.find_all("a"):
        urls.append(link.get("href"))
    return urls


"""
 def get_url_list_from_file(filename = "input/urls.txt"):
    with open(filename, 'r', encoding='UTF-8') as file:
    while line := file.readline():
        print(line.rstrip())
"""


# Renames URL to a Windows and Unix compatible filename.
def rename_url_to_pdf(url):
    return url.replace("https://", "").replace("/", "-") + ".pdf"


# Returns file path with directory
# If the directory does not exist, creates it.
def move_to_directory(file):
    path = "output/"
    path_exists = os.path.exists(path)
    if not path_exists:
        os.makedirs(path)
        print("Directory {} does not exist. Creating directory.".format(path))
    return path + file


def delay(seconds=1):
    print("Sleeping for {} seconds".format(seconds))
    time.sleep(seconds)


def main():
    print("Parsing websites to pdf.")
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    # options_wkhtmltopdf = {"enable-local-file-access": None}

    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    urls_to_parse = get_url_list_from_site("https://howmuch.water.vic.gov.au/")
    print(urls_to_parse)

    # Working:
    pdfkit.from_url(
        "http://google.com",
        move_to_directory("_test-passed-with-google-com.pdf"),
        configuration=config,
    )

    # Iteration working with delay.
    for link in urls_to_parse:
        try:
            pdfkit.from_url(
                link, move_to_directory(rename_url_to_pdf(link)), configuration=config
            )
            print("Succesfully parsed {}".format(link))
        except:
            print("Failed to parse {}".format(link))
        delay(0.7)

    print("Website to pdf parsing complete.")


if __name__ == "__main__":
    main()
