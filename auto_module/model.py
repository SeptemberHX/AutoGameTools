# encoding: utf-8

import os
import json
import math
import queue
import networkx as nx
import matplotlib.pyplot as plt

from auto_module.exception import DatabaseIllegalException, GameConfigIllegalException, NoPathFindException
from auto_module.image import get_resource_img, check_contain_img, get_matched_area
from auto_module.logger import get_logger
from typing import List, Dict

GAME_DATABASE_DIR = 'D:\Workspace\git\AutoGameTools\game_tools'
GAME_CONFIG_FILENAME = 'config.json'

logger = get_logger('model')


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
                game_state = GameState(state_json['name'], state_json['condition'], game_config.game_config_dir, state_json['type'])
                for action_json in state_json['actions']:
                    p = action_json['predecessor'] if 'predecessor' in action_json else None
                    game_action = GameAction(action_json['name'], action_json['method'],
                                             action_json['condition'], action_json['successor'], p)
                    game_state.add_action(game_action)
                game_config.add_state(game_state)
            game_config.build_graph()
            game_config.draw_graph()
            return game_config
    except Exception as e:
        raise GameConfigIllegalException(e)


class GameAction:
    def __init__(self, name, method, condition, successor, predecessor=None):
        """

        :param name: action name
        :param method: action active method: click or swipe
        :param condition: condition picture for finding the clicking position
        :param successor: next state name
        :param predecessor: action only be executed when the previous status is predecessor if presented
                            will be checked when finding the shortest path for execution
        """
        self.name = name
        self.method = method
        self.condition = condition
        self.successor = successor
        self.data_dir = ''
        self.predecessor = predecessor

    def __str__(self) -> str:
        return '{0}|{1}|{2}|{3}'.format(self.name, self.method, self.condition, self.successor)
    
    def __repr__(self) -> str:
        return self.__str__()

    def get_action_area(self, src_img):
        c_img = get_resource_img(self.data_dir, self.condition)
        return get_matched_area(src_img, c_img)

    def check_if_condition_met(self, src_img):
        c_img = get_resource_img(self.data_dir, self.condition)
        return check_contain_img(src_img, c_img)


class GameState:
    def __init__(self, name, conditions, game_config_dir, state_type):
        """

        :param name: state name, should be unique
        :param conditions: conditions for classifying game screenshots. It should be some specific sub-images,
                           and/or will be supported in the future
        """
        self.name = name
        self.conditions = conditions
        self.action_dict = {}
        self.game_config_dir = game_config_dir
        self.type = state_type

    def add_action(self, game_action: GameAction):
        game_action.data_dir = os.path.join(self.game_config_dir, self.name)
        self.action_dict[game_action.name] = game_action

    def check_if_conditions_met(self, src_img) -> bool:
        if len(self.conditions) == 0:
            return False

        condition_img_list = self.conditions.split('|')
        for condition in condition_img_list:
            not_flag = False
            if condition.startswith('!'):
                condition_img = condition[1:]
                not_flag = True
            else:
                condition_img = condition
            c_img = get_resource_img(os.path.join(self.game_config_dir, self.name), condition_img)
            if_contains = check_contain_img(src_img, c_img)
            if not_flag == if_contains:
                return False
        return True


