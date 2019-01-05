""" App commands.
"""

from abstract import Command


class Configurate(Command):

    """ Help to configure weatherapp providers.
    """

    def get_parser(self):
        parser = super().get_parser()
        parser.add_argument('provider', help='Provider name')
        return parser

    def run(self, argv):
        """ Runs command.
        """

        parsed_args = self.get_parser().parse_args(argv)
        if parsed_args.provider:
            provider_name = parsed_args.provider
            if provider_name in self.app.providermanager:
                provider_factory = self.app.providermanager.get(provider_name)
                provider_factory(self.app).configurate()