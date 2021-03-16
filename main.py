import math
import random

import pygame as pg

BLACK = (0, 0, 0)
GRAY = (224, 224, 224)
WHITE = (255, 255, 255)
GREEN = (23, 232, 215)
GREEN1 = (172, 255, 112)
# Initialize the pygame
pg.init()

# parameter
NumberOfTracks = 5
weight = 400
high = 750
slowSpeed = 0.01
fastSpeed = 10
space = 1
track = weight / NumberOfTracks
index = 0
boxSpeed = slowSpeed
backgroundTopMargin = 50
boxMoving = backgroundTopMargin - 10

# Box rect size
sizeBox = track - 4 * space

# Box
boxScore = []
boxX = []
boxY = []
positionY = []
# # how many tracks
# for i in range(NumberOfTracks):
#     boxScore.append([])
#     boxX.append([])
#     boxY.append([])
#     positionY.append(high - sizeBox)

# Create the screen
screen = pg.display.set_mode((weight, high))

# Background
background = pg.image.load('image/background.jpg')
background = pg.transform.scale(background, (weight, high))

# font
font_32 = pg.font.Font('freesansbold.ttf', 32)
font_16 = pg.font.Font('freesansbold.ttf', 16)
text_size_x = 9.5
text_size_y = 16
# get score
total_score = 0


# computing length of text
def compute_length_of_text(text):
    return len(str(text)) * text_size_x


# restart game
def restart_game():
    global boxScore, boxY, boxX, positionY, total_score
    boxScore = []
    boxX = []
    boxY = []
    positionY = []
    total_score = 0
    # how many tracks
    for k in range(NumberOfTracks):
        boxScore.append([])
        boxX.append([])
        boxY.append([])
        positionY.append(high - sizeBox)


# get score
def get_score():
    score_str = font_32.render(str(total_score), True, WHITE)
    screen.blit(score_str, (weight / 2 - compute_length_of_text(total_score), text_size_y))


# background
def set_background():
    screen.blit(background, (0, 0))
    for i in range(NumberOfTracks - 1):
        pg.draw.rect(screen, GRAY, pg.Rect((i + 1) * (track - space), backgroundTopMargin, 2 * space, high))
    pg.draw.rect(screen, BLACK, pg.Rect(0, backgroundTopMargin, weight, 5 * space))


# Create Box
def create_box(score, x, y, size_box):
    global text_size_x, text_size_y
    pg.draw.rect(screen, color(score), pg.Rect(x, round(y), size_box, size_box))
    score_str = font_32.render(str(score), True, WHITE)
    screen.blit(score_str, (x + size_box / 2 - compute_length_of_text(score), y + size_box / 2 - text_size_y))
    # pg.display.flip()


# Computer color by score
def color(score):
    green = 229 - score * 2 if 229 - score * 2 > 128 else 128
    blue = 204 - score * 2 if 204 - score * 2 > 0 else 0
    red = 255 - score * 2 if 204 - score * 2 > 0 else 0
    return red, green, blue


# check box collision
# score 分數
# y 座標
# x 座標
# tracks_index 第幾軌道
# item_index 上一個item位置
def is_collision(score, box_y, box_x, tracks_index, item_index):
    global total_score
    if item_index < 0:
        return len(score[tracks_index])
    is_mix = False  # 是否有合併
    high_box = len(score[tracks_index]) - 1
    if high_box < 0:
        return len(score[tracks_index])
    temp_get_score = 0  # 得分
    target = score[tracks_index][high_box]  # 目標分數
    save_index = item_index  # 最後儲存的座標
    # 合併規則
    # EX 2(L)2(T)
    if tracks_index - 1 >= 0 and high_box < len(score[tracks_index - 1]) and target == score[tracks_index - 1][
        high_box]:
        score[tracks_index][high_box] *= 2
        temp_get_score = score[tracks_index][high_box]
        del_box(score, box_x, box_y, tracks_index - 1, high_box)  # delete box
        is_mix = True
    # EX 2(T)2(R)
    if tracks_index + 1 < len(score) and high_box < len(score[tracks_index + 1]) and target == score[tracks_index + 1][
        high_box]:
        score[tracks_index][high_box] *= 2
        temp_get_score = score[tracks_index][high_box]
        del_box(score, box_x, box_y, tracks_index + 1, high_box)  # delete box
        is_mix = True
    # EX:   2(T)
    #       2
    if high_box > 0 and target == score[tracks_index][high_box - 1]:
        score[tracks_index][high_box] *= 2
        score[tracks_index][high_box - 1] = score[tracks_index][high_box]
        del_box(score, box_x, box_y, tracks_index, high_box)  # delete box
        is_mix = True
        save_index -= 1
        temp_get_score = score[tracks_index][high_box - 1]

    total_score += temp_get_score  # 得分
    if not is_mix:
        return len(score[tracks_index])

    return is_collision(score, box_y, box_x, tracks_index, save_index)


