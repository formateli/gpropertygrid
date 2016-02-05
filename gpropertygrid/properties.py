# This file is part of GPropertyGrid project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

from gi.repository import Gtk, Gdk, Pango

class PropertyGridProperty(Gtk.Paned):
    def __init__(self, name,
                value_widget,
                id=None,
                default=None,
                description=None,
                force_value=False):
        """Main property class from where all property classes must derives.

        Args:
            name: The name of the property.

            value_widget: The widget used for manages the property value.

            id (string): Optional. The id of the property. 
                Must be uniq per property. 
                It is only important if this property will be retreiving by 
                the property grid using the get_property_by_id function. 
                Default None.

            default: Optional. The default value for this property.

            description (string): Optional. The property description.

            force_value (boolean): Optional. If True, default is asigned to the property value 
                at object creation time, otherwise value remains None until it changes by user.
        """

        super(PropertyGridProperty,
                self).__init__(orientation=Gtk.Orientation.HORIZONTAL)

        self.name = name
        self.id = id
        self.description = description

        self._group = None
        self._value = None
        self._curr_width = -1
        self._curr_position = -1
        self._has_focus = False
        self._read_only = False

        self.do_force_value(force_value, default)

        self._name_widget = self._get_display_widget(0)
        self._name_widget._main_label.set_text(name)
        self._display_widget = self._get_display_widget(1)
        self.update_display_value()

        self.pack1(self._name_widget, True, True)
        self.pack2(self._display_widget, True, True)
        self.connect("draw", self._on_draw)

        self._value_widget = value_widget

    @property
    def has_focus(self):
        return self._has_focus

    @property
    def value(self):
        """
        The current value of the property.
        """
        return self._value

    def do_force_value(self, force_value, default):
        """Forces default value at property creation time.

        This method is called when property object is created,
        it can be overriden for special cases, for example, when
        default_value is of diferent type that the value of 
        the property.

        Args:
            force_value (boolean): If True, default value is set.

            default: Default value to set if force_value is True.
        """
        if force_value:
            self._value = default

    def update_display_value(self):
        """
        Update current display value of the property.

        This method should not be called unless a
        special representation were needed, in this case
        function must be overriden.
        """
        if self._value == None:
            text = '[No value]'
        else:
            text = str(self._value)
        self._display_widget._main_label.set_text(text)

    def has_changed(self):
        """Tells the property grid that the property Value has changed.

        Every property object must call this function
        each time its value changes.
        """
        self._group._grid._property_changed(self)
        self.update_display_value()

    def set_read_only(self, readonly):
        """Sets ReadOnly state of the property.

        Args:
            readonly: Boolean value that sets the ReadOnly state.
        """
        self._read_only = readonly
        self._display_widget._main_label.set_selectable(readonly)

    def on_change(self, data=None):
        return self._has_focus

    def on_display_notify(self, box, event_type, data):
        """Event called when mouse in/out over display widgets
        """
        self._name_widget.change_color(data["type"])
        self._display_widget.change_color(data["type"])

    def on_display_click(self, box, event_type, data):
        """Event called when mouse click on display widgets
        """
        self._show_hide_value_widget()

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

    def _show_hide_value_widget(self):
        if self._read_only:
            self._on_enter() # This way we force on_leave() on all other properties.
            return
        curr_wg = self._display_widget.get_children()[0]
        if self._has_focus:
            new_wg = self._display_widget.box
        else:
            new_wg = self._value_widget

        self._display_widget.remove(curr_wg)
        self._display_widget.pack_start(new_wg, True, True, 0)
        self._display_widget.show_all()
        if not self._has_focus:
            new_wg.grab_focus()
            self._on_enter()
        self._has_focus = not self._has_focus

    def _on_enter(self, data=None):
        self._group.grid._on_enter_widget(self.id)

    def _get_display_widget(self, index):
        return _DisplayWidget(
            index,
            self.on_display_notify,
            self.on_display_click)


