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
player_speed = 5
player_bullet_points = []

# ---------------------------
# Load images
background = pygame.transform.scale(pygame.image.load("chess-background.png").convert(), (WIDTH, HEIGHT))

# Functions



running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("click")
            bullet = [circle_x, circle_y, 5, 0]
            player_bullet_points.append(bullet)
        if event.type == pygame.QUIT:
            running = False

    # GAME STATE UPDATES
    # All game math and comparisons happen here
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for b in player_bullet_points:
        b[0] += b[2]
        b[1] -= b[3]

    # WASD movement
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

    # background
    screen.fill((255, 255, 255))  # always the first drawing command
    # screen.blit(background, (0,0))

    # dummy enemy
    pygame.draw.circle(screen, (255, 0, 0), (WIDTH/2, HEIGHT/2), 30)
    # player
    pygame.draw.circle(screen, (0, 255, 0), (circle_x, circle_y), 15)

    # bullet tragectory
    pygame.draw.line(screen, (0, 0, 0), (circle_x, circle_y), (mouse_x, mouse_y), 5)

    # bullet
    for b in player_bullet_points:
        x = b[0]
        y = b[1]
        pygame.draw.circle(screen, (255, 255, 0), (x, y), 2)


    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)
    #---------------------------


pygame.quit()
