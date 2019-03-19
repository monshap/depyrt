try:
    from PyQt4.QtGui import *
    from PyQt4 import *
except:
    from PyQt5.QtGui import *
    from PyQt5 import *
    from PyQt5.QtWidgets import *
import sys
import re

""" global positioning params """
cen = QtCore.Qt.AlignHCenter
right = QtCore.Qt.AlignRight
left = QtCore.Qt.AlignLeft
top = QtCore.Qt.AlignTop
bot = QtCore.Qt.AlignBottom


class StatMechNewMolecule(QDialog):
    def __init__(self, parent, taken_names):
        cl = QtCore.Qt.WindowCloseButtonHint
        super(StatMechNewMolecule, self).__init__(parent, cl)
        self.setFixedSize(700, 500)
        self.font = QFont('SansSerif', 14)
        self.setFont(self.font)
        self.setWindowTitle('New Molecule')
        self.passed = False
        self.taken_names = taken_names

        # regex pattern to match rot & vib inputs
        self.rv_regex = '^[0-9]+\.?[0-9]*(\([1-9][0-9]?\))?$'

        self.build_layout()

    def build_layout(self):
        lay = QFormLayout()

        # molecule name
        self.name = QLineEdit()

        # linear or nonlinear
        self.linear = QRadioButton("Linear")
        self.linear.setChecked(True)
        self.nonlinear = QRadioButton("Nonlinear")
        box = QHBoxLayout()
        box.addWidget(self.linear)
        box.addWidget(self.nonlinear)
        box.setAlignment(cen)
        box.setSpacing(100)

        # molecular weight
        self.mw = QLineEdit()

        # dissociation energy
        self.D0 = QLineEdit()
        # electronic ground state degeneracy
        self.W0 = QLineEdit()

        # symmetry constant
        self.sigma = QLineEdit()

        # characteristic vibrational temp
        self.theta_v = QLineEdit()

        # characteristic rotational temp
        self.theta_r = QLineEdit()

        # save button
        self.okay = QPushButton("Save")

        for w in [self.name, self.mw,
                  self.D0, self.W0,
                  self.sigma, self.theta_v,
                  self.theta_r]:
            w.setAlignment(cen)

        self.all_widgets = [self.name, self.mw,
                            self.D0, self.W0,
                            self.sigma, self.theta_r,
                            self.theta_v
                            ]

        self.name.textEdited.connect(self.check_name)
        self.mw.textEdited.connect(lambda f: self.isposfloat(self.mw))
        self.D0.textEdited.connect(lambda f: self.isposfloat(self.D0))
        self.W0.textEdited.connect(lambda f: self.isint(self.W0))
        self.sigma.textEdited.connect(lambda f: self.isint(self.sigma))
        self.theta_v.textEdited.connect(lambda f: self.check_rv(self.theta_v))
        self.theta_r.textEdited.connect(lambda f: self.check_rv(self.theta_r))
        self.okay.clicked.connect(self.check_all)

        lay.addRow("Name:", self.name)
        lay.addRow("Type:", box)
        lay.addRow("Mw (g / mol):", self.mw)
        lay.addRow(u'D\u2080  (J / mol):', self.D0)
        lay.addRow(u'W\u2080:', self.W0)
        lay.addRow(u'\u03c3:', self.sigma)
        lay.addRow(u'\u03f4\u1d65 (K):', self.theta_v)
        lay.addRow(u'\u03f4\u1d63 (K):', self.theta_r)
        lay.addWidget(self.okay)

        lay.setSpacing(20)
        self.setLayout(lay)

    def check_all(self):
        for w in self.all_widgets:
            if 'passed' not in w.__dict__:
                self.passed = False
                return

            elif not w.passed:
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

    def isint(self, widget, lim=1000):
        widget.passed = False
        text = widget.text()
        try:
            if int(text) - float(text) == 0 and int(text) < lim:
                widget.setStyleSheet('background-color: lightgreen;')
                widget.setFont(self.font)
                widget.passed = True
            else:
                raise ValueError()
        except:
            widget.setStyleSheet('background-color: salmon')
            widget.setFont(self.font)

    def isposfloat(self, widget, lim=1e12):
        widget.passed = False
        text = widget.text()
        try:
            val = float(text)
            if val <= 0 or val >= lim:
                raise ValueError('Number must be positive')
            widget.setStyleSheet('background-color: lightgreen;')
            widget.setFont(self.font)
            widget.passed = True
        except:
            widget.setStyleSheet('background-color: salmon')
            widget.setFont(self.font)

    def check_rv(self, widget, lim=30):
        widget.passed = False
        text = widget.text()
        vals = text.replace(',', ' ').split()
        if len(vals) >= lim:
            return
        for v in vals:
            if not re.match(self.rv_regex, v):
                widget.setStyleSheet('background-color: salmon;')
                widget.setFont(self.font)
                return
        else:
            widget.setStyleSheet('background-color: lightgreen;')
            widget.setFont(self.font)
            widget.passed = True

if __name__ == '__main__':
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    ui = StatMechNewMolecule(None, ['apple'])
    ui.show()
    sys.exit(app.exec_())
