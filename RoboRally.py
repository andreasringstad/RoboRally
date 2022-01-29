import pygame
from sys import exit
from random import randint, choice
import ctypes
ctypes.windll.user32.SetProcessDPIAware()

def reshuffle():
    "shuffling"

def loadSprites():
    return {
        "normalTile": [pygame.image.load('images/normalTile.png').convert()],
        "spawnTile": [pygame.image.load('images/spawnTile.png').convert()],
        "conveyorForwardOne": [
                pygame.image.load('images/conveyorForwardOne0.png').convert(),
                pygame.image.load('images/conveyorForwardOne1.png').convert()
        ],
        "conveyorForwardTwo": [
                pygame.image.load('images/conveyorForwardTwo0.png').convert(),
                pygame.image.load('images/conveyorForwardTwo1.png').convert(),
                pygame.image.load('images/conveyorForwardTwo2.png').convert(),
                pygame.image.load('images/conveyorForwardTwo3.png').convert()
        ],
        "wallTile": [
                pygame.image.load('images/wallTile0.png').convert(),
                pygame.image.load('images/wallTile1.png').convert(),
                pygame.image.load('images/wallTile2.png').convert(),
                pygame.image.load('images/wallTile3.png').convert()
        ],
        "twonky": [
                pygame.image.load('images/twonky0.png').convert(),
                pygame.image.load('images/twonky1.png').convert(),
                pygame.image.load('images/twonky2.png').convert(),
                pygame.image.load('images/twonky3.png').convert()
        ],
        "card": {
                "again": pygame.image.load('images/cards/again.png').convert(),
                "leftTurn": pygame.image.load('images/cards/leftTurn.png').convert(),
                "move1": pygame.image.load('images/cards/move1.png').convert(),
                "move2": pygame.image.load('images/cards/move2.png').convert(),
                "move3": pygame.image.load('images/cards/move3.png').convert(),
                "moveBack": pygame.image.load('images/cards/moveBack.png').convert(),
                "powerUp": pygame.image.load('images/cards/powerUp.png').convert(),
                "rightTurn": pygame.image.load('images/cards/rightTurn.png').convert(),
                "uTurn": pygame.image.load('images/cards/uTurn.png').convert()
        }
    }

class robot:
    global robots
    def draw():
        for robot in robots:
            screen.blit(allSprites[robot.sprite][robot.orientation], (robot.tileX*100+robot.pixelX, robot.tileY*100+robot.pixelY))
    
    def drawRegister():
        for i in range(len(robots[playersTurn].register)):
            screen.blit(allSprites["card"][robots[0].register[i]], (1300+124*i,0))
        pygame.draw.rect(screen, (255, 0, 0), [1300+124*register, 0, 124, 171], 10)
    
    def discardRegisters(): # Needs to be changed to discard cards to players discard pile in the future
        for robot in robots:
            robot.register = []
    
    def fillRegisters():
        for robot in robots:
            for y in range(5):
                robot.register.append(choice(robot.deck))


    tileX = 0
    tileY = 0
    pixelX = 0
    pixelY = 0
    orientation = 1
    deck = [ #"again", "again", removed as for now it makes no sense
        "leftTurn", "leftTurn", "leftTurn", "move1", "move1", "move1", "move1", "move1", "move2", "move2", "move2", "move3", "moveBack", "powerUp", "rightTurn", "rightTurn", "rightTurn", "uTurn"
    ]
    hand = []
    discard = []
    register = []
    sprite = "twonky"
    moved = False
    moving = False
    movementLeftInTiles = 0
    movementLeftInTicks = 0
    movementDirection = 0
    movementAxis = "X"
    movement = 0
    alive = True


def drawGameBoard():
    screen.fill((0,0,0))
    for tile in listOfTiles:
        screen.blit(allSprites[tile["sprite"]][tile["orientation"]], (tile["tileX"]*100, tile["tileY"]*100))

