# pygame template

import pygame
import random 
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

# background chess brown
background = pygame.image.load("Untitled drawing.png")
#adding the white pawn png into the code 
white_pawn = pygame.image.load("white-chess-piece.png")
#change the scale of the picture so it isn't so large
white_pawn = pygame.transform.scale(white_pawn, (50, 115))

#queen power up image and scale
queenPUP = pygame.image.load("queen_powerup.png")
queenPUP = pygame.transform.scale(queenPUP, (80, 80))

#health power up image and scale
healthPUP = pygame.image.load("health_potion.png")
healthPUP = pygame.transform.scale(healthPUP, (50, 50))


pygame.init()
#Christina changed the size to 1000 x 800 for a more comfortable user gameplay
WIDTH = 800
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables

#catherines code for the player but Christina changed the "circle" to pawn to make it the character
click = False
player_speed = 5 
pawn_x = WIDTH/2
pawn_y = HEIGHT/2

#queen powerup location, maybe to be changed to not be random
queenPUP_x = random.randrange(0, 800)
queenPUP_y = random.randrange(0,700)

#health powerup location, maybe to be changed to not be random
healthPUP_x = random.randrange(0, 800)
healthPUP_y = random.randrange(0,700)

# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False

    # GAME STATE UPDATES
    # All game math and comparisons happen here

    #!! taken from mrgallo site
    keys = pygame.key.get_pressed()
    if keys[119] == True:  # w
        circle_y -= 10

    if keys[97] == True:  # a
        circle_x -= 10

    if keys[115] == True:  # s
        circle_y += 10

    if keys[100] == True:  # d
        circle_x += 10

    #following code is t
    if pawn_x ==  queenPUP_x and pawn_y == queenPUP_y:
        #CODE NEEDS TO GO IN HERE FOR QUEEN POWER UPS
        # will be made to include all the different power ups: lazers, health, rook
    
    if pawn_x ==  healthPUP_x and pawn_y == healthPUP_y:
        #CODE NEEDS TO GO IN HERE FOR HEALTH POWER UPS 
        # will be made when health system is figured out

    # DRAWING
    screen.fill((255, 255, 255))  # always the first drawing command

    # background image
    screen.blit(background, (0,0))

    pygame.draw.circle(screen, (0, 0, 255), (circle_x, circle_y), 30)

    #draw the pawn image onto the screen
    screen.blit(white_pawn, (pawn_x, pawn_y))

    # draw the pawn image
    screen.blit(white_pawn, (pawn_x, pawn_y))
    #queen power up 
    screen.blit(queenPUP, (queenPUP_x, queenPUP_y))
    #health power up 
    screen.blit(healthPUP, (healthPUP_x, healthPUP_y))


    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
