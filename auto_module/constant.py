# pre-defined state
RESERVED_STATE = {
    'NEED_IDENTIFY': '_NEED_IDENTIFY',  # we don't know current state. A judgement should be executed
}

# state type
STATE_TYPE = {
    'NORMAL': 'normal',
    'JUMP': 'jump',  # jump scare !!!
    'HORIZONTAL_SWIPE': 'horizontal_swipe',  # need to swipe horizontally to seek the position of the actions
    'VERTICAL_SWIPE': 'vertical_swipe',  # need to swipe vertically to seek the position of the actions
    'NEED_IDENTIFY': 'NEED_IDENTIFY',
}

DIRECT_STATE_TYPE = [
    STATE_TYPE['NORMAL'],
    STATE_TYPE['HORIZONTAL_SWIPE'],
    STATE_TYPE['VERTICAL_SWIPE'],
]


DIRECTION = {
    'LEFT': 0,
    'UP': 1,
    'RIGHT': 2,
    'DOWN': 3
}
