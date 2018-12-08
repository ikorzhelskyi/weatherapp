#!/usr/bin/env python

"""Script for scraping data from weather sites.
"""

import sys
import html
import re
import argparse
import configparser
from pathlib import Path
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup

ACCU_URL = ("https://www.accuweather.com/"
            "uk/ua/lviv/324561/weather-forecast/324561")
ACCU_TAGS = ('<span class="large-temp">', '<span class="cond">')
ACCU_BROWSE_LOCATIONS = 'https://www.accuweather.com/uk/browse-locations'

DEFAULT_NAME = 'Lviv'
DEFAULT_URL = ('https://www.accuweather.com/uk/ua/'
               'lviv/324561/weather-forecast/324561')

CONFIG_LOCATION = 'Location'
CONFIG_FILE = 'weatherapp.ini'

RP5_URL = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D1%83_'
            '%D0%9B%D1%8C%D0%B2%D0%BE%D0%B2%D1%96,_%D0%9B%D1%8C%D0%B2%D1'
            '%96%D0%B2%D1%81%D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1'
            '%81%D1%82%D1%8C')

RP5_TAGS = ('<span class="t_0" style="display: block;">',
            '<div class="cn5" onmouseover="tooltip(this, \'<b>')

SIN_URL = ('https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE'
            '%D0%B4%D0%B0-%D0%BB%D1%8C%D0%B2%D1%96%D0%B2')

SIN_TAGS = ('<p class="today-temp">'
            '<div class="description"> <!--noindex-->')

def get_request_headers():
    """Returns custom headers for url request.
    """
    
    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}

def get_page_source(url):
    """Gets page source by given url address.
    """

    request = Request(url, headers=get_request_headers())
    page_source = urlopen(request).read()
    return page_source.decode('utf-8')

def get_locations(locations_url):
    locations_page = get_page_source(locations_url)
    soup = BeautifulSoup(locations_page, 'html.parser')

    locations = []
    for location in soup.find_all('li', class_='drilldown cl'):
        url = location.find('a').attrs['href']
        location = location.find('em').text
        locations.append((location, url))
    return locations

def get_configuration_file():
    """Returns path to configuration file in home directory.
    """

    return Path.home() / CONFIG_FILE

def save_configuration(name, url):
    """Save selected location to configuration file.
    """

    parser = configparser.ConfigParser()
    parser[CONFIG_LOCATION] = {'name': name, 'url': url}
    with open(get_configuration_file(), 'w') as configfile:
       parser.write(configfile)

def get_configuration():
    """Returns configured location name and url.
    """
    name = DEFAULT_NAME
    url = DEFAULT_URL

    parser = configparser.ConfigParser()
    parser.read(get_configuration_file())

    if CONFIG_LOCATION in parser.sections():
        config = parser[CONFIG_LOCATION]
        name, url = config['name'], config['url']
    
    return name, url

def configurate():
    locations = get_locations(ACCU_BROWSE_LOCATIONS)
    while locations:
        for index, location in enumerate(locations):
            print(f'{index + 1}. {location[0]}')
        selected_index = int(input('Please select location: '))
        location = locations[selected_index - 1]
        locations = get_locations(location[1])

    save_configuration(*location)

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

def get_weather_info(page_content):
    """Gets data from the site using the BeautifulSoup library
    """

    city_page = BeautifulSoup(page_content, 'html.parser')
    current_day_section = city_page.find(
        'li', class_=re.compile('(day|night) current first cl'))

    weather_info = {}
    if current_day_section:
        current_day_url = current_day_section.find('a').attrs['href']
        if current_day_url:
            current_day_page = get_page_source(current_day_url)
            if current_day_page:
                current_day = \
                    BeautifulSoup(current_day_page, 'html.parser')
                weather_details = \
                    current_day.find('div', attrs={'id': 'detail-now'})
                condition = weather_details.find('span', class_='cond')
                if condition:
                    weather_info['cond'] = condition.text
                temp = weather_details.find('span', class_='large-temp')
                if temp:
                    weather_info['temp'] = temp.text
                feal_temp = weather_details.find('span', class_='small-temp')
                if feal_temp:
                    weather_info['feal-temp'] = feal_temp.text

                wind_info = weather_details.find_all('li', class_='wind')
                if wind_info:
                    weather_info['wind'] = \
                        ' '.join(map(lambda t: t.text.strip(),wind_info))

    return weather_info

def produce_output(city_name, info):
    """Formats and displays the found data.
    """
    print('AccuWeather: \n')
    print(f'{city_name}')
    print('_'*20)
    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')

def get_accu_weather_info():
    city_name, city_url = get_configuration()
    content = get_page_source(city_url)
    produce_output(city_name, get_weather_info(content))

def main(argv):
    """Main entry point.
    """

    KNOWN_COMMANDS = {'accu': get_accu_weather_info,
                      'config': configurate}

    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs=1)
    params = parser.parse_args(argv)

    if params.command:
        command = params.command[0]
        if command in KNOWN_COMMANDS:
            KNOWN_COMMANDS[command]()
        else:
            print("Unknown command provided!")
            sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])