class _DisplayWidget(Gtk.Box):
    def __init__(self, index, notify_handler, click_handler):
        super(_DisplayWidget, self).__init__()

        self._main_label = Gtk.Label(xalign=0)
        self._main_label.set_single_line_mode(True)
        self._main_label.set_ellipsize(Pango.EllipsizeMode.END)
        self._event_box = Gtk.EventBox()

        self._main_label.set_name('cell')
        self._event_box.add(self._main_label)

        self._event_box.connect("enter-notify-event", notify_handler,
                    {"index":index,
                     "type":"in"})
        self._event_box.connect("leave-notify-event", notify_handler,
                    {"index":index,
                     "type":"out"})
        self._event_box.connect("button-press-event", click_handler,
                                {"index":index})

        self.box = Gtk.Box()
        self.box.pack_start(self._event_box, True, True, 0)
        self.pack_start(self.box, True, True, 0)

    def change_color(self, data_type):
        ctx = self._main_label.get_style_context()
        if data_type == 'in':
            ctx.add_class('cell_in')
        else:
            ctx.remove_class('cell_in')


class PropertyString(PropertyGridProperty):
    def __init__(self, name,
                id=None,
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

        super(PropertyString, self).__init__(
            name=name,
            value_widget=self._txt,
            id=id,
            default=default,
            description=description,
            force_value=force_value)

        if default == None:
            default = ''
        self._txt.set_text(default)

    def on_change(self):
        if not super(PropertyString, self).on_change():
            return False
        self._value = self._txt.get_text()
        self.has_changed()
        return True

    def _on_txt_changed(self, wg):
        self.on_change()


class PropertyBool(PropertyGridProperty):

    def __init__(self, name, id=None,
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

        if default == True:
            self._check.set_active(True)

    def on_change(self):
        if not super(PropertyBool, self).on_change():
            return False
        self._value = self._check.get_active()
        self.has_changed()
        return True

    def _on_toggled(self, wg):
        self.on_change()


class PropertyColor(PropertyGridProperty):
    """
    A Color property class. Derived from PropertyGridProperty.
    Uses the Gtk.ColorButton as a value widget.
    value is a Gdk.RGBA object or None.
    """
    def __init__(self, name, id=None,
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

        self._color_label = Gtk.Label(xalign=0)
        self._color_label.set_name('cell')
        self._style_provider = Gtk.CssProvider()
        ctx = self._color_label.get_style_context()
        ctx.add_provider(
            self._style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        super(PropertyColor, self).__init__(
            name=name,
            value_widget=hbox,
            id=id,
            default=default,
            description=description,
            force_value=force_value)

        self._display_widget.box.pack_start(self._color_label, True, True, 0)
        self._display_widget.box.reorder_child(self._color_label, 0)
        self._display_widget.box.connect("draw", self._on_draw_color_display)

    def on_change(self):
        if not super(PropertyColor, self).on_change():
            return False

        color = self._get_color_from_str(self._txt.get_text())
        if color:
            self._buttom.set_rgba(color)
            self._value = self._buttom.get_rgba()
        else:
            self._buttom.set_rgba(Gdk.RGBA())
            self._value = None
        self.has_changed()
        return True

    def do_force_value(self, force_value, default):
        color = self._get_color_from_str(default)
        if color:
            if force_value:
                self._value = color
            self._buttom.set_rgba(color)
            self._txt.set_text(default)
        else:
            self._txt.set_text('')

    def update_display_value(self):
        ctx = self._color_label.get_style_context()

        if self._value is None:
            super(PropertyColor, self).update_display_value()
            ctx.remove_class('color_label')
            return

        self._display_widget._main_label.set_text(
            self._txt.get_text())

        #self._style_provider.load_from_data ('#cell.color_label {background-color: ' + self._txt.get_text() + ';}')
        self._style_provider.load_from_data(
                self._get_css_color_class(self._txt.get_text())
            )
        ctx.add_class('color_label')

    def _on_draw_color_display(self, wg, data):
        wd = wg.get_allocated_width() / 4
        self._color_label.set_size_request(
            wd, self._color_label.get_allocated_height())
        self._display_widget._main_label.set_size_request(
            wd * 3, self._color_label.get_allocated_height())

    def _get_css_color_class(self, color):
        css = '#cell.color_label {background-color: ' + color + ';}'    
        return css.encode('utf8')

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

