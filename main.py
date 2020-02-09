# encoding: utf-8
from auto_module import image
from auto_module.executor import Executor
from auto_module.image import GameWindow
from auto_module.model import load_game_databases

import aircv as ac
import sys

from PyQt5.QtWidgets import QApplication

from gui.mainwindow import AutoGameToolWindow


def aircv_test():
    imsrc = ac.imread('./game_tools/Arknights/test/home_mark.png')
    imsch = ac.imread('./game_tools/Arknights/test/test_home.png')

    imsrc = image.get_resource_img('./game_tools/Arknights/test', 'home_mark.png')
    imsch = image.get_resource_img('./game_tools/Arknights/test', 'test_home.png')

    print(image.get_matched_area_(imsch, imsrc))


# if __name__ == '__main__':
    # game_databases = load_game_databases()
    # game_window = GameWindow('明日方舟 - MuMu模拟器')
    #
    # # aircv_test()
    # debug_judge_state(game_databases['Arknights'], game_window)

    # game_databases['Arknights'].get_shortest_action_list_dijkstra('LS-3选中', 'LS-3行动结束')
    # execute_to(game_databases['Arknights'], '异卵同生', 'S2-4选中', game_window)
    # execute_to_loop(game_databases['Arknights'], 'LS-3选中', 'LS-3行动结束', game_window)
    # execute_to_loop(game_databases['Arknights'], '货物运送', '行动结束', game_window, ['CE-3选中'])
    # game_window.swipe(2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = AutoGameToolWindow()
    main_window.show()
    main_window.start()
    app.exec()
