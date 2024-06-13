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
#______________________________________________
#catherines code for the player
player_x = WIDTH/2
player_y = HEIGHT/2
player_speed = 5
player_width = 60
player_height = 115

player_bullets = []
bullet_speed = 10
bullet_life = 200

enemies = []
enemies_rect = []
enemy_health = 100
enemy_speed = 1
b_x = 0
b_y = 0
e_colour = (0,255,0)
e_rect = (0, 0)

# points system
points = 0
bullet_hit = 10
enemy_kill = 200

#font 
text_font = pygame.font.SysFont(None, 40, bold = True)
text_font_smaller = pygame.font.SysFont(None, 20, bold = True)

# points system
points = 0
bullet_hit = 10
enemy_kill = 200

#font 
text_font = pygame.font.SysFont(None, 40, bold = True)
text_font_smaller = pygame.font.SysFont(None, 20, bold = True)

#queen powerup location
queenPUP_x = random.randrange(0, 750)
queenPUP_y = random.randrange(60, 500)
queen_visible = True 
queenPUP_list = [
    pygame.Rect(queenPUP_x, queenPUP_y, 2, 5)
]
queenPUP_counter = 0
queenPUP_x2 = 1000
queenPUP_y2 = -1000

#health powerup location
healthPUP_x = random.randrange(0, 800)
healthPUP_y = random.randrange(60, 500)
heath_visible = True 
healthPUP_list = [
    pygame.Rect(healthPUP_x, healthPUP_y, 2, 5)
]
healthPUP_counter = 0
healthPUP_x2 = 1000
healthPUP_y2 = -1000


#laser powerup location
laserPUP_x = random.randrange(0, 800)
laserPUP_y = random.randrange(60, 500)
laser_visible = True 
laserPUP_list = [
    pygame.Rect(laserPUP_x, laserPUP_y, 2, 5)
]
laserPUP_counter = 0
laserPUP_x2 = 1000
laserPUP_y2 = -1000

#rook powerup location
rookPUP_x = random.randrange(0, 800)
rookPUP_y = random.randrange(60, 500)
rook_visible = True 
rookPUP_list = [
    pygame.Rect(rookPUP_x, rookPUP_y, 2, 5)
]
rookPUP_counter = 0
rookPUP_x2 = 1000
rookPUP_y2 = -1000

coins = [
    pygame.Rect(100, 255, 23, 23),
    pygame.Rect(600, 333, 23, 23)
]
c_collected = 100
#coin bar
coin_bar_height = 60
coin_bar_width = 200
coin_bar_color = (255, 215, 0)

# Chest parameters
chest_x, chest_y = 500, 500
closedchest_list = [pygame.Rect(chest_x, chest_y, 90, 90)]
fullchest_list = []
emptychest_list = []

#inventory bar
inventory_bar_height = 80
inventory_bar_width = 580
inventory_bar_colour = (139, 69, 19) 
slot_measurements = 65
slot_colour = (196, 164, 132)
slot_x = 120

#locations of the slots
slots = [
    (110, 620),
    (190, 620), 
    (270, 620), 
    (350, 620), 
    (430, 620), 
    (510, 620),
    (590, 620)
]


#store 
store_width = 800
store_height = 700
store_colour = (92, 64, 51)
coin_colour = (196, 164, 132)
purchase_slots_width = 150
purchase_slots_height = 250 
og_purchase_x = 25
og_purchase_y = 200
laser_price = 10
queenPUP_price = 30
rookPUP_price = 20 
healthPUP_price = 20

store_open = False
chest_open = False
e_key_pressed = False
f_key_pressed = False

#locations for the powerups within the store for later purchases used
queen_in_store = pygame.Rect(og_purchase_x, og_purchase_y, purchase_slots_width, purchase_slots_height)
laser_in_store = pygame.Rect(225, og_purchase_y, purchase_slots_width, purchase_slots_height)
rookPUP_in_store = pygame.Rect(425, og_purchase_y, purchase_slots_width, purchase_slots_height)
health_in_store = pygame.Rect(625, og_purchase_y, purchase_slots_width, purchase_slots_height)

