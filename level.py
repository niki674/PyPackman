import curses
import os.path
from enum import Enum
from window import Graph


class Position:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def set(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y


class Direct(Enum):
    NO = 0
    HH = 1
    VV = 2
    UP = 4
    DW = 8
    LF = 16
    RG = 32


class Level:
    maxLevel = -1

    def __init__(self, game, num: int = 1):
        self.game = game
        self.num = num
        self.maxPos = Position()
        self.maze = []

        self.bountyCount = 0
        self.gamerStart = Position()
        self.enemyStart = []

        self.readLevel(self.num)

    def readLevel(self, num: int) -> bool:
        fname = 'levels/level-%0.2d.txt' % num
        f = open(fname, 'r')
        if f:
            self.maxPos.set()
            self.maze = []
            while True:
                s = f.readline()
                if not s or s.rstrip() == '':
                    break
                row = bytearray(s.rstrip(), 'utf-8')
                if self.maxPos.x < len(row):
                    self.maxPos.x = len(row)
                self.maze.append(row)
                self.maxPos.y += 1
            f.close()
            self.num = num

            self.bountyCount = 0
            self.gamerStart.set()
            self.enemyStart = []
            for y in range(len(self.maze)):
                for x in range(len(self.maze[y]), self.maxPos.x):
                    self.maze[y].append(ord(' '))
                for x in range(self.maxPos.x):
                    if self.maze[y][x] == ord('G'):
                        self.gamerStart.set(x, y)
                        self.maze[y][x] = ord(' ')
                    if self.maze[y][x] == ord('E'):
                        self.enemyStart.append(Position(x, y))
                        self.maze[y][x] = ord(' ')
                    if self.maze[y][x] == ord('*') or self.maze[y][x] == ord('8'):
                        self.bountyCount += 1
            return True
        return False

    def draw(self):
        self.game.window.scr.clear()
        self.game.window.scr.attron(curses.color_pair(self.game.defaultColorIndex))
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.maze[y][x] != ord('+') and self.maze[y][x] != ord('-') and self.maze[y][x] != ord('|'):
                    self.game.window.scr.addstr(self.game.startY + y, self.game.startX + x, chr(self.maze[y][x]))
                else:
                    direct = Direct.NO.value
                    if self.maze[y][x] == ord('-'):
                        direct |= Direct.HH.value
                    elif self.maze[y][x] == ord('|'):
                        direct |= Direct.VV.value
                    if y > 0 and (self.maze[y-1][x] == ord('+') or self.maze[y-1][x] == ord('-') or self.maze[y-1][x] == ord('|')):
                        direct |= Direct.UP.value
                    if x > 0 and (self.maze[y][x-1] == ord('+') or self.maze[y][x-1] == ord('-') or self.maze[y][x-1] == ord('|')):
                        direct |= Direct.LF.value
                    if y < len(self.maze)-1    and (self.maze[y+1][x] == ord('+') or self.maze[y+1][x] == ord('-') or self.maze[y+1][x] == ord('|')):
                        direct |= Direct.DW.value
                    if x < len(self.maze[y])-1 and (self.maze[y][x+1] == ord('+') or self.maze[y][x+1] == ord('-') or self.maze[y][x+1] == ord('|')):
                        direct |= Direct.RG.value
                    ch = ' '
                    if direct & Direct.UP.value:
                        if direct & Direct.DW.value:
                            if direct & Direct.LF.value:
                                if direct & Direct.RG.value:
                                    ch = Graph.LineBoldTT.value
                                else:
                                    ch = Graph.LineBoldRT.value
                            elif direct & Direct.RG.value:
                                ch = Graph.LineBoldLT.value
                            else:
                                ch = Graph.LineBoldVV.value
                        elif direct & Direct.LF.value:
                            if direct & Direct.RG.value:
                                ch = Graph.LineBoldDT.value
                            else:
                                ch = Graph.LineBoldDR.value
                        elif direct & Direct.RG.value:
                            ch = Graph.LineBoldDL.value
                        else:
                            ch = Graph.LineBoldVU.value
                    elif direct & Direct.DW.value:
                        if direct & Direct.LF.value:
                            if direct & Direct.RG.value:
                                ch = Graph.LineBoldUT.value
                            else:
                                ch = Graph.LineBoldUR.value
                        elif direct & Direct.RG.value:
                            ch = Graph.LineBoldUL.value
                        else:
                            ch = Graph.LineBoldVD.value
                    elif direct & Direct.LF.value:
                        if direct & Direct.RG.value:
                            ch = Graph.LineBoldHH.value
                        else:
                            ch = Graph.LineBoldHL.value
                    elif direct & Direct.RG.value:
                        ch = Graph.LineBoldHR.value
                    elif direct & Direct.HH.value:
                        ch = Graph.LineBoldHH.value
                    elif direct & Direct.VV.value:
                        ch = Graph.LineBoldVV.value
                    self.game.window.scr.addstr(self.game.startY + y, self.game.startX + x, ch)
        self.game.window.scr.attroff(curses.color_pair(self.game.defaultColorIndex))

    @classmethod
    def getMaxLevel(cls):
        if cls.maxLevel < 0:
            cls.maxLevel = 0
            i = 1
            while True:
                fname = 'levels/level-%0.2d.txt' % i
                if not os.path.isfile(fname):
                    break
                cls.maxLevel = i
                i += 1
        return cls.maxLevel