def initiateRobots():
    robots = []
    for i in range(numberOfPlayers):
        robots.append(robot)
    return robots

def movementValid(): # Returns True or False

    if robots[playersTurn].register[register] == "leftTurn" or robots[playersTurn].register[register] == "powerUp" or robots[playersTurn].register[register] == "rightTurn" or robots[playersTurn].register[register] == "uTurn":
        return True
    
    elif robots[playersTurn].register[register] == "move1" or robots[playersTurn].register[register] == "move2" or robots[playersTurn].register[register] == "move3": # Kan muligens refactoreres ettersom orientasjonene er 0 og 2 eller 1 og 3...
        if robots[playersTurn].orientation == 0:
            for tile in listOfTiles:
                if (tile["tileX"] == robots[playersTurn].tileX) and (tile["tileY"] == robots[playersTurn].tileY):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 0:
                            return False
                elif (tile["tileX"] == robots[playersTurn].tileX) and (tile["tileY"] == robots[playersTurn].tileY-1):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 2:
                            return False
        
        if robots[playersTurn].orientation == 1:
            for tile in listOfTiles:
                if (tile["tileX"] == robots[playersTurn].tileX) and (tile["tileY"] == robots[playersTurn].tileY):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 1:
                            return False
                elif (tile["tileX"] == robots[playersTurn].tileX+1) and (tile["tileY"] == robots[playersTurn].tileY):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 3:
                            return False
        
        if robots[playersTurn].orientation == 2:
            for tile in listOfTiles:
                if (tile["tileX"] == robots[playersTurn].tileX) and (tile["tileY"] == robots[playersTurn].tileY):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 2:
                            return False
                elif (tile["tileX"] == robots[playersTurn].tileX) and (tile["tileY"] == robots[playersTurn].tileY+1):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 0:
                            return False
        
        if robots[playersTurn].orientation == 3:
            for tile in listOfTiles:
                if (tile["tileX"] == robots[playersTurn].tileX) and (tile["tileY"] == robots[playersTurn].tileY):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 3:
                            return False
                elif (tile["tileX"] == robots[playersTurn].tileX-1) and (tile["tileY"] == robots[playersTurn].tileY):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 1:
                            return False
    
    elif robots[playersTurn].register[register] == "moveBack":
        if robots[playersTurn].orientation == 0:
            for tile in listOfTiles:
                if (tile["tileX"] == robots[playersTurn].tileX) and (tile["tileY"] == robots[playersTurn].tileY):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 2:
                            return False
                elif (tile["tileX"] == robots[playersTurn].tileX) and (tile["tileY"] == robots[playersTurn].tileY+1):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 0:
                            return False
                            
        if robots[playersTurn].orientation == 1:
            for tile in listOfTiles:
                if (tile["tileX"] == robots[playersTurn].tileX) and (tile["tileY"] == robots[playersTurn].tileY):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 3:
                            return False
                elif (tile["tileX"] == robots[playersTurn].tileX-1) and (tile["tileY"] == robots[playersTurn].tileY):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 1:
                            return False
                            
        if robots[playersTurn].orientation == 2:
            for tile in listOfTiles:
                if (tile["tileX"] == robots[playersTurn].tileX) and (tile["tileY"] == robots[playersTurn].tileY):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 0:
                            return False
                elif (tile["tileX"] == robots[playersTurn].tileX) and (tile["tileY"] == robots[playersTurn].tileY-1):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 2:
                            return False
                            
        if robots[playersTurn].orientation == 3:
            for tile in listOfTiles:
                if (tile["tileX"] == robots[playersTurn].tileX) and (tile["tileY"] == robots[playersTurn].tileY):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 1:
                            return False
                elif (tile["tileX"] == robots[playersTurn].tileX+1) and (tile["tileY"] == robots[playersTurn].tileY):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 3:
                            return False
    return True

