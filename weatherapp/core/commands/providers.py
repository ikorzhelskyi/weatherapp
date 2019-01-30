from weatherapp.core.abstract.command import Command


class Providers(Command):

    """ Prints list of all providers.
    """

    name = 'providers'

    def run(self, argv):
        """ Runs command.
        """

        for name in self.app.providermanager._providers:
            self.app.stdout.write(f"{provider[0]} \n")