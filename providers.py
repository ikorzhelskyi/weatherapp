import time
import hashlib
import configparser
from pathlib import Path

from bs4 import BeautifulSoup

import config


class AccuWeatherProvider:

    """Weather provider for AccuWeather site.
    """

    def __init__(self):
        self.name = config.ACCU_PROVIDER_NAME

        url, location = self.get_configuration()
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
        url = config.DEFAULT_LOCATION_URL
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

        return Path.home() / CACHE_DIR


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
            cache_path = cache_dir / self.get_url_hash()
            if cache_path.exists() and self.is_valid(cache_path):
                with cache_path.open('rb') as cache_file:
                    cache = cache_file.read()

        return cache


    def save_cache(self, url, page_source):
        """Save page source data to file.
        """

        cache_dir = get_cache_directory()
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)

        with  (cache_dir / self.get_url_hash()).open('wb') as cache_file:
            cache_file.write(page_source)