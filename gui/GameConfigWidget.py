import json
import sys
import resource.resource

from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView

from auto_module.model import load_game_databases, GameConfig, GameState
from gui.ActionEditWidget import ActionEditWidget
from gui.StatusEditWidget import StatusEditWidget
from gui.Ui_GameConfigWidget import Ui_GameConfigWidget


class GameConfigWidget(QWidget, Ui_GameConfigWidget):
    load_config = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.game_config = load_game_databases()

        self.game_combobox.currentIndexChanged.connect(self.init_resolution_selector)
        self.init_game_selector()
        self.load_button.clicked.connect(self.load_button_clicked)

        self.state_edit_widget = StatusEditWidget(self)
        self.state_edit_widget.hide()
        self.main_layout.addWidget(self.state_edit_widget)

        self.action_edit_widget = ActionEditWidget(self)
        self.action_edit_widget.hide()
        self.main_layout.addWidget(self.action_edit_widget)

        self.web_view = QWebEngineView(self)
        self.web_channel = QWebChannel(self.web_view.page())
        self.web_channel.registerObject('configWidget', self)
        self.web_view.page().setWebChannel(self.web_channel)
        self.web_view.load(QUrl('qrc:/resource/html/draw.html'))
        self.main_layout.addWidget(self.web_view)

        self.current_config = None  # type: GameConfig

        self.action_listWidget.currentItemChanged.connect(self.action_click_changed)
        self.state_listWidget.currentItemChanged.connect(self.state_click_changed)

        self.state_add_toolButton.clicked.connect(self.add_default_state)

    def add_default_state(self):
        gs = GameState.default(self.current_config.game_config_dir)
        self.current_config.game_state_dict[gs.name] = gs
        self.state_listWidget.insertItem(0, gs.name)

    def show_status_edit_widget(self):
        self.state_edit_widget.show()
        self.placeholder_label.hide()
        self.action_edit_widget.hide()

    def show_action_edit_widget(self):
        self.state_edit_widget.hide()
        self.placeholder_label.hide()
        self.action_edit_widget.show()

    def init_game_selector(self):
        self.game_combobox.clear()
        for game in self.game_config:
            self.game_combobox.addItem(game)

    def init_resolution_selector(self):
        r = list(self.game_config[self.game_combobox.currentText()].keys())
        sorted(r)
        self.resolution_combobox.clear()
        self.resolution_combobox.addItems(r)

    def state_click_changed(self):
        self.show_status_edit_widget()
        self.state_edit_widget.load_status(
            self.current_config.game_state_dict[self.state_listWidget.currentItem().text()])

    def action_click_changed(self):
        self.show_action_edit_widget()
        self.action_edit_widget.load_action(
            self.current_config.game_action_dict[self.action_listWidget.currentItem().text()],
            self.current_config.game_state_dict.keys()
        )

    def set_config(self, game_config: GameConfig):
        self.load_config.emit(json.dumps(game_config.get_d3_data()))
        self.state_listWidget.clear()
        self.state_listWidget.addItems(game_config.get_all_user_state())
        self.action_listWidget.clear()
        self.action_listWidget.addItems(sorted(game_config.game_action_dict.keys()))

    def load_button_clicked(self):
        if self.game_combobox.currentText() not in self.game_config or \
                self.resolution_combobox.currentText() not in self.game_config[self.game_combobox.currentText()]:
            QMessageBox.information(None, 'Invalid', 'Cannot load game {0} with resolution {1}.'
                                    .format(self.game_combobox.currentText(), self.resolution_combobox.currentText()),
                                    QMessageBox.Yes)
        self.current_config = self.game_config[self.game_combobox.currentText()][self.resolution_combobox.currentText()]
        self.set_config(self.current_config)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = GameConfigWidget()
    w.show()
    app.exec()
