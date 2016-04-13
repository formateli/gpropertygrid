# This file is part of GPropertyGrid project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import unittest
from gi.repository import Gdk
from gpropertygrid import PropertyGrid
from gpropertygrid.properties import PropertyString, \
    PropertyColor


class PropertiesTest(unittest.TestCase):
    def testProperties(self):
        pass

    def testPropertyString(self):
        ps = PropertyString(
            name='Test string',
            default='Hello world!',
            force_value=False)
        self.assertEqual(ps.value, None)

        ps = PropertyString(
            name='Test string',
            default='Hello world!',
            force_value=True)
        self.assertEqual(ps.value[0], 'Hello world!')

    def testPropertyColor(self):
        pc = PropertyColor(name='Test color')
        self.assertEqual(pc.value, None)

        pc = PropertyColor(
            name='Test color',
            default='black',
            force_value=False)
        self.assertEqual(pc.value, None)

        pc = PropertyColor(
            name='Test color',
            default='black',
            force_value=True)
        self.assertEqual(isinstance(pc.value[0], Gdk.RGBA), True)
