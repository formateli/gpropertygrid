# This file is part of GPropertyGrid project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

"GPropertyGrid unittest suite"

import sys
import os
import unittest

DIR = os.path.dirname(os.path.realpath(__file__))
DIR = os.path.normpath(os.path.join(DIR, '../..', 'gpropertygrid'))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))

import propertygrid
import properties

LOADER = unittest.TestLoader()

SUITE = LOADER.loadTestsFromModule(propertygrid)
SUITE.addTests(LOADER.loadTestsFromModule(properties))

RUNNER = unittest.TextTestRunner(verbosity=2)
RESULT = RUNNER.run(SUITE)

