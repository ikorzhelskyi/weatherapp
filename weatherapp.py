#!/usr/bin/env python

"""Script for scraping data from weather sites.
"""

import sys
import html
import argparse

from providers import AccuWeatherProvider, Rp5WeatherProvider


def produce_output_accu(city_name, info):
    """Formats and displays the found data.
    """

    print('AccuWeather: \n')
    print(f'{city_name}')
    print('_'*20)
    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')


def produce_output_rp5(city_name, info):
    """Formats and displays the found data.
    """

    print('Rp5: \n')
    print(f'{city_name}')
    print('_'*20)
    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')


def get_accu_weather_info(refresh=False):
    accu = AccuWeatherProvider()
    produce_output_accu(accu.location, accu.run(refresh=refresh))


def get_rp5_weather_info(refresh=False):
    rp5 = Rp5WeatherProvider()
    produce_output_rp5(rp5.location, rp5.run(refresh=refresh))


def main(argv):
    """Main entry point.
    """

    KNOWN_COMMANDS = {'accu': get_accu_weather_info,
                      'rp5': get_rp5_weather_info} #'config': configurate}

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