# pygame template

import pygame, sys, math, random
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, K_RIGHT, K_LEFT, MOUSEBUTTONDOWN
#__________________________________
pygame.init()

WIDTH = 800
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)

def print_text(text, font, text_colour, text_x, text_y):
    image = font.render(text, True, text_colour)
    screen.blit(image, (text_x, text_y))

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# Initialize global variables
#________________________________________
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

#font 
text_font = pygame.font.SysFont(None, 40, bold = True)
text_font_smaller = pygame.font.SysFont(None, 20, bold = True)


#catherines code for the player
player_x = WIDTH/2
player_y = HEIGHT/2
player_speed = 5 
player_bullet = []
enemy_health = 100
death = False

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

#Maggie variables for images in main menu
circle_x = 200
circle_y = 200
pygame.font.get_default_font()
scene_title_font = pygame.font.SysFont('Courier New', 45)
current_screen = 0

startx = 150
starty = 120
exitx = 403
exity = 120
settingx = 604
settingy = 6

mouse_x = 0
mouse_y = 0
clicked = False

# Function to get the next available slot
def get_next_available_slot():
    for i, occupied in enumerate(full_slots):
        if not occupied:
            full_slots[i] = True
            return slots[i]
    return None 

# ---------------------------
# Functions
running = True
while running:
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_RIGHT:
                print("RIGHT ARROW PRESSED")
                current_screen += 1
                print(current_screen)
            elif event.key == K_LEFT:
                print("LEFT ARROW PRESSED")
                current_screen -= 1
                print(current_screen)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_x2, click_y2 = event.pos
            life = 30
            dx = (click_x2 - player_x)/5
            dy = (-click_y2 + player_y)/5
            bullet = [player_x, player_y, dx, dy, life]
            player_bullet.append(bullet)
        elif event.type == pygame.QUIT:
            running = False

    # GAME STATE UPDATES
    # All game math and comparisons happen here
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if event.type == MOUSEBUTTONDOWN:
        mouse_x, mouse_y = event.pos
        print(mouse_x, mouse_y)
        
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

    # Catherine's bullet system

    for b in player_bullet:
        b[0] += b[2]
        b[1] -= b[3] 
        b[4] -= 1
        if b[0]>WIDTH/2-15 and b[0]<WIDTH/2+15 and b[1]>HEIGHT/2-15 and b[1]<HEIGHT/2+15:
            b[4] = -1
            enemy_health -= 10
        
    player_bullet_alive = []
    for b in player_bullet:
        if b[4] > 0:
            player_bullet_alive.append(b)
    player_bullet = player_bullet_alive

    if enemy_health <= 0:
        death = True

     
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
    # dummy enemy
    if death == False:
        pygame.draw.polygon(screen, (255, 0, 0), ((WIDTH/2-15, HEIGHT/2-15),(WIDTH/2+15, HEIGHT/2-15),(WIDTH/2+15, HEIGHT/2 + 15),(WIDTH/2-15, HEIGHT/2 + 15)))


    # bullet tragectory
    pygame.draw.line(screen, (0, 0, 255), (player_x, player_y), (mouse_x, mouse_y), 1)

    # bullet
    for b in player_bullet:
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
        print_text(f"{queenPUP_counter}", text_font_smaller, (0,0,0), 250, 630)
    
    if rookPUP_x == 285 and rookPUP_y == 640:
        print_text(f"{rookPUP_counter}", text_font_smaller, (0,0,0), 330, 630)
    
    if healthPUP_x == 370 and healthPUP_y == 640:
        print_text(f"{healthPUP_counter}", text_font_smaller, (0,0,0), 410, 630)

    if laserPUP_x == 435 and laserPUP_y == 625:
        print_text(f"{laserPUP_counter}", text_font_smaller, (0,0,0), 490, 630)
    

#MAIN MENU(Maggie)
    chessboardImg = pygame.image.load('chessboard.jpg')
    screen.blit(chessboardImg, (100,100))


    screen.fill((123, 134, 150))  # always the first drawing command
    pygame.draw.circle(screen, (255, 254, 245), (circle_x, circle_y), 30)

    # Scene 1 (Menu screen) chessboard + title
    if current_screen == 0:

        chessboardImg = pygame.image.load('chessboard.jpg')
        # smallchessboard = pygame.transform.scale(chessboardImg, (30,30))

        screen.blit(chessboardImg, (2,-20))
        scene_title = scene_title_font.render('Menu Screen', True, (219, 33, 98))
        screen.blit(scene_title, (200, 0))

        pygame.draw.rect(screen, (242, 177, 202), (102,74,179,180))
        pygame.draw.rect(screen, (217, 87, 147), (364,74,179,180))

        #Start Button
        startImg = pygame.image.load('startbutton.png')
        smallstart = pygame.transform.scale(startImg, (97,80))
        screen.blit(smallstart, (startx, starty))
        #Exit Button
        ExitImg = pygame.image.load('exitbutton.png')
        smallexit = pygame.transform.scale(ExitImg, (97,60))
        screen.blit(smallexit, (exitx, exity))

        SettingImg = pygame.image.load('settingsbutton.png')
        smallsetting = pygame.transform.scale(SettingImg, (30,30))
        screen.blit(smallsetting, (settingx, settingy))


        #check if button clicked
        if (mouse_x>=startx and mouse_x<=startx+100) and (mouse_y>=starty and mouse_y<=starty+50) and clicked == False:
            
            print("Start Button CLicked")
            current_screen = 2
            mouse_x = 0
            mouse_y = 0
        elif (mouse_x>=exitx and mouse_x<=exitx+100) and (mouse_y>=exity and mouse_y<=exity+50) and clicked == False:
            print("Exit Button Clicked")
            mouse_x = 0 
            mouse_y = 0

            break
    # Scene 2 (Instructions screen)
    elif current_screen == 1:

        screen.fill((224, 202, 211)) 
        scene_title = scene_title_font.render('Instructions Screen', True, (242, 17, 109))
        screen.blit(scene_title, (90, 0))



    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)
    #---------------------------


pygame.quit()
