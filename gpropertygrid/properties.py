# This file is part of GPropertyGrid project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

from gi.repository import Gtk, Gdk, Pango


class PropertyGridProperty(Gtk.Paned):
    def __init__(
            self, name,
            value_widget,
            id=None,
            default=None,
            description=None,
            force_value=False):
        """Main property class from where all property classes must derives.

        Args:
            name (string): The name of the property.

            value_widget (gtk widget): The widget used for manages
                the property value.

            id (string): Optional. The id of the property.
                Must be uniq per property.
                It is only important if this property will be
                retreived by the property grid using the
                get_property_by_id function.
                Default None.

            default: Optional. The default value for this property.

            description (string): Optional. The property description.

            force_value (boolean): Optional. If True, default is asigned
                to the property value at object creation time,
                otherwise value remains None until it changes by user.
        """

        super(PropertyGridProperty, self).__init__(
            orientation=Gtk.Orientation.HORIZONTAL)

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
        It is a virtual method, so each property must override it.

        It verify the default value and if it has to be forced to
        get a value, and set the value_widget.

        Args:
            force_value (boolean): If True, default value is set.

            default: Default value to set if force_value is True.
        """
        error = "do_force_value() function must be defined for property '{0}'"
        raise NotImplementedError(error.format(
                self.__class__.__name__))

    def update_display_value(self):
        """
        Update current display value of the property.

        This method should not be called unless a
        special representation were needed, in this case
        function must be overriden.
        """
        if self._value is None:
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
            readonly (boolean): Value that sets the ReadOnly state.
        """
        self._read_only = readonly
        self._display_widget._main_label.set_selectable(readonly)

    def on_change(self, data=None):
        return self._has_focus

    def _on_display_notify(self, box, event_type, data):
        """Event called when mouse in/out over display widgets
        """
        self._name_widget.change_color(data["type"])
        self._display_widget.change_color(data["type"])

    def _on_display_click(self, box, event_type, data):
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
            # This way we force on_leave() on all other properties.
            self._on_enter()
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
            self._on_display_notify,
            self._on_display_click)


class _DisplayWidget(Gtk.Box):
    def __init__(self, index, notify_handler, click_handler):
        super(_DisplayWidget, self).__init__()

        self._main_label = Gtk.Label(xalign=0)
        self._main_label.set_single_line_mode(True)
        self._main_label.set_ellipsize(Pango.EllipsizeMode.END)
        self._event_box = Gtk.EventBox()

        self._main_label.set_name('cell')
        self._event_box.add(self._main_label)

        self._event_box.connect(
            "enter-notify-event", notify_handler,
            {"index": index, "type": "in"})
        self._event_box.connect(
            "leave-notify-event", notify_handler,
            {"index": index, "type": "out"})
        self._event_box.connect(
            "button-press-event", click_handler,
            {"index": index})

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
    def __init__(
            self, name,
            id=None,
            default=None,
            description=None,
            force_value=False):
        """A String property class.

        Value is a string or None.

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

    def do_force_value(self, force_value, default):
        if default is not None and force_value:
            self._value = default
        if default is None:
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


class PropertyStringMultiline(PropertyGridProperty):
    class _DialogMultiline(Gtk.Dialog):
        def __init__(self, parent, text):
            super(PropertyStringMultiline._DialogMultiline, self).__init__(
                'Multiline string', parent, 0,
                (
                    Gtk.STOCK_CANCEL,
                    Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_OK, Gtk.ResponseType.OK
                ))

            self.set_modal(True)
            self.set_default_size(300, 300)

            text_view = Gtk.TextView()
            self._buffer = text_view.get_buffer()
            if text is not None:
                self._buffer.set_text(text)

            sw = Gtk.ScrolledWindow()
            sw.set_shadow_type(Gtk.ShadowType.IN)
            sw.add(text_view)

            box = self.get_content_area()
            box.pack_start(sw, True, True, 0)
            self.show_all()

        def get_text(self):
            return self._buffer.get_text(
                self._buffer.get_start_iter(),
                self._buffer.get_end_iter(),
                True)

    def __init__(
            self,
            name,
            parent_window,
            id=None,
            default=None,
            description=None,
            force_value=False):
        """A property that manages multiline string.

        Value is a string or None.

        See :class:`PropertyGridProperty` for parameters.

        Args:
            parent_window (Gtk.Window): The parent window.

        Note:
            *default* parameter must be a valid string object.
        """
        self._window = parent_window

        hbox = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL)

        self._label = Gtk.Label(xalign=0)
        self._label.set_single_line_mode(True)
        self._label.set_ellipsize(Pango.EllipsizeMode.END)
        self._button = Gtk.Button.new_with_label('...')
        self._button.connect("clicked", self._on_click_button)

        hbox.pack_start(self._label, True, True, 0)
        hbox.pack_start(self._button, True, True, 0)

        self._default = default

        super(PropertyStringMultiline, self).__init__(
            name=name,
            value_widget=hbox,
            id=id,
            default=default,
            description=description,
            force_value=force_value)

    def do_force_value(self, force_value, default):
        if default is not None:
            self._label.set_text(default)
            if force_value:
                self._value = default

    def on_change(self, txt):
        if not super(PropertyStringMultiline, self).on_change():
            return False
        self._value = txt
        self._label.set_text(txt)
        self.has_changed()
        return True

    def _on_click_button(self, btn):
        txt = None
        if self._value is not None:
            txt = self._value
        elif self._default is not None:
            txt = self._default
        dialog = PropertyStringMultiline._DialogMultiline(
            self._window, txt)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.on_change(dialog.get_text())
        dialog.destroy()


class PropertyBool(PropertyGridProperty):
    def __init__(
            self, name, id=None,
            default=None, description=None,
            force_value=False):
        """A Boolean property class.

        Value is True, False or None.

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

        if default is True:
            self._check.set_active(True)

    def do_force_value(self, force_value, default):
        if default and force_value:
            self._value = default
        if default is True:
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
    def __init__(
            self, name, id=None,
            default=None, description=None,
            force_value=False):
        """A Color property class.

        Value is a Gdk.RGBA object or None.

        See :class:`PropertyGridProperty` for parameters.

        Note:
            *default* parameter must be a color string that can be
            used to create the Gdk.RGBA object.
            Ex: red, black, #000000, rgb(52,101,164)
        """
        hbox = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL)

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
            self._style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

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

        self._style_provider.load_from_data(
                self._get_css_color_class(self._txt.get_text())
            )
        ctx.add_class('color_label')

    def _on_draw_color_display(self, wg, data):
        wd = wg.get_allocated_width() / 5
        self._color_label.set_size_request(
            wd, self._color_label.get_allocated_height())
        self._display_widget._main_label.set_size_request(
            wd * 4, self._color_label.get_allocated_height())

    def _get_css_color_class(self, color):
        css = '#cell.color_label {background-color: ' + color + ';}'
        return css.encode('utf8')

    def _on_toggled(self, wg):
        self._txt.set_text(self._buttom.get_rgba().to_string())

    def _on_txt_changed(self, wg):
        self.on_change()

    def _get_color_from_str(self, str_color):
        if str_color is None:
            return
        color = Gdk.RGBA()
        if color.parse(str_color):
            return color


