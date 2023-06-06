# Website to PDF

A web crawler that prints a website to .pdf format

### Requirements:

:heavy_check_mark: :snake: python 3.x

:heavy_check_mark: [wkHTMLtoPDF](https://wkhtmltopdf.org/) installed on system

:heavy_check_mark: :snake: [pdfkit](https://pypi.org/project/pdfkit/) pypi library. pdfkit is a python wrapper for wkHTMLtoPDF.

:heavy_check_mark: :snake: [BeautifulSoup 4](https://pypi.org/project/beautifulsoup4/) pypi library


### How to use:

:arrow_forward: Set list `urls_to_parse` with all URLs to save to .pdf format.
```python
urls_to_parse = ["<URL_1>", "<URL_2>", ..., "<URL_N>"] # Where URL_n is your desired URL.
```

:arrow_forward: Run *website-to-pdf.py*

:arrow_forward: All URLs will be saved as .pdf to the same directory as *website-to-pdf.py*
