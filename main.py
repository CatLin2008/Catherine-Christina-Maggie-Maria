# you can delete this file lol

# pygame template

import pygame, sys, math, random, json
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
white_player = pygame.image.load("pawn.png").convert_alpha()
player_hp = 100
player_center = [(player_width / 2), (player_height / 2)]

damage_cooldown = 0

bullet_img = pygame.image.load("bullet.png").convert_alpha()
player_bullets = []
bullet_speed = 15
bullet_life = 200

laser_on = False
click = False
laser_life = 60
laser_cd = 299

dash = 1
dash_on = False
dash_life = 30
dash_cd = 119

enemy_img = pygame.image.load("e_pawn.png")
enemies = []
enemies_rect = []
enemy_health = 50
enemy_speed = 1
b_x = 0
b_y = 0

e_rect = (0, 0)

# points system
points = 0
bullet_hit = 10
enemy_kill = 200

# waves
wave = 0
e_spawn_rate = 0
spawn_chest = False
clear = False
tutorial = True
wave_cd = 179

# Catherine sfx
collect_coin_sfx = pygame.mixer.Sound("pickupCoin 2.wav")
player_hit_sfx = pygame.mixer.Sound("hitHurt.wav")
clear_stage_sfx = pygame.mixer.Sound("dash.wav")
click_sfx = pygame.mixer.Sound("click.wav")
death_sfx = pygame.mixer.Sound("death.mp3")
error_sfx = pygame.mixer.Sound("error.wav")
laser_sfx = pygame.mixer.Sound("laser.mp3")
dash_sfx = pygame.mixer.Sound("dash.wav")


#font 
text_font = pygame.font.SysFont(None, 40, bold = True)
text_font_smaller = pygame.font.SysFont(None, 20, bold = True)

#queen power up image
queenPUP = pygame.image.load("queen_powerup.png")
queenPUP = pygame.transform.scale(queenPUP, (90, 90))
        #health power up image
healthPUP = pygame.image.load("heartpup.png")
healthPUP = pygame.transform.scale(healthPUP, (90, 90))

#rook power up image
rookPUP = pygame.image.load("rookpup.png")
rookPUP = pygame.transform.scale(rookPUP, (90, 90))

#laser power up image
laserPUP = pygame.image.load("laserpup.png")
laserPUP = pygame.transform.scale(laserPUP, (90, 90))
coin_image = pygame.image.load('coin.png')
coin_image = pygame.transform.scale(coin_image, (45, 50))
queenPUP_counter = 0
queenPUP_x = 1000
queenPUP_y = -1000

healthPUP_counter = 0
healthPUP_x = 1000
healthPUP_y = -1000

#laser powerup location
laserPUP_counter = 0

laserPUP_x = 1000
laserPUP_y = -1000

rookPUP_counter = 0
rookPUP_x = 1000
rookPUP_y = -1000

coins = [
    pygame.Rect(random.randrange(125,700), random.randrange(100,550), 23, 23),
    pygame.Rect(random.randrange(125,700), random.randrange(100,550), 23, 23),
    pygame.Rect(random.randrange(125,700), random.randrange(100,550), 23, 23),
    pygame.Rect(random.randrange(125,700), random.randrange(100,550), 23, 23)
]
c_collected = 0
#coin bar
coin_bar_height = 60
coin_bar_width = 200
coin_bar_color = (255, 215, 0)

# Chest parameters
chest_x, chest_y = (random.randrange(50,550)), random.randrange(125, 500)
closedchest_list = [pygame.Rect(chest_x, chest_y, 90, 90)]
fullchest_list = []
emptychest_list = []
chest_items = [laserPUP, healthPUP, rookPUP, coin_image]

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
rookPUP_price = 20 
healthPUP_price = 20

store_open = False
chest_open = False
draw_empty = False
f_key_pressed = False

#locations for the powerups within the store for later purchases used
laser_in_store = pygame.Rect(og_purchase_x, og_purchase_y, purchase_slots_width, purchase_slots_height)
rookPUP_in_store = pygame.Rect(400, og_purchase_y, purchase_slots_width, purchase_slots_height)
health_in_store = pygame.Rect(600, og_purchase_y, purchase_slots_width, purchase_slots_height)


