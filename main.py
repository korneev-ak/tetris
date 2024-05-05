import random
from copy import *

from pygame import *
from pygame.draw import *


def putTheFigure():
    for i in figure:
        gridStats[i.y // tileSize][i.x // tileSize] = color
    return spawnFigure(-1)


def moveDown(currentFigure):
    figureCopy = deepcopy(currentFigure)
    [i.move_ip(0, tileSize) for i in currentFigure]
    if isCollide() == True:
        currentFigure[:] = deepcopy(figureCopy)
        return putTheFigure()


def isCollide():
    f = False
    for i in figure:
        for y in range(len(gridStats)):
            for x in range(len(gridStats[y])):
                if i.x == x * tileSize and i.y == y * tileSize and gridStats[y][
                    x] != None or i.y >= tileSize * tileCountVer or i.x not in range(0, tileCountHor * tileSize):
                    f = True
                    break
    if f == True:
        return True
    else:
        return False


# spawns figures from list "figures" by index
# figuresIndex = -1 => random
def spawnFigure(figuresIndex: int):
    global color, nextColor, figureInd, nextFigureInd
    figureInd = nextFigureInd
    figure[:] = deepcopy(nextFigure)
    color = deepcopy(nextColor)
    nextFigure.clear()
    if figuresIndex == -1:
        nextFigureInd = random.randint(0, len(figures) - 1)
        for i in figures[figureInd]:
            nextFigure.append(
                Rect(tileCountHor // 2 * tileSize + i[0] * tileSize, i[1] * tileSize, tileSize - 1, tileSize - 1))

    else:
        for i in figures[figuresIndex]:
            nextFigure.append(
                Rect(tileCountHor // 2 * tileSize + i[0] * tileSize, i[1] * tileSize, tileSize - 1, tileSize - 1))
    nextColor = colors[random.randint(0, len(colors) - 1)]

    # ends the game if just spawned figure is blocked
    if isCollide():
        return False


def moveSide(direction: int):  # direction= 1 or -1
    figureCopy = deepcopy(figure)
    [i.move_ip(tileSize * direction, 0) for i in figure]
    if isCollide():
        figure[:] = figureCopy
        return True
    return False


def getHighestPoses():
    maxes = [tileCountVer for x in range(tileCountHor)]
    for i in range(len(gridStats)):
        for a in range(len(maxes)):
            if maxes[a] == tileCountVer and gridStats[i][a] != None: maxes[a] = i
    return maxes


init()
clock = time.Clock()

updateTime = 60

height = 800
width = 1920

tileCountVer = 14
tileCountHor = 9

tileSize = 40

figures = [
    [(0, 0), (1, 0), (-1, 0), (2, 0)],
    [(0, 0), (1, 0), (-1, 0), (2, 0)],
    [(0, 1), (1, 0), (-1, 0), (0, 0)],
    [(0, 0), (1, 0), (-1, 0), (1, 1)],
    [(0, 1), (1, 1), (-1, 1), (1, 0)],
    [(0, 0), (1, 1), (-1, 0), (0, 1)],
    [(0, 0), (0, -1), (-1, 0), (1, -1)],
    [(0, 0), (1, -1), (0, -1), (1, 0)]
]
colors = [
    (200, 0, 0),
    (0, 200, 0),
    (0, 0, 200),
    (200, 200, 0),
    (0, 200, 200),
    (200, 0, 200)
]

screen = display.set_mode((width, height))

grid = [Rect(x * tileSize, y * tileSize, tileSize, tileSize) for x in range(tileCountHor) for y in range(tileCountVer)]
gridStats = [[None for y in range(tileCountHor)] for x in range(tileCountVer)]

figure = []
color = colors[random.randint(0, len(colors) - 1)]
figureInd = random.randint(0, len(figures) - 1)
for i in figures[figureInd]:
    figure.append(Rect(tileCountHor // 2 * tileSize + i[0] * tileSize, i[1] * tileSize, tileSize - 1, tileSize - 1))

nextFigure = []
nextFigureInd = random.randint(0, len(figures) - 1)
for i in figures[nextFigureInd]:
    nextFigure.append(Rect(tileCountHor // 2 * tileSize + i[0] * tileSize, i[1] * tileSize, tileSize - 1, tileSize - 1))
nextColor = colors[random.randint(0, len(colors) - 1)]

fallsPerSec = 1.2
framesToFall = updateTime / fallsPerSec
framesTillFall = updateTime

run = True
points = 0
while run:

    screen.fill((30, 30, 30))
    for ev in event.get():
        if ev.type == QUIT:
            quit()
        if ev.type == KEYDOWN:
            if ev.key == K_DOWN:
                moveDown(figure)
            if ev.key == K_UP:
                figureCopy = deepcopy(figure)
                center = deepcopy(figure[0])
                for i in range(len(figure)):
                    x = figure[i].y - center.y
                    y = figure[i].x - center.x
                    figure[i].x = center.x - x
                    figure[i].y = center.y + y
                if isCollide() == True:
                    figure = figureCopy
            figureCopy = deepcopy(figure)
            if ev.key == K_RIGHT:
                moveSide(1)
            if ev.key == K_LEFT:
                moveSide(-1)

    if framesTillFall <= 0:
        if moveDown(figure) == False:
            run = False
        framesTillFall = framesToFall

    # destroying filled rows
    filledRows = 0
    ind = len(gridStats) - 1
    while (ind != -1):
        flag = False
        if gridStats[ind].count(None) == 0:
            filledRows += 1
            flag = True
            for a in range(ind, 0, -1):
                gridStats[a] = deepcopy(gridStats[a - 1])
        if flag == False: ind -= 1

    points += (filledRows ** 2)

    for i in nextFigure:
        rect(screen, nextColor,
             Rect(i.x - (tileCountHor // 2) * tileSize + tileCountHor * tileSize + tileSize * 1, i.y + tileSize,
                  tileSize, tileSize))

    [rect(screen, (color), i) for i in figure]
    for y in range(len(gridStats)):
        for x in range(len(gridStats[0])):
            if gridStats[y][x] != None:
                rect(screen, gridStats[y][x], Rect(x * tileSize, y * tileSize, tileSize, tileSize))
    [rect(screen, (200, 200, 200), IamTile, 1) for IamTile in grid]
    framesTillFall -= 1

    myFont = font.SysFont(None, 24)

    screen.blit(myFont.render("points: " + str(points), True, (255, 0, 0)),
                (tileCountHor * tileSize + tileSize, tileCountVer * tileSize // 2))
    screen.blit(myFont.render("gained points = (number of detroyed rows at a time)^2", True, (0, 255, 0)),
                (tileCountHor * tileSize + 5 * tileSize, tileSize))

    display.flip()
    clock.tick(updateTime)
myFont = font.SysFont(None, 50)
screen.blit(myFont.render("game over", True, (255, 0, 0)),
            (tileCountHor * tileSize + tileSize, tileSize * tileCountVer - tileSize))
display.flip()

while True:
    for ev in event.get():
        if ev.type == QUIT:
            quit()