def move():
    global firstItterationOfRegister
    movement = 50 # Movement * movementTicks should be roughly 100 to avoid the bot from jumping when ariving at new tiles
    movementTicks = 2
    if firstItterationOfRegister:
        robots[playersTurn].moved = True
        firstItterationOfRegister = False
        if movementValid():
            robots[playersTurn].moving = True
            robots[playersTurn].movement = movement

            if robots[playersTurn].register[register] == "move1":
                robots[playersTurn].movementLeftInTiles = 1
                robots[playersTurn].movementLeftInTicks = movementTicks
                if robots[playersTurn].orientation == 0:
                    robots[playersTurn].movementDirection = -1
                    robots[playersTurn].movementAxis = "Y"
                    robots[playersTurn].tileY -= 1
                    robots[playersTurn].pixelY = movement * movementTicks
                elif robots[playersTurn].orientation == 1:
                    robots[playersTurn].movementDirection = 1
                    robots[playersTurn].movementAxis = "X"
                elif robots[playersTurn].orientation == 2:
                    robots[playersTurn].movementDirection = 1
                    robots[playersTurn].movementAxis = "Y"
                else:
                    robots[playersTurn].movementDirection = -1
                    robots[playersTurn].movementAxis = "X"
                    robots[playersTurn].tileX -= 1
                    robots[playersTurn].pixelX = movement * movementTicks

            elif robots[playersTurn].register[register] == "move2":
                robots[playersTurn].movementLeftInTiles = 2
                robots[playersTurn].movementLeftInTicks = movementTicks
                if robots[playersTurn].orientation == 0:
                    robots[playersTurn].movementDirection = -1
                    robots[playersTurn].movementAxis = "Y"
                    robots[playersTurn].tileY -= 1
                    robots[playersTurn].pixelY = movement * movementTicks
                elif robots[playersTurn].orientation == 1:
                    robots[playersTurn].movementDirection = 1
                    robots[playersTurn].movementAxis = "X"
                elif robots[playersTurn].orientation == 2:
                    robots[playersTurn].movementDirection = 1
                    robots[playersTurn].movementAxis = "Y"
                else:
                    robots[playersTurn].movementDirection = -1
                    robots[playersTurn].movementAxis = "X"
                    robots[playersTurn].tileX -= 1
                    robots[playersTurn].pixelX = movement * movementTicks

            elif robots[playersTurn].register[register] == "move3":
                robots[playersTurn].movementLeftInTiles = 3
                robots[playersTurn].movementLeftInTicks = movementTicks
                if robots[playersTurn].orientation == 0:
                    robots[playersTurn].movementDirection = -1
                    robots[playersTurn].movementAxis = "Y"
                    robots[playersTurn].tileY -= 1
                    robots[playersTurn].pixelY = movement * movementTicks
                elif robots[playersTurn].orientation == 1:
                    robots[playersTurn].movementDirection = 1
                    robots[playersTurn].movementAxis = "X"
                elif robots[playersTurn].orientation == 2:
                    robots[playersTurn].movementDirection = 1
                    robots[playersTurn].movementAxis = "Y"
                else:
                    robots[playersTurn].movementDirection = -1
                    robots[playersTurn].movementAxis = "X"
                    robots[playersTurn].tileX -= 1
                    robots[playersTurn].pixelX = movement * movementTicks

            elif robots[playersTurn].register[register] == "moveBack":
                robots[playersTurn].movementLeftInTiles = 1
                robots[playersTurn].movementLeftInTicks = movementTicks
                if robots[playersTurn].orientation == 0:
                    robots[playersTurn].movementDirection = 1
                    robots[playersTurn].movementAxis = "Y"
                elif robots[playersTurn].orientation == 1:
                    robots[playersTurn].movementDirection = -1
                    robots[playersTurn].movementAxis = "X"
                    robots[playersTurn].tileX -= 1
                    robots[playersTurn].pixelX = movement * movementTicks
                elif robots[playersTurn].orientation == 2:
                    robots[playersTurn].movementDirection = -1
                    robots[playersTurn].movementAxis = "Y"
                    robots[playersTurn].tileY -= 1
                    robots[playersTurn].pixelY = movement * movementTicks
                else:
                    robots[playersTurn].movementDirection = 1
                    robots[playersTurn].movementAxis = "X"        

        if robots[playersTurn].register[register] == "leftTurn":
            robots[playersTurn].moving = False
            if robots[playersTurn].orientation == 0:
                robots[playersTurn].orientation = 3
            else: robots[playersTurn].orientation -= 1

        elif robots[playersTurn].register[register] == "rightTurn":
            robots[playersTurn].moving = False
            if robots[playersTurn].orientation == 3:
                robots[playersTurn].orientation = 0
            else: robots[playersTurn].orientation += 1  

        elif robots[playersTurn].register[register] == "uTurn":
            robots[playersTurn].moving = False
            if robots[playersTurn].orientation < 2:
                robots[playersTurn].orientation += 2
            else: robots[playersTurn].orientation -= 2

        elif robots[playersTurn].register[register] == "powerUp": # Todo, needs work
            robots[playersTurn].moving = False

        elif robots[playersTurn].register[register] == "again": # Todo, needs work
            robots[playersTurn].moving = False

    if robots[playersTurn].movementLeftInTicks:
        if robots[playersTurn].movementAxis == "x":
            robots[playersTurn].pixelX += robots[playersTurn].movement * robots[playersTurn].movementDirection
        else:
            robots[playersTurn].pixelY += robots[playersTurn].movement * robots[playersTurn].movementDirection
        robots[playersTurn].movementLeftInTicks -= 1

    elif robots[playersTurn].movementLeftInTiles:
        if robots[playersTurn].movementAxis == "x":
            robots[playersTurn].pixelX = 0
        else:
            robots[playersTurn].pixelY = 0 # her blir det enten pixelX eller PixelY ut ifra hva som ligger i movementAxis. Hvordan gjør man dette med classer?
        if robots[playersTurn].register[register] == "move1" or robots[playersTurn].register[register] == "move2" or robots[playersTurn].register[register] == "move3": 
            if robots[playersTurn].orientation == 1: #Move these four lines to after the movement pixelX/Y is done, check todo at the bottom!
                robots[playersTurn].tileX += 1
            elif robots[playersTurn].orientation == 2:
                robots[playersTurn].tileY += 1
        robots[playersTurn].movementLeftInTiles -= 1
        if robots[playersTurn].movementLeftInTiles:
            if movementValid():
                robots[playersTurn].movementLeftInTicks = movementTicks
                if robots[playersTurn].orientation == 0:
                    robots[playersTurn].movementDirection = -1
                    robots[playersTurn].movementAxis = "Y"
                    robots[playersTurn].tileY -= 1
                    robots[playersTurn].pixelY = movement * movementTicks
                elif robots[playersTurn].orientation == 3:
                    robots[playersTurn].movementDirection = -1
                    robots[playersTurn].movementAxis = "X"
                    robots[playersTurn].tileX -= 1
                    robots[playersTurn].pixelX = movement * movementTicks

        else:
            robots[playersTurn].movementLeftInTiles = 0
            robots[playersTurn].moving = False