class PropertyList(PropertyGridProperty):
    def __init__(
            self, name, list_values,
            id=None, default=None,
            description=None, force_value=False):
        """A List property class.

        Value is a list of two components [id, string] or None.

        See :class:`PropertyGridProperty` for parameters.

        Args:
            list_values (list): List of values to display.
                Its format is as follow:
                ::
                    [
                        [id_0, string_0],
                        [id_1, string_1],
                        [id_n, string_n],
                    ]
                string_n is the string to show in the dropdown menu and
                id_n is its id, id can be None if it is not necessary.

        Note:
            *default* parameter must a dictionary of one element,
            where key can be 'id' or 'string'.
            Ex: {'id': '5'} select the element in the dropdown with id='5'.
            {'string': 'Hello world'} select the element in the dropdown
            with string='Hello world'.
        """
        self._list_values = list_values

        self._combo = Gtk.ComboBoxText()
        for v in list_values:
            self._combo.append(v[0], v[1])

        self._combo.connect('changed', self._on_combo_changed)

        super(PropertyList, self).__init__(
                name=name, value_widget=self._combo,
                id=id, default=default, description=description,
                force_value=force_value)

    def do_force_value(self, force_value, default):
        found = -1
        if default:
            if 'id' in default:
                found = self._set_active(0, default['id'])
            else:
                found = self._set_active(1, default['string'])
        self._value is None
        if force_value:
            if found > -1:
                self._value = self._list_values[found]

    def on_change(self):
        if not super(PropertyList, self).on_change():
            return False
        active = self._combo.get_active()
        if active == -1:
            self._value = None
        else:
            self._value = self._list_values[active]
        self.has_changed()
        return True

    def update_display_value(self):
        if self._value is None:
            super(PropertyList, self).update_display_value()
            return
        self._display_widget._main_label.set_text(
            self._value[1])

    def _set_active(self, index, value):
        found = False
        found_index = 0
        for l in self._list_values:
            if l[index] == value:
                found = True
                break
            found_index += 1
        if found:
            self._combo.set_active(found_index)
        else:
            self._combo.set_active(-1)
            found_index = -1
        return found_index

    def _on_combo_changed(self, wg):
        self.on_change()
