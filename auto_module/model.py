# encoding: utf-8

import os
import json
import math
import queue
import networkx as nx

from auto_module.constant import STATE_TYPE, RESERVED_STATE
from auto_module.exception import DatabaseIllegalException, GameConfigIllegalException, NoPathFindException
from auto_module.image import get_gray_resource_img, check_contain_img, get_matched_area, get_raw_resource_img_QImage
from auto_module.logger import get_logger
from typing import List, Dict, Tuple

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
        game_specific_path = os.path.join(GAME_DATABASE_DIR, game_dir)
        if not os.path.isdir(game_specific_path):
            continue

        for resolution in os.listdir(game_specific_path):
            resolution_path = os.path.join(game_specific_path, resolution)
            if not os.path.isdir(resolution_path):
                continue
            game_specific_config_path = os.path.join(resolution_path, GAME_CONFIG_FILENAME)
            if not os.path.exists(game_specific_config_path) or not os.path.isfile(game_specific_config_path):
                logger.info('Not exist or illegal config.json in game ' + game_dir)
                continue

            try:
                logger.info('loading game ' + game_dir)
                if game_dir not in result_dict:
                    result_dict[game_dir] = {}
                result_dict[game_dir][resolution] = read_game_config_file(resolution_path, GAME_CONFIG_FILENAME)
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
                game_config_dir=config_dir
            )
            for state_json in config_json['states']:
                game_state = GameState(state_json['name'], state_json['condition'], game_config.game_config_dir,
                                       state_json['type'])
                for action_json in state_json['actions']:
                    p = action_json['predecessor'] if 'predecessor' in action_json else None
                    game_action = GameAction(action_json['name'], action_json['method'],
                                             action_json['condition'], game_state.name, action_json['successor'], p)
                    game_state.add_action(game_action)
                game_config.add_state(game_state)
            game_config.prepare()
            # game_config.draw_graph()
            return game_config
    except Exception as e:
        raise GameConfigIllegalException(e)


class GameAction:
    def __init__(self, name, method, condition, from_state, to_state, predecessor=None):
        """

        :param name: action name
        :param method: action active method: click or swipe
        :param condition: condition picture for finding the clicking position
        :param to_state: next state name
        :param predecessor: action only be executed when the previous status is predecessor if presented
                            will be checked when finding the shortest path for execution
        """
        self.name = name
        self.method = method
        self.condition = condition
        self.to_state = to_state
        self.data_dir = ''
        self.predecessor = predecessor
        self.from_state = from_state
        self.condition_img = None  # only used during editing

    @staticmethod
    def default(from_state):
        return GameAction(
            name='DEFAULT_ACTION',
            method='click',
            condition='',
            to_state=None,
            predecessor=None,
            from_state=from_state,
        )

    def to_json(self):
        return {
            'name': self.name,
            'method': 'click',
            'condition': self.condition,
            'successor': self.to_state
        }

    def __str__(self) -> str:
        return '{0}|{1}|{2}|{3}'.format(self.name, self.method, self.condition, self.to_state)

    def __repr__(self) -> str:
        return self.__str__()

    def get_action_area(self, src_img):
        c_img = get_gray_resource_img(self.data_dir, self.condition)
        return get_matched_area(src_img, c_img)

    def get_raw_condition_img(self):
        if self.condition_img is None:
            self.condition_img = get_raw_resource_img_QImage(self.data_dir, self.condition)
        return self.condition_img

    def check_if_condition_met(self, src_img):
        c_img = get_gray_resource_img(self.data_dir, self.condition)
        return check_contain_img(src_img, c_img)[0]

    def prepare(self):
        self.condition_img = self.get_raw_condition_img()


