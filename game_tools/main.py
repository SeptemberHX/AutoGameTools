from auto_module.executor import execute_to
from auto_module.model import load_game_databases

if __name__ == '__main__':
    game_databases = load_game_databases()
    game_databases['Arknights'].get_shortest_action_list('公告', '主页')
    execute_to(game_databases['Arknights'], '公告', '主页')
