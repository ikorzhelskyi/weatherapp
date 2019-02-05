import unittest

from weatherapp.core.providermanager import ProviderManager


class DummyCommand:
    pass


class ProviderManagerTestCase(unittest.TestCase):

    """ Unit test case for providers manager.
    """

    def setUp(self):
        self.provider_manager = ProviderManager()

    def test_load_commands(self):
        """ Test load commands method for providers manager.
        """

        self.provider_manager.add('dummy', DummyCommand)

        self.assertTrue('dummy' in self.provider_manager._commands)
        self.assertEqual(self.provider_manager.get('dummy'), DummyCommand)
        self.assertFalse('bar' in self.provider_manager)
        self.assertIsNone(self.provider_manager.get('bar'))


if __name__ == '__main__':
    unittest.main()