def nextPlayer():
    global playersTurn
    if (robots[playersTurn].moved) or (not(robots[playersTurn].moving)):
        playersTurn += 1
        if playersTurn > numberOfPlayers-1:
            playersTurn = 0

def nextRegister():
    global register
    global firstItterationOfRegister
    allPlayersDoneMoving = True
    for robot in robots:
        if (not(robot.moved)) or (robot.moving):
            allPlayersDoneMoving = False
    if allPlayersDoneMoving:
        for robot in robots:
            robot.moved = False
        firstItterationOfRegister = True
        register += 1
        if register > 4:
            register = 0
            robot.discardRegisters()

pygame.init()
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption('Robo Rally')
clock = pygame.time.Clock()
pygame.font.init()
myFont = pygame.font.SysFont('Times New Roman', 40)

logo = pygame.image.load('images/logo.png').convert()
logoRect = logo.get_rect(center = (960,200))
allSprites = loadSprites()
normalTile = pygame.image.load('images/normalTile.png').convert()
testMode = True


if testMode:
    listOfTiles = [{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 0,
        "tileY": 0
        },{
        "sprite": "wallTile",
        "orientation": 2,
        "tileX": 1,
        "tileY": 0
        },{
        "sprite": "wallTile",
        "orientation": 2,
        "tileX": 2,
        "tileY": 0
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 3,
        "tileY": 0
        },

        {
        "sprite": "wallTile",
        "orientation": 1,
        "tileX": 0,
        "tileY": 1
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 1,
        "tileY": 1
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 2,
        "tileY": 1
        },{
        "sprite": "wallTile",
        "orientation": 3,
        "tileX": 3,
        "tileY": 1
        },

        {
        "sprite": "wallTile",
        "orientation": 1,
        "tileX": 0,
        "tileY": 2
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 1,
        "tileY": 2
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 2,
        "tileY": 2
        },{
        "sprite": "wallTile",
        "orientation": 3,
        "tileX": 3,
        "tileY": 2
        },

        {
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 0,
        "tileY": 3
        },{
        "sprite": "wallTile",
        "orientation": 0,
        "tileX": 1,
        "tileY": 3
        },{
        "sprite": "wallTile",
        "orientation": 0,
        "tileX": 2,
        "tileY": 3
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 3,
        "tileY": 3
        }]
