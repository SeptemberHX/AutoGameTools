# coding = utf-8

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from auto_module.executor import Executor
from auto_module.image import GameWindow
from auto_module.model import load_game_databases
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
        self.status_widget = StatusWindow(self)
        self.main_layout.addWidget(self.status_widget)
        self.game_databases = load_game_databases()
        self.load_data()

    def load_data(self):
        self.game_window = GameWindow('明日方舟 - MuMu模拟器')
        self.game_executor = Executor(game_config=self.game_databases['Arknights']['1920x1080'], game_window=self.game_window)
        self.game_executor.game_state_changed.connect(self.status_widget.set_current_status)
        self.game_executor.action_executed.connect(self.status_widget.set_current_action)
        self.game_executor.screenshot_catched.connect(self.status_widget.set_current_screenshot)

    def start(self):
        self.thread = RunThread(self.game_executor, '货物运送', '行动结束', ['CE-3选中'])
        self.thread.start()
