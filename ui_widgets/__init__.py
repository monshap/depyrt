from __future__ import absolute_import
from .peng_tab import PengTab
from .statmech_tab import StatMechTab
from .depart_tab import DepartTab
from .diff_tab import DiffETab
try:
    from PyQt4.QtGui import *
    from PyQt4 import *
except:
    from PyQt5.QtGui import *
    from PyQt5 import *
    from PyQt5.QtWidgets import *

#           TabObject, 'Tab Title in UI'
all_tabs = [(PengTab, "PengRob Volume"),
            (StatMechTab, "StatMech Props"),
            (DepartTab, "Departure Functions"),
            (DiffETab, u"\u2206E's Calculator")
            ]
