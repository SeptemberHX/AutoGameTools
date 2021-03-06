# encoding: utf-8
import time

import cv2
import numpy
from PyQt5.QtCore import QObject, pyqtSignal

from auto_module.constant import DIRECT_STATE_TYPE, RESERVED_STATE, STATE_TYPE, DIRECTION
from auto_module.exception import CannotMoveForwardException, CannotFindActionBySwipe
from auto_module.image import GameWindow, check_img_equal
from auto_module.model import GameConfig, GameAction, GameState
from auto_module.logger import get_logger

import random

logger = get_logger('executor')
SCT_INTERVAL = 1


class Executor(QObject):

    game_state_changed = pyqtSignal(dict)
    action_executed = pyqtSignal(str)
    screenshot_catched = pyqtSignal(dict)
    exception_happened = pyqtSignal(str)
    screenshot_status_sure = pyqtSignal(dict)

    def __init__(self, game_config: GameConfig, game_window: GameWindow):
        super().__init__()
        self.game_config = game_config
        self.game_window = game_window
        self.status_hit_dict = {}

    def debug_judge_state(self):
        while True:
            game_img = self.get_screenshot()
            state_id = self.judge_state(game_img)
            logger.info('state from screenshot: {0}'.format(state_id))
            time.sleep(1)

    def execute_to_loop(self, from_state: str, to_state: str, must_have_states=[]):
        while True:
            self.execute_to(from_state, to_state, must_have_states)

    def execute_to(self, from_state: str, to_state: str, must_have_states=[]):
        """
        This function will try to move from the from_state to to_state
        from_state != real current state is allowed
        the state when this function finishes is guaranteed to be to_state
        """
        try:
            logger.info('In execute_to({0}, {1})'.format(from_state, to_state))
            state_id, _ = self.get_valid_state(from_state)
            if self.game_config.game_state_dict[state_id].type not in DIRECT_STATE_TYPE and to_state != RESERVED_STATE['NEED_IDENTIFY']:
                state_id, _ = self.handle_abnormal_state(state_id)

            action_list = self.game_config.get_shortest_action_list_with_predecessor(from_state, to_state, must_have_states)
            curr_state = from_state
            game_img = None
            action_index = 0
            while action_index < len(action_list):
                action = action_list[action_index]
                logger.info('trying to move from {0} to {1}...'.format(curr_state, action.to_state))
                if state_id == to_state:
                    break

                middle_state_flag = False
                if state_id != curr_state:
                    # check whether it is a middle state
                    for index in range(action_index, len(action_list)):
                        if action_list[index].to_state == state_id:
                            action_index = index + 1  # state_id will never equal to to_state, thus index + 1 < len(action_list)
                            middle_state_flag = True
                            break
                    if middle_state_flag:  # if true, jump to corresponding action
                        curr_state = state_id
                        logger.info('Middle state met, jump to action {0}'.format(action_list[action_index].name))
                        continue
                    else:
                        state_id, game_img = self.execute_to(state_id, from_state)
                        curr_state = state_id
                        action_index = 0
                        continue
                else:
                    # do the action to move on to the next state
                    logger.info('move from {0} to {1}'.format(curr_state, action.to_state))
                    while state_id != action.to_state:
                        logger.info('Executing action {0}...'.format(action.name))
                        self.execute_action(self.game_config.game_state_dict[curr_state], action)
                        time.sleep(SCT_INTERVAL)
                        state_id, game_img = self.get_valid_state(action.to_state)
                        if state_id == action.to_state:
                            break
                        if self.game_config.game_state_dict[state_id].type not in DIRECT_STATE_TYPE:
                            state_id, game_img = self.handle_abnormal_state(state_id)
                        if state_id != action.to_state and to_state == RESERVED_STATE['NEED_IDENTIFY']:
                            break
                        if state_id != curr_state and state_id != action.to_state \
                                and self.game_config.game_state_dict[state_id].type in DIRECT_STATE_TYPE:
                            self.execute_to(state_id, action.to_state)

                    logger.info('Action {0} finished'.format(action.name))
                    logger.info('move from {0} to {1} finished'.format(curr_state, action.to_state))
                    curr_state = action.to_state
                action_index += 1

            while to_state != RESERVED_STATE['NEED_IDENTIFY'] and state_id != to_state:
                logger.info('Trying to solve unmatched to_state {0}...'.format(state_id))
                if self.game_config.game_state_dict[state_id].type not in DIRECT_STATE_TYPE:
                    state_id, game_img = self.handle_abnormal_state(state_id)
                else:
                    raise CannotMoveForwardException('Cannot move from status {0}!!!'.format(state_id))
            logger.info('Execute from {0} to {1} finished'.format(from_state, to_state))
            return state_id, game_img
        except Exception as e:
            logger.debug(e)
            self.exception_happened.emit(e.msg)
            raise e

    def wait_until_screen_change(self, src_img):
        logger.info('Wait until screen change...')
        curr_img = self.get_screenshot()
        while check_img_equal(src_img, curr_img):
            time.sleep(SCT_INTERVAL)
            curr_img = self.get_screenshot()
        logger.info('Wait until screen change finished')

    def wait_until_status_meet(self, game_state, prev_state):
        logger.info('Wait until current status is {0} or {1}'.format(game_state, prev_state))
        state_id, game_img = self.get_valid_state(game_state)
        while state_id not in [game_state, prev_state]:
            if self.game_config.game_state_dict[state_id].type not in DIRECT_STATE_TYPE:
                self.handle_abnormal_state(state_id)
            time.sleep(SCT_INTERVAL)
            state_id, game_img = self.get_valid_state(game_state)
        logger.info('Wait finished at {0}'.format(state_id))
        return state_id, game_img

    def get_valid_state(self, potential_status_name=None):
        """
        Get a valid state from current screenshot.
        If current screenshot's status is invalid, it will loop
        """
        game_img, state_id = self.get_screenshot_and_status(potential_status_name)
        logger.info('state from screenshot: {0}'.format(state_id))
        while state_id is None:
            game_img, state_id = self.get_screenshot_and_status(potential_status_name)
            logger.info('state from screenshot: {0}'.format(state_id))
            time.sleep(SCT_INTERVAL)
        return state_id, game_img

    def handle_abnormal_state(self, game_state):
        """
        handle the abnormal state
        JUMP: it will try execute from game state to NEED_IDENTIFY state
        NEED_IDENTIFY: it is impossible to get this status since this status has no condition !!!
        """
        if self.game_config.game_state_dict[game_state].type == STATE_TYPE['JUMP']:
            return self.execute_to(game_state, RESERVED_STATE['NEED_IDENTIFY'])

    def judge_state(self, game_img, potential_status_name=None):
        result = None
        rect_list = None
        if potential_status_name:
            r = self.game_config.game_state_dict[potential_status_name].check_if_conditions_met(game_img)
            if r[0]:
                result = potential_status_name
                rect_list = r[1]

        if result is None:
            sorted_list = sorted(self.status_hit_dict.items(), key=lambda x: x[1])
            visited_set = set(potential_status_name)
            for s, _ in sorted_list:
                if s not in visited_set:
                    r = self.game_config.game_state_dict[s].check_if_conditions_met(game_img)
                    if r[0]:
                        result = s
                        rect_list = r[1]
                        break
                    visited_set.add(s)

            for game_state_id, game_state in self.game_config.game_state_dict.items():
                if game_state_id in visited_set:
                    continue
                visited_set.add(game_state_id)
                r = game_state.check_if_conditions_met(game_img)
                if r[0]:
                    result = game_state_id
                    rect_list = r[1]
                    break

        if result is not None:
            if result not in self.status_hit_dict:
                self.status_hit_dict[result] = 0
            self.status_hit_dict[result] += 1

            for rect in rect_list:
                cv2.rectangle(game_img, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 0), 2)
            self.screenshot_status_sure.emit({'screenshot': game_img})
        return result

    def execute_action(self, game_state: GameState, game_action: GameAction):
        self.action_executed.emit(game_action.name)
        game_img = self.get_screenshot()
        if game_state.type == STATE_TYPE['NORMAL'] or game_state.type == STATE_TYPE['JUMP']:
            self.execute_click_action(game_action)
        elif game_state.type == STATE_TYPE['HORIZONTAL_SWIPE']:
            curr_img = game_img
            prev_img = None
            action_satisfied = game_action.check_if_condition_met(curr_img)
            direction_list = [DIRECTION['RIGHT'], DIRECTION['LEFT']]
            for direction in direction_list:
                logger.info('Trying to swipe to {0}'.format(direction))
                while not action_satisfied:
                    prev_img = curr_img
                    self.game_window.swipe(direction)
                    time.sleep(0.5)
                    logger.info('swipe finished')
                    curr_img = self.get_screenshot()
                    action_satisfied = game_action.check_if_condition_met(curr_img)
                    if check_img_equal(curr_img, prev_img):  # swipe to the end
                        break
            if not action_satisfied:
                raise CannotFindActionBySwipe('Trying to find {0} in state {1} failed'
                                              .format(game_action.name, game_state.name))
            else:
                self.execute_click_action(game_action)

    def check_condition(self, game_action, curr_img):
        return game_action.check_if_condition_met(curr_img)

    def execute_click_action(self, game_action: GameAction):
        game_img = self.get_screenshot()
        area = game_action.get_action_area(game_img)
        if not area:
            logger.warning('Failed to execute {0} due to miss match'.format(game_action.name))
            return
        l, t, r, b = area
        logger.info('src_img shape: {0}'.format(game_img.shape))
        logger.info('action area: ({0}, {1}, {2}, {3})'.format(l, t, r, b))
        x = random.randint(l, r)
        y = random.randint(t, b)
        self.game_window.click(x, y)

    def get_screenshot_and_status(self, potential_status=None):
        img = self.get_screenshot()
        status_id = self.judge_state(img, potential_status)
        self.game_state_changed.emit({
            'status': self.game_config.game_state_dict[status_id] if status_id is not None else None
        })
        return img, status_id

    def get_screenshot(self):
        img = self.game_window.game_screenshot()
        self.screenshot_catched.emit({'screenshot': img})
        return img
