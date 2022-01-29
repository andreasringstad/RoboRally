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

def drawGameBoard():
    screen.fill((0,0,0))
    for tile in listOfTiles:
        screen.blit(allSprites[tile["sprite"]][tile["orientation"]], (tile["tileX"]*100, tile["tileY"]*100))

def initiatePlayers():
    player = {
        "tileX": 0,
        "tileY": 0,
        "pixelX": 0,
        "pixelY": 0,
        "orientation": 1,
        "deck": [ #"again", "again", removed as for now it makes no sense
            "leftTurn", "leftTurn", "leftTurn", "move1", "move1", "move1", "move1", "move1", "move2", "move2", "move2", "move3", "moveBack", "powerUp", "rightTurn", "rightTurn", "rightTurn", "uTurn"
        ],
        "hand": [],
        "discard": [],
        "register": [],
        "sprite": "twonky",
        "moved": False,
        "moving": False,
        "movementLeftInTiles": 0,
        "movementLeftInTicks": 0,
        "movementDirection": 0,
        "movementAxis": "X",
        "movement": 0,
        "alive": True 
    }
    players = []
    for i in range(numberOfPlayers):
        players.append(player.copy())
    return players

def drawPlayers():
    for player in players:
        screen.blit(allSprites[player["sprite"]][player["orientation"]], (player["tileX"]*100+player["pixelX"], player["tileY"]*100+player["pixelY"]))

def drawRegister():
    for i in range(len(players[playersTurn]["register"])):
        screen.blit(allSprites["card"][players[0]["register"][i]], (1300+124*i,0))
    pygame.draw.rect(screen, (255, 0, 0), [1300+124*register, 0, 124, 171], 10)

def movementValid(): # Returns True or False

    if players[playersTurn]["register"][register] == "leftTurn" or players[playersTurn]["register"][register] == "powerUp" or players[playersTurn]["register"][register] == "rightTurn" or players[playersTurn]["register"][register] == "uTurn":
        return True
    
    elif players[playersTurn]["register"][register] == "move1" or players[playersTurn]["register"][register] == "move2" or players[playersTurn]["register"][register] == "move3": # Kan muligens refactoreres ettersom orientasjonene er 0 og 2 eller 1 og 3...
        if players[playersTurn]["orientation"] == 0:
            for tile in listOfTiles:
                if (tile["tileX"] == players[playersTurn]["tileX"]) and (tile["tileY"] == players[playersTurn]["tileY"]):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 0:
                            return False
                elif (tile["tileX"] == players[playersTurn]["tileX"]) and (tile["tileY"] == players[playersTurn]["tileY"]-1):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 2:
                            return False
        
        if players[playersTurn]["orientation"] == 1:
            for tile in listOfTiles:
                if (tile["tileX"] == players[playersTurn]["tileX"]) and (tile["tileY"] == players[playersTurn]["tileY"]):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 1:
                            return False
                elif (tile["tileX"] == players[playersTurn]["tileX"]+1) and (tile["tileY"] == players[playersTurn]["tileY"]):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 3:
                            return False
        
        if players[playersTurn]["orientation"] == 2:
            for tile in listOfTiles:
                if (tile["tileX"] == players[playersTurn]["tileX"]) and (tile["tileY"] == players[playersTurn]["tileY"]):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 2:
                            return False
                elif (tile["tileX"] == players[playersTurn]["tileX"]) and (tile["tileY"] == players[playersTurn]["tileY"]+1):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 0:
                            return False
        
        if players[playersTurn]["orientation"] == 3:
            for tile in listOfTiles:
                if (tile["tileX"] == players[playersTurn]["tileX"]) and (tile["tileY"] == players[playersTurn]["tileY"]):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 3:
                            return False
                elif (tile["tileX"] == players[playersTurn]["tileX"]-1) and (tile["tileY"] == players[playersTurn]["tileY"]):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 1:
                            return False
    
    elif players[playersTurn]["register"][register] == "moveBack":
        if players[playersTurn]["orientation"] == 0:
            for tile in listOfTiles:
                if (tile["tileX"] == players[playersTurn]["tileX"]) and (tile["tileY"] == players[playersTurn]["tileY"]):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 2:
                            return False
                elif (tile["tileX"] == players[playersTurn]["tileX"]) and (tile["tileY"] == players[playersTurn]["tileY"]+1):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 0:
                            return False
                            
        if players[playersTurn]["orientation"] == 1:
            for tile in listOfTiles:
                if (tile["tileX"] == players[playersTurn]["tileX"]) and (tile["tileY"] == players[playersTurn]["tileY"]):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 3:
                            return False
                elif (tile["tileX"] == players[playersTurn]["tileX"]-1) and (tile["tileY"] == players[playersTurn]["tileY"]):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 1:
                            return False
                            
        if players[playersTurn]["orientation"] == 2:
            for tile in listOfTiles:
                if (tile["tileX"] == players[playersTurn]["tileX"]) and (tile["tileY"] == players[playersTurn]["tileY"]):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 0:
                            return False
                elif (tile["tileX"] == players[playersTurn]["tileX"]) and (tile["tileY"] == players[playersTurn]["tileY"]-1):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 2:
                            return False
                            
        if players[playersTurn]["orientation"] == 3:
            for tile in listOfTiles:
                if (tile["tileX"] == players[playersTurn]["tileX"]) and (tile["tileY"] == players[playersTurn]["tileY"]):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 1:
                            return False
                elif (tile["tileX"] == players[playersTurn]["tileX"]+1) and (tile["tileY"] == players[playersTurn]["tileY"]):
                    if tile["sprite"] == "wallTile":
                        if tile["orientation"] == 3:
                            return False
    return True