class GameConfig:
    def __init__(self, game_name, game_config_dir, game_title):
        self.game_name = game_name
        self.game_config_dir = game_config_dir
        self.game_state_dict = {}  # type: Dict[str, GameState]
        self.game_action_dict = {}
        self.graph = nx.DiGraph()  # type: nx.DiGraph
        self.game_title = game_title

    def add_state(self, game_state: GameState):
        self.game_state_dict[game_state.name] = game_state
        for k, v in game_state.action_dict.items():
            self.game_action_dict[k] = v

    def build_graph(self):
        for state_name, _ in self.game_state_dict.items():
            self.graph.add_node(state_name)
        for state_name, state in self.game_state_dict.items():
            for action in state.action_dict.values():
                self.graph.add_edge(state_name, action.successor, action=action.name, weight=1)

    def get_shortest_action_list(self, source_state, target_state) -> List[GameAction]:
        """
        abandon due to the lack of the predecessor
        """
        action_list = []
        path_list = nx.algorithms.shortest_paths.shortest_path(self.graph, source_state, target_state, weight='weight')
        for i in range(0, len(path_list) - 1):
            edge_data = self.graph.get_edge_data(path_list[i], path_list[i+1])
            action = self.game_action_dict[edge_data['action']]
            action_list.append(action)
            logger.info('{0}->{1}: {2}'.format(path_list[i], path_list[i+1], action))

        return action_list

    def get_shortest_action_list_dijkstra(self, source_state, target_state) -> List[GameAction]:
        """
        abandon due to the lack of the predecessor
        """
        action_list = []
        adj = {}
        dis = {}
        visited = [source_state]

        # prepare the adj dict and the distance dict
        for u, v, data in self.graph.edges.data():
            if u not in adj:
                adj[u] = {}
            adj[u][v] = data['weight']
            if u == source_state:
                dis[v] = data['weight']
        for node in self.graph.nodes:
            if node not in dis:
                dis[node] = math.inf
            if node not in adj:
                adj[node] = {}
        dis.pop(source_state)

        # run Dijkstra until the target_state is visited or loop ends
        parents_node = {}
        for _ in range(len(dis)):
            sort_dis = sorted(dis.items(), key=lambda item: item[1])
            for p, d in sort_dis:
                if p not in visited:
                    min_dis_point = p
                    min_dis = d
                    visited.append(p)
                    break
            # 更新相邻点的开销
            for n in adj[min_dis_point].keys():
                if n in visited:
                    continue
                update = min_dis + adj[min_dis_point][n]
                if dis[n] > update:
                    dis[n] = update
                    parents_node[n] = min_dis_point
                else:
                    parents_node[n] = source_state
            if target_state in visited:
                break

        if target_state not in visited or dis[target_state] == math.inf:
            raise NoPathFindException('From {0} to {1}'.format(source_state, target_state))
        else:
            curr_state = target_state
            while curr_state in parents_node:
                action_list.append(self.game_action_dict[
                    self.graph.get_edge_data(parents_node[curr_state], curr_state)['action']
                ])
                curr_state = parents_node[curr_state]
            action_list.append(self.game_action_dict[
                self.graph.get_edge_data(source_state, curr_state)['action']
            ])
            action_list.reverse()
        logger.info('Path {0} -> {1}: {2}'.format(source_state, target_state, action_list))
        return action_list

    def get_shortest_action_list_with_predecessor(self, source_state, target_state, must_have_states=[]) -> List[GameAction]:
        """
        We will use BFS to search the path with the consideration of the predecessor
        """
        if source_state == target_state:
            return []

        class _route:
            def __init__(self, cost, path, action_path):
                self.cost = cost
                self.path = path
                self.action_path = action_path

            def __lt__(self, other):
                return self.cost < other.cost

            def walk(self, weight, next_point, action_id):
                if next_point in self.path:
                    return None
                t_path = self.path[:]
                t_path.append(next_point)
                t_action_path = self.action_path[:]
                t_action_path.append(action_id)
                return _route(self.cost + weight, t_path, t_action_path)

            def last(self):
                return self.path[-1]

            def predecessor(self):
                return self.path[-2] if len(self.path) >= 2 else None

            def check_must_have(self, must_have_states):
                for s in must_have_states:
                    if s not in self.path:
                        return False
                return True

        q = queue.PriorityQueue()
        q.put(_route(0, [source_state], []))
        result = None
        while not q.empty() and not result:
            r = q.get()
            for u, v, d in self.graph.edges.data():
                if u != r.last():
                    continue
                p = r.predecessor()
                n = None
                t_action = self.game_action_dict[d['action']]
                if not t_action.predecessor or not p or t_action.predecessor == p:
                    n = r.walk(1, v, t_action)
                if n:
                    q.put(n)
                    if v == target_state and n.check_must_have(must_have_states):
                        result = n
        if not result:
            raise NoPathFindException('From {0} to {1} with must_have {2}'
                                      .format(source_state, target_state, must_have_states))
        else:
            return result.action_path

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
        pos = nx.spring_layout(self.graph, k=5, scale=3)
        nx.draw(self.graph, pos, with_labels=True, edge_color='black',
                width=1, linewidths=1, node_size=500, node_color='pink', alpha=0.9)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_label_dict, font_color='red')
        plt.show()
