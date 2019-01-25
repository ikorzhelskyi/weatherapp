import re

from bs4 import BeautifulSoup

from weatherapp.core import config
from weatherapp.core.abstract import WeatherProvider


class AccuWeatherProvider(WeatherProvider):

    """ Weather provider for AccuWeather site.
    """

    name = config.ACCU_PROVIDER_NAME
    title = config.ACCU_PROVIDER_TITLE

    def get_name(self):
        return self.name

    def get_default_location(self):
        return config.DEFAULT_ACCU_LOCATION_NAME

    def get_default_url(self):
        return config.DEFAULT_ACCU_LOCATION_URL

    def get_locations(self, locations_url):
        """ Gets list of available locations.
        """

        locations_page = self.get_page_source(locations_url)
        soup = BeautifulSoup(locations_page, 'html.parser')
        locations = []
        for location in soup.find_all('li', attrs={'class': 'drilldown cl'}):
            url = location.find('a').attrs['href']
            location = location.find('em').text
            locations.append((location, url))
        return locations

    def configurate(self):
        """ Configure provider.
        """

        locations = self.get_locations(config.ACCU_BROWSE_LOCATIONS)
        while locations:
            for index, location in enumerate(locations):
                print(f'{index + 1}. {location[0]}')

            try:
                selected_index = int(input('Please select location: '))
                location = locations[selected_index - 1]
                locations = self.get_locations(location[1])
            except IndexError:
                msg = 'You have entered a wrong number.'
                if self.app.options.debug:
                    self.app.logger.exception(msg)
                else:
                    self.app.logger.error(msg)
            except ValueError:
                msg = "You didn't enter the number."
                if self.app.options.debug:
                    self.app.logger.exception(msg)
                else:
                    self.app.logger.error(msg)

        self.save_configuration(*location)

    def get_weather_info(self, page_source):
        """ Gets data from the site using the BeautifulSoup library.
        """

        city_page = BeautifulSoup(page_source, 'html.parser')
        current_day_section = city_page.find(
            'li', class_=re.compile('(day|night) current first cl'))

        weather_info = {}
        if current_day_section:
            current_day_url = current_day_section.find('a').attrs['href']
            if current_day_url:
                current_day_page = self.get_page_source(current_day_url)
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
                    feal_temp = weather_details.find('span',
                                                     class_='small-temp')
                    if feal_temp:
                        weather_info['feal-temp'] = feal_temp.text

                    wind_info = weather_details.find_all('li', class_='wind')
                    if wind_info:
                        weather_info['wind'] = \
                            ' '.join(map(lambda t: t.text.strip(),wind_info))
        return weather_info