import argparse
import json
import requests
import xml.etree.ElementTree as ET

from subprocess import call


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', help='Configure output filename', type=str)
parser.add_argument('-s', '--summary', action='store_true', help='Output Summary')
parser.add_argument('-u', '--url', help='Provide the url of an html page, or a sitemap.xml', type=str)
parser.add_argument('-v', '--violation', help='Violation id details', type=str)
args = parser.parse_args()

violations = {}
details = {}


def fetch(url, filename):
    if url.lower().endswith('sitemap.xml'):
        sitemap_request = requests.get(url)
        sitemap_xml_root = ET.fromstring(sitemap_request.text)
        urls = set()
        for sitemap_xml_child in sitemap_xml_root:
            urls.add(sitemap_xml_child.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text)
    else:
        urls = { url }

    command = './node_modules/axe-cli/axe-cli --no-reporter -s '+ filename + ' --tags wcag2a,section508 ' + ' '.join(urls)
    call(command.split())


def parse_file(filename):
    with open(filename) as json_file:
        json_payload = json.load(json_file)
        for object in json_payload:
            url = object['url']

            for violation in object['violations']:

                key = violation['id']

                details[key] = {
                    'description': violation['description'],
                    'help': violation['help'],
                    'tags': ', '.join(violation['tags']),
                    'url': violation['helpUrl']
                }

                if key not in violations:
                    violations[key] = []

                for node in violation['nodes']:
                    violations[key].append({
                        'url': url,
                        'html': node['html']
                    })


def print_violation_summary(violation):
    print(violation + ': ' + str(len(violations[violation])))
    print('\tdesc:\t\t' + details[violation]['description'])
    print('\thelp:\t\t' + details[violation]['help'])
    print('\ttags:\t\t' + details[violation]['tags'])
    print('\turl:\t\t' + details[violation]['url'])
    print('\thtml:\t\t' + violations[violation][0]['html'])
    print()


filename = args.filename or 'axe-cli.json'

if args.url:
    fetch(args.url, filename)

parse_file(filename)

if not args.violation:
    for key in sorted(violations):
        print_violation_summary(key)

else:
    if args.summary:
        print_violation_summary(args.violation)
    else:
        for violation in violations[args.violation]:
            print(violation['url'])
            print('\t' + violation['html'])
            print()
