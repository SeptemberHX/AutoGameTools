# encoding: utf-8

import os
import json
import networkx as nx
import matplotlib.pyplot as plt

from auto_module.exception import DatabaseIllegalException, GameConfigIllegalException
from .image import get_resource_img, check_contain_img, get_matched_area
from .logger import get_logger
from typing import List, Dict

GAME_DATABASE_DIR = 'D:\Workspace\git\AutoGameTools\game_tools'
GAME_CONFIG_FILENAME = 'config.json'

logger = get_logger('model')


# pre-defined state
RESERVED_STATE = {
    'NEED_IDENTIFY': 'NEED_IDENTIFY',  # we don't know current state. A judgement should be executed
}


def load_game_databases():
    """
    Read all the game configure files in the $GAME_DATABASE_DIR
    Each game has a separate dir, and a configure file named $GAME_CONFIG_FILENAME in the game dir
    :return: game config dict
    """
    logger.info('loading database from ' + GAME_DATABASE_DIR + ' ...')
    if not os.path.exists(GAME_DATABASE_DIR):
        os.mkdir(GAME_DATABASE_DIR)
    elif not os.path.isdir(GAME_DATABASE_DIR):
        raise DatabaseIllegalException('Load database failed')

    result_dict = {}
    for game_dir in os.listdir(GAME_DATABASE_DIR):
        if not os.path.isdir(os.path.join(GAME_DATABASE_DIR, game_dir)):
            continue

        game_specific_config_path = os.path.join(GAME_DATABASE_DIR, game_dir, GAME_CONFIG_FILENAME)
        if not os.path.exists(game_specific_config_path) or not os.path.isfile(game_specific_config_path):
            logger.info('Not exist or illegal config.json in game ' + game_dir)
            continue

        try:
            logger.info('loading game ' + game_dir)
            result_dict[game_dir] = read_game_config_file(os.path.join(GAME_DATABASE_DIR, game_dir), GAME_CONFIG_FILENAME)
        except GameConfigIllegalException as e:
            logger.debug(e)
    return result_dict


def read_game_config_file(config_dir, config_name):
    """
    Parse the config file into GameConfig object
    :param config_dir: the path of the config dir
    :param config_name: the name of the config file
    :return: GameConfig object
    """
    try:
        with open(os.path.join(config_dir, config_name), 'r', encoding='utf-8') as f:
            json_str = ''.join(f.readlines())
            config_json = json.loads(json_str, encoding='utf-8')
            print(config_json)
            game_config = GameConfig(
                game_name=config_json['name'],
                game_config_dir=config_dir,
                game_title=config_json['title'],
            )
            for state_json in config_json['states']:
                game_state = GameState(state_json['name'], state_json['condition'], game_config.game_config_dir)
                for action_json in state_json['actions']:
                    game_action = GameAction(action_json['name'], action_json['method'], action_json['condition'], action_json['successor'])
                    game_state.add_action(game_action)
                game_config.add_state(game_state)
            game_config.build_graph()
            game_config.draw_graph()
            return game_config
    except Exception as e:
        raise GameConfigIllegalException(e)


class GameAction:
    def __init__(self, name, method, condition, successor):
        """

        :param name: action name
        :param method: action active method: click or swipe
        :param condition: condition picture for finding the clicking position
        :param successor: next state name
        """
        self.name = name
        self.method = method
        self.condition = condition
        self.successor = successor
        self.data_dir = ''

    def __str__(self) -> str:
        return '{0}|{1}|{2}|{3}'.format(self.name, self.method, self.condition, self.successor)

    def get_action_area(self, src_img):
        c_img = get_resource_img(self.data_dir, self.condition)
        return get_matched_area(src_img, c_img)


class GameState:
    def __init__(self, name, conditions, game_config_dir):
        """

        :param name: state name, should be unique
        :param conditions: conditions for classifying game screenshots. It should be some specific sub-images,
                           and/or will be supported in the future
        """
        self.name = name
        self.conditions = conditions
        self.action_dict = {}
        self.game_config_dir = game_config_dir

    def add_action(self, game_action: GameAction):
        game_action.data_dir = os.path.join(self.game_config_dir, self.name)
        self.action_dict[game_action.name] = game_action

    def check_if_conditions_met(self, src_img) -> bool:
        condition_img_list = self.conditions.split('|')
        for condition_img in condition_img_list:
            c_img = get_resource_img(os.path.join(self.game_config_dir, self.name), condition_img)
            if not check_contain_img(src_img, c_img):
                return False
        return True


class GameConfig:
    def __init__(self, game_name, game_config_dir, game_title):
        self.game_name = game_name
        self.game_config_dir = game_config_dir
        self.game_state_dict = {}  # type: Dict[str, GameState]
        self.game_action_dict = {}
        self.graph = None  # type: nx.DiGraph
        self.game_title = game_title

    def add_state(self, game_state: GameState):
        self.game_state_dict[game_state.name] = game_state
        for k, v in game_state.action_dict.items():
            self.game_action_dict[k] = v

    def build_graph(self):
        self.graph = nx.DiGraph()
        for state_name, _ in self.game_state_dict.items():
            self.graph.add_node(state_name)
        for state_name, state in self.game_state_dict.items():
            for action in state.action_dict.values():
                self.graph.add_edge(state_name, action.successor, action=action.name, weight=1)

    def get_shortest_action_list(self, source_state, target_state) -> List[GameAction]:
        action_list = []
        path_list = nx.algorithms.shortest_paths.shortest_path(self.graph, source_state, target_state, weight='weight')
        for i in range(0, len(path_list) - 1):
            edge_data = self.graph.get_edge_data(path_list[i], path_list[i+1])
            action = self.game_action_dict[edge_data['action']]
            action_list.append(action)
            logger.info('{0}->{1}: {2}'.format(path_list[i], path_list[i+1], action))

        return action_list

    def check_current_state(self, wanted_state, src_img) -> bool:
        if wanted_state not in self.game_state_dict:
            return False
        return self.game_state_dict[wanted_state].check_if_conditions_met(src_img)

    def draw_graph(self):
        edge_label_dict = {}
        for u, v, n in self.graph.edges.data('action'):
            edge_label_dict[(u, v)] = n

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.subplot(121)
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, edge_color='black',
                width=1, linewidths=1, node_size=500, node_color='pink', alpha=0.9)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_label_dict, font_color='red')
        plt.show()
