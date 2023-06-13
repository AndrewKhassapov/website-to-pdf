# Website to PDF

A web crawler that prints a website to .pdf format

## Requirements:

:heavy_check_mark: :snake: [python 3.x](https://www.python.org/downloads/) environment

:heavy_check_mark: :file_folder: [wkHTMLtoPDF](https://wkhtmltopdf.org/) installed on system

:heavy_check_mark: :snake: [pdfkit](https://pypi.org/project/pdfkit/) pypi library. pdfkit is a python wrapper for wkHTMLtoPDF.

:heavy_check_mark: :snake: [BeautifulSoup 4](https://pypi.org/project/beautifulsoup4/) pypi library
</br></br>

## How to use:

:arrow_forward: Set list `urls_to_parse` with all URLs to save to .pdf format.
```python
urls_to_parse = ["<URL_1>", "<URL_2>", ..., "<URL_N>"] # Where URL_n is your desired URL.
```
The list can be collected by either:

:a: :arrow_right: Using return from `get_url_list_from_site( <MY SITE eg. http://example.com> )`

or

:b: :arrow_right: Using return from `get_url_list_from_file( <MY FILE | DEFAULT = input/urls.txt> )` 

:arrow_forward: Run *website-to-pdf.py*

:arrow_forward: All URLs will be saved as .pdf to the `output/` directory from source *website-to-pdf.py*
</br></br>

## License:

MIT license compliant. Software provided as is. All content is free to use and modify.

![andrewkhassapov github](https://github.com/AndrewKhassapov/website-to-pdf/assets/53222142/903caf24-211d-41e8-b526-3b474198f9fe)[^1]
[^1]: GitHub shields provided by [Shields.io](https://shields.io/)
