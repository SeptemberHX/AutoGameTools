# coding = utf-8
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem, QHeaderView, QMessageBox, QWidget
from win32gui import IsWindowEnabled, IsWindow, GetWindowText, EnumWindows, IsWindowVisible, IsIconic

from auto_module.exception import NoPathFindException
from auto_module.executor import Executor
from auto_module.image import GameWindow
from auto_module.model import load_game_databases
from gui.UI_StatusWidget import Ui_StatusWidget

CHECKING_STATUS = 'Checking'
status_list = [
    'Current Status',
    'Previous Status',
    'Current Action',
]


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


class StatusWindow(QWidget, Ui_StatusWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        self.curr_pixmap = None
        self.game_config = load_game_databases()

        self.game_combobox.currentIndexChanged.connect(self.init_resolution_list)
        self.resolution_combobox.currentIndexChanged.connect(self.init_status)

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setEnabled(False)

        # ------

        self.screen_label.setScaledContents(True)
        self.prev_screen_label.setScaledContents(True)

        self.window_chosen_refresh_button.clicked.connect(self.refresh_window_title_list)
        self.refresh_window_title_list()

        self.status_table.setColumnCount(2)
        self.status_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.status_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.status_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.status_table.resizeRowsToContents()
        self.status_table.resizeColumnsToContents()
        self.status_table.verticalHeader().setHidden(True)
        self.prepare_status_table()

        # ------
        self.init_game_list()

    def refresh_window_title_list(self):
        self.window_chosen_combo_box.clear()
        titles = set()

        def _f(hwnd, mouse):
            if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd) and not IsIconic(hwnd):
                titles.add(GetWindowText(hwnd))

        EnumWindows(_f, 0)
        self.window_chosen_combo_box.addItems(titles)

    def start(self):
        try:
            self.game_config[self.game_combobox.currentText()][
                self.resolution_combobox.currentText()].get_shortest_action_list_with_predecessor(
                self.from_combobox.currentText(),
                self.to_combobox.currentText(),
                [self.must_combobox.currentText()]
            )
        except NoPathFindException as e:
            QMessageBox.information(self, 'Cannot Start',
                                    'No path found from {0} to {1} with {2}'.format(
                                        self.from_combobox.currentText(),
                                        self.to_combobox.currentText(),
                                        self.must_combobox.currentText()
                                    ), QMessageBox.Ok
                                    )
            return

        try:
            self.game_window = GameWindow(self.window_chosen_combo_box.currentText())
        except Exception as e:
            QMessageBox.information(self, 'Wrong Window',
                                    'Cannot initialize with the window title {0}. Please do not minimize the window!'
                                    .format(self.window_chosen_combo_box.currentText()), QMessageBox.Ok
                                    )
            return

        self.game_executor = Executor(
            game_config=self.game_config[self.game_combobox.currentText()][self.resolution_combobox.currentText()],
            game_window=self.game_window
        )
        self.game_executor.game_state_changed.connect(self.set_current_status)
        self.game_executor.action_executed.connect(self.set_current_action)
        self.game_executor.screenshot_catched.connect(self.set_current_screenshot)
        self.game_executor.exception_happened.connect(self.deal_with_exception)
        self.thread = RunThread(
            self.game_executor,
            self.from_combobox.currentText(),
            self.to_combobox.currentText(),
            [self.must_combobox.currentText()]
        )
        self.thread.start()
        self.set_start_or_end_status(True)

    def deal_with_exception(self, msg):
        QMessageBox.critical(self, 'Error!!!', msg, QMessageBox.Ok)
        self.stop()

    def set_start_or_end_status(self, is_start):
        self.game_groupbox.setEnabled(not is_start)
        self.status_groupbox.setEnabled(not is_start)
        self.start_button.setEnabled(not is_start)
        self.stop_button.setEnabled(is_start)

    def stop(self):
        if self.thread is not None and self.thread.isRunning():
            self.thread.terminate()
        self.set_start_or_end_status(False)

    def init_game_list(self):
        self.game_combobox.clear()
        self.game_combobox.addItems(self.game_config.keys())

    def init_resolution_list(self):
        self.resolution_combobox.clear()
        r = sorted(self.game_config[self.game_combobox.currentText()])
        self.resolution_combobox.addItems(r)

    def init_status(self):
        s_l = self.game_config[self.game_combobox.currentText()][
            self.resolution_combobox.currentText()].game_state_dict.keys()
        self.from_combobox.clear()
        self.from_combobox.addItems(s_l)

        self.to_combobox.clear()
        self.to_combobox.addItems(s_l)

        self.must_combobox.clear()
        self.must_combobox.addItems(s_l)

    def prepare_status_table(self):
        self.status_table.clear()
        for status in status_list:
            r = self.status_table.rowCount()
            self.status_table.insertRow(r)
            item_1 = QTableWidgetItem(status)
            item_1.setTextAlignment(QtCore.Qt.AlignVCenter)
            self.status_table.setItem(r, 0, item_1)
            item_2 = QTableWidgetItem('None')
            item_2.setTextAlignment(QtCore.Qt.AlignVCenter)
            self.status_table.setItem(r, 1, item_2)
            self.status_table.setRowHeight(r, 50)
        self.status_table.setHorizontalHeaderLabels(['Property', 'Value'])

    def set_current_screenshot(self, img_dict):
        self.set_screenshot(img_dict['screenshot'])
        self.set_current_and_prev_status(CHECKING_STATUS)

    def set_current_and_prev_status(self, current_status):
        if self.status_table.item(0, 1).text() != CHECKING_STATUS:
            self.status_table.item(1, 1).setText(self.status_table.item(0, 1).text())
        self.status_table.item(0, 1).setText(current_status)

    def set_current_status(self, status):
        status_name = 'None'
        if status['status'] is not None:
            status_name = status['status'].name
        self.set_current_and_prev_status(status_name)

    def set_current_action(self, action_name):
        self.status_table.setItem(2, 1, QTableWidgetItem(action_name))

    def set_screenshot(self, t_img):
        if self.curr_pixmap:
            self.prev_screen_label.setPixmap(self.curr_pixmap)
        height, width, channel = t_img.shape
        bytes_per_line = channel * width
        self.curr_pixmap = QPixmap.fromImage(
            QImage(t_img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped())
        self.screen_label.setPixmap(self.curr_pixmap)
        self.repaint()
