# This file is part of GPropertyGrid project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import sys
import os

try:
    DIR = os.path.dirname(os.path.realpath(__file__))
    DIR = os.path.normpath(os.path.join(DIR, '..', 'gpropertygrid'))
    if os.path.isdir(DIR):
        sys.path.insert(0, os.path.dirname(DIR))
except NameError:
    pass

from gi.repository import Gtk
from gpropertygrid import PropertyGrid
from gpropertygrid.properties import PropertyString, \
    PropertyBool, PropertyColor, PropertyList


class PropertyGridExample(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="PropertyGrid Quick Sample")
        self.set_border_width(10)
        self.set_size_request(300, 300)

        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=1)

        self._value_label = Gtk.Label(xalign=0)
        box.pack_start(self._value_label, False, False, 0)

        # Create the property grid object
        pg = PropertyGrid('My Porperties')
        pg.connect("changed", self._on_change_pg)

        # Create the property group object
        group = pg.create_group("Group")

        # Create property object
        str_property = PropertyString(
            name="String",
            id="1",
            default="Default value 1 for str",
            description="This is property 1 description")

        # Add property to the group
        group.add_property(str_property)

        # A readonly property
        str_readonly = PropertyString(
            name="String readonly",
            id="str_readonly",
            default="Default read only",
            description="This is the string read only description")
        str_readonly.set_read_only(True)
        group.add_property(str_readonly)

        # A string with lines
        str_lines = PropertyString(
            name="String Lines",
            id="str_lines",
            default="Line 1\nLine 2\nLine 3",
            description="This is the string with lines")
        group.add_property(str_lines)

        # Other group
        other_group = pg.create_group("Other group")

        bool_property = PropertyBool(
                    name="Boolean",
                    id="2",
                    default=True,
                    force_value=True,
                    description="This is a boolean property")

        color_property = PropertyColor(
                    name="Color",
                    id="color",
                    description="This is a color property")

        color_property2 = PropertyColor(
                    name="Color 2",
                    id="color2",
                    default='red',
                    description="This is a color property 2")

        color_property3 = PropertyColor(
                    name="Color 3",
                    id="color3",
                    default='green',
                    force_value=True,
                    description="This is a color property 3")

        other_group.add_property(bool_property)
        other_group.add_property(color_property)
        other_group.add_property(color_property2)
        other_group.add_property(color_property3)

        list_values = [
            ['0', 'Element 0'],
            ['1', 'Element 1'],
            ['2', 'Element 2'],
            [None, 'Element 3'],
            ['4', 'Element 4'],
        ]

        list_property1 = PropertyList(
                    name="List 1",
                    list_values=list_values,
                    description="This is a list property 1")

        list_property2 = PropertyList(
                    name="List 2",
                    list_values=list_values,
                    default={'id': '2'},
                    force_value=True,
                    description="This is a list property 2 with default")

        other_group.add_property(list_property1)
        other_group.add_property(list_property2)

        box.pack_start(pg, True, True, 0)

        # Show the content of groups
        pg.set_expanded(True)

        self.add(box)

    def _on_change_pg(self, grid, property_):
        text = "New value of '{0}': {1}".format(
                property_.name,
                property_.value)
        self._value_label.set_text(text)


win = PropertyGridExample()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
