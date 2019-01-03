# axe-output-parser

## Requirements
* Python 3.6+
* npm 6.5.0+

## Install Dependencies
* `python -m venv venv`
* `pip install -r requirements.txt`
* `npm install`

## Run application
Ensure you're utilizing the virtual environment
* `source ./venv/bin/activate`

To fetch axe output and run a summary against an sitemap.xml
* `python axe-parser.py -u http://localhost:4503/content/site/en.sitemap.xml -f localhost-site-sitemap.json`

To run a summary against an existing output
* `python axe-parser.py -f localhost-site-sitemap.json`

To fetch axe output and run a summary against a single page
* `python axe-parser.py -u http://localhost:4503/content/site/en/search-results.html -f localhost-site-search-results.json`

To see page details for a specific violation
* `python axe-parser.py -f localhost-site-sitemap.json -v duplicate-id`

To see summary for a specific violation
* `python axe-parser.py -f localhost-site-sitemap.json -v duplicate-id -s`