#chatgpt
full_slots = [False] * len(slots)

#Maggie variables in main menu
pygame.font.get_default_font()
scene_title_font = pygame.font.SysFont('Courier New', 37)
instruction_title_font = pygame.font.SysFont('Courier New', 16)
current_screen = 0
startx = 180
starty = 190
exitx = 540
exity = 190
settingx = 750
settingy = 6
titlex = 300
titley = 6
pausex = 746
pausey = 81
backx = 654
backy = 24
click_x = 0
click_y = 0
clicked = False
pause_open = False
menu_open = True

#______________________________________________
# Function to get the next available slot

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

def handle_powerup_collision(powerup_x, powerup_y, counter):
        if pygame.Rect(powerup_x, powerup_y, 80, 80).colliderect(player_rect):
            new_slot = slots[0]
            slots.pop(0)
            if new_slot:
                counter += 1
                powerup_x, powerup_y = new_slot
        return powerup_x, powerup_y, counter
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
        elif event.type == pygame.MOUSEBUTTONDOWN: #vectors for bullet
            if event.button == 1:  # Left mouse button
                click_x, click_y = event.pos
                angle = calc_angle(player_x, player_y, mouse_x, mouse_y)
                dx, dy = calc_velocity(bullet_speed, angle)
                player_bullets.append([player_x, player_y, dx, dy, bullet_life])
            
            #christina's code for the counters of parameters of the obejcts 
            if laserPUP_counter >= 1:
                if laser_parameters.collidepoint(event.pos):
                    laserPUP_counter -= 1
                    if laserPUP_counter < 1: 
                                laserPUP_x, laserPUP_y = -100, -100
                                laserPUP_x2, laserPUP_y2 = -100, -100
            if queenPUP_counter >= 1:
                if queen_parameters.collidepoint(event.pos):
                     queenPUP_counter -= 1
                     if queenPUP_counter < 1: 
                        queenPUP_x, queen_y = -100, -100
                        queenPUP_x2, queen_y2 = -100, -100
            if healthPUP_counter >= 1:
                if health_parameters.collidepoint(event.pos):
                     healthPUP_counter -= 1
                     if healthPUP_counter < 1: 
                        healthPUP_x, healthPUP_y = -100, -100
                        healthPUP_x2, healthPUP_y2 = -100, -100
            if rookPUP_counter >= 1:
                if rook_parameters.collidepoint(event.pos):
                    rookPUP_counter -= 1
                    if rookPUP_counter < 1: 
                                rookPUP_x, rookPUP_y = -100, -100
                                rookPUP_x2, rookPUP_y2 = -100, -100
            #if the store_open is true, then the coins collected go down in price
            if store_open:
                if queen_in_store.collidepoint(event.pos):
                    if c_collected > queenPUP_price:
                        c_collected -= queenPUP_price
                        queenPUP_counter += 1 
                        if queenPUP_y > 600: 
                            queenPUP_x2, queenPUP_y2 = queenPUP_x,queenPUP_y
                        elif slots: 
                            new_slot = slots.pop(0)
                            queenPUP_x2, queenPUP_y2 = new_slot
                if laser_in_store.collidepoint(event.pos):
                    if c_collected > laser_price:
                        c_collected -= laser_price
                        laserPUP_counter += 1
                        if laserPUP_y > 600: 
                            laserPUP_x2, laserPUP_y2 = laserPUP_x, laserPUP_y
                        elif slots: 
                            new_slot = slots.pop(0)
                            laserPUP_x2, laserPUP_y2 = new_slot
                if rookPUP_in_store.collidepoint(event.pos):
                    if c_collected > rookPUP_price:
                        c_collected -= rookPUP_price
                        rookPUP_counter += 1
                        if rookPUP_y > 600: 
                            rookPUP_x2, rookPUP_y2 = rookPUP_x, rookPUP_y
                        elif slots: 
                            new_slot = slots.pop(0)
                            rookPUP_x2, rookPUP_y2 = new_slot
                if health_in_store.collidepoint(event.pos):
                    if c_collected > healthPUP_price:
                        c_collected -= healthPUP_price
                        healthPUP_counter += 1
                        if healthPUP_y > 600: 
                            healthPUP_x2, healthPUP_y2 = healthPUP_x, healthPUP_y
                        elif slots and healthPUP_y < 600: 
                            new_slot = slots.pop(0)
                            healthPUP_x2, healthPUP_y2 = new_slot


        elif event.type == pygame.QUIT:
            running = False

    # GAME STATE UPDATES
    # All game math and comparisons happen here

    #parameters so theyre always updated
    rook_parameters = pygame.Rect(rookPUP_x, rookPUP_y, 90, 90)
    laser_parameters = pygame.Rect(laserPUP_x, laserPUP_y, 90, 90)
    queen_parameters = pygame.Rect(queenPUP_x, queenPUP_y, 90, 90)
    health_parameters = pygame.Rect(healthPUP_x, healthPUP_y, 90, 90)

        
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

      #adding a key press on E to open the store
    if keys[101]:  
        if not e_key_pressed:
            store_open = not store_open
            e_key_pressed = True

        else:
          e_key_pressed = False
    
    #PRESS f to collect the chest materials
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for chest in closedchest_list:
        if chest.colliderect(player_rect):
            closedchest_list.remove(chest)
            fullchest_list.append(pygame.Rect(chest_x, chest_y, 90, 90))
            selected_item = random.choice(chest_items)

    for chest in fullchest_list:
        if keys[102]:  
            if not f_key_pressed:
                f_key_pressed = True
            if fullchest_list:
                fullchest_list.pop()
                emptychest_list.append(pygame.Rect(chest_x, chest_y, 90, 90))
            if selected_item == laserPUP2:
                laserPUP_counter += 1
                laserPUP_x2, laserPUP_y2, laserPUP_counter = handle_powerup_collision(laserPUP_x2, laserPUP_y2, laserPUP_counter)
                if laserPUP_y > 600:
                        laserPUP_x2, laserPUP_y2 = laserPUP_x, laserPUP_y
                elif slots: 
                    new_slot = slots.pop(0)
                    laserPUP_x2, laserPUP_y2 = new_slot
            elif selected_item == healthPUP2:
                healthPUP_counter += 1 
                healthPUP_x2, healthPUP_y2, healthPUP_counter = handle_powerup_collision(healthPUP_x2, healthPUP_y2, healthPUP_counter)
                if healthPUP_y > 600:
                    healthPUP_x2, healthPUP_y2 = healthPUP_x, healthPUP_y
                elif slots: 
                    new_slot = slots.pop(0)
                    healthPUP_x2, healthPUP_y2 = new_slot
            elif selected_item == rookPUP2:
                rookPUP_counter += 1
                rookPUP_x2, rookPUP_y2, rookPUP_counter = handle_powerup_collision(rookPUP_x2, rookPUP_y2, rookPUP_counter)
                if rookPUP_y > 600:
                        rookPUP_x2, rookPUP_y2 = rookPUP_x, rookPUP_y
                elif slots:  
                    new_slot = slots.pop(0)
                    rookPUP_x2, rookPUP_y2 = new_slot
                    
            elif selected_item == coin_image:
                c_collected +=  1
                if slots:
                    slots.pop(0)  # Remove the slot if a coin is collected
        else:
            f_key_pressed = False

    # Catherine's bullet system
    for b in player_bullets:
        b[0] += b[2]
        b[1] += b[3]
        b[4] -= 1
        
    player_bullets_alive = []
    for b in player_bullets:
        if b[4] >= 0:
            player_bullets_alive.append(b)

    player_bullets = player_bullets_alive

    if enemy_health <= 0:
        points += enemy_kill

    # Catherine Enemy beta system

    if keys[112] == True:  # p
        for _ in range(1):
            e_x = random.randrange(0, WIDTH)
            e_y = random.randrange(0, HEIGHT)
            
            enemy = [e_x, e_y, 0, 0, enemy_health] 
            enemies.append(enemy)

            e_rect = pygame.Rect(e_x-10, e_y-10, 20, 20)
            enemies_rect.append(e_rect)

    
    enemies_alive = []

    for e in enemies:
        enemy_to_player_dist = calc_dist(player_x, player_y, e[0], e[1])
        enemy_angle = calc_angle(e[0], e[1], player_x, player_y)
        e[2], e[3] = calc_velocity(enemy_speed, enemy_angle)
        e_rect = pygame.Rect(e[0]-10, e[1]-10, 20, 20)

        if enemy_to_player_dist != 0:
            e[0] += e[2]
            e[1] += e[3]
        
        if e_rect.collidelist(enemies_rect):
            print("COLLIDE!!!")
        
        for b in player_bullets:
            b_rect = pygame.Rect(b[0]-2, b[1]-2, 4, 4)
            if b_rect.colliderect(e_rect):
                e[4] -= 10
                b[4] = -1
                points += bullet_hit
        
        if e[4] >= 0:
            enemies_alive.append(e)

    enemies = enemies_alive
    #coins being collected 
