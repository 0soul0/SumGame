import pygame as pg

BLACK = (0, 0, 0)
GRAY = (224, 224, 224)

# Initialize the pygame
pg.init()

# parameter
weight = 400
high = 750
slowSpeed = 0.01
fastSpeed = 10
spaceW = 1
track = weight / 4
index = 0
boxSpeed = slowSpeed
boxMoving = 0

# Box rect size
sizeBox = track - 4 * spaceW;

# Box
boxScore = [[], [], [], []]
boxX = [[], [], [], []]
boxY = [[], [], [], []]
positionY = [high - sizeBox, high - sizeBox, high - sizeBox, high - sizeBox]

# Create the screen
screen = pg.display.set_mode((weight, high))

# Background
background = pg.image.load('image/background.jpg')
background = pg.transform.scale(background, (weight, high))

# font
font = pg.font.Font('freesansbold.ttf', 32)


# background
def setBackground():
    screen.blit(background, (0, 0))
    for i in range(3):
        pg.draw.rect(screen, GRAY, pg.Rect((i + 1) * (track - spaceW), 0, 2 * spaceW, high))
    # pg.display.flip()


# Create Box
def box(score, x, y):
    pg.draw.rect(screen, color(score), pg.Rect(x, round(y), sizeBox, sizeBox))
    scoreStr = font.render(str(score), True, (255, 255, 255))
    textX=9*len(str(score));
    textY=16;
    screen.blit(scoreStr, (x + sizeBox / 2 - textX, y + sizeBox / 2 - textY))
    # pg.display.flip()


# Computer color by score
def color(score):
    green = 229 - score / 2 if 229 - score / 2 > 128 else 128;
    blue = 204 - score / 2 if 204 - score / 2 > 0 else 0;
    return 255, green, blue


# check box collision
def isCollision(score, y, x):
    delScore = 0;
    for i in range(len(score) - 1, 0, -1):
        if score[i] == score[i - 1]:
            score[i - 1] *= 2
            delScore += 1;
        #else:
            #y[i] -= sizeBox

    for i in range(delScore):
        del score[len(score)-1]
        del y[len(y)-1]
        del x[len(x)-1]

    return len(score) + 1


# Game Loop
running = True
while running:
    screen.fill(BLACK)
    setBackground()

    # Listen event
    for event in pg.event.get():
        # Close screen
        if event.type == pg.QUIT:
            running = False
        # Right Click
        if event.type == pg.MOUSEBUTTONDOWN:
            index = int(pg.mouse.get_pos()[0] / track)
            boxSpeed = fastSpeed

    # Show all of Box
    for i in range(len(boxScore)):
        for j in range(len(boxScore[i])):
            box(boxScore[i][j], boxX[i][j], boxY[i][j])

    # Box moving
    boxMoving += boxSpeed
    positionX = 2 * spaceW + index * track
    box(2, positionX, boxMoving)

    # initial box and save box
    if positionY[index] < boxMoving:
        boxScore[index].append(2)
        boxX[index].append(positionX)
        boxY[index].append(positionY[index])
        boxMoving = 0
        boxSpeed = slowSpeed

    number = isCollision(boxScore[index], boxY[index], boxX[index])
    # check box collision
    positionY[index] = high - number * sizeBox-number*2

    # update draw
    pg.display.flip()
    # update screen
    pg.display.update()
