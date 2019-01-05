""" Abstract classes for project.
"""

import abc
import time
import hashlib
import argparse
import configparser
from pathlib import Path
from urllib.request import Request, urlopen

import config


class Command(abc.ABC):

    """ Base class for commands.

    :param app: Main application instance
    :type app: 'app.App'
    """

    def __init__(self, app):
        self.app = app

    @staticmethod
    def get_parser():
        """ Initialize argument parser for command.
        """
        parser = argparse.ArgumentParser()
        return parser

    @abc.abstractmethod
    def run(self, argv):
        """ Invoked by application when the command is run.

        Should be overriden in subclass.
        """


class WeatherProvider(Command):

    """ Weather provider abstract class.

    Defines behavior for all weather providers.
    """

    def __init__(self, app):
        super().__init__(app)

        location, url = self._get_configuration()
        self.location = location
        self.url = url

    @abc.abstractmethod
    def configurate(self):
        """ Performs provider cnfiguration.
        """

    @abc.abstractmethod
    def get_weather_info(self, content):
        """ Collects weather information.

        Gets weather information from source and produce it in 
        the following format.

        weather_info = {
            'cond':       ''  # weather condition
            'temp':       ''  # temperature
            'feels_like': ''  # feels like temperature
            'wind':       ''  # information about wind
        }
        """

    @staticmethod
    def get_configuration_file():
        """ Returns path to configuration file in home directory.
        """

        return Path.home() / config.CONFIG_FILE

    def _get_configuration(self):
        """ Returns configured location name and url.

        :return: city name and url
        :rtype: tuple
        """

        name = self.default_location
        url = self.default_url
        configuration = configparser.ConfigParser()

        configuration.read(self.get_configuration_file())
        if config.CONFIG_LOCATION in configuration.sections():
            location_config = configuration[config.CONFIG_LOCATION]
            name, url = location_config['name'], location_config['url']
        return name, url

    def save_configuration(self, name, url):
        """ Saves selected location to configuration file.

        :param name: city name
        :param type: str

        :param url: preferred location URL
        :param type: str
        """

        parser = configparser.ConfigParser()
        parser[config.CONFIG_LOCATION] = {'name': name, 'url': url}
        with open(self.get_configuration_file(), 'w') as configfile:
            parser.write(configfile)

    @staticmethod
    def get_request_headers():
        """ Returns custom headers for url request.
        """

        return {'User-Agent': config.FAKE_MOZILLA_AGENT}

    @staticmethod
    def get_url_hash(url):
        """ Generates url hash.
        """

        return hashlib.md5(url.encode('utf-8')).hexdigest()

    @staticmethod
    def get_cache_directory():
        """ Path to cache directory.
        """

        return Path.home() / config.CACHE_DIR

    @staticmethod
    def is_valid(path):
        """ Checks if current cache is valid.
        """

        return (time.time() - path.stat().st_mtime) < config.CACHE_TIME

    def get_cache(self, url):
        """ Returns cache by given url address if any.
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
        """ Saves page source data to file.
        """

        cache_dir = self.get_cache_directory()
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)

        with  (cache_dir / self.get_url_hash(url)).open('wb') as cache_file:
            cache_file.write(page_source)

    def get_page_source(self, url, refresh=False):
        """ Gets page source by given url address.
        """

        cache = self.get_cache(url)
        if cache and not self.app.options.refresh:
            page_source = cache
        else:
            request = Request(url, headers=self.get_request_headers())
            page_source = urlopen(request).read()
            self.save_cache(url, page_source)
        return page_source.decode('utf-8')

    def run(self, argv):
        """ Runs provider.
        """

        content = self.get_page_source(self.url)
        return self.get_weather_info(content)