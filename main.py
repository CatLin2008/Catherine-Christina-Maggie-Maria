# pygame template

import pygame, sys, math
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

pygame.init()

WIDTH = 800
HEIGHT = 650
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables

circle_x = WIDTH/2
circle_y = HEIGHT/2
click = False
player_speed = 5

# ---------------------------
# Load images
background = pygame.transform.scale(pygame.image.load("chess-background.png").convert(), (WIDTH, HEIGHT))

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            x, y = event.pos
            click = True
        if event.type == pygame.QUIT:
            running = False

    # GAME STATE UPDATES
    # All game math and comparisons happen here


    #!! taken from mrgallo site
    keys = pygame.key.get_pressed()
    if keys[119] == True:  # w
        circle_y -= player_speed

    if keys[97] == True:  # a
        circle_x -= player_speed

    if keys[115] == True:  # s
        circle_y += player_speed

    if keys[100] == True:  # d
        circle_x += player_speed
    

    # DRAWING
    screen.fill((255, 255, 255))  # always the first drawing command

    screen.blit(background, (0,0))

    pygame.draw.circle(screen, (255, 0, 0), (WIDTH/2, HEIGHT/2), 30)
    pygame.draw.circle(screen, (0, 255, 0), (circle_x, circle_y), 15)

    if click == True:
        pygame.draw.line(screen, (0, 0, 0), (circle_x, circle_y), (x, y), 5)

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)
    #---------------------------


pygame.quit()
