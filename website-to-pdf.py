"""
Website to .pdf converter

Description: Converts a list of URLs to .pdf files either from a file or from a website.

Author: Andrew Khassapov
Date created: 5 June 2023
Date updated: 20 June 2023
Version: 1.0.1
"""

import pdfkit
import time
import requests
import os
from bs4 import BeautifulSoup


PATH_WKHTMLTOPDF = (
    r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # Your path to wkhtmltopdf.exe
)
CONFIG = pdfkit.configuration(wkhtmltopdf=PATH_WKHTMLTOPDF)
PDFKIT_OPTIONS = {
    "orientation": "Portrait",
    "zoom": 1,
    "no-stop-slow-scripts": True,
    "disable-external-links": True,
    "disable-internal-links": True,
    "disable-forms": True,
    # "disable-smart-shrinking": True,
    "no-outline": True,
    "print-media-type": True,
}
"""Options for .pdf output\n
See for full property list:
    https://wkhtmltopdf.org/usage/wkhtmltopdf.txt
"""
STOP_AFTER_FAILS = 10000  # Stop parsing after sequential fails.
urls_to_parse = []


def get_url_list_from_site(homepage_url):
    """Web crawler to get all linked urls from a website.
    Converts relative paths to absolute paths.

    Args:
        homepage_url (str): The url of the website to crawl. eg. https://www.example.com

    Returns:
        list: list of urls

    TODO: Add recursion to get all urls from a website.
    Refer: https://stackoverflow.com/questions/59347372/how-extract-all-urls-in-a-website-using-beautifulsoup
    """

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


def get_url_list_from_file(filename="input/urls.txt"):
    """Get URLs from newline- or comma- separated file.

    Args:
        filename (str, optional): File path and name. Defaults to "input/urls.txt".

    Returns:
        list: list of urls
    """
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


def set_url_list_to_file(urls, filename="input/urls_from_site.txt"):
    """Creates new file with URL list

    Args:
        urls (list): list to save as file
        filename (str, optional): Filename and path. Path must exist. Defaults to "input/urls_from_site.txt".
    """
    with open(filename, "w", encoding="UTF-8") as file:
        for url in urls:
            file.write("%s\n" % url)
    print("Succesfully created URL list {}".format(filename))


def rename_url_to_pdf(url):
    """Renames URL to a Windows and Unix compatible filename.

    Args:
        url (str): URL to convert to filename

    Returns:
        str: Filename from URL. Compatible with Windows and Unix/Linux/macOS.
    """
    return url.replace("https://", "").replace("/", "-") + ".pdf"


def move_to_directory(file, path="output/"):
    """Prefixes directory to filename

    Args:
        file (str): Filenae
        path (str, optional): Path. Path will be created if it does not exist. Defaults to "output/".

    Returns:
        str: Path + filename. eg. output/filename.pdf
    """

    path_exists = os.path.exists(path)
    if not path_exists:
        os.makedirs(path)
        print("Directory {} does not exist. Creating directory.".format(path))
    return path + file


def delay(seconds=1):
    print("Sleeping for {} seconds".format(seconds))
    time.sleep(seconds)


def get_network_connection():
    """Returns true if pdfkit detects a valid network connection.

    Returns:
        bool: True if network connection is valid for pdfkit.
    """

    try:
        pdfkit.from_url(
            "http://google.com",
            move_to_directory("_test-passed-with-google-com.pdf", "network-check/"),
            configuration=CONFIG,
            options=PDFKIT_OPTIONS,
        )
    except Exception as e:
        print("Unable to connect due to {}".format(e))
        return False
    return True


def main():
    print("=== Parsing websites to pdf. ===\n")

    urls_to_parse = get_url_list_from_file()
    # urls_to_parse = get_url_list_from_site("https://www.google.com")
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
                configuration=CONFIG,
                options=PDFKIT_OPTIONS,
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
