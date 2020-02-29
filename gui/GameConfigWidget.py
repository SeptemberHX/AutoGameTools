import json
import os
import shutil
import sys


from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView

from auto_module.model import load_game_databases, GameConfig, GameState, GameAction
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
        self.action_add_toolButton.clicked.connect(self.add_default_action)

        self.buttonBox.accepted.connect(self.save_current_config)
        self.state_edit_widget.status_saved.connect(self.save_game_state)
        self.action_edit_widget.action_saved.connect(self.save_game_action)

    def add_default_state(self):
        gs = GameState.default(self.current_config.game_config_dir)
        self.current_config.game_state_dict[gs.name] = gs
        self.state_listWidget.insertItem(0, gs.name)

    def add_default_action(self):
        action = GameAction.default(self.state_listWidget.currentItem().text())
        self.current_config.game_state_dict[self.state_listWidget.currentItem().text()].action_dict[action.name] = action
        self.current_config.game_action_dict[action.name] = action
        self.action_listWidget.insertItem(0, action.name)

    def show_status_edit_widget(self):
        self.state_edit_widget.show()
        self.placeholder_label.hide()
        self.action_edit_widget.hide()

    def show_action_edit_widget(self):
        self.state_edit_widget.hide()
        self.placeholder_label.hide()
        self.action_edit_widget.show()
        
    def save_game_state(self, game_state_data):
        modified_state_id = self.state_listWidget.currentItem().text()
        target_state = self.current_config.game_state_dict[modified_state_id]
        target_state.condition_imgs.clear()

        if game_state_data['name'] != target_state.name:
            self.current_config.game_state_dict.pop(target_state.name)
            target_state.name = game_state_data['name']
            self.current_config.game_state_dict[target_state.name] = target_state
        target_state.type = game_state_data['type']
        condition_str = ''
        for condition in game_state_data['conditions']:
            if not condition['contains']:
                condition_str += '!'
            condition_str += condition['name'] + '.png' + '|'
            target_state.condition_imgs[condition['name'] + '.png'] = condition['img']
        target_state.conditions = condition_str[:-1]
        for action in target_state.action_dict.values():
            action.from_state = target_state.name
            action.data_dir = os.path.join(target_state.game_config_dir, target_state.name)
        self.state_listWidget.currentItem().setText(game_state_data['name'])

    def save_game_action(self, game_action_data):
        modified_action_id = self.action_listWidget.currentItem().text()
        target_action = self.current_config.game_action_dict[modified_action_id]

        if target_action.from_state != game_action_data['from']:
            self.current_config.game_state_dict[target_action.from_state].action_dict.pop(target_action.name)
            target_action.from_state = game_action_data['from']
            self.current_config.game_state_dict[target_action.from_state].action_dict[target_action.name] = target_action

        if target_action.name != game_action_data['name']:
            self.current_config.game_action_dict.pop(target_action.name)
            target_action.name = game_action_data['name']
            self.current_config.game_action_dict[target_action.name] = target_action

        target_action.condition = game_action_data['condition'] + '.png'
        target_action.to_state = game_action_data['to']
        target_action.condition_img = game_action_data['img']
        self.action_listWidget.currentItem().setText(target_action.name)

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

    def save_current_config(self):
        try:
            if self.current_config is None:
                return
            game_config_dir = self.current_config.game_config_dir
            game_config_dir = '/var/test'
            if os.path.exists(game_config_dir):
                shutil.rmtree(game_config_dir)
            os.mkdir(game_config_dir)
            for state_name, state in self.current_config.game_state_dict.items():
                state_dir = os.path.join(game_config_dir, state_name)
                if not os.path.exists(state_dir):
                    os.mkdir(state_dir)
                for condition_img_name, condition_img in state.condition_imgs.items():
                    condition_img.save(os.path.join(state_dir, condition_img_name), 'png')

                for action_name, action in state.action_dict.items():
                    action.condition_img.save(os.path.join(state_dir, action.condition), 'png')

            # save config json file
            with open(os.path.join(game_config_dir, 'config.json'), 'w', encoding='utf-8') as f:
                json.dump(self.current_config.to_json(), f, indent=4, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(None, 'Error saving!', 'Cannot save game {0} with resolution {1}, {2}'
                                    .format(self.game_combobox.currentText(), self.resolution_combobox.currentText(), e),
                                    QMessageBox.Yes)
            return
        QMessageBox.information(None, 'Save Successfully!', 'Game {0} with resolution {1} saved!'
                                .format(self.game_combobox.currentText(), self.resolution_combobox.currentText()),
                                QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = GameConfigWidget()
    w.show()
    app.exec()
