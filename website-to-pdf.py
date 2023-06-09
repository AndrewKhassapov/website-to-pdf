import pdfkit
import time
import requests
import os
from bs4 import BeautifulSoup

path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
pdfkit_options = {"orientation": "Landscape", "zoom": 1}
print(pdfkit_options)

urls_to_parse = []


# Web crawler to get all linked urls from a website.
# Converts relative paths to absolute paths.
# @param homepage_url: The url of the website to crawl. eg. https://www.example.com
# @return list of urls
# TODO: Add recursion to get all urls from a website.
# @refer https://stackoverflow.com/questions/59347372/how-extract-all-urls-in-a-website-using-beautifulsoup
def get_url_list_from_site(homepage_url):
    reqs = requests.get(homepage_url)
    soup = BeautifulSoup(reqs.text, "html.parser")

    urls = []
    for link in soup.find_all("a"):
        link_href = link.get("href")
        if (not link_href.startswith("http://")) and (
            not link_href.startswith("https://")
        ):
            if homepage_url.endswith("/"):
                link_href = homepage_url + link_href
            else:
                link_href = homepage_url + "/" + link_href
        urls.append(link_href)
    return urls


# Get URLs from newline- or comma- separated file.
# @return list of urls
def get_url_list_from_file(filename="input/urls.txt"):
    urls = []

    with open(filename, "r", encoding="UTF-8") as file:
        while line := file.readline():
            line = line.strip()
            values = line.split(",")
            for value in values:
                value = value.replace('"', "").replace("'", "").strip()
                if value != "":
                    if value.startswith("http://") or value.startswith("https://"):
                        urls.append(value)
                    else:
                        urls.append("https://" + value)  # Make valid URL

    return urls


# Creates new file with URL list
def set_url_list_to_file(urls, filename="input/urls_from_site.txt"):
    with open(filename, "w", encoding="UTF-8") as file:
        for url in urls:
            file.write("%s\n" % url)
    print("Succesfully created URL list {}".format(filename))


# Renames URL to a Windows and Unix compatible filename.
def rename_url_to_pdf(url):
    return url.replace("https://", "").replace("/", "-") + ".pdf"


# Returns file path with directory
# If the directory does not exist, creates it.
def move_to_directory(file, path="output/"):
    path_exists = os.path.exists(path)
    if not path_exists:
        os.makedirs(path)
        print("Directory {} does not exist. Creating directory.".format(path))
    return path + file


def delay(seconds=1):
    print("Sleeping for {} seconds".format(seconds))
    time.sleep(seconds)


# Returns true if pdfkit detects a valid network connection.
def get_network_connection():
    try:
        pdfkit.from_url(
            "http://google.com",
            move_to_directory("_test-passed-with-google-com.pdf", "network-check/"),
            configuration=config,
            options=pdfkit_options,
        )
    except Exception as e:
        print("Unable to connect due to {}".format(e))
        return False
    return True


def main():
    STOP_AFTER_FAILS = 10000  # Stop parsing after sequential fails.

    print("=== Parsing websites to pdf. ===\n")

    # urls_to_parse = get_url_list_from_site("https://howmuch.water.vic.gov.au/")
    urls_to_parse = get_url_list_from_file()
    print(urls_to_parse)
    set_url_list_to_file(urls_to_parse)

    # Test network connection
    if not get_network_connection():
        print("No network connection for pdfkit. Exiting.")
        return

    # Iteration working with delay.
    fails = 0
    passes = 0

    for link in urls_to_parse:
        try:
            pdfkit.from_url(
                link,
                move_to_directory(rename_url_to_pdf(link)),
                configuration=config,
                options=pdfkit_options,
            )
            passes += 1
            print("Succesfully parsed {}".format(link))
        except Exception as e:
            fails += 1
            print("Failed to parse {0} due to {1}".format(link, e))
        delay(0.7)
        if fails >= STOP_AFTER_FAILS:
            print(
                "Failed to parse {} links in a row. End parsing.".format(
                    STOP_AFTER_FAILS
                )
            )
            break

    print("\n=== Website to pdf parsing complete. ===")
    print(
        "\nWith {2} sites scanned. {0} converted. {1} failed.".format(
            passes, fails, len(urls_to_parse)
        )
    )


if __name__ == "__main__":
    main()
