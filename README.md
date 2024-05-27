# ICS3U-CPT

# Basic Movement
import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables

circle_x = 200
circle_y = 200

# ---------------------------

running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    # GAME STATE UPDATES
    # All game math and comparisons happen here
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
    screen.fill((255, 255, 200))  # always the first drawing command

    pygame.draw.circle(screen, (0, 0, 255), (circle_x, circle_y), 30)




    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