def move():
    global firstItterationOfRegister
    movement = 50 # Movement * movementTicks should be roughly 100 to avoid the bot from jumping when ariving at new tiles
    movementTicks = 2
    if firstItterationOfRegister:
        players[playersTurn]["moved"] = True
        firstItterationOfRegister = False
        if movementValid():
            players[playersTurn]["moving"] = True
            players[playersTurn]["movement"] = movement

            if players[playersTurn]["register"][register] == "move1":
                players[playersTurn]["movementLeftInTiles"] = 1
                players[playersTurn]["movementLeftInTicks"] = movementTicks
                if players[playersTurn]["orientation"] == 0:
                    players[playersTurn]["movementDirection"] = -1
                    players[playersTurn]["movementAxis"] = "Y"
                    players[playersTurn]["tileY"] -= 1
                    players[playersTurn]["pixelY"] = movement * movementTicks
                elif players[playersTurn]["orientation"] == 1:
                    players[playersTurn]["movementDirection"] = 1
                    players[playersTurn]["movementAxis"] = "X"
                elif players[playersTurn]["orientation"] == 2:
                    players[playersTurn]["movementDirection"] = 1
                    players[playersTurn]["movementAxis"] = "Y"
                else:
                    players[playersTurn]["movementDirection"] = -1
                    players[playersTurn]["movementAxis"] = "X"
                    players[playersTurn]["tileX"] -= 1
                    players[playersTurn]["pixelX"] = movement * movementTicks

            elif players[playersTurn]["register"][register] == "move2":
                players[playersTurn]["movementLeftInTiles"] = 2
                players[playersTurn]["movementLeftInTicks"] = movementTicks
                if players[playersTurn]["orientation"] == 0:
                    players[playersTurn]["movementDirection"] = -1
                    players[playersTurn]["movementAxis"] = "Y"
                    players[playersTurn]["tileY"] -= 1
                    players[playersTurn]["pixelY"] = movement * movementTicks
                elif players[playersTurn]["orientation"] == 1:
                    players[playersTurn]["movementDirection"] = 1
                    players[playersTurn]["movementAxis"] = "X"
                elif players[playersTurn]["orientation"] == 2:
                    players[playersTurn]["movementDirection"] = 1
                    players[playersTurn]["movementAxis"] = "Y"
                else:
                    players[playersTurn]["movementDirection"] = -1
                    players[playersTurn]["movementAxis"] = "X"
                    players[playersTurn]["tileX"] -= 1
                    players[playersTurn]["pixelX"] = movement * movementTicks

            elif players[playersTurn]["register"][register] == "move3":
                players[playersTurn]["movementLeftInTiles"] = 3
                players[playersTurn]["movementLeftInTicks"] = movementTicks
                if players[playersTurn]["orientation"] == 0:
                    players[playersTurn]["movementDirection"] = -1
                    players[playersTurn]["movementAxis"] = "Y"
                    players[playersTurn]["tileY"] -= 1
                    players[playersTurn]["pixelY"] = movement * movementTicks
                elif players[playersTurn]["orientation"] == 1:
                    players[playersTurn]["movementDirection"] = 1
                    players[playersTurn]["movementAxis"] = "X"
                elif players[playersTurn]["orientation"] == 2:
                    players[playersTurn]["movementDirection"] = 1
                    players[playersTurn]["movementAxis"] = "Y"
                else:
                    players[playersTurn]["movementDirection"] = -1
                    players[playersTurn]["movementAxis"] = "X"
                    players[playersTurn]["tileX"] -= 1
                    players[playersTurn]["pixelX"] = movement * movementTicks

            elif players[playersTurn]["register"][register] == "moveBack":
                players[playersTurn]["movementLeftInTiles"] = 1
                players[playersTurn]["movementLeftInTicks"] = movementTicks
                if players[playersTurn]["orientation"] == 0:
                    players[playersTurn]["movementDirection"] = 1
                    players[playersTurn]["movementAxis"] = "Y"
                elif players[playersTurn]["orientation"] == 1:
                    players[playersTurn]["movementDirection"] = -1
                    players[playersTurn]["movementAxis"] = "X"
                    players[playersTurn]["tileX"] -= 1
                    players[playersTurn]["pixelX"] = movement * movementTicks
                elif players[playersTurn]["orientation"] == 2:
                    players[playersTurn]["movementDirection"] = -1
                    players[playersTurn]["movementAxis"] = "Y"
                    players[playersTurn]["tileY"] -= 1
                    players[playersTurn]["pixelY"] = movement * movementTicks
                else:
                    players[playersTurn]["movementDirection"] = 1
                    players[playersTurn]["movementAxis"] = "X"        

        if players[playersTurn]["register"][register] == "leftTurn":
            players[playersTurn]["moving"] = False
            if players[playersTurn]["orientation"] == 0:
                players[playersTurn]["orientation"] = 3
            else: players[playersTurn]["orientation"] -= 1

        elif players[playersTurn]["register"][register] == "rightTurn":
            players[playersTurn]["moving"] = False
            if players[playersTurn]["orientation"] == 3:
                players[playersTurn]["orientation"] = 0
            else: players[playersTurn]["orientation"] += 1  

        elif players[playersTurn]["register"][register] == "uTurn":
            players[playersTurn]["moving"] = False
            if players[playersTurn]["orientation"] < 2:
                players[playersTurn]["orientation"] += 2
            else: players[playersTurn]["orientation"] -= 2

        elif players[playersTurn]["register"][register] == "powerUp": # Todo, needs work
            players[playersTurn]["moving"] = False

        elif players[playersTurn]["register"][register] == "again": # Todo, needs work
            players[playersTurn]["moving"] = False

    if players[playersTurn]["movementLeftInTicks"]:
        players[playersTurn]["pixel" + players[playersTurn]["movementAxis"]] += players[playersTurn]["movement"] * players[playersTurn]["movementDirection"]
        players[playersTurn]["movementLeftInTicks"] -= 1

    elif players[playersTurn]["movementLeftInTiles"]:
        players[playersTurn]["pixel" + players[playersTurn]["movementAxis"]] = 0
        if players[playersTurn]["register"][register] == "move1" or players[playersTurn]["register"][register] == "move2" or players[playersTurn]["register"][register] == "move3": 
            if players[playersTurn]["orientation"] == 1: #Move these four lines to after the movement pixelX/Y is done, check todo at the bottom!
                players[playersTurn]["tileX"] += 1
            elif players[playersTurn]["orientation"] == 2:
                players[playersTurn]["tileY"] += 1
        players[playersTurn]["movementLeftInTiles"] -= 1
        if players[playersTurn]["movementLeftInTiles"]:
            if movementValid():
                players[playersTurn]["movementLeftInTicks"] = movementTicks
                if players[playersTurn]["orientation"] == 0:
                    players[playersTurn]["movementDirection"] = -1
                    players[playersTurn]["movementAxis"] = "Y"
                    players[playersTurn]["tileY"] -= 1
                    players[playersTurn]["pixelY"] = movement * movementTicks
                elif players[playersTurn]["orientation"] == 3:
                    players[playersTurn]["movementDirection"] = -1
                    players[playersTurn]["movementAxis"] = "X"
                    players[playersTurn]["tileX"] -= 1
                    players[playersTurn]["pixelX"] = movement * movementTicks

        else:
            players[playersTurn]["movementLeftInTiles"] = 0
            players[playersTurn]["moving"] = False

