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


class GUI:
    def __init__(self):
        self.app = QApplication([])
        print(self.app.style)
        # self.app.setStyle('WindowsXP')
        self.w = QTabWidget()
        self.w.setFixedSize(1000, 800)
        self.w.setWindowTitle('Thermo Project')

    def build_peng(self):
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
        self.title = QLabel('Calculate State using Peng Robinson EOS')
        self.title.setFont(QFont('SansSerif', 18, QtGui.QFont.Bold))

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
        self.V_lbl = QLabel('Volume (L / mol)')
        self.V = QLabel()
        self.V.setFrameShape(QFrame.Panel)
        self.V.setFrameShadow(QFrame.Sunken)
        self.V.setFixedSize(300, 50)
        self.V.setAlignment(QtCore.Qt.AlignCenter)

        for w in [self.p_lbl, self.p, self.T_lbl,
                  self.T, self.root_lbl, self.liq,
                  self.vap, self.V_lbl, self.V]:
            w.setFont(font)

        root = QHBoxLayout()
        root.addWidget(self.liq)
        root.addWidget(self.vap)
        root.setAlignment(cen)

        # shrink row with volume label and value
        lay.setRowStretch(4, 0.2)

        lay.addWidget(self.title, 0, 1, 1, 2, topcen)
        lay.addWidget(self.p_lbl, 1, 0, right)
        lay.addWidget(self.p, 1, 1, 1, 2)
        lay.addWidget(self.T_lbl, 2, 0, right)
        lay.addWidget(self.T, 2, 1, 1, 2)
        lay.addWidget(self.root_lbl, 3, 0, right | top)
        lay.addWidget(self.liq, 3, 1, topcen)
        lay.addWidget(self.vap, 3, 2, topcen)
        lay.addWidget(self.V_lbl, 4, 1, 1, 2, topcen)
        lay.addWidget(self.V, 4, 1, 1, 2, botcen)

        lay.setSpacing(50)
        lay.setContentsMargins(5, 50, 150, 50)
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
                val = peng.calc_v(p, T, root)
                val_str = '%.3f L' if 100 > val > 1 else '%.3e L'
                self.V.setText('%.4e' % val)
                self.V.setStyleSheet('background-color: lightgreen;')

        calculate()
        self.p.textChanged.connect(calculate)
        self.T.textChanged.connect(calculate)
        self.vap.toggled.connect(calculate)

        self.w.addTab(tab, 'Peng Robinson EOS')

    def main(self):
        self.build_peng()
        self.w.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    p = GUI()
    p.main()
