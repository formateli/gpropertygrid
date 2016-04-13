# This file is part of GPropertyGrid project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import sys
import os


DIR = os.path.dirname(os.path.realpath(__file__))
DIR = os.path.normpath(os.path.join(DIR, '../..', 'gpropertygrid'))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))
