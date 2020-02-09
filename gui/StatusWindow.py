# coding = utf-8

import cv2

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel


class StatusDashboard(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.curr_status_widget = QWidget(self)
        self.curr_status_layout = QHBoxLayout(self.curr_status_widget)
        self.curr_status_widget.setLayout(self.curr_status_layout)
        self.curr_status_tip = QLabel(self.curr_status_widget)
        self.curr_status_tip.setText('Current Status: ')
        self.curr_status_label = QLabel(self.curr_status_widget)
        self.curr_status_label.setText('None')
        self.curr_status_layout.addWidget(self.curr_status_tip)
        self.curr_status_layout.addWidget(self.curr_status_label)
        self.main_layout.addWidget(self.curr_status_widget)

        self.curr_action_widget = QWidget(self)
        self.curr_action_layout = QHBoxLayout(self.curr_action_widget)
        self.curr_action_widget.setLayout(self.curr_action_layout)
        self.curr_action_tip = QLabel(self.curr_action_widget)
        self.curr_action_tip.setText('Current Action: ')
        self.curr_action_label = QLabel(self.curr_action_widget)
        self.curr_action_label.setText('None')
        self.curr_action_layout.addWidget(self.curr_action_tip)
        self.curr_action_layout.addWidget(self.curr_action_label)
        self.main_layout.addWidget(self.curr_action_widget)

        self.main_layout.addStretch()

    def set_current_status(self, status):
        status_name = 'None'
        if status is not None:
            status_name = status.name
        self.curr_status_label.setText(status_name)

    def set_current_status_text(self, status_name):
        self.curr_status_label.setText(status_name)

    def set_current_action(self, action_name):
        self.curr_action_label.setText(action_name)


class StatusWindow(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)

        self.screen_label = QLabel(self)
        self.screen_label.setFixedSize(960, 540)
        self.status_widget = StatusDashboard(self)
        self.main_layout.addWidget(self.screen_label)
        self.main_layout.addWidget(self.status_widget)

    def set_current_screenshot(self, img_dict):
        self.set_screenshot(img_dict['screenshot'])
        self.status_widget.set_current_status_text('Checking')

    def set_current_status(self, game_status):
        self.status_widget.set_current_status(game_status['status'])

    def set_current_action(self, action_name):
        self.status_widget.set_current_action(action_name)

    def set_screenshot(self, game_img):
        # t_img = cv2.resize(
        #     game_img, (self.screen_label.width(), self.screen_label.height()), interpolation=cv2.INTER_AREA)
        t_img = game_img
        height, width, channel = t_img.shape
        bytes_per_line = channel * width
        qt_img = QImage(t_img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        self.screen_label.setPixmap(QPixmap.fromImage(qt_img))
        self.screen_label.setScaledContents(True)
        self.screen_label.repaint()
