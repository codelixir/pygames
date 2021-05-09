#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from config import *  # Configuration File
pygame.init()

# images

bg = pygame.image.load('assets/konoha.jpg')
panel = pygame.image.load('assets/panel.jpg')
shuriken = [pygame.image.load('assets/shuriken0.png'),
			pygame.image.load('assets/shuriken15.png'),
			pygame.image.load('assets/shuriken30.png'),
            pygame.image.load('assets/shuriken45.png'),
            pygame.image.load('assets/shuriken60.png'),
            pygame.image.load('assets/shuriken75.png')
            ]
rotnum = 6
paperbomb = pygame.image.load('assets/paperbomb.jpg')
sasuke = pygame.image.load('assets/sasuke.png')
naruto = pygame.image.load('assets/naruto.png')
sasukewin = pygame.image.load('assets/sasuke2.png')
narutowin = pygame.image.load('assets/naruto2.png')

#music
soundtrack = pygame.mixer.music.load('assets/fighting.mp3')
pygame.mixer.music.set_volume(250)
pygame.mixer.music.play(-1)

# variables

playWidth = 500
playHeight = 500
velocity = 10
currentPlayer = 1
t = 0


# player

class player(object):

    def __init__(
        self,
        x,
        y,
        width,
        height,
        ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = [x, y, x + width, y + height]
        self.start = [x, y]
        self.level = 1
        self.image = shuriken[0]
        self.score = 0
        self.final = 0

    def draw(self, window):

    # ....width = self.width
    # ....height = self.height

        window.blit(self.image, (self.x, self.y))

    # ....pygame.draw.rect(window, self.color, (x,y, width, height))

    def hit(self):
        self.x = self.start[0]
        self.y = self.start[1]


# moving obstacle

class enemy(object):

    def __init__(
        self,
        x,
        y,
        width,
        height,
        ):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.vel = 10
        self.rotation = 0
        self.hitbox = [x, y, x + width, y + height]

    def draw(self, window):
        window.blit(shuriken[self.rotation], (self.x, self.y))

    # ....pygame.draw.rect(window, self.color, (x, y, width, height))

    def move(self):
        if self.vel > 0:
            self.vel = 5 + 5*players[currentPlayer].level
            if self.x < playWidth:
                self.x += self.vel
            else:
                self.vel *= -1
            self.rotation = (self.rotation-1)%rotnum
        else:
            self.vel = -5 - 5*players[currentPlayer].level
            if self.x + self.width > 0:
                self.x += self.vel
            else:
                self.vel *= -1
            self.rotation = (self.rotation+1)%rotnum
        self.hitbox = [self.x, self.y, self.x + self.width, self.y + self.height]
        


# static obstacle

class hurdle(object):

    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.hitbox = [x, y, x + width, y + height]
        self.score = 0

    def draw(self, window):
        window.blit(paperbomb, (self.x, self.y))


    # ....pygame.draw.rect(window, self.color, (x, y, width, height))

# game window

window = pygame.display.set_mode((playWidth + 250, playHeight))
pygame.display.set_caption('Team 7')

# Characters and obstacles

adam = player(220, 450, 38, 40)
steve = player(220, 10, 36, 40)
adam.image = naruto
steve.image = sasuke
players = [steve, adam]
enemy1 = enemy(300, 100, 30, 30)
enemy2 = enemy(200, 200, 30, 30)
enemy3 = enemy(400, 300, 30, 30)
enemy4 = enemy(100, 400, 30, 30)
enemies = [enemy1, enemy2, enemy3, enemy4]
bomb1 = hurdle(50, 50, 60, 30)
bomb2 = hurdle(350, 250, 60, 30)
bomb3 = hurdle(250, 350, 60, 30)
bomb4 = hurdle(150, 150, 60, 30)
bomb5 = hurdle(400, 450, 60, 30)
hurdles = [bomb1, bomb2, bomb3, bomb4, bomb5]
obstacles = [enemy1, enemy2, enemy3, enemy4, bomb1, bomb2, bomb3, bomb4, bomb5]


# update score of player1 (only when active)

def scoreP1():
    arr = [0, 80, 120, 180, 220, 280, 320, 380, 420]
    point = [5, 15, 20, 30, 35, 45, 50, 60]
    yScore = 0
    for i in range(0, 8):
        if adam.y >= arr[i] and adam.y < arr[i + 1]:
            yScore = point[-i]
    adam.score = 100 * (adam.level - 1) - t + yScore


# update score of player2 (only when active)

def scoreP2():
    arr = [0, 80, 120, 180, 220, 280, 320, 380, 420]
    point = [5, 15, 20, 30, 35, 45, 50, 60]
    yScore = 0
    for i in range(0, 8):
        if steve.y >= arr[i] and steve.y < arr[i + 1]:
            yScore = point[i]
    steve.score = 100 * (steve.level - 1) - t + yScore


# text

FontSmall = pygame.font.SysFont('comicsans', 30)
FontMedium = pygame.font.SysFont('comicsans', 50)

# display text

text = ['(up,left, down, right)', '', 'Player 1: W/ A/ S/ D',
        'Player 2: I / J / K / L', 'Pause:   <SPACE>']
label1 = []
for line in text:
    label1.append(FontSmall.render(line, 1, (255, 255, 255)))
side1 = FontMedium.render('CONTROLS', 1, (255, 255, 255))
side2 = FontMedium.render('SCORE', 1, (255, 255, 255))


def showText():
    global pause, games
    score1 = FontSmall.render('Player 1: ' + str(int(adam.score)), 1,
                              (255, 255, 255))
    score2 = FontSmall.render('Player 2: ' + str(int(steve.score)), 1,
                              (255, 255, 255))
    side4 = FontMedium.render('LEVEL : '
                              + str(players[currentPlayer].level), 1,
                              (255, 255, 255))
    side3 = FontMedium.render('PLAYER ' + str(2 - currentPlayer), 1,
                              (255, 255, 255))
    window.blit(side1, (520, 30))
    pos = 70
    for text in label1:
        window.blit(text, (520, pos))
        pos += 20
    window.blit(side2, (520, 180))
    window.blit(score1, (520, 225))
    window.blit(score2, (520, 250))
    window.blit(side3, (520, 280))
    window.blit(side4, (520, 320))
    if pause and games:
        window.blit(alert1, (540, 410))  # temp# Paused
    if games == 0:
        window.blit(alert4a, (545, 385))
        window.blit(alert4b, (540, 435))


# reset display

def redrawWindow():
    global games
    window.blit(bg, (0, 0))

    if games:
        if currentPlayer:
            adam.draw(window)
        else:
            steve.draw(window)
        for thing in obstacles:
            thing.draw(window)
    else:
        pygame.draw.rect(window, (0, 0, 0), (80, 380, 340, 60))
        if adam.final > steve.final:
            window.blit(narutowin, (80, 124))
            window.blit(alert6, (100, 390))
        else:
            window.blit(sasukewin, (80, 124))
            window.blit(alert5, (100, 390))

    window.blit(panel, (500, 0))
    box = pygame.draw.rect(window, (0, 0, 0), (520, 370, 210, 120))
    showText()
    pygame.display.update()


# move player 1

def moveP1():
    global flagCount, velocity
    key = pygame.key.get_pressed()
    if key[pygame.K_a] and adam.x > velocity:
        adam.x -= velocity
    if key[pygame.K_d] and adam.x < playWidth - adam.width - velocity:
        adam.x += velocity
    if key[pygame.K_w] and adam.y > velocity:
        adam.y -= velocity
    if key[pygame.K_s] and adam.y < playHeight - adam.height - velocity:
        adam.y += velocity
    adam.hitbox = [adam.x, adam.y, adam.x + adam.width, adam.y
                   + adam.height]

    if adam.y < 50:
        adam.level += 1
        velocity += 3
        flagCount = 5
        adam.hit()


# move player 2

def moveP2():
    global flagCount, velocity 
    key = pygame.key.get_pressed()
    if key[pygame.K_j] and steve.x > velocity:
        steve.x -= velocity
    if key[pygame.K_l] and steve.x < playWidth - steve.width - velocity:
        steve.x += velocity
    if key[pygame.K_i] and steve.y > velocity:
        steve.y -= velocity
    if key[pygame.K_k] and steve.y < playHeight - steve.height \
        - velocity:
        steve.y += velocity
    steve.hitbox = [steve.x, steve.y, steve.x + steve.width, steve.y
                    + steve.height]

    if steve.y > 410:
        steve.level += 1
        flagCount = 5
        velocity += 3
        steve.hit()


# collision has happened

def collision():
    global currentPlayer, t, pause, games, velocity
    pl = players[currentPlayer]
    pl.final = pl.score
    pause = 1
    window.blit(alert3, (525, 410))
    pygame.display.update()
    pygame.time.delay(500)
    pl.hit()
    pl.level = 1
    velocity = 7
    currentPlayer ^= 1
    t = 0
    games -= 1


# Collision Check

def collide():
    global currentPlayer, pause
    pl = players[currentPlayer]
    for obs in enemies:
        if obs.hitbox[1] <= pl.hitbox[3] and obs.hitbox[1] \
            >= pl.hitbox[1]:
            if obs.hitbox[2] <= pl.hitbox[2] and obs.hitbox[2] \
                >= pl.hitbox[0]:
                collision()
            elif obs.hitbox[0] <= pl.hitbox[2] and obs.hitbox[0] \
                >= pl.hitbox[0]:
                collision()
        elif obs.hitbox[3] <= pl.hitbox[3] and obs.hitbox[3] \
            >= pl.hitbox[1]:
            if obs.hitbox[2] <= pl.hitbox[2] and obs.hitbox[2] \
                >= pl.hitbox[0]:
                collision()
            elif obs.hitbox[0] <= pl.hitbox[2] and obs.hitbox[0] \
                >= pl.hitbox[0]:
                collision()
    for obs in hurdles:
        if obs.hitbox[1] <= pl.hitbox[3] and obs.hitbox[1] \
            >= pl.hitbox[1]:
            if pl.hitbox[2] <= obs.hitbox[2] and pl.hitbox[2] \
                >= obs.hitbox[0]:
                collision()
            elif pl.hitbox[0] <= obs.hitbox[2] and pl.hitbox[0] \
                >= obs.hitbox[0]:
                collision()
        elif obs.hitbox[3] <= pl.hitbox[3] and obs.hitbox[3] \
            >= pl.hitbox[1]:
            if pl.hitbox[2] <= obs.hitbox[2] and pl.hitbox[2] \
                >= obs.hitbox[0]:
                collision()
            elif pl.hitbox[0] <= obs.hitbox[2] and pl.hitbox[0] \
                >= obs.hitbox[0]:
                collision()


# Main Loop

run = True
pause = 1
flagCount = 0
games = 2
while run:
    pygame.time.delay(100)

    # quitting/pausing the game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause ^= 1
            if event.key == pygame.K_p:
                games = 2
                steve.final = 0
                adam.final = 0

    # pause the movements

    if pause == 0:

        # update score due to time

        t += 0.1

        # check collisions through outside function

        collide()

        # move only the player which is active
        # and simultaneously update the score

        if currentPlayer:
            moveP1()
            scoreP1()
        else:
            moveP2()
            scoreP2()

        # keep moving enemies (speed based on level)

        for thing in enemies:
            thing.move()

    # to create blinking effect

    if flagCount:
        window.blit(alert2, (525, 410))
        pygame.display.update()
        flagCount -= 1

    redrawWindow()

# Quit

pygame.display.quit()
pygame.quit()
