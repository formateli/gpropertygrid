# This file is part of GPropertyGrid project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

"""
A simple python gtk 3 property grid widget.
"""

from gi.repository import Gtk, Gdk
from . propertygrid import PropertyGrid

PROJECT_NAME = "GPropertyGrid"
AUTHOR = "Fredy Ramirez"
COPYRIGHT = "2014-2016, Fredy Ramirez - http://www.formateli.com"
VERSION = "1.0.0"

def get_rgb_string(rgb):
    result = "rgb({0},{1},{2})".format(int(rgb.red * 255),
        int(rgb.green * 255), 
        int(rgb.blue * 255))
    return result

wg = Gtk.Window()
ctx = wg.get_style_context()
bg_color = get_rgb_string(ctx.get_background_color(Gtk.StateFlags.NORMAL))
fg_color = get_rgb_string(ctx.get_color(Gtk.StateFlags.NORMAL))
bg_selected = get_rgb_string(ctx.get_background_color(Gtk.StateFlags.SELECTED))
fg_selected = get_rgb_string(ctx.get_color(Gtk.StateFlags.SELECTED))
wg.destroy()

define_color = "@define-color pg_bg_color {0};\n".format(bg_color)
define_color = "{0}@define-color pg_fg_color {1};\n".format(define_color, fg_color)
define_color = "{0}@define-color pg_selected_bg_color {1};\n".format(define_color, bg_selected)
define_color = "{0}@define-color pg_selected_fg_color {1};".format(define_color, fg_selected)

css = """
#property_grid_header {
    background-color: @pg_fg_color;
    color: @pg_bg_color;
    font-weight: bold;
    padding-top: 2px;
    padding-left: 2px;
    padding-bottom: 2px;
}

#group_header {
    background-color: @pg_fg_color;
}

#group_header_label {
    background-color: @pg_fg_color;
    color: @pg_bg_color;
    font-weight: bold;
    font-size: small;
    padding-top: 2px;
    padding-left: 2px;
    padding-bottom: 2px;
}

#cell {
    background-color: @pg_bg_color;
    color: @pg_fg_color;
    font-weight: normal;
    font-size: small;
    padding-top: 2px;
    padding-left: 2px;
    padding-bottom: 2px;
    border-style: solid;    
}

#cell.cell_in {
    background-color: @pg_selected_bg_color;
    color: @pg_selected_fg_color;    
}

#description_name {
    font-weight: bold;
    font-size: small;
}

"""

css = define_color + css

style_provider = Gtk.CssProvider ()
style_provider.load_from_data (css.encode('utf8'))
Gtk.StyleContext.add_provider_for_screen (Gdk.Screen.get_default(),
                    style_provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

