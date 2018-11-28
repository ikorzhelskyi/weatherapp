#!/usr/bin/python3

"""Weather app project.
"""

import sys
import html
import argparse
from urllib.request import urlopen, Request

ACCU_URL = "https://www.accuweather.com/uk/ua/lviv/324561/weather-forecast/324561"
ACCU_TAGS = ('<span class="large-temp">', '<span class="cond">')

RP5_URL = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D1%83_'
            '%D0%9B%D1%8C%D0%B2%D0%BE%D0%B2%D1%96,_%D0%9B%D1%8C%D0%B2%D1'
            '%96%D0%B2%D1%81%D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1'
            '%81%D1%82%D1%8C')
RP5_TAGS = ('<span class="t_0" style="display: block;">', '<div class="cn5" onmouseover="tooltip(this, \'<b>')

SIN_URL = ('https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE'
            '%D0%B4%D0%B0-%D0%BB%D1%8C%D0%B2%D1%96%D0%B2')
SIN_TAGS = ('<p class="today-temp">', '<div class="description"> <!--noindex-->')

def get_request_headers():
    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}

def get_page_source(url):
    """Returns the content of the page by the given URL address.
    """

    request = Request(url, headers=get_request_headers())
    page_source = urlopen(request).read()
    return page_source.decode('utf-8')

def get_tag_content(page_content, tag):
    """Finds the necessary data in the content of the page.
    """

    tag_index = page_content.find(tag)
    tag_size = len(tag)
    value_start = tag_index + tag_size

    content = ''
    for c in page_content[value_start:]:
        if c != '<':
            content += c
        else:
            break
    return content

def get_weather_info(page_content, tags):
    """Returns information collected from tags.
    """

    return tuple([get_tag_content(page_content, tag) for tag in tags])

def produce_output(provider_name, temp, condition):
    """Formats and displays the found data.
    """
    
    print(f'\n{provider_name}:\n')
    print(f'Temperature: {html.unescape(temp)}\n')
    print(f'Condition: {condition}\n')

def main(argv):
    """Main entry point.
    """
    
    KNOWN_COMMANDS = {'accu': 'AccuWeather'}

    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs=1)
    params = parser.parse_args(argv)
    
    weather_sites = {"AccuWeather": (ACCU_URL, ACCU_TAGS),
                     "RP5": (RP5_URL, RP5_TAGS),
                     "SINOPTIK": (SIN_URL, SIN_TAGS)}

    if params.command:
        command = params.command[0]
        if command in KNOWN_COMMANDS:
            weather_sites = {
                KNOWN_COMMANDS[command]: weather_sites[KNOWN_COMMANDS[command]]
                }
        else:
            print("Unknown command provided!")
            sys.exit(1)

    for name in weather_sites:
        url, tags = weather_sites[name]
        content = get_page_source(url)
        temp, condition = get_weather_info(content, tags)
        produce_output(name, temp, condition)

if __name__ == '__main__':
    main(sys.argv[1:])