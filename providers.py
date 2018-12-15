from pathlib import Path
import configparser
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