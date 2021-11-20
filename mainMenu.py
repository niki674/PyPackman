from window import Window
from game import State, Game
from confirm import Confirm
from level import Level
from menu import Menu
from info import Info
from doc import Doc


class MainMenu(Menu):
    def __init__(self, window: Window = None):
        super().__init__(window, 'Игра Packman')
        self.items = [
            'Играть',
            'Правила',
            'Рекорды',
            'Создание уровней',
            'Автор',
            'Выход'
        ]
        self.sizeX = 20
        self.sizeY = len(self.items) + 2

    def startGame(self):
        maxLevel = Level.getMaxLevel()
        level = 1
        while level <= maxLevel:
            game = Game(self.window, level)
            state = game.run()
            self.window.scr.timeout(-1)
            confirm = None
            if state == State.WIN:
                level += 1
                if level > maxLevel:
                    confirm = Confirm(self.window, 'Поздравляем, Вы прошли все уровни!', 'Играть снова?', 38)
            elif state == State.LOOSE:
                confirm = Confirm(self.window, 'Вы проиграли!', 'Играть снова?', 17)
            elif state == State.BREAK:
                confirm = Confirm(self.window, 'Выход!', 'Может ещё поиграем?', 23)
            else:
                info = Info(self.window, '', [' Что то пошло не так :/ '], 26, 3)
                info.run()
                break
            if confirm is not None:
                if confirm.run():
                    level = 1
                else:
                    break

    def showRecords(self):
        pass

    def showInfo(self, title='', fileName='', sizeX: int = 3, sizeY: int = 3):
        info = Doc(self.window, title, fileName, sizeX, sizeY)
        info.run()

    def run(self):
        while self.state != State.BREAK and super().run() >= 0:
            if self.selected == 0:
                self.startGame()
            elif self.selected == 1:
                self.showInfo(self.items[self.selected], 'info/rules.txt', 40, 10)
            elif self.selected == 2:
                self.showRecords()
            elif self.selected == 3:
                self.showInfo(self.items[self.selected], 'info/editLevels.txt', 40, 10)
            elif self.selected == 4:
                self.showInfo(self.items[self.selected], 'info/author.txt', 40, 10)
            else:
                break
