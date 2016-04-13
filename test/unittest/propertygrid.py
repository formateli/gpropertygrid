# This file is part of GPropertyGrid project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import unittest
from gpropertygrid import PropertyGrid
from gpropertygrid.propertygrid import PropertyGridGroup


class PropertygridTest(unittest.TestCase):
    def testPropertygrid(self):
        pg = PropertyGrid('Property Grid Test')
        self.assertEqual(pg.get_title(), 'Property Grid Test')
        pg.set_title('New Title')
        self.assertEqual(pg.get_title(), 'New Title')

        grp = pg.create_group('Group 1')
        self.assertEqual(True, isinstance(grp, PropertyGridGroup))