#Maggie variables in main menu
pygame.font.get_default_font()
scene_title_font = pygame.font.SysFont('Courier New', 37)
instruction_title_font = pygame.font.SysFont('Courier New', 16)
dead_title_font = pygame.font.SysFont('Courier New', 20)
current_screen = 0

#buttons
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
menu_x = 208 
menu_y =348

#scene boolenans
clicked = False
pause_open = False
menu_open = True
dead_open = False

#power ups booleans
queen_powerup_activated = False
laser_powerup_activated = False
rook_powerup_activated = False
health_powerup_activated = False
chest_number = random.randrange(0,10)

# MARIIanitial variables
font_small = pygame.font.SysFont('Fira Sans Extra Condensed', 30)
font_medium = pygame.font.SysFont('Fira Sans Extra Condensed', 40)
font_large = pygame.font.SysFont('Fira Sans Extra Condensed', 50)
dark_brown = 139, 69, 19
tan = 210, 180, 140
black = 0, 0, 0

# Slider properties
slider_length = 400
slider_height = 5
slider_radius = 10

# Checkbox properties
checkbox_size = 30
checkbox_margin = 150  

# Load checkbox tick image
checkmark = pygame.transform.scale(pygame.image.load('tick.png'), (checkbox_size, checkbox_size))

# Load and scale slider images
minus_sign = pygame.transform.scale(pygame.image.load('minus_sign.png'), (80,80))
plus_sign = pygame.transform.scale(pygame.image.load('plus_sign.png'), (80,80))

# Load and scale the back button image
back_button = pygame.transform.scale(pygame.image.load('backbutton.png'), (200, 200))  # Adjust the size as needed
back_button_x = WIDTH - 200
back_button_y = HEIGHT - 200 + 10
back_button_width = 200
back_button_height = 200
back_button_rect = pygame.Rect(back_button_x, back_button_y, back_button_width, back_button_height)

# Load and scale keybind images
w_image = pygame.transform.scale(pygame.image.load('w_image.png'), (30, 30))
s_image = pygame.transform.scale(pygame.image.load('s_image.png'), (30, 30))
a_image = pygame.transform.scale(pygame.image.load('a_image.png'), (30, 30))
d_image = pygame.transform.scale(pygame.image.load('d_image.png'), (30, 30))


# Initial settings
settings = {
    "game_modes": ["easy", "medium", "hard"],
    "volume": {
        "sfx": 0,  
        "music": 0  
    },
    "keybinds": {
        "move up": "W",
        "move down": "S",
        "move left": "A",
        "move right": "D",
    }
}
def load_settings():
    with open('settings.json', 'r') as file:
        return json.load(file)
settings_screen = False
selected_option = None
game_modes = ["easy", "medium", "hard"]
settings = load_settings()

