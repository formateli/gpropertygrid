Usage
=====

Following topics covers the usage
of GPropertyGrid and how easy it is
to implement.


Quick example
-------------

::

    from gi.repository import Gtk
    from gpropertygrid import PropertyGrid
    from gpropertygrid.properties import PropertyString

    class PropertyGridExample(Gtk.Window):
        def __init__(self):
            Gtk.Window.__init__(self, title="PropertyGrid Quick Sample")
            self.set_border_width(10)
            self.set_size_request(300,200)
            
            # Create the property grid object
            pg = PropertyGrid('My Porperties')

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

            self.add(pg)

    win = PropertyGridExample()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

In the example above, property grid is created in four steps:

1. Create the :py:class:`PropertyGrid <gpropertygrid.propertygrid.PropertyGrid>` object.
2. Create a :py:class:`PropertyGridGroup <gpropertygrid.propertygrid.PropertyGridGroup>` object.
3. Create property object (:py:class:`PropertyString <gpropertygrid.properties.PropertyString>` in this case).
4. Add the property to the group.

That result in:

.. image:: http://www.formateli.com/software/images/gpropertygrid_qs_1.png
    :alt: GPropertyGrid quick sample 1

We can add another group and add two other properties to them::

    from gpropertygrid.properties import PropertyString, \
        PropertyBool, PropertyColor

::

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

Now it looks like

.. image:: http://www.formateli.com/software/images/gpropertygrid_qs_2.png
    :alt: GPropertyGrid quick sample 1

Let's play with color property, first we select it in the 
grid and then change its color using the color button

.. image:: http://www.formateli.com/software/images/gpropertygrid_qs_3.png
    :alt: GPropertyGrid quick sample 1

.. image:: http://www.formateli.com/software/images/gpropertygrid_qs_4.png
    :alt: GPropertyGrid quick sample 1

.. image:: http://www.formateli.com/software/images/gpropertygrid_qs_5.png
    :alt: GPropertyGrid quick sample 1

Now its new value is showing in the row property

.. image:: http://www.formateli.com/software/images/gpropertygrid_qs_6.png
    :alt: GPropertyGrid quick sample 1


Retrieving values
-----------------

We can retrieve property values in one of two ways:

* Retrieving the property object from grid and get its value::

    # Using the get_property_by_id function
    color = pg.get_property_by_id('color')
    print(color.value)

    # Or using the properties list
    for pr in pg.properties:
        print(pr.value)

* Using the 'changed' signal of the property grid::
    
    def create_pg():
        pg = PropertyGrid('Another Porperties')
        pg.connect("changed", self.on_change_pg)

    def on_change_pg(self, grid, property_):
        text = "Property '{0}' has changed. New value: {1}".format(
                property_.name,
                property_.value)
        print(text)


Properties implemented
----------------------

Currently GPropertyGrid has implemented the following porperties:

* :py:class:`PropertyString <gpropertygrid.properties.PropertyString>`
* :py:class:`PropertyBool <gpropertygrid.properties.PropertyBool>`
* :py:class:`PropertyColor <gpropertygrid.properties.PropertyColor>`
* :py:class:`PropertyList <gpropertygrid.properties.PropertyList>`

We expect to extend this list in new realeases.


Creating a new Property
-----------------------

New properties can be created deriving from 
:py:class:`PropertyGridProperty <gpropertygrid.properties.PropertyGridProperty>` class.

Take care of following when creating a new porperty class:

* The ``do_force_value`` function must overriden. This way we indicate how default value must be treated at creation time.
* The ``on_change`` function must be extended. This way we can tell to property grid that value has changed.
* In special cases ``update_display_value`` function can be overriden if property need a custom display representation.

See :py:class:`PropertyString <gpropertygrid.properties.PropertyString>` class 
as a basic example of how to extend :py:class:`PropertyGridProperty <gpropertygrid.properties.PropertyGridProperty>` class.

