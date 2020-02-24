import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox

import auto_module
from auto_module.model import GameState, load_game_databases
from gui.Ui_StatusEditWidget import Ui_StatusEditWidget
from pyqt_screenshot.screenshot import Screenshot, constant, pyqtSignal


class StatusEditWidget(QWidget, Ui_StatusEditWidget):

    status_saved = pyqtSignal(dict)
    status_canceled = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.img = None
        self.img_1 = None
        self.img_2 = None

        self.screenshot_button.clicked.connect(self.screenshot_clicked)
        self.screenshot_button_1.clicked.connect(self.screenshot_clicked)
        self.screenshot_button_2.clicked.connect(self.screenshot_clicked)

        self.button_group.accepted.connect(self.save_button_clicked)
        self.button_group.rejected.connect(self.status_canceled)

        self.type_comboBox.addItems(sorted(auto_module.constant.STATE_TYPE.values()))

    def screenshot_clicked(self):
        img = Screenshot.take_screenshot(constant.CLIPBOARD)
        if img is None:
            return

        if self.sender() == self.screenshot_button:
            self.img = img
            self.preview_label.setPixmap(QPixmap(img).scaled(self.preview_label.size(), Qt.KeepAspectRatio))
        elif self.sender() == self.screenshot_button_1:
            self.img_1 = img
            self.preview_label_1.setPixmap(QPixmap(img).scaled(self.preview_label_1.size(), Qt.KeepAspectRatio))
        elif self.sender() == self.screenshot_button_2:
            self.img_2 = img
            self.preview_label_2.setPixmap(QPixmap(img).scaled(self.preview_label_2.size(), Qt.KeepAspectRatio))

    def reset(self):
        self.name_lineEdit.clear()
        self.condition_name.clear()
        self.condition_name_1.clear()
        self.condition_name_2.clear()
        self.img = None
        self.img_1 = None
        self.img_2 = None
        self.preview_label.clear()
        self.preview_label_1.clear()
        self.preview_label_2.clear()
        self.contain_comboBox.setCurrentIndex(0)
        self.contain_comboBox_1.setCurrentIndex(0)
        self.contain_comboBox_2.setCurrentIndex(0)
        self.optional_groupbox_1.setChecked(False)
        self.optional_groupbox_2.setChecked(False)

    def load_status(self, game_status: GameState):
        self.reset()
        self.name_lineEdit.setText(game_status.name)
        self.type_comboBox.setCurrentText(game_status.type)

        i = 0
        for condition in game_status.conditions.split('|'):
            if len(condition) == 0:
                continue

            condition_img = condition
            if condition[0] == '!':
                condition_img = condition[1:]

            img = game_status.get_raw_condition_img(condition_img)
            if i == 0:
                self.img = img
                self.contain_comboBox.setCurrentIndex(condition[0] == '!')
                self.condition_name.setText(condition_img[:condition_img.find('.')])
            elif i == 1:
                self.optional_groupbox_1.setChecked(True)
                self.img_1 = img
                self.contain_comboBox_1.setCurrentIndex(condition[0] == '!')
                self.condition_name_1.setText(condition_img[:condition_img.find('.')])
            elif i == 2:
                self.optional_groupbox_2.setChecked(True)
                self.img_2 = img
                self.contain_comboBox_2.setCurrentIndex(condition[0] == '!')
                self.condition_name_2.setText(condition_img[:condition_img.find('.')])
            i += 1
        self.draw_preview()

    def draw_preview(self):
        if self.img is not None:
            self.preview_label.setPixmap(QPixmap(self.img).scaled(self.preview_label.size() - QSize(6, 6), Qt.KeepAspectRatio))
        if self.img_1 is not None:
            self.preview_label_1.setPixmap(QPixmap(self.img_1).scaled(self.preview_label_1.size() - QSize(6, 6), Qt.KeepAspectRatio))
        if self.img_2 is not None:
            self.preview_label_2.setPixmap(QPixmap(self.img_2).scaled(self.preview_label_2.size() - QSize(6, 6), Qt.KeepAspectRatio))

    def check_legal(self):
        if len(self.name_lineEdit.text()) == 0:
            QMessageBox.information(self, 'Illegal Information', 'Status Name cannot be empty!', QMessageBox.Ok)
            return False

        if self.img is None:
            QMessageBox.information(self, 'Illegal Information', 'Condition image is empty!', QMessageBox.Ok)
            return False

        if (self.optional_groupbox_1.isChecked() and self.img_1 is None) \
            or (self.optional_groupbox_2.isChecked() and self.img_2 is None):
            QMessageBox.information(self, 'Illegal Information', 'Condition image is empty!', QMessageBox.Ok)
            return False
        return True

    def save_button_clicked(self):
        if self.check_legal():
            self.status_saved.emit(self.collect_data())

    def collect_data(self):
        conditions = [
            {
                'name': self.condition_name.text(),
                'contains': self.contain_comboBox.currentIndex() == 0,
                'img': self.img
            }
        ]

        if self.optional_groupbox_1.isChecked():
            conditions.append(
                {
                    'name': self.condition_name_1.text(),
                    'contains': self.contain_comboBox_1.currentIndex() == 0,
                    'img': self.img_1
                }
            )

        if self.optional_groupbox_2.isChecked():
            conditions.append(
                {
                    'name': self.condition_name_2.text(),
                    'contains': self.contain_comboBox_2.currentIndex() == 0,
                    'img': self.img_2
                }
            )

        return {
            'name': self.name_lineEdit.text(),
            'type': self.type_comboBox.currentText(),
            'conditions': conditions
        }


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = StatusEditWidget()

    game_config = load_game_databases()
    w.show()
    w.load_status(game_config['Arknights']['1920x1080'].game_state_dict['战术演习'])

    app.exec()
