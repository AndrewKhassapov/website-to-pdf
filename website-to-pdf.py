import pdfkit
import time
import requests
from bs4 import BeautifulSoup

urls_to_parse = [
    "https://howmuch.water.vic.gov.au/",
    "https://howmuch.water.vic.gov.au/how-much-water-was-available.php",
]


# Web crawler to get all linked urls from a website.
# @return list of urls
# TODO: Add recursion to get all urls from a website.
# TODO: Convert relative links to absolute links.
# @refer https://stackoverflow.com/questions/59347372/how-extract-all-urls-in-a-website-using-beautifulsoup
def get_url_list_from_site(homepage_url):
    url = homepage_url
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, "html.parser")

    # urls = []
    for link in soup.find_all("a"):
        print(link.get("href"))


def get_url_list_from_file(filename = "input/urls.txt"):
    with open(filename, 'r', encoding='UTF-8') as file:
    while line := file.readline():
        print(line.rstrip())


# Renames URL to a compatible filename.
def rename_url_to_pdf(url):
    return url.replace("https://", "").replace("/", "-") + ".pdf"


# Returns file path with directory
# NOTE: Subdirectories not working with current version of pdfkit.
def move_to_directory(file):
    return file


def delay(seconds):
    print("Sleeping for {} seconds".format(seconds))
    time.sleep(seconds)


def main():
    print("Parsing websites to pdf.")
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    # options_wkhtmltopdf = {"enable-local-file-access": None}

    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    get_url_list("https://howmuch.water.vic.gov.au/")

    # Working:
    pdfkit.from_url(
        "http://google.com", "test-passed-google-com.pdf", configuration=config
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
        delay(1)


if __name__ == "__main__":
    main()
