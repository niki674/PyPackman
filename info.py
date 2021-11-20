import curses
from window import Window
from frame import Frame
from game import State


class Info(Frame):
    def __init__(self, window: Window = None, title='', text=None, sizeX: int = 3, sizeY: int = 3, defaultColorIndex=None):
        super().__init__(window, title, sizeX, sizeY, defaultColorIndex)
        if text is None:
            text = []
        self.text = text
        self.maxWidth = 0

        self.state = State.INIT
        self.oldWidth = 0
        self.oldHeight = 0
        self.lastX = -1
        self.lastY = -1
        self.textX = 0
        self.textY = 0
        self.lastKey = 0

        self.checkText()

    def checkText(self):
        self.maxWidth = 0
        for i in range(len(self.text)):
            if len(self.text[i]) > self.maxWidth:
                self.maxWidth = len(self.text[i])
            self.text.append(self.text[i])

    def drawText(self):
        self.window.scr.attron(curses.color_pair(self.defaultColorIndex))
        for i in range(self.sizeY - 2):
            if self.textY + i < len(self.text):
                self.window.scr.addstr(self.startY + i + 1, self.startX + 1, self.text[self.textY + i][self.textX:self.textX+self.sizeX-2].ljust(self.sizeX - 2))
            else:
                self.window.scr.addstr(self.startY + i + 1, self.startX + 1, ' '.ljust(self.sizeX - 2))
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
            self.window.scr.attron(curses.color_pair(self.defaultColorIndex))
            self.window.scr.addstr(self.startY + self.sizeY - 1, self.startX + 1, ' F10 - выход ')
            self.window.scr.attroff(curses.color_pair(self.defaultColorIndex))

        if self.lastX != self.textX or self.lastY != self.textY:
            self.drawText()
            self.lastX = self.textX
            self.lastY = self.textY

        self.window.scr.move(self.window.height - 1, self.window.width - 1)
        self.window.scr.refresh()

    def loop(self):
        while self.state == State.RUN:
            if self.lastKey == curses.KEY_UP and self.lastY - 1 >= 0:
                self.textY -= 1
            elif self.lastKey == curses.KEY_DOWN and self.lastY + self.sizeY - 2 < len(self.text):
                self.textY += 1
            if self.lastKey == curses.KEY_LEFT and self.lastX - 1 >= 0:
                self.textX -= 1
            elif self.lastKey == curses.KEY_RIGHT and self.lastX + self.sizeX - 2 < self.maxWidth:
                self.textX += 1
            elif self.lastKey == curses.KEY_F10 or self.lastKey == ord('q') or self.lastKey == ord('Q') or self.lastKey == ord('й') or self.lastKey == ord('Й'):
                self.state = State.BREAK
                break

            self.draw()
            self.lastKey = self.window.scr.getch()

    def run(self):
        self.state = State.RUN
        self.window.scr.timeout(-1)
        self.oldWidth = 0
        self.oldHeight = 0
        self.lastKey = 0
        self.textX = 0
        self.textY = 0
        self.loop()
        return self.state
