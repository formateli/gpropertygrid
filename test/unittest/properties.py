# This file is part of GPropertyGrid project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import unittest
from gi.repository import Gtk, Gdk
from gpropertygrid import PropertyGrid
from gpropertygrid.properties import PropertyString, \
    PropertyColor, PropertyList


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

    def testPropertyList(self):
        pl = PropertyList(name='Test list', list_values=None)
        self.assertEqual(pl.value, None)
        pl = PropertyList(name='Test list', list_values=[])
        self.assertEqual(pl.value, None)

        values = [
            ['0', 'ZERO'],
            ['1', 'ONE'],
            ['2', 'TWO']
        ]

        pl = PropertyList(
            name='Test list',
            list_values=values)
        self.assertEqual(pl.value, None)

        pl = PropertyList(
            name='Test list',
            list_values=values,
            default={'id': '1'},
            force_value=False)
        self.assertEqual(pl.value, None)

        pl = PropertyList(
            name='Test list',
            list_values=values,
            default={'id': '1'},
            force_value=True)
        self.assertEqual(pl.value[0], '1')
        self.assertEqual(pl.value[1], 'ONE')

        # With entry
        pl = PropertyList(
            name='Test list',
            list_values=values,
            with_entry=True,
            default={'id': '1'},
            force_value=True)
        self.assertEqual(pl.value[0], '1')
        self.assertEqual(pl.value[1], 'ONE')

        entry = Gtk.Bin.get_child(pl._combo)
        entry.set_text('Hello')
        self.assertEqual(pl._combo.get_active_text(), 'Hello')
