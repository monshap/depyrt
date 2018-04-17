from __future__ import absolute_import
from .peng_tab import PengTab
from .statmech_tab import StatMechTab
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
            (QWidget, "Departure Functions"),
            (QWidget, u"\u2206" + "E's of Gas")
            ]
