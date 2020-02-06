# encoding: utf-8
import time

from auto_module.exception import UnmatchedGameStateException, CannotMoveForwardException
from auto_module.image import GameWindow
from auto_module.model import GameConfig, GameAction, RESERVED_STATE, STATE_TYPE
from auto_module.logger import get_logger
import cv2

import random
import platform

logger = get_logger('executor')
SCT_INTERVAL = 1


def debug_judge_state(game_config: GameConfig, game_window: GameWindow):
    while True:
        game_img = game_window.game_screenshot()
        state_id = judge_state(game_img, game_config)
        logger.info('state from screenshot: {0}'.format(state_id))
        time.sleep(1)


def execute_to_loop(game_config: GameConfig, from_state: str, to_state: str, game_window: GameWindow):
    while True:
        execute_to(game_config, from_state, to_state, game_window)


def execute_to(game_config: GameConfig, from_state: str, to_state: str, game_window: GameWindow):
    """
    This function will try to move from the from_state to to_state
    from_state != real current state is allowed
    the state when this function finishes is guaranteed to be to_state
    """
    logger.info('In execute_to({0}, {1})'.format(from_state, to_state))
    action_list = game_config.get_shortest_action_list_dijkstra(from_state, to_state)
    curr_state = from_state
    for action in action_list:
        logger.info('trying to move from {0} to {1}...'.format(curr_state, action.successor))
        state_id, game_img = get_valid_state(game_config, game_window)

        while state_id != curr_state and game_config.game_state_dict[state_id].type != STATE_TYPE['NORMAL']:
            state_id, game_img = handle_abnormal_state(game_config, game_window, state_id)

        while state_id != curr_state:
            logger.info('current status not match, trying to correct it')
            state_id, game_img = execute_to(game_config, state_id, curr_state, game_window)

        # do the action to move on to the next state
        logger.info('move from {0} to {1}'.format(curr_state, action.successor))
        execute_action(action, game_img, game_window)
        curr_state = action.successor
        time.sleep(SCT_INTERVAL)
    # make sure the state after executing equals to to_state
    state_id, game_img = get_valid_state(game_config, game_window)
    while to_state != RESERVED_STATE['NEED_IDENTIFY'] and state_id != to_state:
        if game_config.game_state_dict[state_id].type != STATE_TYPE['NORMAL']:
            state_id, game_img = handle_abnormal_state(game_config, game_window, state_id)
        else:
            raise CannotMoveForwardException(state_id)
    return state_id, game_img


def get_valid_state(game_config: GameConfig, game_window: GameWindow):
    """
    Get a valid state from current screenshot.
    If current screenshot's status is invalid, it will loop
    """
    game_img = game_window.game_screenshot()
    state_id = judge_state(game_img, game_config)
    logger.info('state from screenshot: {0}'.format(state_id))
    while state_id is None:
        game_img = game_window.game_screenshot()
        state_id = judge_state(game_img, game_config)
        logger.info('state from screenshot: {0}'.format(state_id))
        time.sleep(SCT_INTERVAL)
    return state_id, game_img


def handle_abnormal_state(game_config: GameConfig, game_window: GameWindow, game_state):
    """
    handle the abnormal state
    JUMP: it will try execute from game state to NEED_IDENTIFY state
    NEED_IDENTIFY: it is impossible to get this status since this status has no condition !!!
    """
    if game_config.game_state_dict[game_state].type == STATE_TYPE['JUMP']:
        return execute_to(game_config, game_state, RESERVED_STATE['NEED_IDENTIFY'], game_window)


def judge_state(game_img, game_config: GameConfig):
    for game_state_id, game_state in game_config.game_state_dict.items():
        if game_state.check_if_conditions_met(game_img):
            return game_state_id
    return None


def execute_action(game_action: GameAction, game_img, game_window: GameWindow):
    l, t, r, b = game_action.get_action_area(game_img)
    cv2.rectangle(game_img, (l, t), (r, b), (7, 249, 151), 2)
    logger.info('src_img shape: {0}'.format(game_img.shape))

    # cv2.imshow("announcement", game_img)
    # # Press "q" to quit
    # if cv2.waitKey(0) & 0xFF == ord("q"):
    #     cv2.destroyAllWindows()

    logger.info('action area: ({0}, {1}, {2}, {3})'.format(l, t, r, b))
    x = random.randint(l, r)
    y = random.randint(t, b)
    game_window.click(x, y)


def transform_to_actual_pos(w_x, w_y, x, y):
    return w_x + x, w_y + y


def get_windows_info(window_title):
    sys_name = platform.system()
    if sys_name == 'Linux':
        from Xlib.display import Display
        display = Display()
        root = display.screen().root
        for w in root.query_tree().children:
            if w.get_wm_name() == window_title:
                geo = w.get_geometry()
                print(geo.x, geo.y, geo.width, geo.height)


if __name__ == '__main__':
    get_windows_info('AutoGameTools : python3')
