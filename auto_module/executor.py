from auto_module.exception import UnmatchedGameStateException
from auto_module.image import get_game_frame
from auto_module.model import GameConfig, GameAction
from pymouse import PyMouse
from .logger import get_logger
import cv2

import random
import platform

mouse = PyMouse()
logger = get_logger('executor')

game_window = {
    'x': 0,
    'y': 60,
    'width': 3100,
    'height': 2000
}


def execute_to(game_config: GameConfig, from_state: str, to_state: str):
    action_list = game_config.get_shortest_action_list(from_state, to_state)
    curr_state = from_state
    for action in action_list:
        # check if the current state matches the state in the action list
        game_img = get_game_frame(**game_window)
        # cv2.imshow('s', game_img)
        # if cv2.waitKey(0) & 0xFF == ord("q"):
        #     cv2.destroyAllWindows()

        if not game_config.check_current_state(curr_state, game_img):
            raise UnmatchedGameStateException(action)

        # do the action to move on to the next state
        execute_action(action, game_img)
        curr_state = action.successor


def execute_action(game_action: GameAction, game_img):
    l, t, r, b = game_action.get_action_area(game_img)
    logger.info('({0}, {1}, {2}, {3})'.format(l, t, r, b))
    x = random.randint(l, r)
    y = random.randint(t, b)
    t_x, t_y = transform_to_actual_pos(game_window['x'], game_window['y'], x, y)
    mouse.click(t_x, t_y)


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
