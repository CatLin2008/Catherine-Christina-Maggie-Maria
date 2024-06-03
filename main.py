# pygame template

import pygame, sys, math, random
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

# background
# background
background = pygame.image.load("Untitled drawing.png")
white_player = pygame.image.load("white-chess-piece.png")
player_width = 60
player_height = 115
white_player = pygame.transform.scale(white_player, (player_width, player_height))


#queen power up image
queenPUP = pygame.image.load("queen_powerup.png")
queenPUP = pygame.transform.scale(queenPUP, (80, 80))

#health power up image
healthPUP = pygame.image.load("health_potion.png")
healthPUP = pygame.transform.scale(healthPUP, (50, 50))

#rook power up image
rookPUP = pygame.image.load("rook_potion.png")
rookPUP = pygame.transform.scale(rookPUP, (50, 50))

#laser power up image
laserPUP = pygame.image.load("laser_powerup.png")
laserPUP = pygame.transform.scale(laserPUP, (70, 70))

pygame.init()

WIDTH = 800
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)

#font 
text_font = pygame.font.SysFont(None, 40, bold = True)
text_font_smaller = pygame.font.SysFont(None, 20, bold = True)

def print_text(text, font, text_colour, text_x, text_y):
    image = font.render(text, True, text_colour)
    screen.blit(image, (text_x, text_y))

# caption
pygame.display.set_caption("Dethroned")

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# Initialize global variables

#catherines code for the player
player_x = WIDTH/2
player_y = HEIGHT/2
player_speed = 5

player_bullets = []
bullet_speed = 10
bullet_life = 200

enemies = []
enemy_health = 100
enemy_speed = 3
b_x = 0
b_y = 0

# points system
points = 0
bullet_hit = 10
enemy_kill = 200

#queen powerup location
queenPUP_x = random.randrange(0, 800)
queenPUP_y = random.randrange(0,700)
queenPUP_list = [
    pygame.Rect(queenPUP_x, queenPUP_y, 2, 5)
]
queenPUP_counter = 0

#health powerup location
healthPUP_x = 70
healthPUP_y = 60
healthPUP_list = [
    pygame.Rect(healthPUP_x, healthPUP_y, 2, 5)
]
healthPUP_counter = 0

#laser powerup location
laserPUP_x = 150
laserPUP_y = 150
laserPUP_list = [
    pygame.Rect(laserPUP_x, laserPUP_y, 2, 5)
]
laserPUP_counter = 0

#rook powerup location
rookPUP_x = 100
rookPUP_y = 100
rookPUP_list = [
    pygame.Rect(rookPUP_x, rookPUP_y, 2, 5)
]
rookPUP_counter = 0

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
slot_x = 120

#locations of the slots, testing it for now 
slots = [
    (190, 620),  #1
    (285, 640),  #2
    (370, 640),  #3
    (435, 625),  #4
    (slot_x + 320, 630),  #5
    (slot_x + 400, 630),  #6
    (slot_x + 480, 630),  #7

]
#chatgpt
full_slots = [False] * len(slots)

# Function to get the next available slot
def get_next_available_slot():
    for i, occupied in enumerate(full_slots):
        if not occupied:
            full_slots[i] = True
            return slots[i]
    return None 

# distance calculator
def calc_dist(x1, y1, x2, y2):
    a = y2 - y1
    b = x2 - x1
    return (a**2 + b**2)**0.5

# vectors calculator
def calc_angle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1) # chat gpt

def calc_velocity(speed, angle):
    dx, dy = [speed * math.cos(angle), speed * math.sin(angle)]
    return dx, dy

# ----------------
# ---------------------------
# Functions
running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: # vectors for bullet
            click_x2, click_y2 = event.pos
            angle = calc_angle(player_x, player_y, mouse_x, mouse_y)
            dx, dy = calc_velocity(bullet_speed, angle)
            player_bullets.append([player_x, player_y, dx, dy, bullet_life])
        if event.type == pygame.QUIT:
            running = False

    # GAME STATE UPDATES
    # All game math and comparisons happen here

    # WASD movement
    #!! taken from mrgallo site
    keys = pygame.key.get_pressed()
    if keys[119] == True:  # w
        player_y -= 10

    if keys[97] == True:  # a
        player_x -= 10

    if keys[115] == True:  # s
        player_y += 10

    if keys[100] == True:  # d
        player_x += 10

    # Catherine's bullet & point system

    for b in player_bullets:
        b[0] += b[2]
        b[1] += b[3]
        b[4] -= 1
        
    player_bullets_alive = []
    for b in player_bullets:
        if b[4] >= 0:
            player_bullets_alive.append(b)
        
        b_x = b[0]
        b_y = b[1]
        b_hp = b[4]
    player_bullets = player_bullets_alive

    if enemy_health <= 0:
        points += enemy_kill

    # Catherine Enemy beta system

    if keys[112] == True:  # ~
        for _ in range(5):
                enemy = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT), 0, 0, enemy_health] 
                enemies.append(enemy)

    for e in enemies:
        enemy_to_player_dist = calc_dist(player_x, player_y, e[0], e[1])
        enemy_angle = calc_angle(e[0], e[1], player_x, player_y)
        e[2], e[3] = calc_velocity(enemy_speed, enemy_angle)
        bullet_to_enemy_dist = calc_dist(b_x, b_y, e[0], e[1])

        if enemy_to_player_dist != 0:
            e[0] += e[2]
            e[1] += e[3]

        if bullet_to_enemy_dist <= 40:
            b_hp = -1
            enemy_health -= 10
            points += bullet_hit





    #coins being collected 

