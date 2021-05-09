#!/usr/bin/python
# -*- coding: utf-8 -*-

# # CONFIG FILE

import pygame
pygame.init()

FontAlert = pygame.font.SysFont('comicsans', 60)
color1 = (156,156,156)
alert1 = FontAlert.render("PAUSED", 1, color1)
color2 = (0,255,0)
alert2 = FontAlert.render("LEVEL UP", 1, color2)
color3 = (255,0,0)
alert3 = FontAlert.render("YOU DIED", 1, color3)

color4 = (255, 255, 255)
alert4a = FontAlert.render("Press 'P'", 1, color4)
alert4b = FontAlert.render("to restart", 1, color4)

color5 = (0,0,255)
alert5 = FontAlert.render("SASUKE WON", 1, color5)
color6 = (255, 165, 0)
alert6 = FontAlert.render("NARUTO WON", 1, color6)
