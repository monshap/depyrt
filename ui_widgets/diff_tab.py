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
        super(DiffETab, self).__init__(*args)
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
        if 'mol' in dir(self):
            self.mol.clear()
            curtext = self.mol.currentText()
            self.mol.addItems(sorted(self.mol_keys))
            for i in range(self.mol.count()):
                self.mol.setItemData(i, cen, QtCore.Qt.TextAlignmentRole)
            if curtext in self.mol_keys:
                self.mol.setCurrentText(curtext)

    def build_layout(self):
        lay = QGridLayout()

        self.title = QLabel(u"\u2206E Calculator: Real & Ideal")
        self.title.setFixedSize(650, 40)
        self.title.setFont(QFont('SansSerif', 18, QtGui.QFont.Bold))
        self.title.setAlignment(QtCore.Qt.AlignCenter)

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
        self.update()

        row = 0

        # title
        lay.addWidget(self.title, row, 1, 1, 2, cen)
        row += 1

        # molecule combo box
        lay.addWidget(self.mol_lbl, row, 0, right)
        lay.addWidget(self.mol, row, 1, 1, 2)
        row += 1

        # overall layout formatting
        lay.setVerticalSpacing(20)
        lay.setHorizontalSpacing(40)
        lay.setContentsMargins(5, 30, 100, 50)
        self.setLayout(lay)