class GameState:
    def __init__(self, name, conditions, game_config_dir, state_type):
        """

        :param name: state name, should be unique
        :param conditions: conditions for classifying game screenshots. It should be some specific sub-images,
                           and/or will be supported in the future
        """
        self.name = name
        self.conditions = conditions
        self.condition_imgs = {}
        self.action_dict = {}  # type: Dict[str, GameAction]
        self.game_config_dir = game_config_dir
        self.type = state_type
        self.modified = False

    def to_json(self):
        action_json_list = []
        for action in self.action_dict.values():
            action_json_list.append(action.to_json())
        return {
            'name': self.name,
            'condition': self.conditions,
            'type': self.type,
            'actions': action_json_list
        }

    @staticmethod
    def default(game_config_dir):
        return GameState('DEFAULT', '', game_config_dir, STATE_TYPE['NORMAL'])

    def add_action(self, game_action: GameAction):
        game_action.data_dir = os.path.join(self.game_config_dir, self.name)
        self.action_dict[game_action.name] = game_action

    def get_raw_condition_img(self, condition):
        if condition not in self.condition_imgs:
            self.condition_imgs[condition] = get_raw_resource_img_QImage(os.path.join(self.game_config_dir, self.name), condition)
        return self.condition_imgs[condition]

    def get_gray_condition_img(self, condition):
        return get_gray_resource_img(os.path.join(self.game_config_dir, self.name), condition)

    def prepare(self):
        if len(self.conditions) == 0:
            return
        for condition in self.conditions.split('|'):
            if condition.startswith('!'):
                self.get_raw_condition_img(condition[1:])
            else:
                self.get_raw_condition_img(condition)
        for action in self.action_dict.values():
            action.prepare()

    def check_if_conditions_met(self, src_img) -> Tuple[bool, list]:
        if len(self.conditions) == 0:
            return False, []

        condition_img_list = self.conditions.split('|')
        rect_list = []
        for condition in condition_img_list:
            not_flag = False
            if condition.startswith('!'):
                condition_img = condition[1:]
                not_flag = True
            else:
                condition_img = condition
            c_img = self.get_gray_condition_img(condition_img)
            if_contains, rect = check_contain_img(src_img, c_img)
            if if_contains:
                rect_list.append(rect)
            if not_flag == if_contains:
                return False, []
        return True, rect_list


class GameConfig:
    def __init__(self, game_name, game_config_dir):
        self.game_name = game_name
        self.game_config_dir = game_config_dir
        self.game_state_dict = {}  # type: Dict[str, GameState]
        self.game_action_dict = {}
        self.graph = nx.DiGraph()  # type: nx.DiGraph

    def to_json(self):
        state_json_list = []
        for state in self.game_state_dict.values():
            state_json_list.append(state.to_json())
        return {
            'name': self.game_name,
            'states': state_json_list
        }

    def get_all_user_state(self):
        r = []
        for s in self.game_state_dict.keys():
            if s not in RESERVED_STATE.values():
                r.append(s)
        return sorted(r)

    def add_state(self, game_state: GameState):
        self.game_state_dict[game_state.name] = game_state
        for k, v in game_state.action_dict.items():
            self.game_action_dict[k] = v

    def prepare(self):
        for state in self.game_state_dict.values():
            state.prepare()
        self.build_graph()

    def build_graph(self):
        for state_name, _ in self.game_state_dict.items():
            self.graph.add_node(state_name)
        for state_name, state in self.game_state_dict.items():
            for action in state.action_dict.values():
                self.graph.add_edge(state_name, action.to_state, action=action.name, weight=1)

    def get_shortest_action_list(self, source_state, target_state) -> List[GameAction]:
        """
        abandon due to the lack of the predecessor
        """
        action_list = []
        path_list = nx.algorithms.shortest_paths.shortest_path(self.graph, source_state, target_state, weight='weight')
        for i in range(0, len(path_list) - 1):
            edge_data = self.graph.get_edge_data(path_list[i], path_list[i + 1])
            action = self.game_action_dict[edge_data['action']]
            action_list.append(action)
            logger.info('{0}->{1}: {2}'.format(path_list[i], path_list[i + 1], action))

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

    def get_shortest_action_list_with_predecessor(self, source_state, target_state, must_have_states=[]) -> List[
        GameAction]:
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

    def get_d3_data(self):
        nodes = []
        group_dict = {
            STATE_TYPE['NORMAL']: 0,
            STATE_TYPE['JUMP']: 1,
            STATE_TYPE['HORIZONTAL_SWIPE']: 2,
            STATE_TYPE['VERTICAL_SWIPE']: 3,
            STATE_TYPE['NEED_IDENTIFY']: 4
        }
        for n in self.graph.nodes():
            nodes.append({
                'id': n,
                'group': group_dict[self.game_state_dict[n].type]
            })
        links = []
        for u, v, n in self.graph.edges.data('action'):
            links.append({
                'source': u,
                'target': v,
                'value': n
            })
        return {'nodes': nodes, 'links': links}
