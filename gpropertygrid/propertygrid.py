# This file is part of GPropertyGrid project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

from gi.repository import Gtk, GObject
from . properties import PropertyGridProperty


class PropertyGrid(Gtk.Box, GObject.GObject):
    __gsignals__ = {
        'changed': (
            GObject.SIGNAL_RUN_FIRST, None,
            (PropertyGridProperty,))
    }

    def __init__(self, title):
        """The main PropertyGrid widget class.

        Args:
            title (string): The title of the property grid.

        Signals:
            **changed**: Emited when a property object changes.
        """

        Gtk.Box.__init__(
            self,
            orientation=Gtk.Orientation.VERTICAL,
            spacing=1)
        GObject.GObject.__init__(self)

        self._groups = []
        self._properties = []
        self._property_names = {}
        self._next_id = -1
        self._expanded = False

        event_box = Gtk.EventBox()
        self._grid_header = Gtk.Label(xalign=0)
        self._grid_header.set_name("property_grid_header")
        self._grid_header.set_text(title)
        event_box.add(self._grid_header)
        event_box.connect("button-press-event", self._on_header_click, {})
        self.pack_start(event_box, False, False, 0)

        self._description = _PropertyDescription()
        self.pack_end(self._description, False, False, 0)

        self._sw = Gtk.ScrolledWindow()
        self.pack_start(self._sw, False, False, 0)

        self._groups_rows = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self._sw.add(self._groups_rows)

        self.connect("draw", self._on_draw)

    @property
    def properties(self):
        """
        List of all properties objects that belongs to the property grid.
        """
        return self._properties

    def get_title(self):
        """Gets the current title of the property grid.

        Returns:
            The current title string of property grid.
        """
        return self._grid_header.get_text()

    def set_title(self, title):
        """Sets the title for the property grid.

        Args:
            title (string): The title of the property grid.
        """
        self._grid_header.set_text(title)

    def create_group(self, group_title):
        """Create a new group of properties.

        It Automatically adds the group created to the property grid.

        Args:
            group_title (string): The title of the group.

        Returns:
            A :class:`PropertyGridGroup` object.
        """
        group = PropertyGridGroup(group_title)
        self._groups.append(group)
        group._grid = self
        self._groups_rows.pack_start(group, False, False, 0)
        return group

    def remove_all_groups(self):
        """Removes all groups from property grid.
        """
        for g in self._groups:
            self._groups_rows.remove(g)
        self._description.set_value('', '')
        self._groups = []

    def get_property_by_id(self, id):
        """Finds and returns a PropertyGridProperty for given id.

        Args:
            id (string): The id of the PropertyGridProperty object fo find.

        Returns:
            A PropertyGridProperty object. None if property is not found.
        """
        if id not in self._property_names:
            return
        return self._property_names[id]

    def set_expanded(self, expanded):
        """Sets the expanded state of the group.

        Args:
            expanded (boolean): If True, group expands to show
                its properties.
        """
        for g in self._groups:
            g.set_expanded(expanded)
        self._expanded = expanded

    def _on_header_click(self, box, event_type, data):
        self.set_expanded(not self._expanded)

    def _property_changed(self, property_):
        self.emit("changed", property_)

    def _on_draw(self, wg, data):
        w = self.get_allocated_width() - 50
        h = self.get_allocated_height() - \
            self._description.get_allocated_height() - 40
        self._sw.set_size_request(w, h)

    def _add_property(self, group, property_):
        property_._group = group
        if property_.id is None:
            property_.id = "property_{0}".format(self._next_id)
            self._next_id += 1
        if property_.id in self._property_names:
            property_.value_widget.set_sensitive(False)
            raise ValueError(
                "Properpy with id {0} already exists in property grid".format(
                    property_.id))
        self._properties.append(property_)
        self._property_names[property_.id] = property_
        group._properties.append(property_)

    def _on_enter_widget(self, id):
        for p in self._properties:
            if p.id == id:
                self._description.set_value(p.name, p.description)
                continue
            if p._has_focus:
                p._show_hide_value_widget()


class PropertyGridGroup(Gtk.Expander):
    def __init__(self, title):
        """Manages a group of :class:`PropertyGridProperty` objects.

        Args:
            title (string): The title of the group.
        """
        super(PropertyGridGroup, self).__init__()
        self._grid = None
        self._properties = []
        self.set_name("group_header")

        self._row = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=0)

        label = Gtk.Label(xalign=0)
        label.set_name("group_header_label")
        label.set_text(title)
        self.set_label_widget(label)
        self.set_label_fill(True)
        self.add(self._row)

    @property
    def grid(self):
        """
        PropertyGrid object owner of the group. Read only.
        """
        return self._grid

    @property
    def properties(self):
        """
        Read only. List of PropertyGridProperty objects
        that belongs to group.
        """
        return self._properties

    def add_property(self, property_):
        """Adds a PropertyGridProperty object to this group.

        Args:
            property_: A PropertyGridProperty object.
        """
        if not self._grid:
            raise ValueError(
                "Group must be added to PropertyGrid first.")
        self._grid._add_property(self, property_)
        self._row.pack_start(property_, False, False, 0)


class _PropertyDescription(Gtk.Frame):
    def __init__(self):
        super(_PropertyDescription, self).__init__()
        self.set_shadow_type(Gtk.ShadowType.IN)

        self._name = Gtk.Label(xalign=0)
        self._name.set_name("description_name")
        self._description = Gtk.Label(xalign=0)
        self._description.set_name("description_description")

        vbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=1)
        vbox.pack_start(self._name, False, False, 0)
        vbox.pack_start(self._description, False, False, 0)
        self.add(vbox)

    def set_value(self, name, description):
        self._name.set_text(name)
        self._description.set_text(description)
