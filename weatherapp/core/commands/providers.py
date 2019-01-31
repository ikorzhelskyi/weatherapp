from weatherapp.core.abstract.command import Command


class Providers(Command):

    """ Prints list of all providers.
    """

    name = 'providers'

    def run(self, argv):
        """ Runs command.
        """

        for provider in self.app.providermanager:
            self.app.stdout.write(f"{provider[0]} \n")