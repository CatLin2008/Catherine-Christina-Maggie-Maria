# pygame template

import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

# background
background = pygame.image.load("chess-background.jpg")
#adding the white pawn png into the code 
white_pawn = pygame.image.load("white-chess-piece.png")
#change the scale of the picture so it isn't so large
white_pawn = pygame.transform.scale(white_pawn, (50, 115))



pygame.init()
#Christina changed the size to 1000 x 800 for a more comfortable user gameplay
WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables

circle_x = WIDTH/2
circle_y = HEIGHT/2
#inital trial for where to place pawn, creating variable later to be edited
pawn_x = 50
pawn_y = 50
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
    

    # DRAWING
    screen.fill((255, 255, 255))  # always the first drawing command

    # background image
    screen.blit(background, (0,0))

    pygame.draw.circle(screen, (0, 0, 255), (circle_x, circle_y), 30)

    #draw the pawn image onto the screen
    screen.blit(white_pawn, (pawn_x, pawn_y))


    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
