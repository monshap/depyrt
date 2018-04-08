from PyQt5.QtGui import *
from PyQt5 import *
from PyQt5.QtWidgets import *


class NewMolecule(QDialog):
    def __init__(self, parent):
        cl = QtCore.Qt.WindowCloseButtonHint
        super(NewMolecule, self).__init__(parent, cl)
        self.setFixedSize(400, 200)
        self.setWindowTitle('New Molecule')
        self.passed = False

        self.setFont(QFont('SansSerif', 15))
        form = QFormLayout()
        self.name = QLineEdit()
        self.pc = QLineEdit()
        self.Tc = QLineEdit()
        self.omega = QLineEdit()
        self.okay = QPushButton('Save')
        for w in [self.name, self.pc, self.Tc, self.omega]:
            w.setAlignment(QtCore.Qt.AlignCenter)

        form.addRow('Name:', self.name)
        form.addRow('Pc:', self.pc)
        form.addRow('Tc:', self.Tc)
        form.addRow('Omega:', self.omega)
        form.addWidget(self.okay)

        self.okay.clicked.connect(self.check_mol)

        self.setLayout(form)

    def check_mol(self):
        self.passed = False
        if self.name.text():
            for n in [i.text() for i in [self.pc, self.Tc, self.omega]]:
                try:
                    n = float(n)
                    if n <= 0:
                        break
                except:
                    break
            else:
                self.passed = True
                self.close()
