from __future__ import absolute_import
from PyQt5.QtGui import *
from PyQt5 import *
from PyQt5.QtWidgets import *
import json
from calculators import statmech_calculator
from .newmol import NewMolecule

""" global positioning params """
cen = QtCore.Qt.AlignHCenter
right = QtCore.Qt.AlignRight
left = QtCore.Qt.AlignLeft
top = QtCore.Qt.AlignTop
bot = QtCore.Qt.AlignBottom


class StatMechTab(QWidget):
    def __init__(self, *args):
        super(StatMechTab, self).__init__(*args)

        # statmech calculator
        self.calculator = None
