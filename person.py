import time
import random
import curses
from level import Position
from window import Window


class Person:
    def __init__(self, game, skin: str, color=curses.COLOR_BLACK, speed=0.5, skinSpeed=0.2):
        self.game = game
        self.skin = skin
        self.indSkin = 0
        self.upSkinTm = 0
        self.indColor = Window.getIndexColor(color, self.game.bgColor)

        self.pos = Position(-1, -1)
        self.direct = Position()
        self.nextPos = Position()
        self.speed = speed
        self.skinSpeed = skinSpeed
        self.lastStepTm = 0

    def nextSkin(self):
        if len(self.skin) > 1:
            tm = time.time()
            if tm - self.upSkinTm > self.skinSpeed:
                self.upSkinTm = tm
                self.indSkin += 1
                if self.indSkin >= len(self.skin):
                    self.indSkin = 0

    def show(self):
        self.nextSkin()
        self.game.window.scr.attron(curses.color_pair(self.indColor))
        self.game.window.scr.addstr(self.game.startY + self.pos.y, self.game.startX + self.pos.x, self.skin[self.indSkin])
        self.game.window.scr.attroff(curses.color_pair(self.indColor))

    def step(self):
        if self.direct.x != 0 or self.direct.y != 0:
            tm = time.time()
            if tm - self.lastStepTm > self.speed:
                self.lastStepTm = tm

                self.nextPos.x = self.pos.x + self.direct.x
                self.nextPos.y = self.pos.y + self.direct.y
                if self.nextPos.y < 0:
                    self.nextPos.y = len(self.game.level.maze) - 1
                elif self.nextPos.y >= len(self.game.level.maze):
                    self.nextPos.y = 0
                if self.nextPos.x < 0:
                    self.nextPos.x = len(self.game.level.maze[self.nextPos.y]) - 1
                elif self.nextPos.x >= len(self.game.level.maze[self.nextPos.y]):
                    self.nextPos.x = 0
                self.move()

    def checkMove(self) -> bool:
        if self.game.level.maze[self.nextPos.y][self.nextPos.x] != ord('|')\
                and self.game.level.maze[self.nextPos.y][self.nextPos.x] != ord('-')\
                and self.game.level.maze[self.nextPos.y][self.nextPos.x] != ord('+'):
            return True
        self.direct.set()
        return False

    def move(self) -> bool:
        if self.checkMove():
            if self.pos.x >= 0 and self.pos.y >= 0:
                self.game.window.scr.attron(curses.color_pair(self.game.defaultColorIndex))
                self.game.window.scr.addstr(self.game.startY + self.pos.y, self.game.startX + self.pos.x, chr(self.game.level.maze[self.pos.y][self.pos.x]))
                self.game.window.scr.attroff(curses.color_pair(self.game.defaultColorIndex))
            self.pos.set(self.nextPos.x, self.nextPos.y)
            self.show()
            return True
        return False


class Gamer(Person):
    # def __init__(self, game, skin: str = '⚇ᗢᗣᗤᗧ', color=curses.COLOR_MAGENTA, speed=0.2, skinSpeed=0.3):
    def __init__(self, game, skin: str = 'Oo', color=curses.COLOR_MAGENTA, speed=0.2, skinSpeed=0.3):
        super().__init__(game, skin, color, speed, skinSpeed)

    def checkMove(self) -> bool:
        if self.game.level.maze[self.nextPos.y][self.nextPos.x] == ord('='):
            self.direct.set()
            return False
        return super().checkMove()

    def move(self):
        if self.checkMove():
            if self.game.level.maze[self.nextPos.y][self.nextPos.x] == ord('*'):
                self.game.score += 1
                self.game.level.bountyCount -= 1
                self.game.level.maze[self.nextPos.y][self.nextPos.x] = ord(' ')
            if self.game.level.maze[self.nextPos.y][self.nextPos.x] == ord('8'):
                self.game.score += 10
                self.game.level.bountyCount -= 1
                self.game.level.maze[self.nextPos.y][self.nextPos.x] = ord(' ')
            super().move()


class Enemy(Person):
    # def __init__(self, game, skin: str = '-\\|/', color=curses.COLOR_RED, speed=0.4, skinSpeed=0.1):
    def __init__(self, game, skin: str = '', color=curses.COLOR_RED, speed=0.3, skinSpeed=0.1):
        super().__init__(game, skin, color, speed, skinSpeed)

    def nextDirect(self):
        x = random.randint(-1, 1)
        if x == 0:
            y = random.randint(0, 1)
            if y == 0:
                y = -1
        else:
            y = 0
        if x == self.direct.x and y == self.direct.y:
            self.nextDirect()
        else:
            self.direct.set(x, y)

    def checkMove(self) -> bool:
        canMove = super().checkMove()
        self.nextDirect()
        return canMove

    def move(self):
        if self.checkMove():
            if self.game.gamer.pos.x == self.nextPos.x and self.game.gamer.pos.y == self.nextPos.y:
                self.game.gamer.nextPos.set(self.game.level.gamerStart.x, self.game.level.gamerStart.y)
                self.game.gamer.move()
                self.game.lifeCount -= 1
            super().move()
