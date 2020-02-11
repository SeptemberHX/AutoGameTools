import json
import sys

from PyQt5.QtCore import QUrl, pyqtSignal, qDebug, QSize
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QVBoxLayout, QGroupBox, QComboBox, \
    QSizePolicy, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView

from auto_module.model import load_game_databases, GameConfig


class GameConfigWidget(QWidget):
    load_config = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.game_config = load_game_databases()
        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)
        self.setMinimumSize(QSize(1200, 800))

        self.config_widget = QWidget(self)
        self.config_widget_layout = QVBoxLayout(self.config_widget)
        self.config_widget.setLayout(self.config_widget_layout)

        self.select_groubbox = QGroupBox(self.config_widget)
        self.select_groubbox_layout = QHBoxLayout(self.select_groubbox)
        self.select_groubbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.select_groubbox.setTitle('Game')
        self.game_combobox = QComboBox(self.config_widget)
        self.game_combobox.setFixedHeight(40)
        self.game_combobox.currentIndexChanged.connect(self.init_resolution_selector)
        self.select_groubbox_layout.addWidget(self.game_combobox)

        self.resolution_combobox = QComboBox(self.config_widget)
        self.resolution_combobox.setFixedHeight(40)
        # self.resolution_combobox.currentIndexChanged.connect(self.init_game_selector)
        self.select_groubbox_layout.addWidget(self.resolution_combobox)
        self.init_game_selector()

        self.load_button = QPushButton('Load', self.config_widget)
        self.load_button.setFixedWidth(100)
        self.load_button.setFixedHeight(40)
        self.load_button.clicked.connect(self.load_button_clicked)
        self.select_groubbox_layout.addWidget(self.load_button)
        self.config_widget_layout.addWidget(self.select_groubbox)

        self.status_config_groupbox = QGroupBox(self.config_widget)
        self.status_config_groupbox.setTitle('Game Status')
        self.config_widget_layout.addWidget(self.status_config_groupbox)

        self.action_config_groupbox = QGroupBox(self.config_widget)
        self.action_config_groupbox.setTitle('Game Action')
        self.config_widget_layout.addWidget(self.action_config_groupbox)
        self.main_layout.addWidget(self.config_widget)
        self.main_layout.setStretchFactor(self.config_widget, 1)

        self.web_view = QWebEngineView(self)
        self.web_channel = QWebChannel(self.web_view.page())
        self.web_channel.registerObject('configWidget', self)
        self.web_view.page().setWebChannel(self.web_channel)
        self.web_view.load(QUrl('file:///gui/resource/draw.html'))
        self.main_layout.addWidget(self.web_view)

        self.main_layout.setStretchFactor(self.web_view, 3)

    def init_game_selector(self):
        self.game_combobox.clear()
        for game in self.game_config:
            self.game_combobox.addItem(game)

    def init_resolution_selector(self):
        r = list(self.game_config[self.game_combobox.currentText()].keys())
        sorted(r)
        self.resolution_combobox.clear()
        self.resolution_combobox.addItems(r)

    def set_config(self, game_config: GameConfig):
        self.load_config.emit(json.dumps(game_config.get_d3_data()))

    def load_button_clicked(self):
        if self.game_combobox.currentText() not in self.game_config or \
                self.resolution_combobox.currentText() not in self.game_config[self.game_combobox.currentText()]:
            QMessageBox.information(None, 'Invalid', 'Cannot load game {0} with resolution {1}.'
                                    .format(self.game_combobox.currentText(), self.resolution_combobox.currentText()),
                                    QMessageBox.Yes)

        self.set_config(self.game_config[self.game_combobox.currentText()][self.resolution_combobox.currentText()])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = GameConfigWidget()
    w.show()
    app.exec()
