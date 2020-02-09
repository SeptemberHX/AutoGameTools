# coding = utf-8
import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QToolButton, QFileIconProvider, \
    QPushButton, QApplication
from win32gui import IsWindow, IsWindowEnabled, IsWindowVisible, GetWindowText, EnumWindows, IsIconic


class PrepareWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # game window title chosen widget
        self.window_chosen_widget = QWidget(self)
        self.window_chosen_layout = QHBoxLayout(self.window_chosen_widget)
        self.window_chosen_widget.setLayout(self.window_chosen_layout)

        self.window_chosen_label = QLabel(self.window_chosen_widget)
        self.window_chosen_label.setText('Game Window Title: ')
        self.window_chosen_layout.addWidget(self.window_chosen_label)

        self.window_chosen_combo_box = QComboBox(self.window_chosen_widget)
        self.window_chosen_layout.addWidget(self.window_chosen_combo_box)
        self.refresh_window_title_list()

        self.window_chosen_refresh_button = QPushButton(self.window_chosen_widget)
        self.window_chosen_refresh_button.setText('Refresh')
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
    w = PrepareWidget()
    w.show()
    app.exec()
