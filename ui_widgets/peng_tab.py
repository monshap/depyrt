from __future__ import absolute_import
try:
    from PyQt4.QtGui import *
    from PyQt4 import *
except:
    from PyQt5.QtGui import *
    from PyQt5 import *
    from PyQt5.QtWidgets import *
import json
from calculators import PengRobinsonEOS
from .peng_newmol import PengNewMolecule
from .locked_data import locked_mols

""" global positioning params """
cen = QtCore.Qt.AlignHCenter
right = QtCore.Qt.AlignRight
left = QtCore.Qt.AlignLeft
top = QtCore.Qt.AlignTop
bot = QtCore.Qt.AlignBottom


class PengTab(QWidget):
    def __init__(self, *args):
        super(PengTab, self).__init__(*args)
        self.setFixedSize(1000, 800)
        self.font = QFont('SansSerif', 14)
        self.setFont(self.font)

        # PengRobinsonEOS object
        self.calculator = None

        self.prop_path = 'assets\\data\\mol_props.json'

        self.build_layout()

    def update(self):
        with open(self.prop_path, 'r') as f:
            self.mol_props = json.load(f, encoding='latin1')
        if 'mol' in dir(self):
            curtext = self.mol.currentText()
            self.mol.clear()
            self.mol.addItems(sorted(self.mol_props.keys()))
            for i in range(self.mol.count()):
                self.mol.setItemData(i, cen, QtCore.Qt.TextAlignmentRole)
            if curtext in self.mol_props:
                self.mol.setCurrentText(curtext)

    def build_layout(self):
        lay = QGridLayout()

        # main message
        self.title = QLabel('Peng Robinson Volume Calculator')
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

        # root radio buttons (vapor or liquid)
        self.root_lbl = QLabel('Phase:')
        self.vap = QRadioButton('Vapor')
        self.liq = QRadioButton('Liquid')
        self.vap.setChecked(True)

        # volume label and result label
        self.V_lbl = QLabel('Volume (L / mol):')
        self.V = QLabel()
        self.V.setFont(QFont('SansSerif', 15))
        self.V.setFrameShape(QFrame.Panel)
        self.V.setFrameShadow(QFrame.Sunken)
        self.V.setFixedSize(300, 50)
        self.V.setAlignment(QtCore.Qt.AlignCenter)

        self.Z_lbl = QLabel('Z:')
        self.Z = QLabel()
        self.Z.setFont(QFont('SansSerif', 15))
        self.Z.setFrameShape(QFrame.Panel)
        self.Z.setFrameShadow(QFrame.Sunken)
        self.Z.setFixedSize(300, 50)
        self.Z.setAlignment(QtCore.Qt.AlignCenter)

        root = QHBoxLayout()
        root.addWidget(self.liq)
        root.addWidget(self.vap)
        root.setAlignment(cen)

        lay.setColumnStretch(0, 0.4)

        # use row counter to easily change order of widgets
        row = 0

        lay.addWidget(self.title, row, 1, 1, 2, cen)
        row += 1

        lay.addWidget(self.mol_lbl, row, 0, right)
        lay.addWidget(self.mol, row, 1, 1, 2)
        row += 1

        # lay.setRowStretch(row, 0.1)
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

        lay.addWidget(self.root_lbl, row, 0, right)
        lay.addWidget(self.liq, row, 1, cen)
        lay.addWidget(self.vap, row, 2, cen)
        row += 1

        lay.addWidget(self.V_lbl, row, 0, right)
        lay.addWidget(self.V, row, 1, 1, 2, cen)
        row += 1

        lay.addWidget(self.Z_lbl, row, 0, right)
        lay.addWidget(self.Z, row, 1, 1, 2, cen)

        # overall layout formatting
        lay.setVerticalSpacing(10)
        lay.setHorizontalSpacing(40)
        lay.setContentsMargins(5, 30, 100, 50)

        self.setLayout(lay)

        self.make_calc()
        self.add.clicked.connect(self.add_mol)
        self.mol.currentTextChanged.connect(self.make_calc)

        self.p.textChanged.connect(self.calculate)
        self.T.textChanged.connect(self.calculate)
        self.vap.toggled.connect(self.calculate)
        self.rem.clicked.connect(self.remove_mol)

    def make_calc(self):
        molecule = self.mol.currentText()
        if not molecule:
            return
        props = self.mol_props[molecule]
        self.calculator = PengRobinsonEOS(props['pc'],
                                          props['Tc'],
                                          props['omega'])
        self.pc.setText('%.2f' % props['pc'])
        self.Tc.setText('%.2f' % props['Tc'])
        self.omega.setText('%.3f' % props['omega'])
        self.calculate()

    def calculate(self):
        success = True
        p = 0
        T = 0
        try:
            p = float(self.p.text())
            T = float(self.T.text())
        except:
            success = False
        if p <= 0 or T <= 0:
            success = False
        if not success:
            self.V.setText('')
            self.V.setStyleSheet('background-color: white;')
            self.Z.setText('')
            self.Z.setStyleSheet('background-color: white;')
        else:
            root_inp = 'vapor' if self.vap.isChecked() else 'liquid'

            vol = self.calculator.calc_v(p, T, root_inp)

            vol_str = '%.3f' if 100 > vol > 1 else '%.3e'
            self.V.setText(vol_str % vol)
            self.V.setStyleSheet('background-color: lightgreen;')

            z_str = '%.3f' if self.calculator.z >= 0.1 else '%.3e'
            self.Z.setText(z_str % self.calculator.z)
            self.Z.setStyleSheet('background-color: lightgreen;')
            if self.calculator.phase_guess:
                if self.calculator.phase == 'vapor':
                    self.vap.setChecked(True)
                else:
                    self.liq.setChecked(True)
                self.vap.setDisabled(True)
                self.liq.setDisabled(True)
            else:
                self.vap.setEnabled(True)
                self.liq.setEnabled(True)

    def remove_mol(self):
        text = self.mol.currentText()
        ind = self.mol.currentIndex()
        if text in locked_mols:
            QMessageBox(QMessageBox.Information, " ",
                        "Sorry, you aren't allowed to remove %s" % text,
                        QMessageBox.Ok).exec_()
        else:
            self.mol_props.pop(text)
            self.save_mol_props()
            self.mol.setCurrentIndex(0)
            self.mol.removeItem(ind)

    def add_mol(self):
        """open dialog box for user to input new mol props"""
        newm = PengNewMolecule(self.parent(), self.mol_props.keys())
        newm.exec_()
        if newm.passed:
            name = newm.name.text()
            info = {'pc': float(newm.pc.text()),
                    'Tc': float(newm.Tc.text()),
                    'omega': float(newm.omega.text())}
            self.mol_props[name] = info
            self.save_mol_props()
            index = self.mol.count()
            self.mol.insertItem(index, name)
            self.mol.setItemData(index,
                                 QtCore.Qt.AlignCenter,
                                 QtCore.Qt.TextAlignmentRole
                                 )
            self.mol.setCurrentText(name)

    def save_mol_props(self):
        with open(self.prop_path, 'w') as f:
            json.dump(self.mol_props, f, indent=4, sort_keys=True)
