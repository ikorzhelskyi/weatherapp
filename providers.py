"""Weather providers.
"""

import time
import hashlib
import re
import configparser
from pathlib import Path
import urllib
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

import config


class AccuWeatherProvider:

    """Weather provider for AccuWeather site.
    """

    def __init__(self):
        self.name = config.ACCU_PROVIDER_NAME

        location, url = self.get_configuration()
        self.location = location
        self.url = url

    def get_configuration_file(self):
        """Returns path to configuration file in home directory.
        """

        return Path.home() / config.CONFIG_FILE

    def get_configuration(self):
        """Returns configured location name and url.

        :return: city name and url
        :rtype: tuple
        """

        name = config.DEFAULT_LOCATION_NAME
        url = config.ACCU_DEFAULT_LOCATION_URL
        configuration = configparser.ConfigParser()
        configuration.read(self.get_configuration_file())
        if config.CONFIG_LOCATION in configuration.sections():
            location_config = configuration[config.CONFIG_LOCATION]
            name, url = location_config['name'], location_config['url']
        return name, url

    def save_configuration(self, name, url):
        """Save selected location to configuration file.
        
        :param name: city name
        :param type: str

        :param url: preferred location URL
        :param type: str
        """

        parser = configparser.ConfigParser()
        parser[config.CONFIG_LOCATION] = {'name': name, 'url': url}
        with open(self.get_configuration_file(), 'w') as configfile:
            parser.write(configfile)

    def get_request_headers(self):
        """Returns custom headers for url request.
        """

        return {'User-Agent': config.FAKE_MOZILLA_AGENT}

    def get_url_hash(self, url):
        """Generates url hash.
        """

        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def get_cache_directory(self):
        """Path to cache directory.
        """

        return Path.home() / config.CACHE_DIR

    def is_valid(self, path):
        """Checks if current cache is valid.
        """

        return (time.time() - path.stat().st_mtime) < config.CACHE_TIME

    def get_cache(self, url):
        """Returns cache by given url address if any.
        """

        cache = b''
        cache_dir = self.get_cache_directory()
        if cache_dir.exists():
            cache_path = cache_dir / self.get_url_hash(url)
            if cache_path.exists() and self.is_valid(cache_path):
                with cache_path.open('rb') as cache_file:
                    cache = cache_file.read()
        return cache

    def save_cache(self, url, page_source):
        """Save page source data to file.
        """

        cache_dir = self.get_cache_directory()
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)

        with  (cache_dir / self.get_url_hash(url)).open('wb') as cache_file:
            cache_file.write(page_source)

    def get_page_source(self, url, refresh=False):
        """Gets page source by given url address.
        """

        cache = self.get_cache(url)
        if cache and not refresh:
            page_source = cache
        else:
            request = Request(url, headers=self.get_request_headers())
            page_source = urlopen(request).read()
            self.save_cache(url, page_source)
        return page_source.decode('utf-8')

    def get_locations(self, locations_url, refresh=False):
        locations_page = self.get_page_source(locations_url, refresh=refresh)
        soup = BeautifulSoup(locations_page, 'html.parser')
        locations = []
        for location in soup.find_all('li', class_='drilldown cl'):
            url = location.find('a').attrs['href']
            location = location.find('em').text
            locations.append((location, url))
        return locations

    def configurate(self, refresh=False):
        """Configure provider.
        """
        locations = self.get_locations(config.ACCU_BROWSE_LOCATIONS)
        while locations:
            for index, location in enumerate(locations):
                print(f'{index + 1}. {location[0]}')
            selected_index = int(input('Please select location: '))
            location = locations[selected_index - 1]
            locations = self.get_locations(location[1], refresh=refresh)
        self.save_configuration(*location)

    def get_weather_info(self, page_source, refresh=False):
        """Gets data from the site using the BeautifulSoup library
        """

        city_page = BeautifulSoup(page_source, 'html.parser')
        current_day_section = city_page.find(
            'li', class_=re.compile('(day|night) current first cl'))

        weather_info = {}
        if current_day_section:
            current_day_url = current_day_section.find('a').attrs['href']
            if current_day_url:
                current_day_page = self.get_page_source(current_day_url, 
                                                        refresh=refresh)
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
                    feal_temp = weather_details.find(
                        'span', class_='small-temp')
                    if feal_temp:
                        weather_info['feal-temp'] = feal_temp.text

                    wind_info = weather_details.find_all('li', class_='wind')
                    if wind_info:
                        weather_info['wind'] = \
                            ' '.join(map(lambda t: t.text.strip(),wind_info))
        return weather_info

    def run(self, refresh=False):
        content = self.get_page_source(self.url, refresh=refresh)
        return self.get_weather_info(content,refresh=refresh)


