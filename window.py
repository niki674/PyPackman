import curses
from enum import Enum


class Graph(Enum):
    LineSmallHL = '╴'
    LineSmallHH = '─'
    LineSmallHR = '╶'
    LineSmallVU = '╵'
    LineSmallVV = '│'
    LineSmallVD = '╷'
    LineSmallUL = '┌'
    LineSmallUT = '┬'
    LineSmallUR = '┐'
    LineSmallLT = '├'
    LineSmallTT = '┼'
    LineSmallRT = '┤'
    LineSmallDL = '└'
    LineSmallDT = '┴'
    LineSmallDR = '┘'

    LineBoldHL = '╸'
    LineBoldHH = '━'
    LineBoldHR = '╺'
    LineBoldVU = '╹'
    LineBoldVV = '┃'
    LineBoldVD = '╻'
    LineBoldUL = '┏'
    LineBoldUT = '┳'
    LineBoldUR = '┓'
    LineBoldLT = '┣'
    LineBoldTT = '╋'
    LineBoldRT = '┫'
    LineBoldDL = '┗'
    LineBoldDT = '┻'
    LineBoldDR = '┛'


class Window:
    isInit = False
    screen = None
    colors = {}
    lastColor = 1

    def __init__(self, window: curses.window = None):
        self.__class__.init()
        self.scr = window if window is not None else self.__class__.screen
        self.width = 0
        self.height = 0
        self.checkSize()

    def checkSize(self):
        self.height, self.width = self.scr.getmaxyx()

    @classmethod
    def init(cls):
        if not cls.isInit:
            cls.screen = curses.initscr()
            curses.start_color()
            cls.isInit = True

    @classmethod
    def getIndexColor(cls, frontColor, backColor):
        key = '{}.{}'.format(frontColor, backColor)
        ind = cls.colors.get(key, -1)
        if ind < 0:
            ind = cls.lastColor
            curses.init_pair(ind, frontColor, backColor)
            cls.colors[key] = ind
            cls.lastColor += 1
        return ind