def fillRegisters():
    for player in players:
        for y in range(5):
            player["register"].append(choice(player["deck"]))

def discardRegisters(): # Needs to be changed to discard cards to players discard pile in the future
    for player in players:
        player["register"] = []

def nextPlayer():
    global playersTurn
    if (players[playersTurn]["moved"]) or (not(players[playersTurn]["moving"])):
        playersTurn += 1
        if playersTurn > numberOfPlayers-1:
            playersTurn = 0

def nextRegister():
    global register
    global firstItterationOfRegister
    allPlayersDoneMoving = True
    for player in players:
        if (not(player["moved"])) or (player["moving"]):
            allPlayersDoneMoving = False
    if allPlayersDoneMoving:
        for player in players:
            player["moved"] = False
        firstItterationOfRegister = True
        register += 1
        if register > 4:
            register = 0
            discardRegisters()

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

players = initiatePlayers()
numberOfPlayers -= 1
del players[1]
players[0]["tileY"] = 1
players[0]["tileX"] = 1
gameLoopNumber = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if not(players[playersTurn]["register"]): # In future people will choose card themselves. For now it is automatic and random
        fillRegisters()
    
    if gameLoopNumber > 10:
        print("PlayersTurn:", playersTurn, "Register:", register)
        print("TileX:", players[playersTurn]["tileX"], "TileY:", players[playersTurn]["tileY"], "PixelX:", players[playersTurn]["pixelX"], "PixelY:", players[playersTurn]["pixelY"], "Orientation:", players[playersTurn]["orientation"], "Register:", players[playersTurn]["register"], "Moved:", players[playersTurn]["moved"], "Moving:", players[playersTurn]["moving"])
        move()

        print("TileX:", players[playersTurn]["tileX"], "TileY:", players[playersTurn]["tileY"], "PixelX:", players[playersTurn]["pixelX"], "PixelY:", players[playersTurn]["pixelY"], "Orientation:", players[playersTurn]["orientation"], "Register:", players[playersTurn]["register"], "Moved:", players[playersTurn]["moved"], "Moving:", players[playersTurn]["moving"])
    
        nextPlayer()
    
        nextRegister()
    drawGameBoard()
    drawPlayers()              
    drawRegister()
    print(gameLoopNumber)
    pygame.display.update()
    clock.tick(2)
    gameLoopNumber += 1


""" To do:
Make reshuffle function
When moving after instead of allways changing pixelY or PixelX, check if instead is time to reset it and change tileX or tileY instead(for orientation 1 and 2)
Changed movement to do one bot until that bot is finnished moving. This might have introduced bugs when deciding wether or not to increase register after the first player is done moving(dont think so) or when the code changes moved or moving as it I think the code does it for all of them at the same time.
"""
