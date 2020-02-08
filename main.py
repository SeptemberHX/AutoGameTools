# encoding: utf-8

from auto_module.executor import execute_to, debug_judge_state, execute_to_loop
from auto_module.image import GameWindow
from auto_module.model import load_game_databases

if __name__ == '__main__':
    game_databases = load_game_databases()
    # game_databases['Arknights'].get_shortest_action_list_dijkstra('LS-3选中', 'LS-3行动结束')
    game_window = GameWindow('明日方舟 - MuMu模拟器')
    # debug_judge_state(game_databases['Arknights'], game_window)
    # execute_to(game_databases['Arknights'], '异卵同生', 'S2-4选中', game_window)
    # execute_to_loop(game_databases['Arknights'], 'LS-3选中', 'LS-3行动结束', game_window)
    execute_to_loop(game_databases['Arknights'], '货物运送', '行动结束', game_window, ['CE-3选中'])
    # game_window.swipe(2)
