from __future__ import absolute_import
try:
    from PyQt4.QtGui import *
    from PyQt4 import *
except:
    from PyQt5.QtGui import *
    from PyQt5 import *
    from PyQt5.QtWidgets import *
import os
import sys
import json

""" global positioning params """
cen = QtCore.Qt.AlignHCenter
right = QtCore.Qt.AlignRight
left = QtCore.Qt.AlignLeft
top = QtCore.Qt.AlignTop
bot = QtCore.Qt.AlignBottom


class DepartTab(QWidget):
    def __init__(self, *args):
        super(DepartTab, self).__init__(*args)
        self.setFixedSize(1000, 800)
        self.font = QFont('SansSerif', 14)
        self.setFont(self.font)

        # PengRobinsonEOS object
        self.peng = None

        # statmech ideal potentails object
        self.statmech = None

        # json property data paths
        self.peng_prop_path = 'assets\\data\\mol_props.json'
        self.statmech_prop_path = 'assets\\data\\statmech_props.json'

        # property data objects
        self.peng_props = None
        self.statmech_props = None

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

        self.build_layout()

    def build_layout(self):
        lay = QGridLayout()

        self.title = QLabel('Departure Functions Calculator')
        self.title.setFixedSize(600, 40)
        self.title.setFont(QFont('SansSerif', 18, QtGui.QFont.Bold))

        # molecule selection
        self.mol_lbl = QLabel('Molecule:')
        self.mol = QComboBox()
        self.mol.setToolTip('Please use PengRob Volume & StatMech Props'
                            'to add a new molecule')
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

        # temperature label and input
        self.T_lbl = QLabel('Temperature (K):')
        self.T = QLineEdit(text=str(273.15))
        self.T.setAlignment(cen)

        # pressure label and input
        self.p_lbl = QLabel('Pressure (bar):')
        self.p = QLineEdit(text=str(1.01325))
        self.p.setAlignment(cen)

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

        # constant pressure heat capacity
        self.V = QLabel()

        self.potentials = [('U', '(kJ / mol)'),
                           ('H', '(kJ / mol)'),
                           ('A', '(kJ / mol)'),
                           ('G', '(kJ / mol)'),
                           ('S', '(J / mol K)'),
                           ('V', '(L / mol)')]

        for p in self.potentials:
            attr = getattr(self, p[0])
            attr.setFont(self.font)
            attr.setFixedSize(300, 60)
            attr.setFrameShape(QFrame.Panel)
            attr.setFrameShadow(QFrame.Sunken)
            attr.setAlignment(QtCore.Qt.AlignVCenter)

        row = 0

        # title
        lay.addWidget(self.title, row, 1, 1, 2, cen)
        row += 1

        # molecule combo box
        lay.addWidget(self.mol_lbl, row, 0, right)
        lay.addWidget(self.mol, row, 1, 1, 2)
        row += 1

        lay.addWidget(self.T_lbl, row, 0, right)
        lay.addWidget(self.T, row, 1, 1, 2)
        row += 1

        lay.addWidget(self.p_lbl, row, 0, right)
        lay.addWidget(self.p, row, 1, 1, 2)
        row += 1

        lay.addWidget(QLabel('Results:'), row, 0, right)
        lay.addWidget(self.U, row, 1)
        lay.addWidget(self.H, row, 2)
        row += 1

        lay.addWidget(self.A, row, 1)
        lay.addWidget(self.G, row, 2)
        row += 1

        lay.addWidget(self.S, row, 1)
        lay.addWidget(self.V, row, 2)

        # caclulate departure values when text changes
        self.T.textChanged.connect(self.calculate)
        self.p.textChanged.connect(self.calculate)

        # overall layout formatting
        lay.setVerticalSpacing(20)
        lay.setHorizontalSpacing(40)
        lay.setContentsMargins(5, 30, 100, 50)
        self.setLayout(lay)

    def calculate(self):
        try:
            T = float(self.T.text())
            p = float(self.p.text())
            if T <= 0 or p <= 0:
                raise ValueError('Cannot be negative')
            name = self.mol.currentText()
        except (TypeError, ValueError, OverflowError):
            for p in self.potentials:
                attr = getattr(self, p[0])
                attr.setText('')
                attr.setStyleSheet('background-color: white;')
                attr.setFont(self.font)


if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    ui = DepartTab()
    ui.show()
    sys.exit(app.exec_())
