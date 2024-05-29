# pygame template

import pygame, sys, math
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

pygame.init()

WIDTH = 800
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)

#font 
text_font = pygame.font.SysFont(None, 40, bold = True)

def print_text(text, font, text_colour, text_x, text_y):
    image = font.render(text, True, text_colour)
    screen.blit(image, (text_x, text_y))

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
 

# ---------------------------

# ---------------------------
# Initialize global variables

circle_x = WIDTH/2
circle_y = HEIGHT/2
player_speed = 5
player_bullet_points = []


#Christina added queen powerup location
queenPUP_x = random.randrange(0, 800)
queenPUP_y = random.randrange(0,700)
queenPUP_list = [
    pygame.Rect(queenPUP_x, queenPUP_y, 2, 5)
]

#health powerup location
healthPUP_x = 70
healthPUP_y = 60
healthPUP_list = [
    pygame.Rect(healthPUP_x, healthPUP_y, 2, 5)
]

coin_image = pygame.image.load('coin.png')
coin_image = pygame.transform.scale(coin_image, (45, 50))
coins = [
    pygame.Rect(100, 255, 23, 23),
    pygame.Rect(600, 333, 23, 23)
]
c_collected = 0
#coin bar
coin_bar_height = 60
coin_bar_width = 200
coin_bar_color = (255, 215, 0)

#inventory bar
inventory_bar_height = 80
inventory_bar_width = 580
inventory_bar_colour = (139, 69, 19) 
slot_measurements = 65
slot_colour = (196, 164, 132)
slot_x = 118
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

    # drawing the pawn image
    screen.blit(white_pawn, (pawn_x, pawn_y))
    #inventory lower bar 
    pygame.draw.rect(screen, inventory_bar_colour, (100, 620, inventory_bar_width, inventory_bar_height))
    pygame.draw.rect(screen, slot_colour, (slot_x, 630, slot_measurements, slot_measurements))
    pygame.draw.rect(screen, slot_colour, (slot_x+80, 630, slot_measurements, slot_measurements))
    pygame.draw.rect(screen, slot_colour, (slot_x+160, 630, slot_measurements, slot_measurements))
    pygame.draw.rect(screen, slot_colour, (slot_x+240, 630, slot_measurements, slot_measurements))
    pygame.draw.rect(screen, slot_colour, (slot_x+320, 630, slot_measurements, slot_measurements))
    pygame.draw.rect(screen, slot_colour, (slot_x+400, 630, slot_measurements, slot_measurements))
    pygame.draw.rect(screen, slot_colour, (slot_x+480, 630, slot_measurements, slot_measurements))

    #coin bar 
    pygame.draw.rect(screen, coin_bar_color, (WIDTH - coin_bar_width, 0, coin_bar_width, coin_bar_height))
    screen.blit(coin_image, (600,5))
    print_text(f"$ {c_collected}", text_font, (0,0,0), 650, 18)

    # drawing the coins in random positions 
    for c in coins:
        screen.blit(coin_image, (c[0],c[1]))

    #drawing the different health potions 
    for health_potions in healthPUP_list:
        screen.blit(healthPUP, (healthPUP_x, healthPUP_y))
   #drawing the queen power up 
    for queen_pups in queenPUP_list: 
        screen.blit(queenPUP, (queenPUP_x, queenPUP_y))
        



    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)
    #---------------------------


pygame.quit()
