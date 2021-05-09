#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import random
pygame.init()

# constants
playWidth = 600
playHeight = 500
margin = 20
scoreboard = 100
rows = 20
columns = 24

# colours and fonts
colSnake = (51,102,0)
colHead = (0,153,0)
colFood = (0,102,204)
colBonus = (204,0,0)
colText = (255, 255, 255)
colBG = (255, 255, 192)
colRect = (0,0,0)
font1 = pygame.font.SysFont('freesans', 50)

# relations
totalWidth = playWidth + 2*margin
totalHeight = playHeight+scoreboard+3*margin
cellWidth = playWidth//columns
cellHeight = playHeight//rows

# game window
window = pygame.display.set_mode((totalWidth, totalHeight))
pygame.display.set_caption('Snake')

# variables

### OBJECTS	###

# body segments
class seg(object):

	def __init__(self, coor, dirn, color=colSnake):
		self.i=coor[0]
		self.j=coor[1]
		self.dx=dirn[0]
		self.dy=dirn[1]
		self.color=color

	def draw(self):
		height=cellHeight -2
		width=cellWidth -2
		x = margin + self.i*cellWidth + 1
		y = margin + self.j*cellHeight + 1
		pygame.draw.rect(window, self.color, (x, y, width, height))

	def move(self):
		self.i+=self.dx
		self.j+=self.dy

class snake(object):

	def __init__(self, coor):
		self.head = seg(coor, (1,0), colHead)
		self.body = [self.head]
		self.addSeg()

	def addSeg(self):
		tail = self.body[-1]
		newseg = seg((tail.i-tail.dx,tail.j-tail.dy),(tail.dx,tail.dy))
		self.body.append(newseg)

	def draw(self):
		for c in self.body:
			c.draw()

	def move(self):
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT] and self.head.dx != 1:
			self.head.dx, self.head.dy = -1, 0
		if key[pygame.K_RIGHT] and self.head.dx != -1:
			self.head.dx, self.head.dy = 1, 0
		if key[pygame.K_UP] and self.head.dy != 1:
			self.head.dx, self.head.dy = 0, -1
		if key[pygame.K_DOWN] and self.head.dy != -1:
			self.head.dx, self.head.dy = 0, 1

		for c in self.body:
			c.move()

		n = len(self.body)

		for i in range(1,n):
			self.body[n-i].dx, self.body[n-i].dy = self.body[n-i-1].dx, self.body[n-i-1].dy

class food(object):

	def __init__(self, coor):
		self.i=coor[0]
		self.j=coor[1]
		self.color=colFood

	def draw(self):
		height=cellHeight -2
		width=cellWidth -2
		x = margin + self.i*cellWidth + 1
		y = margin + self.j*cellHeight + 1
		pygame.draw.rect(window, self.color, (x, y, width, height))


###  FUNCTIONS	###

# generate random coordinates
def getCoor():

	invalid = True
	while invalid:
		fx = random.randint(0,columns -1)
		fy = random.randint(0,rows -1)
		invalid = False
		for c in s.body:
			if (fx==c.i and fy==c.j):
				invalid = True
	return (fx, fy)


# score text
def showText():
	global score, highscore
	text1 = font1.render('Score: '+ str(score), 1, colText)
	text2 = font1.render('Highscore: '+ str(highscore), 1, colText)
	window.blit(text1, (2*margin, 3*margin+playHeight))
	window.blit(text2, (playWidth/2, 3*margin+playHeight))

# reset display
def redrawWindow():
	bg = pygame.draw.rect(window, colBG, (0,0,totalWidth, totalHeight))
	playArea = pygame.draw.rect(window, colRect, (margin, margin, playWidth, playHeight))
	scoreArea = pygame.draw.rect(window, colRect, (margin, 2*margin+playHeight, playWidth, scoreboard))
	s.draw()
	bug.draw()

	showText()
	pygame.display.update()

# read highscore from file
def getScore():
	global file
	try:
		file = open("score","r+")
		x = int(file.read())
	except:
		file = open("score","w")
	#	file.write("0")
		return 0;
	else:
		return x

# reset game
def reset():
	global score, highscore, file, s, bug, pause

	print(score)
	if score > highscore:
		highscore = score
	s = snake((7,12))
	bug = food(getCoor())
	score = 0
	pause = 1

# check collision
def collision():
	if (s.head.i < 0 or s.head.i >= columns or s.head.j < 0 or s.head.j >= rows):
		return True
	for c in s.body:
		if ((c != s.head) and (c.i == s.head.i) and (c.j == s.head.j)):
			return True
	return False

# main

def main():

	global score, highscore, file, s, bug, pause

	highscore = getScore()
	score = 0
	reset()

	pause = 1
	run = True
	while run:
	    pygame.time.delay(200)

	    for event in pygame.event.get():
	        if event.type == pygame.QUIT:
	            run = False
	            file.seek(0)
	            file.write(str(highscore))
	            file.close()
	        #    pygame.display.quit()
	        #    pygame.quit()
	        if event.type == pygame.KEYDOWN:
	        	if event.key == pygame.K_SPACE:
	        		pause ^= 1

	    if pause==0:
	    	if (bug.i == s.head.i and bug.j == s.head.j):
	    		s.addSeg()
	    		bug = food(getCoor())
	    		score += 1
	    	s.move()
	    	if (collision()):
	    		reset()
	    redrawWindow()

main()
pygame.display.quit()
pygame.quit()