# delete box
def del_box(score, box_x, box_y, x, y):
    del score[x][y]
    del box_x[x][y]
    del box_y[x][len(box_y[x]) - 1]


# game over
def is_game_over(box_y):
    global total_score
    if len(box_y) - 1 >= 0 and box_y[len(box_y) - 1] <= sizeBox:
        top_score_text = "Top Score"
        restart_text = "RESTART"
        game_over = font_16.render(top_score_text, True, WHITE)
        restart = font_32.render(restart_text, True, WHITE)
        total = font_32.render(str(total_score), True, WHITE)
        pg.draw.rect(screen, GREEN, pg.Rect(weight / 4, high / 3, weight / 2, high / 4))
        screen.blit(game_over, (weight / 2 - len(str(top_score_text)) * 4.5, high / 2 - 7 * text_size_y))
        screen.blit(total, (weight / 2 - compute_length_of_text(total_score), high / 2 - 5.5 * text_size_y))
        screen.blit(restart, (weight / 2 - compute_length_of_text(restart_text) - 7, high / 2 - 2 * text_size_y))
        return True
    return False


# Game Loop
# restart game
restart_game()
running = True
game_pass = True
initial_score = [int(math.pow(2, random.randint(1, 5))), int(math.pow(2, random.randint(1, 5)))]
while running:
    screen.fill(BLACK)
    set_background()
    # get score
    get_score()
    # Listen event
    for event in pg.event.get():
        # Close screen
        if event.type == pg.QUIT:
            running = False
        # Right Click
        if event.type == pg.MOUSEBUTTONDOWN:
            if game_pass:
                index = int(pg.mouse.get_pos()[0] / track)
                boxSpeed = fastSpeed
            elif 120 < pg.mouse.get_pos()[0] in range(120, 290) and pg.mouse.get_pos()[1] in range(340, 370):
                game_pass = True
                restart_game()

    # Show all of box
    for i in range(len(boxScore)):
        for j in range(len(boxScore[i])):
            create_box(boxScore[i][j], boxX[i][j], boxY[i][j], sizeBox)

    # Show next box
    create_box(initial_score[1], weight / 5, 10, sizeBox / 2)

    # check game over
    if is_game_over(boxY[index]):
        game_pass = False
        pg.display.update()
        continue

    # initial Box moving
    boxMoving += boxSpeed
    positionX = 2 * space + index * track
    create_box(initial_score[0], positionX, boxMoving, sizeBox)

    # initial box and save box
    if positionY[index] < boxMoving:
        # save box
        boxScore[index].append(initial_score[0])
        boxX[index].append(positionX)
        boxY[index].append(positionY[index])
        # initial box
        boxMoving = 50
        boxSpeed = slowSpeed
        initial_score[0]=initial_score[1]
        initial_score[1] = int(math.pow(2, random.randint(1, 5)))

    # check box collision
    number = is_collision(boxScore, boxY, boxX, index, len(boxScore) - 1)
    # 計算boxY軸最高線 軌道高-(目前軌道item數量+1)*box高 - box和box之間的距離
    positionY[index] = high - (number + 1) * sizeBox - 2 * number * space

    # update draw
    # pg.display.flip()
    # update screen
    pg.display.update()
