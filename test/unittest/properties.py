# This file is part of GPropertyGrid project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import unittest
from gpropertygrid import PropertyGrid
from gpropertygrid.properties import PropertyString


class PropertiesTest(unittest.TestCase):
    def testProperties(self):
        pass

    def testPropertiesString(self):
        ps = PropertyString(
            name='Test string',
            default='Hello world!',
            force_value=False)
        self.assertEqual(ps.value, None)

        ps = PropertyString(
            name='Test string',
            default='Hello world!',
            force_value=True)
        self.assertEqual(ps.value, 'Hello world!')
