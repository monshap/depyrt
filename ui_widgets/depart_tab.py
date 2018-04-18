from __future__ import absolute_import
try:
    from PyQt4.QtGui import *
    from PyQt4 import *
except:
    from PyQt5.QtGui import *
    from PyQt5 import *
    from PyQt5.QtWidgets import *
from calculators import Departure
from .peng_newmol import PengNewMolecule
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

        # Departure object
        self.depart = None

        # json property data path
        self.peng_prop_path = 'assets\\data\\mol_props.json'
        self.peng_props = None

        self.update()
        self.build_layout()

    def update(self):
        with open(self.peng_prop_path, 'r') as f:
            self.peng_props = json.load(f, encoding='latin1')
        if 'mol' in dir(self):
            curtext = self.mol.currentText()
            self.mol.clear()
            self.mol.addItems(sorted(self.peng_props.keys()))
            for i in range(self.mol.count()):
                self.mol.setItemData(i, cen, QtCore.Qt.TextAlignmentRole)
            if curtext in self.peng_props:
                self.mol.setCurrentText(curtext)

    def build_layout(self):
        lay = QGridLayout()

        self.title = QLabel('Departure Functions Calculator')
        self.title.setFixedSize(650, 40)
        self.title.setFont(QFont('SansSerif', 18, QtGui.QFont.Bold))
        self.title.setAlignment(QtCore.Qt.AlignCenter)

        # molecule selection
        self.mol_lbl = QLabel('Molecule:')
        self.mol = QComboBox()
        self.mol.setFixedHeight(40)
        self.mol.setEditable(True)
        ledit = self.mol.lineEdit()
        ledit.setAlignment(cen)
        ledit.setReadOnly(True)
        self.update()

        # buttons to add & remove molecule data
        self.add = QPushButton('Add Molecule')
        self.add.setFixedHeight(40)
        self.rem = QPushButton('Remove Selected')
        self.rem.setFixedHeight(40)

        # current molecular data
        self.Tc_lbl = QLabel('Tc (K)')
        self.Tc = QLabel()
        self.pc_lbl = QLabel('Pc (bar)')
        self.pc = QLabel()
        self.omega_lbl = QLabel(u'\u03c9   ')
        self.omega = QLabel()
        for w in [self.pc_lbl, self.pc,
                  self.Tc_lbl, self.Tc,
                  self.omega_lbl, self.omega
                  ]:
            w.setFixedHeight(30)

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

        lay.setRowStretch(row, 0.1)
        lay.addWidget(self.add, row, 1)
        lay.addWidget(self.rem, row, 2)
        row += 1

        lay.addWidget(self.Tc_lbl, row, 1, 1, 2, left)
        lay.addWidget(self.pc_lbl, row, 1, 1, 2, cen)
        lay.addWidget(self.omega_lbl, row, 1, 1, 2, right)
        row += 1

        lay.addWidget(self.Tc, row, 1, 1, 2, left)
        lay.addWidget(self.pc, row, 1, 1, 2, cen)
        lay.addWidget(self.omega, row, 1, 1, 2, right)
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

        self.mol.currentTextChanged.connect(self.make_calc)

        # caclulate departure values when text changes
        self.T.textChanged.connect(self.calculate)
        self.p.textChanged.connect(self.calculate)

        # add / remove molecule info
        self.add.clicked.connect(self.add_mol)
        self.rem.clicked.connect(self.remove_mol)

        # overall layout formatting
        lay.setVerticalSpacing(20)
        lay.setHorizontalSpacing(40)
        lay.setContentsMargins(5, 30, 100, 50)
        self.setLayout(lay)

    def make_calc(self):
        molecule = self.mol.currentText()
        if not molecule:
            return
        props = self.peng_props[molecule]
        self.depart = Departure(props['pc'],
                                props['Tc'],
                                props['omega'])
        self.pc.setText('%.2f' % props['pc'])
        self.Tc.setText('%.2f' % props['Tc'])
        self.omega.setText('%.3f' % props['omega'])
        self.calculate()

    def calculate(self):
        try:
            p = float(self.p.text())
            T = float(self.T.text())
            if T <= 0 or p <= 0:
                raise ValueError('Cannot be negative')
            sol = self.depart.get_all(p, T)

            # set potentials
            for p in self.potentials:
                val = sol[p[0]]
                if 'kJ' in p[1]:
                    val /= 1000.

                txt = u"\u2206%s': %.3e %s" % (p[0], val, p[1])

                # attempt to evenly space out label and value
                txt = txt.replace(' ', ' ' * (28 - len(txt)), 1)

                attr = getattr(self, p[0])
                attr.setText(txt)
                attr.setStyleSheet('background-color: lightgreen;')

        except (TypeError, ValueError, OverflowError):
            for p in self.potentials:
                attr = getattr(self, p[0])
                attr.setText('')
                attr.setStyleSheet('background-color: white;')
                attr.setFont(self.font)

    def remove_mol(self):
        text = self.mol.currentText()
        ind = self.mol.currentIndex()
        if text in ['Ammonia (NH3)',
                    'Carbon Dioxide (CO2)',
                    'Chloromethane (CH3Cl)']:
            QMessageBox(QMessageBox.Information, " ",
                        "Sorry, you aren't allowed to remove %s" % text,
                        QMessageBox.Ok).exec_()
        else:
            self.peng_props.pop(text)
            self.save_mol_props()
            self.mol.setCurrentIndex(0)
            self.mol.removeItem(ind)

    def add_mol(self):
        """open dialog box for user to input new mol props"""
        newm = PengNewMolecule(self.parent(), self.peng_props.keys())
        newm.exec_()
        if newm.passed:
            name = newm.name.text()
            info = {'pc': float(newm.pc.text()),
                    'Tc': float(newm.Tc.text()),
                    'omega': float(newm.omega.text())}
            self.peng_props[name] = info
            self.save_mol_props()
            index = self.mol.count()
            self.mol.insertItem(index, name)
            self.mol.setItemData(index,
                                 QtCore.Qt.AlignCenter,
                                 QtCore.Qt.TextAlignmentRole
                                 )
            self.mol.setCurrentText(name)

    def save_mol_props(self):
        with open(self.peng_prop_path, 'w') as f:
            json.dump(self.peng_props, f, indent=4, sort_keys=True)

if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    ui = DepartTab()
    ui.show()
    sys.exit(app.exec_())
