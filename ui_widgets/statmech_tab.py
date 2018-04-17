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
import re
from .statmech_molprop import StatMechInfo
from .statmech_newmol import StatMechNewMolecule
try:
    from calculators import statmech_calculator
except:
    from depyrt.calculators import statmech_calculator

""" global positioning params """
cen = QtCore.Qt.AlignHCenter
right = QtCore.Qt.AlignRight
left = QtCore.Qt.AlignLeft
top = QtCore.Qt.AlignTop
bot = QtCore.Qt.AlignBottom


class StatMechTab(QWidget):
    def __init__(self, *args):
        super(StatMechTab, self).__init__(*args)
        self.setFixedSize(1000, 800)
        self.font = QFont('SansSerif', 14)
        self.setFont(self.font)

        # statmech calculator
        self.calculator = None

        self.prop_path = 'assets\\data\\statmech_props.json'

        if not os.path.isfile(self.prop_path):
            self.prop_path = '..\\' + self.prop_path

        with open(self.prop_path, 'r') as f:
            self.statmech_props = json.load(f, encoding='latin1')

        self.build_layout()

    def build_layout(self):
        lay = QGridLayout()

        self.title = QLabel('StatMech Ideal Properties Calculator')
        self.title.setFixedSize(600, 40)
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
        self.mol.addItems(sorted(self.statmech_props.keys()))
        # remember previous index
        self.prev_ind = 0

        for i in range(self.mol.count()):
            self.mol.setItemData(i, cen, QtCore.Qt.TextAlignmentRole)

        # molecule info button
        self.mol_info = QPushButton('Info')
        self.mol_info.setFixedSize(200, 40)

        # buttons to add & remove molecule data
        self.add = QPushButton('Add Molecule')
        self.add.setFixedHeight(40)
        self.rem = QPushButton('Remove Selected')
        self.rem.setFixedHeight(40)

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
        self.Cv = QLabel()

        self.potentials = [('U', '(kJ / mol)'),
                           ('H', '(kJ / mol)'),
                           ('A', '(kJ / mol)'),
                           ('G', '(kJ / mol)'),
                           ('S', '(J / mol K)'),
                           ('Cv', '(J / mol K)')]

        for p in self.potentials:
            attr = getattr(self, p[0])
            attr.setFont(self.font)
            attr.setFixedSize(300, 60)
            attr.setFrameShape(QFrame.Panel)
            attr.setFrameShadow(QFrame.Sunken)
            attr.setAlignment(QtCore.Qt.AlignVCenter)

        row = 0

        lay.setColumnStretch(0, 0.5)

        # title
        lay.addWidget(self.title, row, 1, 1, 2, cen)
        row += 1

        # molecule combo box
        lay.addWidget(self.mol_lbl, row, 0, right)
        lay.addWidget(self.mol, row, 1, 1, 2)
        row += 1

        lay.addWidget(self.mol_info, row, 1, 1, 2, cen)
        row += 1

        lay.addWidget(self.add, row, 1)
        lay.addWidget(self.rem, row, 2)
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
        lay.addWidget(self.Cv, row, 2)

        # button methods
        self.calculate()
        self.mol.currentTextChanged.connect(self.calculate)
        self.mol_info.clicked.connect(self.get_info)
        self.add.clicked.connect(self.add_mol)
        self.rem.clicked.connect(self.remove_mol)
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
            self.calculator = statmech_calculator(self.statmech_props[name])

            # convert pressure (bar) to ideal volume in m^3
            v_id = 8.314 * T / (p * 1E5)
            sol = self.calculator.calc_all(T, v_id)

            # set potentials
            for p in self.potentials:
                val = sol[p[0]]
                if 'kJ' in p[1]:
                    val /= 1000.

                txt = '%s: %.3e %s' % (p[0], val, p[1])

                # attempt to evenly space out label and value
                txt = txt.replace(' ', ' ' * (27 - len(txt)), 1)

                attr = getattr(self, p[0])
                attr.setText(txt)
                attr.setStyleSheet('background-color: lightgreen;')

        except (TypeError, ValueError, OverflowError):
            for p in self.potentials:
                getattr(self, p[0]).setText('')

    def get_info(self):
        name = self.mol.currentText()
        info_ui = StatMechInfo(self.parent(), name, self.statmech_props[name])
        info_ui.exec_()

    def add_mol(self):
        add_ui = StatMechNewMolecule(self.parent(),
                                     self.statmech_props.keys())
        add_ui.exec_()
        if add_ui.passed:
            name = add_ui.name.text()
            typ = 'linear' if add_ui.linear.isChecked() else 'nonlinear'
            info = {'type': typ,
                    'Mw': float(add_ui.mw.text()),
                    'D0': float(add_ui.D0.text()),
                    'W0': float(add_ui.W0.text()),
                    'sigma': float(add_ui.sigma.text())
                    }

            # format vib & rot into proper lists
            for temp in ['theta_v', 'theta_r']:
                text = getattr(add_ui, temp).text().replace(',', ' ').split()
                vals = []
                for t in text:
                    if '(' not in t:
                        vals.append(float(t))
                    else:
                        reg = '^(.+)\(([0-9]+)\)$'
                        v, n = re.findall(reg, t)[0]
                        vals += [float(v)] * int(n)
                info[temp] = sorted(vals)
            self.statmech_props[name] = info
            self.save_mol_props()
            index = self.mol.count()
            self.mol.insertItem(index, name)
            self.mol.setItemData(index,
                                 QtCore.Qt.AlignCenter,
                                 QtCore.Qt.TextAlignmentRole
                                 )
            self.mol.setCurrentText(name)

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
            self.statmech_props.pop(text)
            self.save_mol_props()
            self.mol.setCurrentIndex(0)
            self.mol.removeItem(ind)

    def save_mol_props(self):
        with open(self.prop_path, 'w') as f:
            json.dump(self.statmech_props, f, indent=4, sort_keys=True)

if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    ui = StatMechTab()
    ui.show()
    sys.exit(app.exec_())
