from PyQt5.QtGui import *
from PyQt5 import *
from PyQt5.QtWidgets import *
import sys


class PengUI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.w = QWidget()
        self.w.setFixedSize(1000, 800)
        self.w.setWindowTitle('PengRobinsonEOS')

    def build_peng(self):
        self.label = QLabel('Test label', self.w)

    def main(self):
        self.build_peng()
        self.w.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    p = PengUI()
    p.main()
