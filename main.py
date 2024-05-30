import pygame
import random 

from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

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

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
 

# ---------------------------
# Initialize global variables

#catherines code for the player
click = False
player_speed = 5
player_bullet_points = []
player_x = WIDTH/2
player_y = HEIGHT/2



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

#locations of the slots
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_x2, click_y2 = event.pos
            life = 30
            dx = (click_x2 - player_x)/5
            dy = (-click_y2 + player_y)/5
            bullet = [player_x, player_y, dx, dy, life]
            player_bullet_points.append(bullet)
        if event.type == pygame.QUIT:
            running = False


    # GAME STATE UPDATES
    # All game math and comparisons happen here
    mouse_x, mouse_y = pygame.mouse.get_pos()

    #code for the bullets 
    for b in player_bullet_points:
        b[0] += b[2]
        b[1] -= b[3] 
        b[4] -= 1
        if b[0]>WIDTH/2-15 and b[0]<WIDTH/2+15 and b[1]>HEIGHT/2-15 and b[1]<HEIGHT/2+15:
            b[4] = -1
        

    #code determining alive or not 
    alive = []
    for b in player_bullet_points:
        if b[4] > 0:
            alive.append(b)
    player_bullet_points = alive
        

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
    
    #coins being collected 

# note: code will be added to store the coin in inventory
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for c in coins: 
        #command found online
        if c.colliderect(player_rect):
            coins.remove(c)
            c_collected += 1

#defining what a powerup should do when colliding with the player
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

 
    screen.fill((255, 255, 255))  # always the first drawing command

    # background image
    screen.blit(background, (0,0))


    # draw the pawn image

    screen.blit(white_player, (player_x, player_y))

     # bullet tragectory
    pygame.draw.line(screen, (0, 0, 255), (player_x, player_y), (mouse_x, mouse_y), 1)

    # bullet
    for b in player_bullet_points:
        x = b[0]
        y = b[1]
        pygame.draw.circle(screen, (0, 0, 0), (x, y), 2)

    #inventory lower bar 
    pygame.draw.rect(screen, inventory_bar_colour, (100, 620, inventory_bar_width, inventory_bar_height))
    pygame.draw.rect(screen, slot_colour, (slot_x, 630, slot_measurements, slot_measurements))
    pygame.draw.rect(screen, slot_colour, (slot_x+80, 630, slot_measurements, slot_measurements))
    pygame.draw.rect(screen, slot_colour, (slot_x+160, 630, slot_measurements, slot_measurements))
    pygame.draw.rect(screen, slot_colour, (slot_x+240, 630, slot_measurements, slot_measurements))
    pygame.draw.rect(screen, slot_colour, (slot_x+320, 630, slot_measurements, slot_measurements))
    pygame.draw.rect(screen, slot_colour, (slot_x+400, 630, slot_measurements, slot_measurements))
    pygame.draw.rect(screen, slot_colour, (slot_x+480, 630, slot_measurements, slot_measurements))

    #dummy enemy
    pygame.draw.polygon(screen, (255, 0, 0), ((WIDTH/2-15, HEIGHT/2-15),(WIDTH/2+15, HEIGHT/2-15),(WIDTH/2+15, HEIGHT/2 + 15),(WIDTH/2-15, HEIGHT/2 + 15)))
    
    #coin bar 
    pygame.draw.rect(screen, coin_bar_color, (WIDTH - coin_bar_width, 0, coin_bar_width, coin_bar_height))
    screen.blit(coin_image, (600,5))
    print_text(f"$ {c_collected}", text_font, (0,0,0), 650, 18)


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
        print_text(f"{queenPUP_counter}", text_font_smaller, (0,0,0), queenPUP_x + 50, 630)
    
    if rookPUP_x == 285 and rookPUP_y == 640:
        print_text(f"{rookPUP_counter}", text_font_smaller, (0,0,0), 330, 630)
    
    if healthPUP_x == 370 and healthPUP_y == 640:
        print_text(f"{healthPUP_counter}", text_font_smaller, (0,0,0), 410, 630)

    if laserPUP_x == 435 and laserPUP_y == 625:
        print_text(f"{laserPUP_counter}", text_font_smaller, (0,0,0), 490, 630)
    


        
    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