pygame.mixer.init()
pygame.mixer.music.load('background_music.mp3') 
pygame.mixer.music.set_volume(settings['volume']['music'] / 100)
pygame.mixer.music.play(-1)
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
# ---------------------------
#Maria Functions



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
                print(click_x, click_y)
                angle = calc_angle(player_x + player_center[0], player_y + player_center[1], mouse_x, mouse_y)
                dx, dy = calc_velocity(bullet_speed, angle)
                if laser_on == False:
                    player_bullets.append([player_x + player_center[0], player_y + player_center[1], dx, dy, bullet_life])

            #christina's code for the counters of parameters of the obejcts 
            if laserPUP_counter >= 1:
                if laser_parameters.collidepoint(event.pos):
                    laserPUP_counter -= 1
                    laser_powerup_activated = True
                    if laser_on == False:
                        player_bullets.append([player_x + player_center[0], player_y + player_center[1], dx, dy, bullet_life])
                    if laserPUP_counter < 1: 
                                laserPUP_x, laserPUP_y = -100, -100
                if healthPUP_counter >= 1:                
                    if health_parameters.collidepoint(event.pos):
                        healthPUP_counter -= 1
                        player_hp += 20
                        if healthPUP_counter < 1: 
                            healthPUP_x, healthPUP_y = -100, -100

            if rookPUP_counter >= 1:
                if rook_parameters.collidepoint(event.pos):
                    rookPUP_counter -= 1
                    rook_powerup_activated = True
                    if rookPUP_counter < 1: 
                                rookPUP_x, rookPUP_y = -100, -100

            #if the store_open is true, then the coins collected go down in price
            if store_open:
                if laser_in_store.collidepoint(event.pos):
                    if c_collected > laser_price:
                        c_collected -= laser_price
                        laserPUP_counter += 1
                        if slots:
                            new_slot = slots.pop(0)
                            laserPUP_x, laserPUP_y = new_slot

                if rookPUP_in_store.collidepoint(event.pos):
                    if c_collected > rookPUP_price:
                        c_collected -= rookPUP_price
                        rookPUP_counter += 1
                        if slots: 
                            new_slot = slots.pop(0)
                            rookPUP_x, rookPUP_y = new_slot
                if health_in_store.collidepoint(event.pos):
                    if c_collected > healthPUP_price:
                        c_collected -= healthPUP_price
                        healthPUP_counter += 1
                        if slots and healthPUP_y < 600: 
                            new_slot = slots.pop(0)
                            healthPUP_x, healthPUP_y = new_slot
    if settings_screen == True:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            slider_x = (WIDTH - slider_length) // 2

            # Check SFX volume control
            if 350 - slider_radius <= y <= 350 + slider_radius:
                if x <= slider_x:
                    settings['volume']['sfx'] = max(settings['volume']['sfx'] - 1, 0)
                elif x >= slider_x + slider_length:
                    settings['volume']['sfx'] = min(settings['volume']['sfx'] + 1, 100)
                save_settings(settings)
                coin_sound.set_volume(settings['volume']['sfx'] / 100)
                coin_sound.play()

            # Check Music volume control
            elif 450 - slider_radius <= y <= 450 + slider_radius:
                if x <= slider_x:
                    settings['volume']['music'] = max(settings['volume']['music'] - 1, 0)
                elif x >= slider_x + slider_length:
                    settings['volume']['music'] = min(settings['volume']['music'] + 1, 100)
                pygame.mixer.music.set_volume(settings['volume']['music'] / 100)
                save_settings(settings)

            # Check game mode selection
            game_mode_x = 250
            for mode in game_modes:
                if game_mode_x <= x <= game_mode_x + checkbox_size and 160 <= y <= 160 + checkbox_size:
                    settings['game_modes'] = mode
                    selected_option = f"game_modes_{mode}"
                    save_settings(settings)
                game_mode_x += checkbox_size + checkbox_margin
        if event.type == pygame.KEYDOWN:
            if selected_option and selected_option.startswith("game_mode"):
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    current_mode_index = game_modes.index(settings['game_mode'])
                    settings['game_mode'] = game_modes[(current_mode_index + 1) % len(game_modes)]
                    save_settings(settings)
        if (click_x >= back_button_x and click_x <= back_button_x + back_button_width) and (click_y >= back_button_y and click_y <= back_button_y + back_button_height) and not clicked:
                print("Back Button Clicked")
                menu_open = True
                settings_screen = False

        elif event.type == pygame.QUIT:
            running = False


    # GAME STATE UPDATES
    # All game math and comparisons happen here

    #parameters so theyre always updated
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    rook_parameters = pygame.Rect(rookPUP_x, rookPUP_y, 90, 90)
    laser_parameters = pygame.Rect(laserPUP_x, laserPUP_y, 90, 90)
    health_parameters = pygame.Rect(healthPUP_x, healthPUP_y, 90, 90)


    # WASD movement
    #!! taken from mrgallo site
    keys = pygame.key.get_pressed()
    if player_y > 0:
        if keys[119] == True:  # w
            player_y -= 10 * dash

    if player_x > 0:
        if keys[97] == True:  # a
            player_x -= 10 * dash

    if player_y < HEIGHT-player_height:
        if keys[115] == True:  # s
            player_y += 10 * dash

    if player_x < WIDTH-player_width:
        if keys[100] == True:  # d
            player_x += 10 * dash

    #   #adding a key press on E to open the store
    # if keys[101]:  
    #     if not e_key_pressed:
    #         store_open = not store_open
    #         e_key_pressed = True

    #     else:
    #       e_key_pressed = False

    # waves
    if clear == True and tutorial == False: 
        wave += 1
        print(f"wave {wave}, spawn {e_spawn_rate} enemies, spawn chest {spawn_chest}")
        e_spawn_rate += 1
        enemy_speed += 0.2
        spawn_chest = False
        draw_empty = False
        if wave > 1: 
            if chest_open == False:
                chest_rect = pygame.Rect(chest_x, chest_y, 90, 90)
                closedchest_list.append(chest_rect)
                spawn_chest = False 
            for _ in range(3):
                coins.append(pygame.Rect(random.randrange(100, 800), random.randrange(600), 23, 23)) 

    if wave % 2 == 0 or wave == 0:
        spawn_chest = True


    if spawn_chest:
        for chest in closedchest_list:
            if chest.colliderect(player_rect):
                closedchest_list.remove(chest)
                fullchest_list.append(pygame.Rect(chest_x, chest_y, 90, 90))
                selected_item = random.choice(chest_items)
                chest_open == True 
                if wave != 0: 
                    selected_item = random.choice(chest_items)
                elif wave == 0: 
                    selected_item = queenPUP
        # this is the problematic code that doesn't run for some reason 
        for chest in fullchest_list:
            if keys[102]:  
                if not f_key_pressed:
                    f_key_pressed = True
                if fullchest_list:
                    fullchest_list.remove(chest)
                    emptychest_list.append(pygame.Rect(chest_x, chest_y, 90, 90))
                    draw_empty = True 
                if selected_item == queenPUP:
                    queen_powerup_activated = True 
                    queenPUP_counter += 1 

                if selected_item == laserPUP:
                    laserPUP_counter += 1
                    if slots: 
                        new_slot = slots.pop(0)
                        laserPUP_x, laserPUP_y = new_slot
                elif selected_item == healthPUP:
                    healthPUP_counter += 1 
                    if slots: 
                        new_slot = slots.pop(0)
                        healthPUP_x, healthPUP_y = new_slot
                elif selected_item == rookPUP:
                    rookPUP_counter += 1
                    if slots:  
                        new_slot = slots.pop(0)
                        rookPUP_x, rookPUP_y = new_slot

                elif selected_item == coin_image:
                    c_collected +=  1
                    if slots:
                        slots.pop(0)  # Remove the slot if a coin is collected
                tutorial = False
            else:
                f_key_pressed = False
    if rook_powerup_activated:
            slots.insert(0, new_slot)

    if health_powerup_activated:
            slots.insert(0, new_slot)

    if laser_powerup_activated:
            slots.insert(0, new_slot)


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

    # LAZERS!!!!
    if laser_powerup_activated == True and laser_on == True:
        if keys[108] == True and laser_cd < 0: # l
            print("FUCK")
            laser_on = True
            laser_cd = 300
            if laser_cd < -1:
                laser_cd = -1
        elif keys[108] == True and laser_cd > 0:
            error_sfx.play()
        else:
            laser_cd -= 1
    
        laser = []

        laser_sfx.play()
        angle = calc_angle(player_x + player_center[0], player_y + player_center[1], mouse_x, mouse_y)
        dx, dy = calc_velocity(bullet_speed, angle)
        laser_x = player_x + player_center[0]
        laser_y = player_y + player_center[1]
        for _ in range(150):
            laser.append([laser_x, laser_y, dx, dy])
            laser_x += dx/2
            laser_y += dy/2
        laser_life -= 1
        if laser_life < 0:
            laser_on = False
            laser_life = 120
        if laser_life == 0: 
            laser_powerup_activated = False 

    if rook_powerup_activated: 
        if keys[101] and laser_cd < 0: # l possible bug? yeah
            dash_on = True
            dash_cd = 120
        elif keys[109] and dash_cd > 0: # l possible bug? yeah
            error_sfx.play()
        else:
            dash_cd -= 1

        if dash_on:
            dash_sfx.play()
            dash = 5
            dash_life -= 1
            if dash_life < 0:
                dash = 1
                dash_on = False
                dash_life = 30

        if dash_life == 0: 
            rook_powerup_activated = False 

    # Catherine Enemy system

    if clear == True and tutorial == False and wave % 6 != 0:  
        print("spawn")
        for _ in range(e_spawn_rate):
            spawn_pos = random.randrange(0, 4)
            if spawn_pos == 0:
                e_x = random.randrange(0, WIDTH)
                e_y = random.randrange(-100, 0)
            if spawn_pos == 1:
                e_x = random.randrange(WIDTH, WIDTH + 100)
                e_y = random.randrange(0, HEIGHT)
            if spawn_pos == 2:
                e_x = random.randrange(0, WIDTH)
                e_y = random.randrange(HEIGHT, HEIGHT + 100)
            if spawn_pos == 3:
                e_x = random.randrange(-100, 0)
                e_y = random.randrange(0, HEIGHT)

            enemy = [e_x, e_y, 0, 0, enemy_health] 
            enemies.append(enemy)


    enemies_alive = []
    e_rects = []

    for e in enemies:
        enemy_to_player_dist = calc_dist(player_x + player_center[0], player_y + player_center[1], e[0], e[1])
        enemy_angle = calc_angle(e[0] + 10, e[1]+10, player_x + player_center[0], player_y + player_center[1]) # +10 needs to change
        e[2], e[3] = calc_velocity(enemy_speed, enemy_angle)
        e_rect = pygame.Rect(e[0]-10, e[1]-10, 45, 75)
        e_rects.append(e_rect)

        if pause_open == False and menu_open == False:
            if enemy_to_player_dist != 0:
                if enemy_to_player_dist < 50:
                    e[0] += e[2]*3
                    e[1] += e[3]*3
                else:
                    e[0] += e[2]
                    e[1] += e[3]
                #add attack animation

        for b in player_bullets:
            b_rect = pygame.Rect(b[0]-2, b[1]-2, 4, 4)
            if b_rect.colliderect(e_rect):
                e[4] -= 10
                b[4] = -1
                points += bullet_hit
                player_hit_sfx.play()
        if laser_powerup_activated == True and laser_on == True:
            for l in laser:
                l_rect = pygame.Rect(l[0], l[1], 20, 20)
                if l_rect.colliderect(e_rect):
                    e[4] -= 5
                    points += 1

        if e[4] > 0:
            enemies_alive.append(e)
        elif e[4] == 0:
            for _ in range(3):
                e_coins = pygame.Rect(e[0], e[1], 23, 23)
                coins.append(e_coins) 

    enemies = enemies_alive

    if len(enemies) == 0 and wave_cd <= 0:
        clear = True
        wave_cd = 179
        clear_stage_sfx.play()
    else:
        clear = False
        if len(enemies) == 0 and tutorial == False:
            wave_cd -= 1

    # player 
    player_hitbox = white_player.get_rect()
    player_hitbox.topleft = (player_x, player_y)

    if damage_cooldown <= 0:
        if player_hitbox.collidelist(e_rects) >= 0 and (pause_open == False) and (menu_open == False):
            player_hp -= 10
            damage_cooldown = 20
            player_hit_sfx.play()
    elif damage_cooldown > 0:
        damage_cooldown -= 1

    if player_hp <= 0:
        print("dead")
        dead_open = True

    #coins being collected 