else:
    listOfTiles = [{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 0,
        "tileY": 0
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 1,
        "tileY": 0
        },{
        "sprite": "conveyorForwardOne",
        "orientation": 1,
        "tileX": 2,
        "tileY": 0
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 3,
        "tileY": 0
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 2,
        "tileX": 4,
        "tileY": 0
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 2,
        "tileX": 5,
        "tileY": 0
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 6,
        "tileY": 0
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 7,
        "tileY": 0
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 8,
        "tileY": 0
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 9,
        "tileY": 0
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 10,
        "tileY": 0
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 11,
        "tileY": 0
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 12,
        "tileY": 0
        },

        {
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 0,
        "tileY": 1
        },{
        "sprite": "spawnTile",
        "orientation": 0,
        "tileX": 1,
        "tileY": 1
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 2,
        "tileY": 1
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 3,
        "tileY": 1
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 2,
        "tileX": 4,
        "tileY": 1
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 3,
        "tileX": 5,
        "tileY": 1
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 3,
        "tileX": 6,
        "tileY": 1
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 3,
        "tileX": 7,
        "tileY": 1
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 3,
        "tileX": 8,
        "tileY": 1
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 3,
        "tileX": 9,
        "tileY": 1
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 3,
        "tileX": 10,
        "tileY": 1
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 3,
        "tileX": 11,
        "tileY": 1
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 3,
        "tileX": 12,
        "tileY": 1
        },

        {
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 0,
        "tileY": 2
        },{
        "sprite": "wallTile",
        "orientation": 0,
        "tileX": 1,
        "tileY": 2
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 2,
        "tileY": 2
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 3,
        "tileY": 2
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 2,
        "tileX": 4,
        "tileY": 2
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 5,
        "tileY": 2
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 6,
        "tileY": 2
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 7,
        "tileY": 2
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 8,
        "tileY": 2
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 9,
        "tileY": 2
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 10,
        "tileY": 2
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 0,
        "tileX": 11,
        "tileY": 2
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 3,
        "tileX": 12,
        "tileY": 2
        },

        {
        "sprite": "spawnTile",
        "orientation": 0,
        "tileX": 0,
        "tileY": 3
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 1,
        "tileY": 3
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 2,
        "tileY": 3
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 3,
        "tileY": 3
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 2,
        "tileX": 4,
        "tileY": 3
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 5,
        "tileY": 3
        },{
        "sprite": "wallTile",
        "orientation": 0,
        "tileX": 6,
        "tileY": 3
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 7,
        "tileY": 3
        },{
        "sprite": "wallTile",
        "orientation": 3,
        "tileX": 8,
        "tileY": 3
        },{
        "sprite": "wallTile",
        "orientation": 1,
        "tileX": 9,
        "tileY": 3
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 10,
        "tileY": 3
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 0,
        "tileX": 11,
        "tileY": 3
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 12,
        "tileY": 3
        },

        {
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 0,
        "tileY": 4
        },{
        "sprite": "spawnTile",
        "orientation": 0,
        "tileX": 1,
        "tileY": 4
        },{
        "sprite": "wallTile",
        "orientation": 1,
        "tileX": 2,
        "tileY": 4
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 3,
        "tileY": 4
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 2,
        "tileX": 4,
        "tileY": 4
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 5,
        "tileY": 4
        },{
        "sprite": "wallTile",
        "orientation": 2,
        "tileX": 6,
        "tileY": 4
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 7,
        "tileY": 4
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 8,
        "tileY": 4
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 9,
        "tileY": 4
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 10,
        "tileY": 4
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 0,
        "tileX": 11,
        "tileY": 4
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 12,
        "tileY": 4
        },

        {
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 0,
        "tileY": 5
        },{
        "sprite": "spawnTile",
        "orientation": 0,
        "tileX": 1,
        "tileY": 5
        },{
        "sprite": "wallTile",
        "orientation": 1,
        "tileX": 2,
        "tileY": 5
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 3,
        "tileY": 5
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 2,
        "tileX": 4,
        "tileY": 5
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 5,
        "tileY": 5
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 6,
        "tileY": 5
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 7,
        "tileY": 5
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 8,
        "tileY": 5
        },{
        "sprite": "wallTile",
        "orientation": 0,
        "tileX": 9,
        "tileY": 5
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 10,
        "tileY": 5
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 0,
        "tileX": 11,
        "tileY": 5
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 12,
        "tileY": 5
        },

        {
        "sprite": "spawnTile",
        "orientation": 0,
        "tileX": 0,
        "tileY": 6
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 1,
        "tileY": 6
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 2,
        "tileY": 6
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 3,
        "tileY": 6
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 2,
        "tileX": 4,
        "tileY": 6
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 5,
        "tileY": 6
        },{
        "sprite": "wallTile",
        "orientation": 3,
        "tileX": 6,
        "tileY": 6
        },{
        "sprite": "wallTile",
        "orientation": 1,
        "tileX": 7,
        "tileY": 6
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 8,
        "tileY": 6
        },{
        "sprite": "wallTile",
        "orientation": 2,
        "tileX": 9,
        "tileY": 6
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 10,
        "tileY": 6
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 0,
        "tileX": 11,
        "tileY": 6
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 12,
        "tileY": 6
        },

        {
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 0,
        "tileY": 7
        },{
        "sprite": "wallTile",
        "orientation": 2,
        "tileX": 1,
        "tileY": 7
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 2,
        "tileY": 7
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 1,
        "tileX": 3,
        "tileY": 7
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 2,
        "tileX": 4,
        "tileY": 7
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 5,
        "tileY": 7
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 6,
        "tileY": 7
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 7,
        "tileY": 7
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 8,
        "tileY": 7
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 9,
        "tileY": 7
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 10,
        "tileY": 7
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 0,
        "tileX": 11,
        "tileY": 7
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 12,
        "tileY": 7
        },

        {
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 0,
        "tileY": 8
        },{
        "sprite": "spawnTile",
        "orientation": 0,
        "tileX": 1,
        "tileY": 8
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 2,
        "tileY": 8
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 1,
        "tileX": 3,
        "tileY": 8
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 1,
        "tileX": 4,
        "tileY": 8
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 1,
        "tileX": 5,
        "tileY": 8
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 1,
        "tileX": 6,
        "tileY": 8
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 1,
        "tileX": 7,
        "tileY": 8
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 1,
        "tileX": 8,
        "tileY": 8
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 1,
        "tileX": 9,
        "tileY": 8
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 1,
        "tileX": 10,
        "tileY": 8
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 0,
        "tileX": 11,
        "tileY": 8
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 12,
        "tileY": 8
        },

        {
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 0,
        "tileY": 9
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 1,
        "tileY": 9
        },{
        "sprite": "conveyorForwardOne",
        "orientation": 1,
        "tileX": 2,
        "tileY": 9
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 3,
        "tileY": 9
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 4,
        "tileY": 9
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 5,
        "tileY": 9
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 6,
        "tileY": 9
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 7,
        "tileY": 9
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 8,
        "tileY": 9
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 9,
        "tileY": 9
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 0,
        "tileX": 10,
        "tileY": 9
        },{
        "sprite": "conveyorForwardTwo",
        "orientation": 0,
        "tileX": 11,
        "tileY": 9
        },{
        "sprite": "normalTile",
        "orientation": 0,
        "tileX": 12,
        "tileY": 9
        }]
    

