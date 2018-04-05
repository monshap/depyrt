from PyQt5.QtGui import *
from PyQt5 import *
from PyQt5.QtWidgets import *
import sys
from peng import PengRobinsonEOS

# Ammonia (NH_3) props
pc = 113.53  # bar
Tc = 405.4   # K
omega = 0.257

peng = PengRobinsonEOS(pc, Tc, omega)

# standard pressure and temperature
stp_p = 1.01325  # bar
stp_T = 273.15   # K
stp_v = peng.calc_v(stp_p, stp_T, 'vapor')


class PengUI:
    def __init__(self):
        self.app = QApplication([])
        self.w = QTabWidget()
        self.w.setFixedSize(1000, 800)
        self.w.setWindowTitle('Thermo Project')

    def build_peng(self):
        tab = QWidget()
        lay = QGridLayout()

        # font = QFont('SansSerif', 14)
        cen = QtCore.Qt.AlignCenter
        right = QtCore.Qt.AlignRight

        self.p_lbl = QLabel('Pressure (bar):')
        self.p = QLineEdit(text=str(stp_p))
        self.p.setAlignment(cen)

        self.T_lbl = QLabel('Temperature (K):')
        self.T = QLineEdit(text=str(stp_T))
        self.T.setAlignment(cen)

        self.root_lbl = QLabel('Phase:')
        self.liq = QRadioButton('Liquid')
        self.liq.setFixedWidth(140)
        self.vap = QRadioButton('Vapor')
        self.vap.setFixedWidth(100)
        self.vap.setChecked(True)
        self.V_lbl = QLabel('Volume (L / mol):')
        self.V = QLabel(text='%.3e L' % stp_v)
        self.V.setAlignment(cen)

        for w in [self.p_lbl, self.p, self.T_lbl,
                  self.T, self.root_lbl, self.liq,
                  self.vap, self.V_lbl, self.V]:
            pass  # w.setFont(font)

        root = QHBoxLayout()
        root.addWidget(self.liq)
        root.addWidget(self.vap)
        root.setAlignment(cen)

        lay.setColumnStretch(1, 2)
        lay.addWidget(self.p_lbl, 0, 0, right)
        lay.addWidget(self.p, 0, 1)
        lay.addWidget(self.T_lbl, 1, 0, right)
        lay.addWidget(self.T, 1, 1)
        lay.addWidget(self.root_lbl, 2, 0, right)
        lay.addLayout(root, 2, 1)
        lay.addWidget(self.V_lbl, 3, 0, right)
        lay.addWidget(self.V, 3, 1)

        lay.setVerticalSpacing(50)
        lay.setContentsMargins(20, 100, 20, 350)
        tab.setLayout(lay)

        @QtCore.pyqtSlot()
        def calculate():
            try:
                p = float(self.p.text())
                T = float(self.T.text())
            except:
                self.V.setText('')
            else:
                if p <= 0 or T <= 0:
                    self.V.setText('')
                else:
                    root = 'vapor' if self.vap.isChecked() else 'liquid'
                    self.V.setText('%.3e L' % (peng.calc_v(p, T, root)))

        self.p.textChanged.connect(calculate)
        self.T.textChanged.connect(calculate)
        self.vap.toggled.connect(calculate)

        self.w.addTab(tab, 'Peng Robinson EOS')

    def main(self):
        self.build_peng()
        self.w.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    p = PengUI()
    p.main()
