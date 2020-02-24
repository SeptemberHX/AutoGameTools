import sys

from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox

from auto_module.model import GameAction, load_game_databases
from gui.Ui_ActionEditWidget import Ui_ActionEditWidget
from pyqt_screenshot.screenshot import Screenshot, constant


class ActionEditWidget(QWidget, Ui_ActionEditWidget):

    action_saved = pyqtSignal(dict)
    status_canceled = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.img = None

        self.screenshot_button.clicked.connect(self.screenshot_clicked)
        self.button_group.accepted.connect(self.save_button_clicked)
        self.button_group.rejected.connect(self.status_canceled)

        self.from_comboBox.currentIndexChanged.connect(self.auto_generate_name)
        self.to_comboBox.currentIndexChanged.connect(self.auto_generate_name)

    def screenshot_clicked(self):
        img = Screenshot.take_screenshot(constant.CLIPBOARD)
        if img is None:
            return

        self.img = img
        self.preview_label.setPixmap(QPixmap(img).scaled(self.preview_label.size(), Qt.KeepAspectRatio))

    def reset(self):
        self.name_lineEdit.clear()
        self.to_comboBox.clear()
        self.preview_label.clear()

    def load_action(self, game_action: GameAction, state_list):
        self.name_lineEdit.setText(game_action.name)
        self.to_comboBox.clear()
        self.to_comboBox.addItems(state_list)
        self.to_comboBox.setCurrentText(game_action.to_state)
        self.from_comboBox.clear()
        self.from_comboBox.addItems(state_list)
        self.from_comboBox.setCurrentText(game_action.from_state)
        self.area_condition.setText(game_action.condition[:game_action.condition.find('.')])
        self.img = game_action.get_raw_condition_img()
        self.preview_label.setPixmap(QPixmap(self.img).scaled(self.preview_label.size() - QSize(6, 6), Qt.KeepAspectRatio))

    def auto_generate_name(self):
        self.name_lineEdit.setText('{0}->{1}'.format(self.from_comboBox.currentText(), self.to_comboBox.currentText()))

    def check_legal(self):
        if len(self.name_lineEdit.text()) == 0:
            QMessageBox.information(self, 'Illegal Information', 'Action Name cannot be empty!', QMessageBox.Ok)
            return False

        if self.img is None:
            QMessageBox.information(self, 'Illegal Information', 'Condition image is empty!', QMessageBox.Ok)
            return False
        return True

    def save_button_clicked(self):
        if self.check_legal():
            self.action_saved.emit(self.collect_data())

    def collect_data(self):
        return {
            'name': self.name_lineEdit.text(),
            'to': self.to_comboBox.currentText(),
            'from': self.from_comboBox.currentText(),
            'condition': self.area_condition.text(),
            'img': self.img
        }


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ActionEditWidget()

    game_config = load_game_databases()
    w.show()
    w.load_action(game_config['Arknights']['1920x1080'].game_action_dict['开始行动'], game_config['Arknights']['1920x1080'].game_state_dict.keys())

    app.exec()
