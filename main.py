# encoding: utf-8

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from gui.mainwindow import AutoGameToolWindow


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    main_window = AutoGameToolWindow()
    main_window.show()
    app.exec()
