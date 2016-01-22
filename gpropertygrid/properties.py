# This file is part of GPropertyGrid project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

from gi.repository import Gtk, Gdk

class PropertyGridProperty(Gtk.Paned):

    def __init__(self, name, value_widget, id=None,
                default=None,
                description=None,
                force_value=False):
        """Main property class from where all property classes must derives.

        Args:
            name: The name of the proeprty.

            value_widget: The widget used for manages the property value.

            id (string): Optional. The id of the property. 
                Must be uniq per property. 
                It is only important if this property will be retreiving by 
                the property grid using the get_property_by_id function. 
                Default None.

            default: The default value for this property.

            description: Optional. The property description.
            
            force_value: Optional. If True, default is asigned to the property value 
                at object creation time, otherwise value remains None until it changes by user.
        """

        super(PropertyGridProperty,
                self).__init__(orientation=Gtk.Orientation.HORIZONTAL)

        self._group = None # PropertyGridGroup
        self.name = name
        self.id = id
        self.default = default
        self.value = None
        self.description = description

        self._curr_width = -1
        self._curr_position = -1
        self._has_focus = False
        self._read_only = False

        if force_value:
            self.value = self.default

        self.box_0 = Gtk.Box()
        self.box_1 = Gtk.Box()
        self.event_box_0 = None
        self.event_box_1 = None
        self.cell_0 = None
        self.cell_1 = None

        self.pack1(self._get_cell(0), True, True)
        self.pack2(self._get_cell(1), True, True)

        self.connect("draw", self._on_draw)
        self.cell_0.set_text(name)
        self.value_widget = value_widget

    @property
    def has_focus(self):
        return self._has_focus

    def has_changed(self):
        """Tells the property grid that the property Value has changed.

        Every property object must call this function
        each time its value changes.
        """
        self._group._grid._property_changed(self)

    def set_value_text(self, text):
        """Sets the text to show in the value area of the row.

        Args:
            text: The text to show. 
                This text is a representation of the current value of the property.
        """
        if not text:
            self.cell_1.set_text("[No value]")
        else:
            self.cell_1.set_text(text)

    def set_read_only(self, readonly):
        """Sets ReadOnly state of the property.

        Args:
            readonly: Boolean value that sets the ReadOnly state.
        """
        self._read_only = readonly
        self.cell_1.set_selectable(readonly)

    def on_change(self, data=None):
        return self._has_focus

    def _get_cell(self, cell_index):
        if cell_index == 0:
            self.cell_0 = Gtk.Label(xalign=0)
            self.event_box_0 = Gtk.EventBox()
            cell = self.cell_0
            ebox = self.event_box_0
            box = self.box_0
        else:
            self.cell_1 = Gtk.Label(xalign=0)
            self.event_box_1 = Gtk.EventBox()
            cell = self.cell_1
            ebox = self.event_box_1
            box = self.box_1
        cell.set_name("cell")
        ebox.add(cell)

        ebox.connect("enter-notify-event", self._on_mouse_notify, 
                    {"index":cell_index,
                     "type":"in"})
        ebox.connect("leave-notify-event", self._on_mouse_notify,
                    {"index":cell_index,
                     "type":"out"})
        ebox.connect("button-press-event", self._on_cell_click,
                                {"index":cell_index})

        box.pack_start(ebox, True, True, 0)
        return box

    def _on_mouse_notify(self, box, event_type, data):
        self._change_cell_color(0, data["type"])
        self._change_cell_color(1, data["type"])

    def _change_cell_color(self, cell_index, data_type):
        if cell_index == 0:
            cell = self.cell_0
        else:
            cell = self.cell_1
        ctx = cell.get_style_context()
        if data_type == "in":
            ctx.add_class("cell_in")
        else:
            ctx.remove_class("cell_in")

    def _on_draw(self, wg, data):
        if self.get_allocated_width() != self._curr_width:
            position = int(self.get_allocated_width() / 3)
            self._set_curr_position(position)
            self._curr_width = self.get_allocated_width()
        else:
            for p in self._group.properties:
                p._set_curr_position(self.get_position())

    def _set_curr_position(self, position):
        if self._curr_position != position:
            self.set_position(position)
        self._curr_position = position

    def _on_cell_click(self, box, event_type, data):
        self._show_hide_value_widget()

    def _show_hide_value_widget(self):
        if self._read_only:
            self._on_enter() # This way we force on_leave() on all other properties.
            return
        curr_wg = self.box_1.get_children()[0]
        if self._has_focus:
            new_wg = self.event_box_1
        else:
            new_wg = self.value_widget

        self.box_1.remove(curr_wg)
        self.box_1.pack_start(new_wg, True, True, 0)
        self.box_1.show_all()
        if not self._has_focus:
            new_wg.grab_focus()
            self._on_enter()
        self._has_focus = not self._has_focus

    def _on_enter(self, data=None):
        self._group.grid._on_enter_widget(self.id)