# note: code will be added to store the coin in inventory
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for c in coins: 
        #command found online
        if c.colliderect(player_rect):
            coins.remove(c)
            c_collected += 1
            collect_coin_sfx.play()
#-------- DRAWING SECTION ---------
    #MAIN MENU(Maggie)
    #
    # Scene 1 (Menu screen) chessboard + title
    if menu_open == True:
        score = 0
        enemy_health < 0
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
            current_screen =2
            menu_open = False
            wave = 0
            click_sfx.play()

        elif (click_x>=exitx and click_x<=exitx+100) and (click_y>=exity and click_y<=exity+50) and clicked == False:
            print("Exit Button Clicked")
            click_sfx.play()
            break

        elif (click_x >= settingx and click_x <= settingx +40) and (click_y>=settingy and click_y<=settingy+40) and clicked == False:
            print("Settings Button Clicked")
            settings_screen = True
            click_sfx.play()


    # Scene 2 (Instructions/setting screen) MARIA ADD UR STUFF HERE
    elif settings_screen == True:
        screen.fill(tan)
        menu_open = False

        with open("settings.json", "w") as file:
            json.dump(settings, file)


        def save_settings(settings):
            with open('settings.json', 'w') as file:
                json.dump(settings, file)

        def render_centered_text(text, font, color, screen, center_x, center_y):
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.center = (center_x, center_y)
            screen.blit(text_surface, text_rect)

        def render_text(text, x, y, color=dark_brown, font=font_small):
            text_surface = font.render(text, True, color)
            screen.blit(text_surface, (x, y))

        def draw_slider(x, y, value, color, left_img, right_img):
            pygame.draw.line(screen, color, (x, y), (x + slider_length, y), slider_height)
            dot_x = x + (value / 100) * slider_length
            pygame.draw.circle(screen, color, (int(dot_x), y), slider_radius)

            screen.blit(left_img, (x - left_img.get_width() - 45, y - left_img.get_height() // 2))
            screen.blit(right_img, (x + slider_length + 50, y - right_img.get_height() // 2))


        def display(screen, settings, selected_option):
            screen.fill(tan)
            render_centered_text("PREFERENCES", font_large, black, screen, WIDTH // 2, HEIGHT - 650)

            render_text("Game Mode", 20, 150, black, font_medium)
            game_mode_x = 250
            for mode in game_modes:
                mode_text_y = 130
                checkbox_y = 160
                render_text(mode.capitalize(), game_mode_x, mode_text_y, dark_brown)
                draw_checkbox(game_mode_x, checkbox_y, mode == settings['game_modes'])
                game_mode_x += checkbox_size + checkbox_margin

            render_text("Volume Settings", 20, 250, black, font_medium)

            # Draw sliders and plus/minus buttons
            draw_slider((WIDTH - slider_length) // 2, 350, settings['volume']['sfx'], black, minus_sign, plus_sign)
            draw_slider((WIDTH - slider_length) // 2, 450, settings['volume']['music'], black, minus_sign, plus_sign)

            # Draw slider labels
            render_centered_text("SFX", font_medium, dark_brown, screen, WIDTH // 2, 310)
            render_centered_text("Music", font_medium, dark_brown, screen, WIDTH // 2, 410)

            render_text("Keybinds", 20, 500, black, font_medium)
            y_offset = 550
            x_offset = 300
            move_up_width = font_medium.size("move up")[0]

            render_text("Move Up", 40, y_offset, dark_brown, font_small)
            screen.blit(w_image, (40 + move_up_width + 10, y_offset))

            render_text("Move Down", 40, y_offset + 40, dark_brown, font_small)
            screen.blit(s_image, (40 + move_up_width + 10, y_offset + 40))

            render_text("Move Left", 40 + x_offset, y_offset, dark_brown, font_small)
            screen.blit(a_image, (40 + x_offset + move_up_width + 10, y_offset))

            render_text("Move Right", 40 + x_offset, y_offset + 40, dark_brown, font_small)
            screen.blit(d_image, (40 + x_offset + move_up_width + 10, y_offset + 40))

            # Draw the back button at the bottom left corner
            screen.blit(back_button, (WIDTH - 200, HEIGHT - 200 + 10))

        def draw_checkbox(x, y, checked):
            pygame.draw.rect(screen, black, (x, y, checkbox_size, checkbox_size), 4)  # Thicker line
            if checked:
                screen.blit(checkmark, (x, y))

        settings = load_settings()
        selected_option = None
        game_modes = ["easy", "medium", "hard"]
        display(screen, settings, selected_option)


    # Scene 3 (Game)
    elif current_screen == 2:
        menu_open = False

        background = pygame.image.load("background.png")
        player_width = 45
        player_height = 75
        white_player = pygame.transform.scale(white_player, (player_width, player_height))
        bullet_img = pygame.transform.scale(bullet_img, (20, 20))
        enemy_img = pygame.transform.scale(enemy_img, (45, 75))

        queensprite = pygame.image.load("queen.png")
        queensprite = pygame.transform.scale(queensprite, (55, 110))
        Closed_chest_img = pygame.image.load("closed_chest.png")
        Closed_chest_img = pygame.transform.scale(Closed_chest_img, (115,115))
        full_chest_img = pygame.image.load("full_chest.png")
        full_chest_img = pygame.transform.scale(full_chest_img, (115,115))
        empty_chest_img = pygame.image.load("empty_chest.png")
        empty_chest_img = pygame.transform.scale(empty_chest_img, (115,115))

        chest_items = [ laserPUP, healthPUP, rookPUP, coin_image]
        #font 
        text_font = pygame.font.SysFont('Courier New', 40, bold = True)
        text_font_smaller = pygame.font.SysFont('Courier New', 20, bold = True)

         # background
        screen.fill((255, 255, 255))  # always the first drawing command

        # background image
        screen.blit(background, (0,0))

        # draw the pawn image
        if queen_powerup_activated == False:
            screen.blit(white_player, (player_x, player_y))
        elif queen_powerup_activated == True: 
            white_player == queensprite
            screen.blit(queensprite, (player_x, player_y))
            queenPUP_x, queenPUP_y = -100, -100

        if laser_powerup_activated == True and not laser_on: 
            print_text(f"Press L to Activate, Right Now", text_font_smaller, (0,0,250), 210, 500)
        if rook_powerup_activated == True and not dash_on:
            print_text(f"Press E to Activate, Right Now", text_font_smaller, (0,0,250), 210, 500)


        # enemy
        for e in enemies:
            e_rect = pygame.Rect(e[0]-10, e[1]-10, 20, 20)
            screen.blit(enemy_img, (e[0]-22.5, e[1]-37.5))    

        # laser!
        if laser_on == True:
            for l in laser:
                l_rect = pygame.Rect(l[0] - 10, l[1] - 10, 20, 20)
                pygame.draw.rect(screen, (255, 0, 0), l_rect)


        # bullet
        for b in player_bullets: 
            screen.blit(bullet_img, (b[0]-7, b[1]-7))

        # Points bar
        print_text(f"{points}", text_font, (0,0,0), 10, 10)

        # health bar
        pygame.draw.rect(screen, (255, 0, 0), (WIDTH/2-250, 595, (player_hp/100) * 500, 25))

        # waves
        if wave_cd == 180:
            print_text(f"WAVE {wave}", text_font, (0,0,0), WIDTH/2-100, 10)
        else: 
            countdown = wave_cd // 60
            print_text(f"NEXT WAVE IN {countdown+1}", text_font, (0,0,0), WIDTH/2-200, 10)


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
        print_text(f"$ {c_collected}", text_font, (0,0,0), 650, 10)

        # Draw coins
        for c in coins:
            screen.blit(coin_image, (c[0],c[1]))

        screen.blit(healthPUP, (healthPUP_x, healthPUP_y))
        screen.blit(laserPUP, (laserPUP_x, laserPUP_y))
        screen.blit(rookPUP, (rookPUP_x, rookPUP_y))

        #this is operating system for the chest to make the random things appear as well as the chest openings 
        if spawn_chest == True: 
            if chest_open == False:
                for chest in closedchest_list:
                    screen.blit(Closed_chest_img, (chest_x, chest_y))
                for chest in fullchest_list:
                    screen.blit(full_chest_img, (chest_x, chest_y))
                    if selected_item:
                        screen.blit(selected_item, (chest_x+10, chest_y+25))  # Draw the selected item below the chest
                        print_text("Press F to Collect", text_font_smaller, (0, 0, 0), chest_x + 10, chest_y)
                if draw_empty == True:
                    for chest in emptychest_list:
                        screen.blit(empty_chest_img, (chest_x, chest_y))

 #coding for numbering how many powerups you pick up: COUNTER
        if rookPUP_counter >= 1:
                if rookPUP_y > 600:
                    print_text(f"{rookPUP_counter}", text_font_smaller, (0,0,0), rookPUP_x + 55, rookPUP_y +10)
        if healthPUP_counter >= 1: 
            if healthPUP_y >600:      
                print_text(f"{healthPUP_counter}", text_font_smaller, (0,0,0), healthPUP_x + 55, healthPUP_y +10)
        if laserPUP_counter >= 1:
            if laserPUP_y >600:
                print_text(f"{laserPUP_counter}", text_font_smaller, (0,0,0), laserPUP_x +55, laserPUP_y + 10)

        #Draw Pause button
        pausebutton = pygame.image.load("pausebutton.png")
        smallpausebutton = pygame.transform.scale(pausebutton, (40, 40))
        screen.blit(smallpausebutton,(743, 76))

        if (click_x>=pausex and click_x<=pausex+40) and (click_y>=pausey and click_y<=pausey+40) and pause_open == False:
            print("Pause Button CLicked")
            pause_open = True

        if wave % 6 == 0 and wave != 0: 
            store_open = True
            if store_open:
                pygame.draw.rect(screen, store_colour, ((WIDTH - store_width) / 2, (HEIGHT - store_height) / 2, store_width, store_height))
                pygame.draw.rect(screen, coin_colour, (300, 600, 250, 50))
                print_text(f"Coins: {c_collected}", text_font, (0, 0, 0), 335,600)
                print_text(f"STORE", text_font, (0, 0, 0), 325,125)
                pygame.draw.rect(screen, (coin_colour), (og_purchase_x, og_purchase_y, purchase_slots_width, purchase_slots_height))
                screen.blit(laserPUP, (og_purchase_x+50, og_purchase_y+ 80))
                print_text(f"Laser Power Up", text_font_smaller, (0, 0, 0), og_purchase_x +10 , og_purchase_y)
                screen.blit(coin_image, (og_purchase_x+ 20, og_purchase_y+ +200))
                print_text(f"{laser_price}", text_font, (0, 0, 0), og_purchase_x+ 90, og_purchase_y+200)

                #rook pup buy
                pygame.draw.rect(screen, (coin_colour), (og_purchase_x+ 270, og_purchase_y, purchase_slots_width, purchase_slots_height))
                screen.blit(rookPUP, (og_purchase_x + 330, og_purchase_y+ 80))
                print_text(f"Rook Power Up", text_font_smaller, (0, 0, 0), og_purchase_x+ 300, og_purchase_y)
                screen.blit(coin_image, (og_purchase_x + 300, og_purchase_y+ +200))
                print_text(f"{rookPUP_price}", text_font, (0, 0, 0), og_purchase_x+350, og_purchase_y+200)

                #health pup buy
                pygame.draw.rect(screen, (coin_colour), (og_purchase_x+ 520, og_purchase_y, purchase_slots_width, purchase_slots_height))
                screen.blit(healthPUP, (og_purchase_x + 580, og_purchase_y+ 80))
                print_text(f"Health Power Up", text_font_smaller, (0, 0, 0), og_purchase_x+530, og_purchase_y)
                screen.blit(coin_image, (og_purchase_x + 550, og_purchase_y+ +200))
                print_text(f"{healthPUP_price}", text_font, (0, 0, 0), og_purchase_x+600, og_purchase_y+200)

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
            click_sfx.play()
            break

        #going make to game after clicking the back button in the pause menu
        if (click_x>=backx and click_x<=backx+80) and (click_y>=backy and click_y<=backy+30) and clicked == False:
            # print("Back Button CLicked")
            pause_open = False
            click_sfx.play()

    if dead_open == True:
        pygame.draw.rect(screen, (232, 183, 199), (100, 67,621,491))
        dead_title = dead_title_font.render('You are dead.Try again?', True, (222, 27, 113))
        screen.blit(dead_title, (115, 152))

        menubutton = pygame.image.load('menubutton.png')
        smallmenubutton = pygame.transform.scale(menubutton, (90, 40))
        screen.blit(smallmenubutton,(208, 348))
        if (click_x>=menu_x and click_x<=menu_x+70) and (click_y>=menu_y and click_y<=menu_y+30) and clicked == False:
            dead_open = False
            menu_open = True
            player_hp = 100
            click_sfx.play()

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)
    #---------------------------


pygame.quit()

# you can delete this file lol

