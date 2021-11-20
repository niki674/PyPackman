from window import Window
from info import Info


class Doc(Info):
    def __init__(self, window: Window = None, title='', fileName='', sizeX: int = 3, sizeY: int = 3, defaultColorIndex=None):
        super().__init__(window, title, [], sizeX, sizeY, defaultColorIndex)
        self.fileName = fileName
        self.readFile()

    def readFile(self):
        f = open(self.fileName, 'r')
        if f:
            self.textX = 0
            self.textY = 0
            self.text = []
            self.maxWidth = 0
            while True:
                s = f.readline()
                if not s:
                    break
                s = s.rstrip()
                if len(s) > self.maxWidth:
                    self.maxWidth = len(s)
                self.text.append(s)
            f.close()
