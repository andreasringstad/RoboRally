import pygame
from sys import exit
from random import lognormvariate, randint

pygame.init()
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption('Robo Rally')
clock = pygame.time.Clock()
pygame.font.init()
myFont = pygame.font.SysFont('Times New Roman', 40)

logo = pygame.image.load('images/logo.png').convert()
logoRect = logo.get_rect(center = (960,200))
normalTile = pygame.image.load('images/normalTile.png').convert()
normalTileRectList = []
for i in range(5):
    normalTileRectList.append(normalTile.get_rect(center = (760 + i*100,600)))
mainMenu = True

while mainMenu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.blit(logo,logoRect)
    screen.blit(myFont.render('How many players?', False, (250,250,250)), (800,350))
    for i in range(5):
        screen.blit(normalTile,normalTileRectList[i])
        screen.blit(myFont.render(str(i+2), False, (0,0,0)), (750 + i*100,580))
    pygame.display.update()
    clock.tick(1)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
    clock.tick(60)
