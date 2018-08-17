import os
import unittest

import botctl.config

from botctl.config import ConfigStore

TEST_HOME = os.path.join(os.path.dirname(__file__), 'home')

class CommandTestCase(unittest.TestCase):
    def setUp(self):
        botctl.config.__configdir__ = TEST_HOME
        self.config = ConfigStore()

    def tearDown(self):
        if os.path.exists(self.config._path):
            os.unlink(self.config._path)

    def set_config_ini_content(self, content):
        with open(self.config._path, 'w') as config_file:
            config_file.write(content)
