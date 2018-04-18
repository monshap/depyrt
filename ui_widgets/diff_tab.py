from __future__ import absolute_import
try:
    from PyQt4.QtGui import *
    from PyQt4 import *
except:
    from PyQt5.QtGui import *
    from PyQt5 import *
    from PyQt5.QtWidgets import *
from calculators import Departure
import os
import sys
import json

""" global positioning params """
cen = QtCore.Qt.AlignHCenter
right = QtCore.Qt.AlignRight
left = QtCore.Qt.AlignLeft
top = QtCore.Qt.AlignTop
bot = QtCore.Qt.AlignBottom


class DiffETab(QWidget):
    def __init__(self, *args):
        super(DepartTab, self).__init__(*args)
        self.setFixedSize(1000, 800)
        self.font = QFont('SansSerif', 14)
        self.setFont(self.font)

        # Departure object
        self.depart = None

        # statmech ideal potentails object
        self.statmech = None

        # json property data paths
        self.peng_prop_path = 'assets\\data\\mol_props.json'
        self.statmech_prop_path = 'assets\\data\\statmech_props.json'

        # property data objects
        self.peng_props = None
        self.statmech_props = None

        # build combobox here to support molecule update
        self.mol = QComboBox()

        self.update()
        self.build_layout()

    def update(self):
        # read in both json datasets
        paths = ['peng', 'statmech']
        for p in paths:
            pathname = '%s_prop_path' % p
            dataname = '%s_props' % p
            at = getattr(self, pathname)
            if not os.path.isfile(at):
                at = '..\\' + at
                setattr(self, pathname, at)
            with open(at, 'r') as f:
                setattr(self, dataname, json.load(f, encoding='latin1'))

        # molecules used must have statmech and peng properties
        self.mol_keys = []
        for n in self.peng_props:
            if n in self.statmech_props:
                self.mol_keys.append(n)
        self.mol.

    def build_layout(self):
        lay = QGridLayout()

        self.title = QLabel('Departure Functions Calculator')
        self.title.setFixedSize(600, 40)
        self.title.setFont(QFont('SansSerif', 18, QtGui.QFont.Bold))

        # molecule selection
        self.mol_lbl = QLabel('Molecule:')
        self.mol = QComboBox()
        self.mol.setToolTip('Please use add molecule using other tabs\n'
                            '(both PengRob & StatMech info needed')
        self.mol.setFixedHeight(40)
        self.mol.setEditable(True)
        ledit = self.mol.lineEdit()
        ledit.setAlignment(cen)
        ledit.setReadOnly(True)
        self.mol.addItems(sorted(self.mol_keys))
        # remember previous index
        self.prev_ind = 0

        for i in range(self.mol.count()):
            self.mol.setItemData(i, cen, QtCore.Qt.TextAlignmentRole)
