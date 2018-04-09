from PyQt5.QtGui import *
from PyQt5 import *
from PyQt5.QtWidgets import *
import sys
from ui_widgets import all_tabs
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('arbitrary')


class ThermoProjectGUI(QTabWidget):
    def __init__(self, parent=None):
        super(ThermoProjectGUI, self).__init__(parent)
        self.setFixedSize(1000, 800)
        self.setFont(QFont('SansSerif', 14))
        self.setWindowTitle('Thermo Project')

    def run(self):
        # NOTE tab titles are created in ui_widgets/__init__.py
        # iterate through all tabs
        for tab in all_tabs:
            # initialize tab and add to main
            self.addTab(tab[0](self), tab[1])
        self.show()


def main():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('assets\\icons\\benzene.png'))
    gui = ThermoProjectGUI()
    gui.run()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
