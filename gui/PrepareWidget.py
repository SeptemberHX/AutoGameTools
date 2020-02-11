# coding = utf-8
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QToolButton, QFileIconProvider, \
    QPushButton, QApplication
from win32gui import IsWindow, IsWindowEnabled, IsWindowVisible, GetWindowText, EnumWindows, IsIconic


class PrepareWidget(QWidget):

    def __init__(self, game_name_list, parent=None):
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.tip_label_width = 270
        self.interaction_width = 400

        # game window title chosen widget
        self.window_chosen_widget = QWidget(self)
        self.window_chosen_layout = QHBoxLayout(self.window_chosen_widget)
        self.window_chosen_widget.setLayout(self.window_chosen_layout)

        self.window_chosen_label = QLabel('Game Window Title: ', self.window_chosen_widget)
        self.window_chosen_label.setAlignment(QtCore.Qt.AlignRight)
        self.window_chosen_label.setFixedWidth(self.tip_label_width)
        self.window_chosen_layout.addWidget(self.window_chosen_label)

        self.window_chosen_combo_box = QComboBox(self.window_chosen_widget)
        self.window_chosen_combo_box.setFixedWidth(self.interaction_width)
        self.window_chosen_layout.addWidget(self.window_chosen_combo_box)
        self.refresh_window_title_list()

        self.window_chosen_refresh_button = QPushButton('Refresh', self.window_chosen_widget)
        self.window_chosen_refresh_button.clicked.connect(self.refresh_window_title_list)
        self.window_chosen_layout.addWidget(self.window_chosen_refresh_button)

        self.main_layout.addWidget(self.window_chosen_widget)

        # last
        self.main_layout.addStretch()

    def refresh_window_title_list(self):
        self.window_chosen_combo_box.clear()
        titles = set()

        def _f(hwnd, mouse):
            if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd) and not IsIconic(hwnd):
                titles.add(GetWindowText(hwnd))

        EnumWindows(_f, 0)
        self.window_chosen_combo_box.addItems(titles)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = PrepareWidget(['明日方舟', '命运之子'])
    w.show()
    app.exec()