numberChoicesRectList = []
for i in range(5):
    numberChoicesRectList.append(allSprites["normalTile"][0].get_rect(center = (730 + i*110,600)))
numberOfPlayers = 0
playersTurn = 0
selectNewCard = True
checkedValidMovement = False
firstItterationOfRegister = True
register = 0
mainMenu = True

while mainMenu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mousePos = pygame.mouse.get_pos()
            for i, normalTileRect in enumerate(numberChoicesRectList):
                if normalTileRect.collidepoint(mousePos):
                    numberOfPlayers = i+2
                    mainMenu = False

    
    screen.blit(logo,logoRect)
    screen.blit(myFont.render('How many players?', False, (250,250,250)), (800,350))
    for i in range(5):
        screen.blit(normalTile, numberChoicesRectList[i])
        screen.blit(myFont.render(str(i+2), False, (0,0,0)), (720 + i*110,580))
    pygame.display.update()
    clock.tick(30)

robots = initiateRobots()
numberOfPlayers -= 1
del robots[1]
robots[0].tileY = 1
robots[0].tileX = 1
gameLoopNumber = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if not(robots[playersTurn].register): # In future people will choose card themselves. For now it picks randomly
        robot.fillRegisters()
    
    if gameLoopNumber > 10:
        print("PlayersTurn:", playersTurn, "Register:", register)
        print("TileX:", robots[playersTurn].tileX, "TileY:", robots[playersTurn].tileY, "PixelX:", robots[playersTurn].pixelX, "PixelY:", robots[playersTurn].pixelY, "Orientation:", robots[playersTurn].orientation, "Register:", robots[playersTurn].register, "Moved:", robots[playersTurn].moved, "Moving:", robots[playersTurn].moving)
        move()

        print("TileX:", robots[playersTurn].tileX, "TileY:", robots[playersTurn].tileY, "PixelX:", robots[playersTurn].pixelX, "PixelY:", robots[playersTurn].pixelY, "Orientation:", robots[playersTurn].orientation, "Register:", robots[playersTurn].register, "Moved:", robots[playersTurn].moved, "Moving:", robots[playersTurn].moving)
    
        nextPlayer()
    
        nextRegister()
    drawGameBoard()
    robot.draw()              
    robot.drawRegister()
    print(gameLoopNumber)
    pygame.display.update()
    clock.tick(2)
    gameLoopNumber += 1


""" To do:
Make reshuffle function
When moving after instead of allways changing pixelY or PixelX, check if instead is time to reset it and change tileX or tileY instead(for orientation 1 and 2)
Changed movement to do one bot until that bot is finnished moving. This might have introduced bugs when deciding wether or not to increase register after the first player is done moving(dont think so) or when the code changes moved or moving as it I think the code does it for all of them at the same time.
"""
