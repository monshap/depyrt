from __future__ import absolute_import
try:
    from PyQt4.QtGui import *
    from PyQt4 import *
except:
    from PyQt5.QtGui import *
    from PyQt5 import *
    from PyQt5.QtWidgets import *
from calculators import Departure, statmech_calculator
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
            curtext = self.mol.currentText()
            self.mol.clear()
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

        # state one
        self.pT1_lbl = QLabel('Initial State:')
        self.p_lbl = QLabel('Pressure (bar)')
        self.p_lbl.setFixedHeight(20)
        self.p_lbl.setFont(QFont('SansSerif', 14, QtGui.QFont.Bold))

        self.T_lbl = QLabel('Temperature (K)')
        self.T_lbl.setFixedHeight(20)
        self.T_lbl.setFont(QFont('SansSerif', 14, QtGui.QFont.Bold))

        self.T1 = QLineEdit('200')
        self.T1.setFixedWidth(300)

        self.p1 = QLineEdit('0.06')
        self.p1.setFixedWidth(300)

        self.vap1 = QRadioButton('Vapor')
        self.liq1 = QRadioButton('Liquid')
        self.liq1.setChecked(True)

        # state two
        self.pT2_lbl = QLabel('Final State:')
        self.p2_lbl = QLabel('Pressure (bar)')
        self.p2_lbl.setFixedHeight(20)
        self.p2_lbl.setFont(QFont('SansSerif', 14, QtGui.QFont.Bold))

        self.T2_lbl = QLabel('Temperature (K)')
        self.T2_lbl.setFixedHeight(20)
        self.T2_lbl.setFont(QFont('SansSerif', 14, QtGui.QFont.Bold))

        self.T2 = QLineEdit('450')
        self.T2.setFixedWidth(300)

        self.p2 = QLineEdit('2.09')
        self.p2.setFixedWidth(300)

        for w in ['p', 'T']:
            getattr(self, '%s1' % w).setAlignment(cen)
            getattr(self, '%s2' % w).setAlignment(cen)

        self.vap2 = QRadioButton('Vapor')
        self.liq2 = QRadioButton('Liquid')
        self.vap2.setChecked(True)

        root1 = QButtonGroup(self)
        root1.addButton(self.liq1)
        root1.addButton(self.vap1)
        root1.setExclusive(True)

        root2 = QButtonGroup(self)
        root2.addButton(self.liq2)
        root2.addButton(self.vap2)
        root2.setExclusive(True)

        """ Potentials """
        # internal energy
        self.U = QLabel()

        # enthalpy
        self.H = QLabel()

        # helmholtz
        self.A = QLabel()

        # gibbs
        self.G = QLabel()

        # entropy
        self.S = QLabel()

        # volume
        self.V = QLabel()

        self.potentials = [('U', '(kJ / mol)'),
                           ('H', '(kJ / mol)'),
                           ('A', '(kJ / mol)'),
                           ('G', '(kJ / mol)'),
                           ('S', '(J / mol K)')]

        for p in self.potentials:
            attr = getattr(self, p[0])
            attr.setAlignment(QtCore.Qt.AlignCenter)
            attr.setFont(self.font)
            attr.setFixedSize(300, 60)
            attr.setFrameShape(QFrame.Panel)
            attr.setFrameShadow(QFrame.Sunken)

        self.make_calc()
        self.mol.currentTextChanged.connect(self.make_calc)
        self.T1.textChanged.connect(self.calculate)
        self.p1.textChanged.connect(self.calculate)
        self.T2.textChanged.connect(self.calculate)
        self.p2.textChanged.connect(self.calculate)
        self.vap1.toggled.connect(self.calculate)
        self.vap2.toggled.connect(self.calculate)

        row = 0

        # title
        lay.addWidget(self.title, row, 1, 1, 2, cen)
        row += 1

        # molecule combo box
        lay.addWidget(self.mol_lbl, row, 0, right)
        lay.addWidget(self.mol, row, 1, 1, 2)
        row += 1

        # initial state
        lay.addWidget(self.T_lbl, row, 1, cen)
        lay.addWidget(self.p_lbl, row, 2, cen)
        row += 1

        lay.addWidget(self.pT1_lbl, row, 0, right)
        lay.addWidget(self.T1, row, 1, cen)
        lay.addWidget(self.p1, row, 2, cen)
        row += 1

        lay.addWidget(self.liq1, row, 1, cen)
        lay.addWidget(self.vap1, row, 2, cen)
        row += 1

        lay.addWidget(self.T2_lbl, row, 1, cen)
        lay.addWidget(self.p2_lbl, row, 2, cen)
        row += 1

        lay.addWidget(self.pT2_lbl, row, 0, right)
        lay.addWidget(self.T2, row, 1, cen)
        lay.addWidget(self.p2, row, 2, cen)
        row += 1

        lay.addWidget(self.liq2, row, 1, cen)
        lay.addWidget(self.vap2, row, 2, cen)
        row += 1

        lay.addWidget(QLabel('Results:'), row, 0, right)
        lay.addWidget(self.U, row, 1, cen)
        lay.addWidget(self.H, row, 2, cen)
        row += 1

        lay.addWidget(self.A, row, 1, cen)
        lay.addWidget(self.G, row, 2, cen)
        row += 1

        lay.addWidget(self.S, row, 1, 1, 2, cen)

        # overall layout formatting
        lay.setVerticalSpacing(5)
        # lay.setHorizontalSpacing(10)
        lay.setColumnMinimumWidth(1, 350)
        lay.setColumnMinimumWidth(2, 350)
        lay.setContentsMargins(20, 50, 100, 50)
        self.setLayout(lay)

    def make_calc(self):
        molecule = self.mol.currentText()
        if not molecule:
            return
        peng = self.peng_props[molecule]
        self.depart = Departure(peng['pc'],
                                peng['Tc'],
                                peng['omega'])

        stat = self.statmech_props[molecule]
        self.statmech = statmech_calculator(stat)
        self.calculate()

    def calculate(self):
        try:
            T1 = float(self.T1.text())
            p1 = float(self.p1.text())

            T2 = float(self.T2.text())
            p2 = float(self.p2.text())

            if T1 <= 0 or p1 <= 0 or T2 <= 0 or p2 <= 0:
                raise ValueError("Must be greater than 0")

            root1 = 'vapor' if self.vap1.isChecked() else 'liquid'
            root2 = 'vapor' if self.vap2.isChecked() else 'liquid'

            # calculate ideal states
            v_id1 = 8.314 * T1 / (p1 * 1E5)
            id_1 = self.statmech.calc_all(T1, v_id1)

            v_id2 = 8.314 * T2 / (p2 * 1E5)
            id_2 = self.statmech.calc_all(T2, v_id2)

            # calculate departures
            dep1 = self.depart.get_all(p1, T1, root1)
            dep2 = self.depart.get_all(p2, T2, root2)

            # calculate change
            sol = {i[0]: dep1[i[0]] - dep2[i[0]] + id_2[i[0]] - id_1[i[0]]
                   for i in self.potentials}

            for p in self.potentials:
                val = sol[p[0]]
                if 'kJ' in p[1]:
                    val /= 1000.

                txt = u"\u2206%s: %.3f %s" % (p[0], val, p[1])

                attr = getattr(self, p[0])
                attr.setText(txt)
                attr.setStyleSheet('background-color: lightgreen;')
                attr.setFont(self.font)

        except Exception as e:
            print(e)
            for p in self.potentials:
                attr = getattr(self, p[0])
                attr.setText('')
                attr.setStyleSheet('background-color: white;')
                attr.setFont(self.font)
