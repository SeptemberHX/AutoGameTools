# coding = utf-8

from PyQt5.QtCore import QThread, QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QButtonGroup

from auto_module.executor import Executor
from auto_module.image import GameWindow
from auto_module.model import load_game_databases
from gui.GameConfigWidget import GameConfigWidget
from gui.StatusWindow import StatusWindow


class RunThread(QThread):
    def __init__(self, executor, start_status, to_status, must_have_status_list):
        super().__init__()
        self.executor = executor
        self.start_status = start_status
        self.to_status = to_status
        self.must_have = must_have_status_list

    def __del__(self):
        self.wait()

    def run(self):
        try:
            self.executor.execute_to_loop(self.start_status, self.to_status, self.must_have)
        except Exception as e:
            print(e)


class AutoGameToolWindow(QWidget):

    def __init__(self):
        super().__init__(None)
        self.setWindowTitle('Auto Game Tool')

        self.main_layout = QHBoxLayout(self)
        self.button_size = QSize(100, 100)

        # ------
        self.button_list = []
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        self.button_group.buttonClicked.connect(self.show_right_widget)

        self.button_widget = QWidget(self)
        self.button_widget_layout = QVBoxLayout(self.button_widget)
        self.button_widget.setLayout(self.button_widget_layout)

        self.game_config_button = QPushButton('Config', self)
        self.game_config_button.setFixedSize(self.button_size)
        self.button_widget_layout.addWidget(self.game_config_button)
        self.button_group.addButton(self.game_config_button)
        self.button_list.append(self.game_config_button)

        self.game_run_button = QPushButton('Run', self)
        self.game_run_button.setFixedSize(self.button_size)
        self.button_widget_layout.addWidget(self.game_run_button)
        self.button_group.addButton(self.game_run_button)
        self.button_list.append(self.game_run_button)

        self.button_widget_layout.addStretch()
        self.main_layout.addWidget(self.button_widget)

        # ------
        self.right_widget_list = []

        self.game_config_widget = GameConfigWidget(self)
        self.main_layout.addWidget(self.game_config_widget)
        self.right_widget_list.append(self.game_config_widget)

        self.status_widget = StatusWindow(self)
        self.main_layout.addWidget(self.status_widget)
        self.right_widget_list.append(self.status_widget)

        # ------
        self.game_run_button.click()

    def invisible_all(self):
        for w in self.right_widget_list:
            w.setVisible(False)

    def show_right_widget(self, btn):
        self.invisible_all()
        self.right_widget_list[self.button_list.index(btn)].setVisible(True)

    def load_data(self):
        self.game_databases = load_game_databases()
        self.game_window = GameWindow('明日方舟 - MuMu模拟器')
        self.game_executor = Executor(game_config=self.game_databases['Arknights']['1920x1080'], game_window=self.game_window)
        self.game_executor.game_state_changed.connect(self.status_widget.set_current_status)
        self.game_executor.action_executed.connect(self.status_widget.set_current_action)
        self.game_executor.screenshot_catched.connect(self.status_widget.set_current_screenshot)

    def start(self):
        self.thread = RunThread(self.game_executor, '货物运送', '行动结束', ['CE-3选中'])
        self.thread.start()
