Changelog
=========

1.1 (2016-04-13)
----------------

New
~~~

- Improvements in code documentation. [formateli]

- New property PropertyStringMultiline. [formateli]

Changes
~~~~~~~

- Property value is a list object. [formateli]

  Now property value is a list, usually its main value is in first index
  (value[0]). This way property classes improve their extensibility.

- Function 'do_force_value' name changed to 'init_value'. close #6.
  [formateli]

Fix
~~~

- PropertyList documentation weird line break. Fix #4. [formateli]


1.0 (2016-02-24)
----------------

New
~~~

- Unitest suite implemented. [formateli]

- Pep8 enforcement. [formateli]

- Properties:

  PropertyString, PropertyBool, PropertyColor and PropertyList

