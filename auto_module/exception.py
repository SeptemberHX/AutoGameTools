class DatabaseIllegalException(Exception):
    def __init__(self, info):
        self.msg = info

    def __str__(self):
        return self.msg


class GameConfigIllegalException(Exception):
    def __init__(self, info):
        self.msg = info

    def __str__(self):
        return self.msg


class UnmatchedGameStateException(Exception):
    def __init__(self, info):
        self.msg = info

    def __str__(self):
        return self.msg


class NoPathFindException(Exception):
    def __init__(self, info):
        self.msg = info

    def __str__(self):
        return self.msg


class CannotMoveForwardException(Exception):
    def __init__(self, info):
        self.msg = info

    def __str__(self):
        return self.msg


class CannotFindActionBySwipe(Exception):
    def __init__(self, info):
        self.msg = info

    def __str__(self):
        return self.msg