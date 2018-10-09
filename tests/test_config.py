from tests import CommandTestCase

from botctl.errors import UndefinedConfigValue
from botctl.types import PlatformEnvironment, PlatformVariable


class TestConfig(CommandTestCase):
    def test_config(self):
        self.config.put_value(PlatformEnvironment.LOCAL,
                              PlatformVariable.CMS,
                              'http://localhost:8001')
        cms = self.config.get_value(PlatformEnvironment.LOCAL,
                                    PlatformVariable.CMS)

        self.assertEqual(cms, 'http://localhost:8001')
        self.config.del_value(PlatformEnvironment.LOCAL,
                              PlatformVariable.CMS)

        with self.assertRaises(UndefinedConfigValue):
            self.config.get_value(PlatformEnvironment.LOCAL,
                                  PlatformVariable.CMS)
