from PyQt5.QtGui import *
from PyQt5 import *
from PyQt5.QtWidgets import *
import sys
import pickle
from peng import PengRobinsonEOS
from newmol import NewMolecule
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('arbitrary')


class GUI:
    def __init__(self):
        self.app = QApplication([])
        self.app.setWindowIcon(QIcon('benzene.png'))

        # self.app.setStyle('WindowsXP')
        self.w = QTabWidget()
        self.w.setFixedSize(1000, 800)
        self.w.setFont(QFont('SansSerif', 15))
        self.w.setWindowTitle('Thermo Project')

        self.prop_path = 'mol_props.pickle'

        with open(self.prop_path, 'r') as f:
            self.mol_props = pickle.load(f)

    def save_mol_props(self):
        with open(self.prop_path, 'w') as f:
            pickle.dump(self.mol_props, f)

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
        # remember previous index
        self.prev_ind = 0

        for i in range(self.mol.count()):
            self.mol.setItemData(i, cen, QtCore.Qt.TextAlignmentRole)

        # buttons to add & remove molecule data
        self.add = QPushButton('Add Molecule')
        self.add.setFixedSize(300, 40)
        self.rem = QPushButton('Remove Selected Molecule')
        self.rem.setFixedSize(300, 40)

        # current molecular data
        self.pc_lbl = QLabel('   Pc')
        self.pc = QLabel()
        self.Tc_lbl = QLabel('Tc')
        self.Tc = QLabel()
        self.omega_lbl = QLabel('Omega')
        self.omega = QLabel()
        for w in [self.pc_lbl, self.pc,
                  self.Tc_lbl, self.Tc,
                  self.omega_lbl, self.omega
                  ]:
            w.setFixedHeight(20)

        # pressure label and input
        self.p_lbl = QLabel('Pressure (bar):')
        self.p = QLineEdit(text=str(1.01325))
        self.p.setAlignment(cen)

        # temperature label and input
        self.T_lbl = QLabel('Temperature (K):')
        self.T = QLineEdit(text=str(273.15))
        self.T.setAlignment(cen)

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

        lay.setRowStretch(row, 0.1)
        lay.addWidget(self.add, row, 1, 1, 2, left)
        lay.addWidget(self.rem, row, 1, 1, 2, right)
        row += 1

        lay.addWidget(self.pc_lbl, row, 1, 1, 2, left)
        lay.addWidget(self.Tc_lbl, row, 1, 1, 2, cen)
        lay.addWidget(self.omega_lbl, row, 1, 1, 2, right)
        row += 1

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
        lay.setSpacing(40)
        lay.setContentsMargins(5, 50, 100, 50)
        tab.setLayout(lay)

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

        @QtCore.pyqtSlot()
        def add_clicked():
            success = self.add_mol()
            if success:
                make_calc()

        @QtCore.pyqtSlot()
        def make_calc():
            molecule = self.mol.currentText()
            props = self.mol_props[molecule]
            self.calculator = PengRobinsonEOS(props['pc'],
                                              props['Tc'],
                                              props['omega'])
            self.pc.setText('%.2f' % props['pc'])
            self.Tc.setText('%.2f' % props['Tc'])
            self.omega.setText('%.3f' % props['omega'])
            self.prev_ind = self.mol.currentIndex()
            calculate()

        make_calc()
        self.add.clicked.connect(add_clicked)
        self.mol.currentTextChanged.connect(make_calc)

        self.p.textChanged.connect(calculate)
        self.T.textChanged.connect(calculate)
        self.vap.toggled.connect(calculate)
        self.rem.clicked.connect(self.remove_mol)

        self.w.addTab(tab, 'Volume Calculator')

    def add_mol(self):
        """open dialog box for user to input new mol props"""
        newm = NewMolecule(self.w)
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
            return True
        else:
            return False

    def remove_mol(self):
        text = self.mol.currentText()
        ind = self.mol.currentIndex()
        if text in ['Ammonia (NH3)', 'Methane (CH4)']:
            QMessageBox(QMessageBox.Information, " ",
                        "Sorry, you aren't allowed to remove %s" % text,
                        QMessageBox.Ok).exec_()
            return
        self.mol_props.pop(text)
        self.save_mol_props()
        self.mol.setCurrentIndex(0)
        self.mol.removeItem(ind)

    def main(self):
        self.build_peng()
        self.w.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    p = GUI()
    p.main()
