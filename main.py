import random
from copy import *

from pygame import *
from pygame.draw import *

import pygame_UI as UI

class Tetris:
    def __init__(self):
        init()
        self.clock = time.Clock()

        self.updateTime = 60

        self.height = 800
        self.width = 1920

        self.tileCountVer = 14
        self.tileCountHor = 9

        self.tileSize = 40

        self.figures = [
            [(0, 0), (1, 0), (-1, 0), (2, 0)],
            [(0, 0), (1, 0), (-1, 0), (2, 0)],
            [(0, 1), (1, 0), (-1, 0), (0, 0)],
            [(0, 0), (1, 0), (-1, 0), (1, 1)],
            [(0, 1), (1, 1), (-1, 1), (1, 0)],
            [(0, 0), (1, 1), (-1, 0), (0, 1)],
            [(0, 0), (0, -1), (-1, 0), (1, -1)],
            [(0, 0), (1, -1), (0, -1), (1, 0)]
        ]
        self.colors = [
            (200, 0, 0),
            (0, 200, 0),
            (0, 0, 200),
            (200, 200, 0),
            (0, 200, 200),
            (200, 0, 200)
        ]

        self.screen = display.set_mode((self.width, self.height))

        self.grid = [Rect(x * self.tileSize, y * self.tileSize, self.tileSize, self.tileSize) for x in range(self.tileCountHor) for y in
                range(self.tileCountVer)]
        self.gridStats = [[None for y in range(self.tileCountHor)] for x in range(self.tileCountVer)]

        self.figure = []
        self.color = self.colors[random.randint(0, len(self.colors) - 1)]
        self.figureInd = random.randint(0, len(self.figures) - 1)
        for i in self.figures[self.figureInd]:
            self.figure.append(
                Rect(self.tileCountHor // 2 * self.tileSize + i[0] * self.tileSize, i[1] * self.tileSize, self.tileSize - 1, self.tileSize - 1))

        self.nextFigure = []
        self.nextFigureInd = random.randint(0, len(self.figures) - 1)
        for i in self.figures[self.nextFigureInd]:
            self.nextFigure.append(
                Rect(self.tileCountHor // 2 * self.tileSize + i[0] * self.tileSize, i[1] * self.tileSize, self.tileSize - 1, self.tileSize - 1))
        self.nextColor = self.colors[random.randint(0, len(self.colors) - 1)]

        self.fallsPerSec = 1.2
        self.framesToFall = self.updateTime / self.fallsPerSec
        self.framesTillFall = self.updateTime

        self.run = True
        self.points = 0
        self.points_display = UI.Text(self.screen, '123', color=Color(250, 250, 250), pos=((self.tileCountHor + 2) * self.tileSize, 200),
                                 isIndependent=True)
        self.points_gain_rule = UI.Text(self.screen, 'gained points = (number of rows destroyed at a time)^2',
                                   color=Color(250, 250, 250), size=30, pos=((self.tileCountHor + 11) * self.tileSize, 20),
                                   isIndependent=True)

    def putTheFigure(self):
        for i in self.figure:
            self.gridStats[i.y // self.tileSize][i.x // self.tileSize] = Color(self.color)
        return self.spawnFigure(-1)


    def moveDown(self,currentFigure):
        figureCopy = deepcopy(currentFigure)
        [i.move_ip(0, self.tileSize) for i in currentFigure]
        if self.isCollide() == True:
            currentFigure[:] = deepcopy(figureCopy)
            return self.putTheFigure()


    def isCollide(self):
        f = False
        for i in self.figure:
            for y in range(len(self.gridStats)):
                for x in range(len(self.gridStats[y])):
                    if i.x == x * self.tileSize and i.y == y * self.tileSize and self.gridStats[y][
                        x] != None or i.y >= self.tileSize * self.tileCountVer or i.x not in range(0, self.tileCountHor * self.tileSize):
                        f = True
                        break
        if f == True:
            return True
        else:
            return False


    # spawns figures from list "figures" by index
    # if figuresIndex = -1 => random
    def spawnFigure(self,figuresIndex: int):
        global color, nextColor, figureInd, nextFigureInd
        self.figureInd = self.nextFigureInd
        self.figure[:] = deepcopy(self.nextFigure)
        self.color = deepcopy(self.nextColor)
        self.nextFigure.clear()
        if figuresIndex == -1:
            self.nextFigureInd = random.randint(0, len(self.figures) - 1)
            for i in self.figures[self.figureInd]:
                self.nextFigure.append(
                    Rect(self.tileCountHor // 2 * self.tileSize + i[0] * self.tileSize, i[1] * self.tileSize, self.tileSize - 1, self.tileSize - 1))

        else:
            for i in self.figures[figuresIndex]:
                self.nextFigure.append(
                    Rect(self.tileCountHor // 2 * self.tileSize + i[0] * self.tileSize, i[1] * self.tileSize, self.tileSize - 1, self.tileSize - 1))
        self.nextColor = self.colors[random.randint(0, len(self.colors) - 1)]

        # ends the game if just spawned figure is blocked
        if self.isCollide():
            return False


    def moveSide(self,direction: int):  # direction= 1 or -1
        figureCopy = deepcopy(self.figure)
        [i.move_ip(self.tileSize * direction, 0) for i in self.figure]
        if self.isCollide():
            self.figure[:] = figureCopy
            return True
        return False


    def getHighestPoses(self):
        maxes = [self.tileCountVer for x in range(self.tileCountHor)]
        for i in range(len(self.gridStats)):
            for a in range(len(maxes)):
                if maxes[a] == self.tileCountVer and self.gridStats[i][a] != None: maxes[a] = i
        return maxes


    def run_game(self):
        while self.run:

            self.screen.fill((30, 30, 30))
            for ev in event.get():
                if ev.type == QUIT:
                    quit()
                if ev.type == KEYDOWN:
                    if ev.key == K_DOWN:
                        self.moveDown(self.figure)
                    if ev.key == K_UP:
                        self.figureCopy = deepcopy(self.figure)
                        center = deepcopy(self.figure[0])
                        for i in range(len(self.figure)):
                            x = self.figure[i].y - center.y
                            y = self.figure[i].x - center.x
                            self.figure[i].x = center.x - x
                            self.figure[i].y = center.y + y
                        if self.isCollide() == True:
                            self.figure = self.figureCopy
                    self.figureCopy = deepcopy(self.figure)
                    if ev.key == K_RIGHT:
                        self.moveSide(1)
                    if ev.key == K_LEFT:
                        self.moveSide(-1)

            if self.framesTillFall <= 0:
                if self.moveDown(self.figure) == False:
                    self.run = False
                self.framesTillFall = self.framesToFall

            # destroying filled rows
            filledRows = 0
            ind = len(self.gridStats) - 1
            while (ind != -1):
                flag = False
                if self.gridStats[ind].count(None) == 0:
                    filledRows += 1
                    flag = True
                    for a in range(ind, 0, -1):
                        self.gridStats[a] = deepcopy(self.gridStats[a - 1])
                if flag == False: ind -= 1

            self.points += (filledRows ** 2)

            for i in self.nextFigure:
                rect(self.screen, self.nextColor,
                     Rect(i.x - (self.tileCountHor // 2) * self.tileSize + self.tileCountHor * self.tileSize + self.tileSize * 1, i.y + self.tileSize,
                          self.tileSize, self.tileSize))

            [rect(self.screen, (self.color), i) for i in self.figure]
            for y in range(len(self.gridStats)):
                for x in range(len(self.gridStats[0])):
                    if self.gridStats[y][x] != None:
                        rect(self.screen, self.gridStats[y][x], Rect(x * self.tileSize, y * self.tileSize, self.tileSize, self.tileSize))
            [rect(self.screen, (200, 200, 200), IamTile, 1) for IamTile in self.grid]
            self.framesTillFall -= 1


            self.points_display.setText(f"points: {self.points}")
            UI.Widget.updateWidgets(event.get())
            UI.Text.update()
            display.flip()
            self.clock.tick(self.updateTime)
if __name__ == '__main__':
    Tetris().run_game()
"""
myFont = font.SysFont(None, 50)
screen.blit(myFont.render("game over", True, (255, 0, 0)),
            (tileCountHor * tileSize + tileSize, tileSize * tileCountVer - tileSize))
display.flip()

while True:
    for ev in event.get():
        if ev.type == QUIT:
            quit()
"""