# note: code will be added to store the coin in inventory
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for c in coins: 
        #command found online
        if c.colliderect(player_rect):
            coins.remove(c)
            c_collected += 1
    
   #this is the code so that it doesnt collide and change spots when the sprite goes near the inventory box
    if queenPUP_y <= 600:
        queenPUP_x, queenPUP_y, queenPUP_counter = handle_powerup_collision(queenPUP_x, queenPUP_y, queenPUP_counter)
        if queenPUP_y2 > 600 and  queenPUP_y > 600:
            queenPUP_x, queenPUP_y = queenPUP_x2, queenPUP_y2
    if healthPUP_y <= 600 :
        healthPUP_x, healthPUP_y, healthPUP_counter = handle_powerup_collision(healthPUP_x, healthPUP_y, healthPUP_counter)
        if healthPUP_y2 > 600 and  healthPUP_y > 600:
                healthPUP_x, healthPUP_y = healthPUP_x2, healthPUP_y2
    if rookPUP_y <= 600:
        rookPUP_x, rookPUP_y, rookPUP_counter = handle_powerup_collision(rookPUP_x, rookPUP_y, rookPUP_counter)
        if rookPUP_y2 > 600  and rookPUP_y > 600:
                rookPUP_x, rookPUP_y = rookPUP_x2, rookPUP_y2
    if laserPUP_y <= 600:
        laserPUP_x, laserPUP_y, laserPUP_counter = handle_powerup_collision(laserPUP_x, laserPUP_y, laserPUP_counter)
        if laserPUP_y2 > 600  and laserPUP_y > 600:
                laserPUP_x, laserPUP_y = laserPUP_x2, laserPUP_y2

