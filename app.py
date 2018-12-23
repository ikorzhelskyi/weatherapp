"""Main application module.
"""

import sys
from argparse import ArgumentParser


class App:

    """Weather aggregator application.
    """

    def __init__(self):
        self.arg_parser = self._arg_parse()

    def _arg_parse(self):
        """Initialize argument parser.
        """

        arg_parser = ArgumentParser(add_help=False)
        arg_parser.add_argument('command', help="Command", nargs='?')
        arg_parser.add_argument('--refresh', help="Bypass caches",
                                action='store_true')
        return arg_parser

    def produce_output(self, title, location, info):
        """Print results.
        """

        print(f'{title}:')
        print("#"*10, end='\n\n')

        print(f'{location}')
        print("-"*20)
        for key, value in info.items():
        print(f'{key}: {value}')
        print("="*40, end="\n\n")

    def run(self, argv):
        """Run application.

        :param argv: list of passed arguments
        """

        self.options, remaining_args = self.arg_parser.parse_known_args(argv)
        command_name = self.options.command

        if not command_name:
            # run all weather providers by default
            pass
        elif command_name in {}:
            # run specific provider
            pass


def main(argv=sys.argv[1:])
    """Main entry point.
    """    

    return App().run(argv)


if __name__ == '__main__':
    main(sys.argv[1:])