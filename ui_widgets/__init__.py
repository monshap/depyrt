from __future__ import absolute_import
from .peng_tab import PengTab
from .statmech_tab import StatMechTab
from PyQt5.QtWidgets import QWidget

#           TabObject, 'Tab Title in UI'
all_tabs = [(PengTab, "PengRob Volume"),
            (StatMechTab, "StatMech Props"),
            (QWidget, "Departure Functions"),
            (QWidget, u"\u2206" + "E's of Real Gas")
            ]
