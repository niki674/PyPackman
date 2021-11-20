import curses
from frame import Frame
from game import State
from window import Window


class Menu(Frame):
    def __init__(self, window: Window = None, title='', items=None, sizeX: int = 3, sizeY: int = 3, defaultColorIndex=None, selectColorIndex=None):
        super().__init__(window, title, sizeX, sizeY, defaultColorIndex)
        if items is None:
            items = []
        self.items = items

        self.state = State.INIT
        self.oldWidth = 0
        self.oldHeight = 0

        self.selected = 0
        self.lastPos = -1
        self.lastKey = 0

        self.selectColorIndex = selectColorIndex if selectColorIndex is not None else self.window.getIndexColor(curses.COLOR_YELLOW, curses.COLOR_MAGENTA)

    def drawItems(self):
        self.window.scr.attron(curses.color_pair(self.defaultColorIndex))
        for i in range(len(self.items)):
            self.window.scr.addstr(self.startY + i + 1, self.startX + 1, self.items[i].center(self.sizeX - 2))
        self.window.scr.attroff(curses.color_pair(self.defaultColorIndex))

    def draw(self):
        self.window.checkSize()
        if self.oldWidth != self.window.width or self.oldHeight != self.window.height:
            self.window.scr.clear()
            self.oldWidth, self.oldHeight = self.window.width, self.window.height
            self.startX = (self.window.width - self.sizeX) // 2
            self.startY = (self.window.height - self.sizeY) // 2
            self.drawFrame()
            self.drawTitle()
            self.drawItems()

        if self.lastPos != self.selected:
            if self.lastPos >= 0:
                self.window.scr.attron(curses.color_pair(self.defaultColorIndex))
                self.window.scr.addstr(self.startY + self.lastPos + 1, self.startX + 1, self.items[self.lastPos].center(self.sizeX - 2))
                self.window.scr.attroff(curses.color_pair(self.defaultColorIndex))

            self.window.scr.attron(curses.color_pair(self.selectColorIndex))
            self.window.scr.addstr(self.startY + self.selected + 1, self.startX + 1, self.items[self.selected].center(self.sizeX - 2))
            self.window.scr.attroff(curses.color_pair(self.selectColorIndex))

            self.lastPos = self.selected

        self.window.scr.move(self.window.height - 1, self.window.width - 1)
        self.window.scr.refresh()

    def loop(self):
        while self.state == State.RUN:
            if self.lastKey == curses.KEY_DOWN:
                self.selected += 1
                if self.selected >= len(self.items):
                    self.selected = 0
            elif self.lastKey == curses.KEY_UP:
                self.selected -= 1
                if self.selected < 0:
                    self.selected = len(self.items) - 1
            elif self.lastKey == curses.KEY_ENTER or self.lastKey == ord('\n') or self.lastKey == ord('\r'):
                self.state = State.WIN
                break
            elif self.lastKey == curses.KEY_F10 or self.lastKey == ord('q') or self.lastKey == ord('Q') or self.lastKey == ord('й') or self.lastKey == ord('Й'):
                self.state = State.BREAK
                break

            self.draw()
            self.lastKey = self.window.scr.getch()

    def run(self):
        self.state = State.RUN
        self.window.scr.timeout(-1)
        self.lastPos = -1
        self.oldWidth = 0
        self.oldHeight = 0
        self.lastKey = 0
        self.loop()
        return self.selected if self.state == State.WIN else -1
