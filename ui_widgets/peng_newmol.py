try:
    from PyQt4.QtGui import *
    from PyQt4 import *
except:
    from PyQt5.QtGui import *
    from PyQt5 import *
    from PyQt5.QtWidgets import *


class NewMolecule(QDialog):
    def __init__(self, parent, taken_names):
        cl = QtCore.Qt.WindowCloseButtonHint
        super(NewMolecule, self).__init__(parent, cl)
        self.setFixedSize(400, 200)
        self.setWindowTitle('New Molecule')

        self.taken_names = taken_names
        self.passed = False

        self.font = QFont('SansSerif', 15)
        self.setFont(self.font)
        form = QFormLayout()

        self.name = QLineEdit()
        self.name.passed = False

        self.Tc = QLineEdit()
        self.Tc.passed = False

        self.pc = QLineEdit()
        self.pc.passed = False

        self.omega = QLineEdit()
        self.omega.passed = False

        self.okay = QPushButton('Save')

        self.line_edits = [self.name, self.Tc, self.pc, self.omega]

        for w in self.line_edits:
            w.setAlignment(QtCore.Qt.AlignCenter)

        form.addRow('Name:', self.name)
        form.addRow('Tc:', self.Tc)
        form.addRow('Pc:', self.pc)
        form.addRow(u'\u03c9:', self.omega)
        form.addWidget(self.okay)

        self.name.textChanged.connect(self.check_name)
        self.Tc.textEdited.connect(lambda: self.check_posnum(self.Tc))
        self.pc.textEdited.connect(lambda: self.check_posnum(self.pc, False))
        self.omega.textEdited.connect(lambda: self.check_posnum(self.omega))
        self.okay.clicked.connect(self.check_all)

        self.setLayout(form)

    def check_all(self):
        for w in self.line_edits:
            if not w.passed:
                self.passed = False
                return
        self.passed = True
        self.close()

    def check_name(self):
        t = self.name.text()
        if not t or t in self.taken_names:
            self.name.setStyleSheet('background-color: salmon;')
            self.name.passed = False
        else:
            self.name.setStyleSheet('background-color: lightgreen;')
            self.name.passed = True
        self.name.setFont(self.font)

    def check_posnum(self, widget, canbe0=True):
        t = widget.text()
        try:
            t = float(t)
            if t == 0 and not canbe0 or t < 0:
                raise ValueError()
        except:
            widget.setStyleSheet('background-color: salmon;')
            widget.passed = False
        else:
            widget.setStyleSheet('background-color: lightgreen;')
            widget.passed = True
        widget.setFont(self.font)
