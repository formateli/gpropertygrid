# This file is part of GPropertyGrid project. 
# The COPYRIGHT file at the top level of this repository 
# contains the full copyright notices and license terms.

import sys, os

try:
    DIR = os.path.dirname(os.path.realpath(__file__))
    DIR = os.path.normpath(os.path.join(DIR, '..', 'gpropertygrid'))
    if os.path.isdir(DIR):
        sys.path.insert(0, os.path.dirname(DIR))
except NameError:
    pass

from gi.repository import Gtk
from gpropertygrid import PropertyGrid
from gpropertygrid.properties import PropertyString, PropertyBool, PropertyColor

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

        other_group.add_property(bool_property)
        other_group.add_property(color_property)

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