# note: code will be added to store the coin in inventory
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for c in coins: 
        #command found online
        if c.colliderect(player_rect):
            coins.remove(c)
            c_collected += 1

#defining what a powerup should do when colliding the player
    def handle_powerup_collision(powerup_x, powerup_y, counter):
        if pygame.Rect(powerup_x, powerup_y, 80, 80).colliderect(player_rect):
            new_slot = get_next_available_slot()
            if new_slot:
                powerup_x, powerup_y = new_slot
                counter += 1
        return powerup_x, powerup_y, counter

    queenPUP_x, queenPUP_y, queenPUP_counter = handle_powerup_collision(queenPUP_x, queenPUP_y, queenPUP_counter)
    healthPUP_x, healthPUP_y, healthPUP_counter = handle_powerup_collision(healthPUP_x, healthPUP_y, healthPUP_counter)
    rookPUP_x, rookPUP_y, rookPUP_counter = handle_powerup_collision(rookPUP_x, rookPUP_y, rookPUP_counter)
    laserPUP_x, laserPUP_y, laserPUP_counter = handle_powerup_collision(laserPUP_x, laserPUP_y, laserPUP_counter)
    # DRAWING

    # background
    screen.fill((255, 255, 255))  # always the first drawing command

    # background image
    screen.blit(background, (0,0))

    # draw the pawn image
    screen.blit(white_player, (player_x, player_y))

    # enemy - Catherine
    for e in enemies:
        pygame.draw.circle(screen, (255, 0, 0), (e[0], e[1]), 25)
    
    # bullet tragectory
    pygame.draw.line(screen, (0, 0, 255), (player_x, player_y), (mouse_x, mouse_y), 1)

    # bullet
    for b in player_bullets:
        x = b[0]
        y = b[1]
        pygame.draw.circle(screen, (0, 0, 0), (x, y), 2)

    for b in player_bullets:
        pygame.draw.circle(screen, (0, 0, 0), (b[0], b[1]), 3)

    # Points bar
    print_text(f"{points}", text_font, (0,0,0), 10, 10)


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
    print_text(f"{c_collected}", text_font, (0,0,0), 650, 18)

    # Draw coins
    for c in coins:
        screen.blit(coin_image, (c[0],c[1]))

#draw health potions
    for health_potions in healthPUP_list:
        screen.blit(healthPUP, (healthPUP_x, healthPUP_y))
   
#draw queen powerups 
    for queen_pups in queenPUP_list: 
        screen.blit(queenPUP, (queenPUP_x, queenPUP_y))

#draw laser power ups    
    for laser_pups in laserPUP_list: 
        screen.blit(laserPUP, (laserPUP_x, laserPUP_y))
#draw rook power ups
    for rook_pups in rookPUP_list: 
        screen.blit(rookPUP, (rookPUP_x, rookPUP_y))

#coding for numbering how many powerups you pick uo 
    if queenPUP_x == 190 and queenPUP_y == 620:
        print_text(f"{queenPUP_counter}", text_font_smaller, (0,0,0), 250, 630)
    
    if rookPUP_x == 285 and rookPUP_y == 640:
        print_text(f"{rookPUP_counter}", text_font_smaller, (0,0,0), 330, 630)
    
    if healthPUP_x == 370 and healthPUP_y == 640:
        print_text(f"{healthPUP_counter}", text_font_smaller, (0,0,0), 410, 630)

    if laserPUP_x == 435 and laserPUP_y == 625:
        print_text(f"{laserPUP_counter}", text_font_smaller, (0,0,0), 490, 630)
    
        



    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)
    #---------------------------


pygame.quit()
