import pygame as pg

BLACK = (0, 0, 0)
GRAY = (224, 224, 224)

# Initialize the pygame
pg.init()

# parameter
weight = 400
high = 750
slowSpeed = 0.05
fastSpeed = 10
spaceW = 1
track = weight / 4
index = 0
boxSpeed = slowSpeed
boxMoving = 0


# Create the screen
screen = pg.display.set_mode((weight, high))

# Background
background = pg.image.load('image/background.jpg')
background = pg.transform.scale(background, (weight, high))

# font
font = pg.font.Font('freesansbold.ttf', 32)

# Box rect size
sizeBox = track - 4 * spaceW;


# background
def setBackground():
    screen.blit(background, (0, 0))
    for i in range(3):
        pg.draw.rect(screen, GRAY, pg.Rect((i + 1) * (track - spaceW), 0, 2 * spaceW, high))
    # pg.display.flip()


# Create Box
def box(score, x, y):
    pg.draw.rect(screen, color(score), pg.Rect(x, y, sizeBox, sizeBox))
    scoreStr = font.render(str(score), True, (255, 255, 255))
    screen.blit(scoreStr, (x + sizeBox / 2 - 10, y + sizeBox / 2 - 16))
    # pg.display.flip()


# Computer color by score
def color(score):
    green = 229 - score / 20 if 229 - score / 20 > 128 else 128;
    blue = 204 - score / 20 if 204 - score / 20 > 0 else 0;
    return 255, green, blue


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

    # box moving
    boxMoving += boxSpeed
    box(2, 2 * spaceW + index * track, boxMoving)
    # update draw
    pg.display.flip()
    # update screen
    pg.display.update()
