import random
import curses
from enum import Enum
from window import Window
from person import Gamer, Enemy
from level import Level


class State(Enum):
    INIT = 0
    RUN = 1
    BREAK = 2
    WIN = 3
    LOOSE = 4


class Game:
    def __init__(self, window: Window = None, numLevel: int = 1, bgColor=curses.COLOR_WHITE):
        random.seed()
        self.window = window if window is not None else Window()
        self.oldWidth = 0
        self.oldHeight = 0
        self.startX = 0
        self.startY = 0
        self.lastKey = 0

        self.bgColor = bgColor
        self.defaultColorIndex = self.window.getIndexColor(curses.COLOR_BLACK, self.bgColor)
        self.statusColorIndex = self.window.getIndexColor(curses.COLOR_BLACK, curses.COLOR_WHITE)

        self.level = Level(self, numLevel)
        self.score = 0
        self.lifeCount = 3
        self.state = State.INIT

        self.gamer = Gamer(self)
        self.gamer.pos.set(self.level.gamerStart.x, self.level.gamerStart.y)

        self.enemies = []
        for i in range(len(self.level.enemyStart)):
            e = Enemy(self)
            e.pos.set(self.level.enemyStart[i].x, self.level.enemyStart[i].y)
            e.nextDirect()
            self.enemies.append(e)

    def draw(self):
        self.window.checkSize()
        if self.oldWidth != self.window.width or self.oldHeight != self.window.height:
            self.window.scr.clear()
            self.oldWidth = self.window.width
            self.oldHeight = self.window.height
            self.startY = int(self.window.height - len(self.level.maze)) // 2
            self.startX = int(self.window.width - len(self.level.maze[0])) // 2
            self.level.draw()
            self.window.scr.refresh()

        self.gamer.step()
        self.gamer.show()

        for i in range(len(self.enemies)):
            self.enemies[i].step()
            self.enemies[i].show()

        statusbarstr = "F10 - выход | {}/{}/{}    ".format(self.score, self.level.bountyCount, self.lifeCount)[:self.window.width - 1]

        self.window.scr.attron(curses.color_pair(self.statusColorIndex))
        self.window.scr.addstr(self.window.height - 1, 0, statusbarstr)
        self.window.scr.attroff(curses.color_pair(self.statusColorIndex))

        self.window.scr.refresh()

    def loop(self):
        while self.state == State.RUN:
            if self.lastKey == curses.KEY_F10 or self.lastKey == ord('q') or self.lastKey == ord('Q') or self.lastKey == ord('й') or self.lastKey == ord('Й'):
                self.state = State.BREAK
                break
            if self.lastKey == ord('L'):
                self.lifeCount = 100
            elif self.lastKey == curses.KEY_DOWN:
                self.gamer.direct.set(0, 1)
            elif self.lastKey == curses.KEY_UP:
                self.gamer.direct.set(0, -1)
            elif self.lastKey == curses.KEY_RIGHT:
                self.gamer.direct.set(1, 0)
            elif self.lastKey == curses.KEY_LEFT:
                self.gamer.direct.set(-1, 0)

            self.draw()

            if self.level.bountyCount <= 0:
                self.state = State.WIN
            if self.lifeCount <= 0:
                self.state = State.LOOSE

            self.lastKey = self.window.scr.getch()

    def run(self):
        self.state = State.RUN
        self.window.scr.timeout(20)
        self.oldWidth = 0
        self.oldHeight = 0
        self.lastKey = 0
        self.loop()
        return self.state
