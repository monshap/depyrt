try:
    from PyQt4.QtGui import *
    from PyQt4 import *
except:
    from PyQt5.QtGui import *
    from PyQt5 import *
    from PyQt5.QtWidgets import *
import sys
import json

""" global positioning params """
cen = QtCore.Qt.AlignHCenter
right = QtCore.Qt.AlignRight
left = QtCore.Qt.AlignLeft
top = QtCore.Qt.AlignTop
bot = QtCore.Qt.AlignBottom


class StatMechInfo(QDialog):
    def __init__(self, parent, name, props_dict):
        cl = QtCore.Qt.WindowCloseButtonHint
        super(StatMechInfo, self).__init__(parent, cl)
        self.setFixedSize(800, 500)
        self.setFont(QFont('SansSerif', 14))
        self.setWindowTitle('%s Info' % name)

        self.name = name
        self.props = props_dict

        self.build_layout()

    def build_layout(self):
        lay = QGridLayout()

        # molecule name
        self.title = QLabel(self.name)
        self.title.setFont(QFont('SansSerif', 14, QtGui.QFont.Bold))

        # molecule type (linear or nonlinear)
        self.type_lbl = QLabel("Type:")
        self.type = QLabel(self.props['type'].title())

        # molecular weight
        self.mw_lbl = QLabel('Mw:')
        self.mw = QLabel('%.2f g / mol' % self.props['Mw'])

        # dissociation energy
        self.d0_lbl = QLabel(u'D\u2080:')
        self.d0 = QLabel('%.2f kJ / mol' % (self.props['D0'] / 1000.))

        # electronic ground state degeneracy
        self.w0_lbl = QLabel(u'W\u2080:')
        self.w0 = QLabel('%i' % self.props['W0'])

        # symmetry constant
        self.sigma_lbl = QLabel(u'\u03c3:')
        self.sigma = QLabel('%i' % self.props['sigma'])

        # characteristic vibrational temperature(s)
        self.theta_v_lbl = QLabel(u'\u03f4\u1d65:')
        self.theta_v = QLabel(', '.join([str(i)
                                         for i
                                         in self.props['theta_v']]) + ' K')

        # characteristic rotational temperature(s)
        self.theta_r_lbl = QLabel(u'\u03f4\u1d63:')
        r = self.props['theta_r']
        if isinstance(r, list):
            val = ', '.join([str(i) for i in r])
        else:
            val = str(r)
        val += ' K'
        self.theta_r = QLabel(val)

        row = 0
        lay.setColumnStretch(1, 3)

        lay.addWidget(self.title, row, 1, cen)
        row += 1

        lay.addWidget(self.type_lbl, row, 0, right)
        lay.addWidget(self.type, row, 1, cen)
        row += 1

        lay.addWidget(self.mw_lbl, row, 0, right)
        lay.addWidget(self.mw, row, 1, cen)
        row += 1

        lay.addWidget(self.d0_lbl, row,  0, right)
        lay.addWidget(self.d0, row, 1, cen)
        row += 1

        lay.addWidget(self.w0_lbl, row, 0, right)
        lay.addWidget(self.w0, row, 1, cen)
        row += 1

        lay.addWidget(self.sigma_lbl, row, 0, right)
        lay.addWidget(self.sigma, row, 1, cen)
        row += 1

        lay.addWidget(self.theta_v_lbl, row, 0, right)
        lay.addWidget(self.theta_v, row, 1, cen)
        row += 1

        lay.addWidget(self.theta_r_lbl, row, 0, right)
        lay.addWidget(self.theta_r, row, 1, cen)

        self.setLayout(lay)

if __name__ == '__main__':
    with open('..\\assets\\data\\statmech_props.json', 'r') as f:
        props = json.load(f)
    name = 'Ammonia (NH3)'
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    ui = StatMechInfo(None, name, props[name])
    ui.show()
    sys.exit(app.exec_())
