# This file is part of GPropertyGrid project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

"GPropertyGrid unittest suite"

import unittest
import load_module
import propertygrid
import properties


LOADER = unittest.TestLoader()

SUITE = LOADER.loadTestsFromModule(propertygrid)
SUITE.addTests(LOADER.loadTestsFromModule(properties))

RUNNER = unittest.TextTestRunner(verbosity=2)
RESULT = RUNNER.run(SUITE)
