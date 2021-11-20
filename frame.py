import curses
from window import Window, Graph


class Frame:
    def __init__(self, window: Window = None, title='', sizeX: int = 3, sizeY: int = 3, defaultColorIndex=None):
        self.window = window if window is not None else Window()
        self.title = title
        self.sizeX = sizeX
        self.sizeY = sizeY

        self.startX = 0
        self.startY = 0

        self.defaultColorIndex = defaultColorIndex if defaultColorIndex is not None else self.window.getIndexColor(curses.COLOR_BLACK, curses.COLOR_WHITE)

    def drawFrame(self):
        self.window.scr.attron(curses.color_pair(self.defaultColorIndex))
        for i in range(self.sizeX - 2):
            self.window.scr.addstr(self.startY,                  self.startX + i + 1, Graph.LineSmallHH.value)
            self.window.scr.addstr(self.startY + self.sizeY - 1, self.startX + i + 1, Graph.LineSmallHH.value)
        for i in range(self.sizeY - 2):
            self.window.scr.addstr(self.startY + i + 1, self.startX,                  Graph.LineSmallVV.value)
            self.window.scr.addstr(self.startY + i + 1, self.startX + self.sizeX - 1, Graph.LineSmallVV.value)

        self.window.scr.addstr(self.startY,                  self.startX,                  Graph.LineSmallUL.value)
        self.window.scr.addstr(self.startY,                  self.startX + self.sizeX - 1, Graph.LineSmallUR.value)
        self.window.scr.addstr(self.startY + self.sizeY - 1, self.startX,                  Graph.LineSmallDL.value)
        self.window.scr.addstr(self.startY + self.sizeY - 1, self.startX + self.sizeX - 1, Graph.LineSmallDR.value)
        self.window.scr.attroff(curses.color_pair(self.defaultColorIndex))

    def drawTitle(self):
        if self.title != '':
            self.window.scr.attron(curses.color_pair(self.defaultColorIndex))
            self.window.scr.addstr(self.startY, self.startX + (self.sizeX - len(self.title) - 2) // 2, (' %s ' % self.title))
            self.window.scr.attroff(curses.color_pair(self.defaultColorIndex))
