from PyQt5.QtGui import *
from PyQt5 import *
from PyQt5.QtWidgets import *
import sys
import pickle
from peng import PengRobinsonEOS

# Ammonia (NH_3) props
pc = 113.53  # bar
Tc = 405.4   # K
omega = 0.257

# standard pressure and temperature
stp_p = 1.01325  # bar
stp_T = 273.15   # K


class GUI:
    def __init__(self):
        self.app = QApplication([])
        # self.app.setStyle('WindowsXP')
        self.w = QTabWidget()
        self.w.setFixedSize(1000, 800)
        self.w.setWindowTitle('Thermo Project')

        with open('mol_props.pickle', 'r') as f:
            self.mol_props = pickle.load(f)

    def build_peng(self):
        # PengRobinsonEOS object
        self.calculator = None

        tab = QWidget()
        lay = QGridLayout()

        font = QFont('SansSerif', 15)
        cen = QtCore.Qt.AlignHCenter
        right = QtCore.Qt.AlignRight
        left = QtCore.Qt.AlignLeft
        top = QtCore.Qt.AlignTop
        bot = QtCore.Qt.AlignBottom
        topcen = top | cen
        botcen = bot | cen

        # main message
        self.title = QLabel('Peng Robinson Volume Calculator')
        self.title.setFont(QFont('SansSerif', 18, QtGui.QFont.Bold))

        # molecule selection
        self.mol_lbl = QLabel('Molecule:')
        self.mol = QComboBox()
        self.mol.setEditable(True)
        ledit = self.mol.lineEdit()
        ledit.setAlignment(cen)
        ledit.setReadOnly(True)
        self.mol.addItems(sorted(self.mol_props.keys()))

        for i in range(self.mol.count()):
            self.mol.setItemData(i, cen, QtCore.Qt.TextAlignmentRole)

        # current molecular data
        self.pc_lbl = QLabel('   Pc')
        self.pc = QLabel()
        self.Tc_lbl = QLabel('Tc')
        self.Tc = QLabel()
        self.omega_lbl = QLabel('Omega')
        self.omega = QLabel()

        # pressure label and input
        self.p_lbl = QLabel('Pressure (bar):')
        self.p = QLineEdit(text=str(stp_p))
        self.p.setAlignment(cen)

        # temperature label and input
        self.T_lbl = QLabel('Temperature (K):')
        self.T = QLineEdit(text=str(stp_T))
        self.T.setAlignment(cen)

        # root radio buttons (vapor or liquid)
        self.root_lbl = QLabel('Phase:')
        self.vap = QRadioButton('Vapor')
        self.liq = QRadioButton('Liquid')
        self.vap.setChecked(True)

        # volume label and result label
        self.V_lbl = QLabel('Volume (L / mol):')
        self.V = QLabel()
        self.V.setFrameShape(QFrame.Panel)
        self.V.setFrameShadow(QFrame.Sunken)
        self.V.setFixedSize(300, 50)
        self.V.setAlignment(QtCore.Qt.AlignCenter)

        for w in [self.mol_lbl, self.mol, self.pc_lbl,
                  self.pc, self.Tc_lbl, self.Tc,
                  self.omega_lbl, self.omega, self.p_lbl, self.p, self.T_lbl,
                  self.T, self.root_lbl, self.liq,
                  self.vap, self.V_lbl, self.V]:
            w.setFont(font)

        root = QHBoxLayout()
        root.addWidget(self.liq)
        root.addWidget(self.vap)
        root.setAlignment(cen)

        # use row counter to easily change order of widgets
        row = 0

        lay.addWidget(self.title, row, 1, 1, 2, topcen)
        row += 1

        lay.addWidget(self.mol_lbl, row, 0, right)
        lay.addWidget(self.mol, row, 1, 1, 2)
        row += 1

        lay.setRowStretch(row, 0.01)
        lay.addWidget(self.pc_lbl, row, 1, 1, 2, left)
        lay.addWidget(self.Tc_lbl, row, 1, 1, 2, cen)
        lay.addWidget(self.omega_lbl, row, 1, 1, 2, right)
        row += 1

        lay.setRowStretch(row, 0.01)
        lay.addWidget(self.pc, row, 1, 1, 2, left)
        lay.addWidget(self.Tc, row, 1, 1, 2, cen)
        lay.addWidget(self.omega, row, 1, 1, 2, right)
        row += 1

        lay.addWidget(self.p_lbl, row, 0, right)
        lay.addWidget(self.p, row, 1, 1, 2)
        row += 1

        lay.addWidget(self.T_lbl, row, 0, right)
        lay.addWidget(self.T, row, 1, 1, 2)
        row += 1

        lay.addWidget(self.root_lbl, row, 0, right | top)
        lay.addWidget(self.liq, row, 1, topcen)
        lay.addWidget(self.vap, row, 2, topcen)
        row += 1

        lay.addWidget(self.V_lbl, row, 0, right)
        lay.addWidget(self.V, row, 1, 1, 2, cen)

        # overall layout formatting
        lay.setSpacing(50)
        lay.setContentsMargins(5, 50, 100, 50)
        tab.setLayout(lay)

        @QtCore.pyqtSlot()
        def make_calc():
            molecule = self.mol.currentText()
            if molecule:
                props = self.mol_props[molecule]
                self.calculator = PengRobinsonEOS(props['pc'],
                                                  props['Tc'],
                                                  props['omega'])
                self.pc.setText('%.2f' % props['pc'])
                self.Tc.setText('%.2f' % props['Tc'])
                self.omega.setText('%.3f' % props['omega'])

                calculate()

        @QtCore.pyqtSlot()
        def calculate():
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
            else:
                root = 'vapor' if self.vap.isChecked() else 'liquid'
                val = self.calculator.calc_v(p, T, root)
                val_str = '%.3f L' if 100 > val > 1 else '%.3e L'
                self.V.setText(val_str % val)
                self.V.setStyleSheet('background-color: lightgreen;')

        make_calc()
        self.mol.currentTextChanged.connect(make_calc)

        calculate()
        self.p.textChanged.connect(calculate)
        self.T.textChanged.connect(calculate)
        self.vap.toggled.connect(calculate)

        self.w.addTab(tab, 'Peng Robinson NEW')

    def main(self):
        self.build_peng()
        self.w.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    p = GUI()
    p.main()
