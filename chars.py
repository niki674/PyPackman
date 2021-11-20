import curses
from game import State
from window import Window


class Chars:
    def __init__(self, window: Window = None):
        self.window = window if window is not None else Window()
        self.state = State.INIT
        self.startX = 0
        self.curPos = 9711
        self.lastKey = 0

        self.defaultColorIndex = self.window.getIndexColor(curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.selectColorIndex = self.window.getIndexColor(curses.COLOR_YELLOW, curses.COLOR_CYAN)

    def draw(self):
        self.window.scr.clear()
        self.window.scr.refresh()

        self.startX = int((self.window.width // 2) - 6)

        self.window.scr.attron(curses.color_pair(self.defaultColorIndex))
        for i in range(self.window.height - 2):
            msg = " %06d - %c " % (self.curPos - (self.window.height // 2) + i, self.curPos - (self.window.height // 2) + i)
            self.window.scr.addstr(1 + i, self.startX, msg)
        self.window.scr.attroff(curses.color_pair(self.defaultColorIndex))

        self.window.scr.attron(curses.color_pair(self.selectColorIndex))
        msg = " %06d - %c " % (self.curPos, self.curPos)
        self.window.scr.addstr(1 + (self.window.height // 2), self.startX, msg)
        self.window.scr.attroff(curses.color_pair(self.selectColorIndex))

        self.window.scr.refresh()

    def loop(self):
        while self.state == State.RUN:
            if self.lastKey == curses.KEY_DOWN:
                self.curPos += 1
            elif self.lastKey == curses.KEY_UP and self.curPos > 38:
                self.curPos -= 1
            elif self.lastKey == ord('q'):
                self.state = State.BREAK
                break

            self.draw()

            self.lastKey = self.window.scr.getch()

    def run(self):
        self.state = State.RUN
        self.window.scr.timeout(-1)
        self.loop()
        return self.state
