from enum import Enum


class Task(Enum):
    WALKING = 1
    STEALING = 2
    NONE = 3


CURRENT_TASK = Task.NONE
