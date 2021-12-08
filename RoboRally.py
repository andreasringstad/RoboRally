import pygame
from sys import exit
from random import randint

pygame.init()
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    clock.tick(60)