#-------- DRAWING SECTION ---------
    #MAIN MENU(Maggie)
    #
    # Scene 1 (Menu screen) chessboard + title
    if menu_open == True:
        chessboardImg = pygame.image.load('chessboard.jpg')
        # smallchessboard = pygame.transform.scale(chessboardImg, (30,30))


        screen.blit(chessboardImg, (2,-20))
        scene_title = scene_title_font.render('Main Menu', True, (219, 33, 98))
        screen.blit(scene_title, (29, 13))
    
        pygame.draw.rect(screen, (242, 177, 202), (102,163,262,359))
        pygame.draw.rect(screen, (217, 87, 147), (461,163,262,359))

        instructions1 = instruction_title_font.render('Welcome to the game!', True, (125, 97, 7))
        instructions2 = instruction_title_font.render('Explore the dungeon,', True, (125, 97, 7))
        instructions3 = instruction_title_font.render('collect coins, powerups', True, (125, 97, 7))
        instructions4 = instruction_title_font.render('and fight opponents.', True, (125, 97, 7))
        screen.blit(instructions1,(128, 260))
        screen.blit(instructions2,(128, 290))
        screen.blit(instructions3,(128, 320))
        screen.blit(instructions4,(128, 350))

        #Start Button
        startImg = pygame.image.load('startbutton.png')
        smallstart = pygame.transform.scale(startImg, (102,60))
        screen.blit(smallstart, (startx, starty))
        #Exit Button
        ExitImg = pygame.image.load('exitbutton.png')
        smallexit = pygame.transform.scale(ExitImg, (97,60))
        screen.blit(smallexit, (exitx, exity))

        SettingImg = pygame.image.load('settingsbutton.png')
        smallsetting = pygame.transform.scale(SettingImg, (30,30))
        screen.blit(smallsetting, (settingx, settingy))

        #Title
        titleImg = pygame.image.load('dethroned_title.png')
        bigtitle = pygame.transform.scale(titleImg, (240,160))
        screen.blit(bigtitle, (titlex, titley))
    

        #check if button clicked
        if (click_x>=startx and click_x<=startx+100) and (click_y>=starty and click_y<=starty+50) and clicked == False:
            print("Start Button CLicked")
            menu_open = False
            current_screen = 2

        elif (click_x>=exitx and click_x<=exitx+100) and (click_y>=exity and click_y<=exity+50) and clicked == False:
            print("Exit Button Clicked")
            break

        elif (click_x >= settingx and click_x <= settingx +40) and (click_y>=settingy and click_y<=settingy+40) and clicked == False:
            print("Settings Button Clicked")
            current_screen = 1


    # Scene 2 (Instructions/setting screen) MARIA ADD UR STUFF HERE
    elif current_screen == 1:
       

        screen.fill((224, 202, 211)) 
        scene_title = scene_title_font.render('Instructions Screen', True, (242, 17, 109))
        screen.blit(scene_title, (90, 0))

    # Scene 3 (Game)
    elif current_screen == 2:

        background = pygame.image.load("Untitled drawing.png")
        white_player = pygame.image.load("white-chess-piece.png")
        player_width = 60
        player_height = 115
        white_player = pygame.transform.scale(white_player, (player_width, player_height))
        #queen power up image
        queenPUP = pygame.image.load("queen_powerup.png")
        queenPUP = pygame.transform.scale(queenPUP, (90, 90))
        queenPUP2 = pygame.transform.scale(queenPUP, (90, 90))
        #health power up image
        healthPUP = pygame.image.load("heartpup.png")
        healthPUP = pygame.transform.scale(healthPUP, (90, 90))
        healthPUP2 = pygame.transform.scale(healthPUP, (90, 90))

        #rook power up image
        rookPUP = pygame.image.load("rookpup.png")
        rookPUP = pygame.transform.scale(rookPUP, (90, 90))
        rookPUP2 = pygame.transform.scale(rookPUP, (90, 90))

        #laser power up image
        laserPUP = pygame.image.load("laserpup.png")
        laserPUP = pygame.transform.scale(laserPUP, (90, 90))
        laserPUP2 = pygame.transform.scale(laserPUP, (90, 90))
        coin_image = pygame.image.load('coin.png')
        coin_image = pygame.transform.scale(coin_image, (45, 50))

        Closed_chest_img = pygame.image.load("closed_chest.png")
        Closed_chest_img = pygame.transform.scale(Closed_chest_img, (115,115))
        full_chest_img = pygame.image.load("full_chest.png")
        full_chest_img = pygame.transform.scale(full_chest_img, (115,115))
        empty_chest_img = pygame.image.load("empty_chest.png")
        empty_chest_img = pygame.transform.scale(empty_chest_img, (115,115))
        
        chest_items = [laserPUP2, healthPUP2, rookPUP2, coin_image]
        #font 
        text_font = pygame.font.SysFont(None, 40, bold = True)
        text_font_smaller = pygame.font.SysFont(None, 20, bold = True)

         # background
        screen.fill((255, 255, 255))  # always the first drawing command

        # background image
        screen.blit(background, (0,0))

        # draw the pawn image
        screen.blit(white_player, (player_x, player_y))
    # dummy enemy
        for e in enemies:
            e_rect = pygame.Rect(e[0]-10, e[1]-10, 20, 20)
            pygame.draw.rect(screen, (255, 0, 0), e_rect)    

    
        # bullet tragectory
        pygame.draw.line(screen, (0, 0, 255), (player_x, player_y), (mouse_x, mouse_y), 1)

        # bullet
        for b in player_bullets:
            b_rect = pygame.Rect(b[0]-2, b[1]-2, 4, 4)
            pygame.draw.rect(screen, (0, 0, 0), b_rect) 


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
        
        screen.blit(healthPUP2, (healthPUP_x2, healthPUP_y2))
        screen.blit(queenPUP2, (queenPUP_x2, queenPUP_y2))
        screen.blit(laserPUP2, (laserPUP_x2, laserPUP_y2))
        screen.blit(rookPUP2, (rookPUP_x2, rookPUP_y2))


        #coding for numbering how many powerups you pick uo 
        #this is operating system for the chest to make the random things appear as well as the chest openings 
        for chest in closedchest_list:
            screen.blit(Closed_chest_img, (chest_x, chest_y))
        for chest in fullchest_list:
            screen.blit(full_chest_img, (chest_x, chest_y))
            if selected_item:
                screen.blit(selected_item, (chest_x+10, chest_y+25))  # Draw the selected item below the chest
            print_text("Press F to Collect", text_font_smaller, (0, 0, 0), chest_x + 10, chest_y)
        for chest in emptychest_list:
            screen.blit(empty_chest_img, (chest_x, chest_y))
        
    #coding for numbering how many powerups you pick up: COUNTER
        if queenPUP_counter >= 1:
                if queenPUP_y > 600:  
                    print_text(f"{queenPUP_counter}", text_font_smaller, (0,0,0), queenPUP_x + 55, queenPUP_y +10)
                elif queenPUP_y2 > 600:  
                    print_text(f"{queenPUP_counter}", text_font_smaller, (0,0,0), queenPUP_x2 + 55, queenPUP_y2 +10)
        if rookPUP_counter >= 1:
                if rookPUP_y > 600:
                    print_text(f"{rookPUP_counter}", text_font_smaller, (0,0,0), rookPUP_x + 55, rookPUP_y +10)
                elif rookPUP_y2 > 600:
                    print_text(f"{rookPUP_counter}", text_font_smaller, (0,0,0), rookPUP_x2 + 55, rookPUP_y2 +10)
        if healthPUP_counter >= 1: 
            if healthPUP_y >600:      
                print_text(f"{healthPUP_counter}", text_font_smaller, (0,0,0), healthPUP_x + 55, healthPUP_y +10)
            elif healthPUP_y2 > 600: 
                print_text(f"{healthPUP_counter}", text_font_smaller, (0,0,0), healthPUP_x2 + 55, healthPUP_y2 +10)
        if laserPUP_counter >= 1:
            if laserPUP_y >600:
                print_text(f"{laserPUP_counter}", text_font_smaller, (0,0,0), laserPUP_x +55, laserPUP_y + 10)
            elif laserPUP_y2 > 600: 
                print_text(f"{laserPUP_counter}", text_font_smaller, (0,0,0), laserPUP_x2 +55, laserPUP_y2 + 10)
        #Draw Pause button
        pausebutton = pygame.image.load("pausebutton.png")
        smallpausebutton = pygame.transform.scale(pausebutton, (40, 40))
        screen.blit(smallpausebutton,(743, 76))

        if (click_x>=pausex and click_x<=pausex+40) and (click_y>=pausey and click_y<=pausey+40) and pause_open == False:
            print("Pause Button CLicked")
            pause_open = True

        if store_open:
            pygame.draw.rect(screen, store_colour, ((WIDTH - store_width) / 2, (HEIGHT - store_height) / 2, store_width, store_height))
            pygame.draw.rect(screen, coin_colour, (300, 600, 200, 50))
            print_text(f"Coins: {c_collected}", text_font, (0, 0, 0), 335,610)
            print_text(f"STORE", text_font, (0, 0, 0), 350,125)
            #queen buy

            pygame.draw.rect(screen, (coin_colour), (og_purchase_x, og_purchase_y, purchase_slots_width, purchase_slots_height))
            screen.blit(queenPUP, (og_purchase_x + 30, og_purchase_y+ 80))
            print_text(f"Queen Power Up", text_font_smaller, (0, 0, 0), og_purchase_x+25, og_purchase_y)
            screen.blit(coin_image, (og_purchase_x + 15, og_purchase_y+ +200))
            print_text(f"{queenPUP_price}", text_font, (0, 0, 0), og_purchase_x+70, og_purchase_y+210)

            #laser pup buy
            pygame.draw.rect(screen, (coin_colour), (og_purchase_x+ 200, og_purchase_y, purchase_slots_width, purchase_slots_height))
            screen.blit(laserPUP, (og_purchase_x + 230, og_purchase_y+ 80))
            print_text(f"Laser Power Up", text_font_smaller, (0, 0, 0), og_purchase_x+230, og_purchase_y)
            screen.blit(coin_image, (og_purchase_x + 210, og_purchase_y+ +200))
            print_text(f"{laser_price}", text_font, (0, 0, 0), og_purchase_x+265, og_purchase_y+210)


            #rook pup buy
            pygame.draw.rect(screen, (coin_colour), (og_purchase_x+ 400, og_purchase_y, purchase_slots_width, purchase_slots_height))
            screen.blit(rookPUP, (og_purchase_x + 430, og_purchase_y+ 80))
            print_text(f"Rook Power Up", text_font_smaller, (0, 0, 0), og_purchase_x+425, og_purchase_y)
            screen.blit(coin_image, (og_purchase_x + 415, og_purchase_y+ +200))
            print_text(f"{rookPUP_price}", text_font, (0, 0, 0), og_purchase_x+470, og_purchase_y+210)
            
            #health pup buy
            pygame.draw.rect(screen, (coin_colour), (og_purchase_x+ 600, og_purchase_y, purchase_slots_width, purchase_slots_height))
            screen.blit(healthPUP, (og_purchase_x + 630, og_purchase_y+ 80))
            print_text(f"Health Power Up", text_font_smaller, (0, 0, 0), og_purchase_x+625, og_purchase_y)
            screen.blit(coin_image, (og_purchase_x + 615, og_purchase_y+ +200))
            print_text(f"{healthPUP_price}", text_font, (0, 0, 0), og_purchase_x+665, og_purchase_y+210)

         #pause menu in game
    #pause menu in game
    if pause_open == True:
        chessboardImg = pygame.image.load('chessboard.jpg')
        # smallchessboard = pygame.transform.scale(chessboardImg, (30,30))

        screen.blit(chessboardImg, (1,-20))
        scene_title = scene_title_font.render('Pause Menu', True, (219, 33, 98))
        screen.blit(scene_title, (29, 13))
    
        pygame.draw.rect(screen, (242, 177, 202), (102,163,262,359))
        pygame.draw.rect(screen, (217, 87, 147), (461,163,262,359))

        #backbutton
        backbutton = pygame.image.load('backbutton.png')
        smallbackbutton = pygame.transform.scale(backbutton, (90, 40))
        screen.blit(smallbackbutton,(650, 21))

        ExitImg = pygame.image.load('exitbutton.png')
        smallexit = pygame.transform.scale(ExitImg, (97,60))
        screen.blit(smallexit, (exitx, exity))

        if (click_x>=exitx and click_x<=exitx+100) and (click_y>=exity and click_y<=exity+50) and clicked == False:
            print("Exit Button Clicked")
            break
    
        #going make to game after clicking the back button in the pause menu
        if (click_x>=backx and click_x<=backx+80) and (click_y>=backy and click_y<=backy+30) and clicked == False:
            print("Back Button CLicked")
            pause_open = False
      





    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)
    #---------------------------


pygame.quit()
