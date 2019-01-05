from providers import AccuWeatherProvider, Rp5WeatherProvider


class ProviderManager:

    """ Discovers registered providers and loads them.
    """

    def __init__(self):
        self._providers = {}
        self._load_providers()

    def _load_providers(self):
        """ Loads all existing providers.
        """

        for provider in [AccuWeatherProvider, Rp5WeatherProvider]:
            self.add(provider.name, provider)
    
    def add(self, name, provider):
        """ Adds new provider by name.
        """

        self._providers[name] = provider

    def get(self, name):
        """ Gets provider by name.
        """

        return self._providers.get(name, None)

    def __len__ (self):
        return len(self._providers)

    def __contains__(self, name):
        return name in self._providers

    def __getitem__(self, name):
        return self._providers[name]