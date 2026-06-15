from enum import Enum
import curses
import copy

# 2-dimentional vector object
class vec2:
    x: int = 0
    y: int = 0
    
    def copy(self: vec2) -> vec2:
        return copy.deepcopy(self)
    
    def __init__(self: vec2, X: int, Y: int):
        self.x = X
        self.y = Y

# NOTE: if you add aother mode, change how Buffer.change_mode() works
class modes(Enum):
    SEARCH = 0
    NAV = 1

# keeps a value between x and y
def clamp(n: int, x: int, y: int = 0) -> int:
    if n < x:
        return x
    if n > y:
        return y
    return n
    #return n % x