class Rp5WeatherProvider:

    """Weather provider for rp5.ua site.
    """

    def __init__(self):
        self.name = config.RP5_PROVIDER_NAME

        location, url = self.get_configuration()
        self.location = location
        self.url = url

    def get_configuration_file(self):
        """Returns path to configuration file in home directory.
        """

        return Path.home() / config.CONFIG_FILE

    def get_configuration(self):
        """Returns configured location name and url.

        :return: city name and url
        :rtype: tuple
        """

        name = config.DEFAULT_LOCATION_NAME
        url = config.RP5_DEFAULT_LOCATION_URL
        configuration = configparser.ConfigParser()
        configuration.read(self.get_configuration_file())
        if config.CONFIG_LOCATION in configuration.sections():
            location_config = configuration[config.CONFIG_LOCATION]
            name, url = location_config['name'], location_config['url']
        return name, url

    def save_configuration(self, name, url):
        """Save selected location to configuration file.

        :param name: city name
        :param type: str

        :param url: preferred location URL
        :param type: str
        """

        parser = configparser.ConfigParser()
        parser[config.CONFIG_LOCATION] = {'name': name, 'url': url}
        with open(self.get_configuration_file(), 'w') as configfile:
            parser.write(configfile)

    def get_request_headers(self):
        """Returns custom headers for url request.
        """

        return {'User-Agent': config.FAKE_MOZILLA_AGENT}

    def get_url_hash(self, url):
        """Generates url hash.
        """

        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def get_cache_directory(self):
        """Path to cache directory.
        """

        return Path.home() / config.CACHE_DIR

    def is_valid(self, path):
        """Checks if current cache is valid.
        """

        return (time.time() - path.stat().st_mtime) < config.CACHE_TIME

    def get_cache(self, url):
        """Returns cache by given url address if any.
        """

        cache = b''
        cache_dir = self.get_cache_directory()
        if cache_dir.exists():
            cache_path = cache_dir / self.get_url_hash(url)
            if cache_path.exists() and self.is_valid(cache_path):
                with cache_path.open('rb') as cache_file:
                    cache = cache_file.read()
        return cache

    def save_cache(self, url, page_source):
        """Save page source data to file.
        """

        cache_dir = self.get_cache_directory()
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)
        with  (cache_dir / self.get_url_hash(url)).open('wb') as cache_file:
            cache_file.write(page_source)

    def get_request_headers(self):
        """Returns custom headers for url request.
        """

        return {'User-Agent': config.FAKE_MOZILLA_AGENT}

    def get_page_source(self, url, refresh=False):
        """Gets page source by given url address.
        """

        cache = self.get_cache(url)
        if cache and not refresh:
            page_source = cache
        else:
            request = Request(url, headers=self.get_request_headers())
            page_source = urlopen(request).read()
            self.save_cache(url, page_source)
        return page_source.decode('utf-8')

    def get_locations_rp5(self, locations_url, refresh=False):
        """Return a list of locations and related urls"""

        locations_page = self.get_page_source(locations_url, refresh=refresh)
        soup = BeautifulSoup(locations_page, 'html.parser')
        locations = []
        places = soup.find_all('div', class_='country_map_links')
        if not places:
            places = soup.find_all('a', class_='href20')
            if not places:
                places = soup.find_all('div', class_='city_link')
                for place in places:
                    url = place.find('a').attrs['href']
                    url = f'http://rp5.ua/{url}'
                    location = place.text
                    locations.append((location, url))
                    return locations
            for place in places:
                url = place.attrs['href']
                url = f'http://rp5.ua/{url}'
                location = place.text
                locations.append((location, url))
        else:
            for location in places:
                url = location.find('b')
                url = url.find('a').attrs['href']
                url = f'http://rp5.ua{url}'
                location = location.find('b').text[:-1]
                locations.append((location, url))
        return locations

    def configurate(self):
        """Configure provider.
        """
        countries = self.get_countries(config.RP5_BROWSE_LOCATIONS)
        for index, country in enumerate(countries):
            self.stdout.write(f'{index + 1}, {country[0]}\n')
        selected_index = int(input('Please select city: '))
        city = cities[selected_index - 1]
        self.save_configuration(*city)

    def get_countries(self, countries_url):
        countries_page = self.get_page_source(countries_url)
        soup = BeautifulSoup(countries_page, countries_url)
        base = urllib.parse.urlunsplit(
            urllib.parse.urlparse(countries_url)[:2] + ('/', '', ''))
        countries = []
        for country in soup.find_all('div', class_='country_map_links'):
            url = urllib.parse.urljoin(base, country.find('a').attrs['href'])
            country = country.find('a').text
            countries.append((country, url))
        return countries

    def get_cities(self, country_url):
        cities = []
        cities_page = self. get_page_source(country_url)
        soup = BeautifulSoup(cities_page, 'html.parser')
        base = urllib.parse.urlunsplit(
            urllib.parse.urlparse(country_url)[:2] + ('/', '', ''))
        country_map = soup.find('div', class_='countryMap')
        if country_map:
            cities_list = country_map.find_all('h3')
            for city in cities_list:
                url = urllib.parse.urljoin(base,city.find('f').attrs['href'])
                city = city.find('a').text
                cities.append((city, url))
        return cities

    def get_weather_info(self, page_source, refresh=False):
        """Gets data from the site using the BeautifulSoup library
        """

        city_page = BeautifulSoup(page_source, 'html.parser')
        current_day = city_page.find('div', id='archiveString')

        weather_info = {'cond': '', 'temp': '', 'feal_temp': '', 'wind': ''}
        if current_day:
            archive_info = current_day.find('div', class_='ArchiveInfo')
            if archive_info:
                archive_text = archive_info.text
                info_list = archive_text.split(',')
                weather_info['cond'] = info_list[1].strip()
                temp = archive_info.find('span', class_='t_0')
                if temp:
                    weather_info['temp'] = temp.text
                wind = info_list[3].strip()[:info_list[3].find(')') + 1]
                wind += info_list[4]
                if wind:
                    weather_info['wind'] = wind
        return weather_info

    def run(self, refresh=False):
        content = self.get_page_source(self.url, refresh=refresh)
        return self.get_weather_info(content,refresh=refresh)