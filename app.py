""" Main application module.
"""

import sys
import traceback
from argparse import ArgumentParser

from commandmanager import CommandManager
from providermanager import ProviderManager


class App:

    """ Weather aggregator application.
    """

    def __init__(self):
        self.arg_parser = self._arg_parse()
        self.providermanager = ProviderManager()
        self.commandmanager = CommandManager()

    def _arg_parse(self):
        """ Initializes argument parser.
        """

        arg_parser = ArgumentParser(add_help=False)
        arg_parser.add_argument('command', help="Command", nargs='?')
        arg_parser.add_argument('--refresh', help="Bypass caches",
                                action='store_true')
        arg_parser.add_argument('--debug', help='Show traceback on errors',
                                action='store_true', default=False)
        return arg_parser

    def produce_output(self, title, location, info):
        """ Prints results.
        """

        print(f'{title}:')
        print("#"*10, end='\n\n')

        print(f'{location}')
        print("-"*20)
        for key, value in info.items():
            print(f'{key}: {value}')
        print("="*40, end="\n\n")

    def run(self, argv):
        """ Runs application.

        :param argv: list of passed arguments
        """

        self.options, remaining_args = self.arg_parser.parse_known_args(argv)
        command_name = self.options.command

        if command_name in self.commandmanager:
            command_factory = self.commandmanager.get(command_name)
            try:
                command_factory(self).run(remaining_args)
            except Exception:
                print('Error during command: %s run')
                if self.options.debug:
                    print(traceback.print_exc())

        if not command_name:
            # runs all weather providers by default
            for name, provider in self.providermanager._commands.items():
                self.produce_output(provider.title,
                                    provider(self).location,
                                    provider(self).run(remaining_args))
        elif command_name in self.providermanager:
            # runs specific provider
            provider = self.providermanager[command_name](self)
            self.produce_output(provider.title,
                                provider.location,
                                provider.run(remaining_args))
        else:
            print('Unknown command provided.')
            sys.exit(1)


def main(argv=sys.argv[1:]):
    """ Main entry point.
    """

    return App().run(argv)


if __name__ == '__main__':
    main(sys.argv[1:])