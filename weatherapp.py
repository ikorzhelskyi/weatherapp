#!/usr/bin/env python

"""Script for scraping data from weather sites.
"""

import sys
import html
import time
import hashlib
import re
import argparse
import configparser
from pathlib import Path
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup


def get_request_headers():
    """Returns custom headers for url request.
    """

    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}


def get_cache_directory():
    """Path to cache directory.
    """

    return Path.home() / CACHE_DIR


def get_url_hash(url):
    """Generates hash for given url.
    """

    return hashlib.md5(url.encode('utf-8')).hexdigest()


def save_cache(url, page_source):
    """Save page source data to file.
    """

    url_hash = get_url_hash(url)
    cache_dir = get_cache_directory()
    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)

    with  (cache_dir / url_hash).open('wb') as cache_file:
        cache_file.write(page_source)


def is_valid(path):
    """Check if current cache is valid.
    """

    return (time.time() - path.stat().st_mtime) < CACHE_TIME


def get_cache(url):
    """Return cache data if any.
    """

    cache = b''
    url_hash = get_url_hash(url)
    cache_dir = get_cache_directory()
    if cache_dir.exists():
        cache_path = cache_dir / url_hash
        if cache_path.exists() and is_valid(cache_path):    
            with cache_path.open('rb') as cache_file:   
                cache = cache_file.read()

    return cache


def get_page_source(url, refresh=False):
    """Gets page source by given url address.
    """

    cache = get_cache(url)
    if cache and not refresh:
        page_source = cache
    else:
        request = Request(url, headers=get_request_headers())
        page_source = urlopen(request).read()
        save_cache(url, page_source)

    return page_source.decode('utf-8')


def get_locations(locations_url, refresh=False):
    locations_page = get_page_source(locations_url, refresh=refresh)
    soup = BeautifulSoup(locations_page, 'html.parser')

    locations = []
    for location in soup.find_all('li', class_='drilldown cl'):
        url = location.find('a').attrs['href']
        location = location.find('em').text
        locations.append((location, url))

    return locations


def configurate(refresh=False):
    locations = get_locations(ACCU_BROWSE_LOCATIONS, refresh=refresh)
    while locations:
        for index, location in enumerate(locations):
            print(f'{index + 1}. {location[0]}')
        selected_index = int(input('Please select location: '))
        location = locations[selected_index - 1]
        locations = get_locations(location[1], refresh=refresh)

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


def get_weather_info(page_content, refresh=False):
    """Gets data from the site using the BeautifulSoup library
    """

    city_page = BeautifulSoup(page_content, 'html.parser')
    current_day_section = city_page.find(
        'li', class_=re.compile('(day|night) current first cl'))

    weather_info = {}
    if current_day_section:
        current_day_url = current_day_section.find('a').attrs['href']
        if current_day_url:
            current_day_page = get_page_source(current_day_url, refresh=refresh)
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


def get_accu_weather_info(refresh=False):
    city_name, city_url = get_configuration()
    content = get_page_source(city_url, refresh=refresh)
    produce_output(city_name, get_weather_info(content, refresh=refresh))


def main(argv):
    """Main entry point.
    """

    KNOWN_COMMANDS = {'accu': get_accu_weather_info,
                      'config': configurate}

    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs=1)
    parser.add_argument('--refresh', help='Update caches', action='store_true')
    params = parser.parse_args(argv)

    if params.command:
        command = params.command[0]
        if command in KNOWN_COMMANDS:
            KNOWN_COMMANDS[command](refresh=params.refresh)
        else:
            print("Unknown command provided!")
            sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])