class PropertyString(PropertyGridProperty):

    def __init__(self, name, id,
                default=None,
                description=None,
                force_value=False):
        """A String property class. It uses the Gtk.Entry as a value widget.        
        
        See :class:`PropertyGridProperty` for parameters.

        Note:
            *default* parameter must be a valid string object.
        """
        self._txt = Gtk.Entry()
        self._txt.connect("changed", self._on_txt_changed)

        super(PropertyString, self).__init__(name=name, value_widget=self._txt,
                id=id, default=default, description=description, force_value=force_value)

        self.set_value_text(default)
        self._txt.set_text(default)

    def on_change(self):
        if not super(PropertyString, self).on_change():
            return False
        self.value = self._txt.get_text()
        self.set_value_text(self.value)
        self.has_changed()
        return True

    def _on_txt_changed(self, wg):
        self.on_change()


class PropertyBool(PropertyGridProperty):

    def __init__(self, name, id, 
            default=None, description=None, force_value=False):
        """A Boolean property class. It uses the Gtk.Check as a value widget.

        See :class:`PropertyGridProperty` for parameters.

        Note:
            *default* parameter must be a boolean value, True or False
        """
        self._check = Gtk.CheckButton()
        self._check.connect("toggled", self._on_toggled)

        super(PropertyBool, self).__init__(
                name=name, value_widget=self._check,
                id=id, default=default, description=description,
                force_value=force_value)

        self._set_text(default)
        if default == True:
            self._check.set_active(True)

    def on_change(self):
        if not super(PropertyBool, self).on_change():
            return False
        self.value = self._check.get_active()
        self._set_text(self.value)
        self.has_changed()
        return True

    def _set_text(self, value):
        if value == None:
            self.set_value_text(None)
        else:
            if value == True:
                self.set_value_text("True")
            else:
                self.set_value_text("False")

    def _on_toggled(self, wg):
        self.on_change()


class PropertyColor(PropertyGridProperty):
    """
    A Color property class. Derived from PropertyGridProperty.
    Uses the Gtk.ColorButton as a value widget.
    value is a Gdk.RGBA object or None.
    """
    def __init__(self, name, id, 
            default=None, description=None, force_value=False):
        """A Color property class. It uses the Gtk.ColorButton as a value widget.

        Value is a Gdk.RGBA object or None.
        
        See :class:`PropertyGridProperty` for parameters.

        Note:
            *default* parameter must be a color string that can be used to create 
            the Gdk.RGBA object. Ex: red, black, #000000, rgb(52,101,164)
        """
        hbox = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL)

        self._txt = Gtk.Entry()
        self._txt.connect("changed", self._on_txt_changed)

        self._buttom = Gtk.ColorButton()
        self._buttom.set_use_alpha(True)
        self._buttom.connect("color_set", self._on_toggled)

        hbox.pack_start(self._buttom, True, True, 0)
        hbox.pack_start(self._txt, True, True, 0)        
        
        super(PropertyColor, self).__init__(name=name, value_widget=hbox,
                id=id, default=default, description=description, force_value=force_value)

        self.set_value_text(default)

        color = self._get_color_from_str(default)
        if color:
            self._buttom.set_rgba(color)
        if default == None:
            default = ''
        self._txt.set_text(default)

    def on_change(self):
        if not super(PropertyColor, self).on_change():
            return False

        color = self._get_color_from_str(self._txt.get_text())
        if color:
            self._buttom.set_rgba(color)
            self.value = self._buttom.get_rgba()
        else:
            self._buttom.set_rgba(Gdk.RGBA())
            self.value = None
        if self.value:
            self.set_value_text(self._txt.get_text())
        else:
            self.set_value_text(None)
        self.has_changed()
        return True

    def _on_toggled(self, wg):
        self._txt.set_text(self._buttom.get_rgba().to_string())

    def _on_txt_changed(self, wg):
        self.on_change()

    def _get_color_from_str(self, str_color):
        if str_color == None:
            return
        color = Gdk.RGBA()
        if color.parse(str_color):
            return color

