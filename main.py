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
e_key_pressed = False

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
current_screen = 0

startx = 180
starty = 190
exitx = 540
exity = 190
settingx = 750
settingy = 6
titlex = 300
titley = 6

click_x = 0
click_y = 0
clicked = False

#______________________________________________
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

def handle_powerup_collision(powerup_x, powerup_y, counter):
        if pygame.Rect(powerup_x, powerup_y, 80, 80).colliderect(player_rect):
            new_slot = slots[0]
            slots.pop(0)
            if new_slot:
                counter += 1
                powerup_x, powerup_y = new_slot

        return powerup_x, powerup_y, counter

#beta code still in development for the activation of powerups 
def check_powerup_click(mouse_x, mouse_y):
    global queenPUP_counter, rookPUP_counter, healthPUP_counter, laserPUP_counter
    for slot in slots:
        slot_rect = pygame.Rect(slot[0], slot[1], 65, 65)
        if slot_rect.collidepoint(mouse_x, mouse_y):
            if queenPUP_counter > 0 and slot_rect.collidepoint(queenPUP_x, queenPUP_y):
                queenPUP_counter -= 1
            elif rookPUP_counter > 0 and slot_rect.collidepoint(rookPUP_x, rookPUP_y):
                rookPUP_counter -= 1
            elif healthPUP_counter > 0 and slot_rect.collidepoint(healthPUP_x, healthPUP_y):
                healthPUP_counter -= 1
            elif laserPUP_counter > 0 and slot_rect.collidepoint(laserPUP_x, laserPUP_y):
                laserPUP_counter -= 1 
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
            check_powerup_click(mouse_x, mouse_y)
            if store_open: #code for purchasing the powerups in the store
                if queen_in_store.collidepoint(event.pos): 
                    if c_collected > queenPUP_price:
                        c_collected -=queenPUP_price
                        queenPUP_counter += 1
                        if slots:  #moving the new item to inventory if not already their and was purchased
                                new_slot = slots.pop(0)
                                queenPUP_x, queenPUP_y = new_slot
                if laser_in_store.collidepoint(event.pos): 
                    if c_collected > laser_price:
                        c_collected -= laser_price
                        laserPUP_counter += 1
                        if slots:  #moving the new laser to inventory if not already their and was purchased
                                new_slot = slots.pop(0)
                                laserPUP_x, laserPUP_y = new_slot
                if rookPUP_in_store.collidepoint(event.pos): 
                    if c_collected > rookPUP_price:
                        c_collected -= rookPUP_price
                        rookPUP_counter += 1
                        if slots:  #moving the new laser to inventory if not already their and was purchased
                                new_slot = slots.pop(0)
                                rookPUP_x, rookPUP_y = new_slot
                if health_in_store.collidepoint(event.pos): 
                    if c_collected > healthPUP_price:
                        c_collected -= healthPUP_price
                        healthPUP_counter += 1
                        if slots:  #moving the new laser to inventory if not already their and was purchased
                                new_slot = slots.pop(0)
                                healthPUP_x, healthPUP_y = new_slot


        elif event.type == pygame.QUIT:
            running = False

    # GAME STATE UPDATES
    # All game math and comparisons happen here
    # mouse_x, mouse_y = pygame.mouse.get_pos()

        
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

    if queenPUP_y <= 600:
        queenPUP_x, queenPUP_y, queenPUP_counter = handle_powerup_collision(queenPUP_x, queenPUP_y, queenPUP_counter)
    if healthPUP_y <= 600:
        healthPUP_x, healthPUP_y, healthPUP_counter = handle_powerup_collision(healthPUP_x, healthPUP_y, healthPUP_counter)
    if rookPUP_y <= 600:
        rookPUP_x, rookPUP_y, rookPUP_counter = handle_powerup_collision(rookPUP_x, rookPUP_y, rookPUP_counter)
    if laserPUP_y <= 600:
        laserPUP_x, laserPUP_y, laserPUP_counter = handle_powerup_collision(laserPUP_x, laserPUP_y, laserPUP_counter)


    queenPUP_x, queenPUP_y, queenPUP_counter = handle_powerup_collision(queenPUP_x, queenPUP_y, queenPUP_counter)
    healthPUP_x, healthPUP_y, healthPUP_counter = handle_powerup_collision(healthPUP_x, healthPUP_y, healthPUP_counter)
    rookPUP_x, rookPUP_y, rookPUP_counter = handle_powerup_collision(rookPUP_x, rookPUP_y, rookPUP_counter)
    laserPUP_x, laserPUP_y, laserPUP_counter = handle_powerup_collision(laserPUP_x, laserPUP_y, laserPUP_counter)
    # DRAWING
    #_________________________________

#MAIN MENU(Maggie)
    # chessboardImg = pygame.image.load('chessboard.jpg')
    # screen.blit(chessboardImg, (100,100))

    # Scene 1 (Menu screen) chessboard + title
    if current_screen == 0:

        chessboardImg = pygame.image.load('chessboard.jpg')
        # smallchessboard = pygame.transform.scale(chessboardImg, (30,30))

        screen.blit(chessboardImg, (2,-20))
        scene_title = scene_title_font.render('Main Menu', True, (219, 33, 98))
        screen.blit(scene_title, (29, 13))

        pygame.draw.rect(screen, (242, 177, 202), (102,163,262,359))
        pygame.draw.rect(screen, (217, 87, 147), (461,163,262,359))

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
            current_screen = 2

        elif (click_x>=exitx and click_x<=exitx+100) and (click_y>=exity and click_y<=exity+50) and clicked == False:
            print("Exit Button Clicked")


            break
        elif (click_x >= settingx and click_x <= settingx +40) and (click_y>=settingy and click_y<=settingy+40) and clicked == False:
            print("Settings Button Clicked")
            current_screen =1


    # Scene 2 (Instructions/setting screen) MARIA ADD UR STUFF HERE
    elif current_screen == 1:
        import json

        WIDTH = 800
        HEIGHT = 700
        SIZE = (WIDTH, HEIGHT)

        # Initialize global variables
        screen = pygame.display.set_mode(SIZE)
        clock = pygame.time.Clock()
        font_small = pygame.font.SysFont('Fira Sans Extra Condensed', 30)
        font_medium = pygame.font.SysFont('Fira Sans Extra Condensed', 40)
        font_large = pygame.font.SysFont('Fira Sans Extra Condensed', 50)
        dark_brown = 139, 69, 19
        tan = 210, 180, 140
        black = 0, 0, 0
        
        screen.fill(tan) 

        # Slider properties
        slider_length = 400
        slider_height = 5
        slider_radius = 10

        # Checkbox properties
        checkbox_size = 30
        checkbox_margin = 150  # Increased to ensure proper spacing

        # Load checkbox tick image
        checkbox_tick_img = pygame.image.load('tick.png')  # Replace with your tick image file
        checkbox_tick_img = pygame.transform.scale(checkbox_tick_img, (checkbox_size, checkbox_size))

        # Load and scale slider images
        minus_sign = pygame.image.load('minus_sign.png')
        plus_sign = pygame.image.load('plus_sign.png')
        minus_sign = pygame.transform.scale(minus_sign, (80, 80))
        plus_sign = pygame.transform.scale(plus_sign, (80, 80))

        # Load and scale the back button image
        back_button = pygame.image.load('backbutton.png')  # Replace with your back button image file
        back_button_size = pygame.transform.scale(back_button, (200, 200))  # Adjust the size as needed


        # Load and scale keybind images
        w_image = pygame.image.load('w_image.png')  # Replace with your w image file
        s_image = pygame.image.load('s_image.png')  # Replace with your s image file
        a_image = pygame.image.load('a_image.png')  # Replace with your a image file
        d_image = pygame.image.load('d_image.png')  # Replace with your d image file

        keybind_image_size = (30, 30)  # Set the size for keybind images
        w_image = pygame.transform.scale(w_image, keybind_image_size)
        s_image = pygame.transform.scale(s_image, keybind_image_size)
        a_image = pygame.transform.scale(a_image, keybind_image_size)
        d_image = pygame.transform.scale(d_image, keybind_image_size)

        # Initial settings
        settings = {
            "game_mode": "easy",
            "volume": {
                "sfx": 0,  # Start at 0
                "music": 0  # Start at 0
            },
            "keybinds": {
                "move up": "W",
                "move down": "S",
                "move left": "A",
                "move right": "D",
            }
        }

        # Save initial settings in a file
        with open("settings.json", "w") as file:
            json.dump(settings, file)

        # Load current settings
        def load_settings():
            with open('settings.json', 'r') as file:
                return json.load(file)

        # Save current settings
        def save_settings(settings):
            with open('settings.json', 'w') as file:
                json.dump(settings, file)

        def render_centered_text(text, font, color, screen, center_x, center_y):
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.center = (center_x, center_y)
            screen.blit(text_surface, text_rect)

        def render_split_text(text, x, y, highlight_part=dark_brown, color=dark_brown, font=font_small):
            parts = text.split(":")
            rendered_text_1 = font.render(parts[0], True, highlight_part)  
            screen.blit(rendered_text_1, (x, y))
            if len(parts) > 1:
                rendered_text_2 = font.render(parts[1], True, color)
                screen.blit(rendered_text_2, (x + rendered_text_1.get_width(), y))

        def display(screen, settings, selected_option):
            screen.fill(tan)
            render_split_text("PREFERENCES", WIDTH / 3, HEIGHT - 650, black, black, font_large)

            render_split_text("Game Mode", 20, 150, black, black, font_medium)  
            game_mode_x = 250 
            for mode in game_modes:
                mode_text_y = 130
                checkbox_y = 160
                render_split_text(mode.capitalize(), game_mode_x, mode_text_y, dark_brown)
                draw_checkbox(game_mode_x, checkbox_y, mode == settings['game_mode'])
                game_mode_x += checkbox_size + checkbox_margin

            render_split_text("Volume Settings", 20, 250, black, black, font_medium)  # Removed the colon

            # Draw sliders
            draw_slider((WIDTH - slider_length) // 2, 350, settings['volume']['sfx'], black, minus_sign, plus_sign)
            draw_slider((WIDTH - slider_length) // 2, 450, settings['volume']['music'], black, minus_sign, plus_sign)

            # Draw slider labels
            render_centered_text("SFX", font_medium, dark_brown, screen, WIDTH // 2, 310)
            render_centered_text("Music", font_medium, dark_brown, screen, WIDTH // 2, 410)

            render_split_text("Keybinds", 20, 500, black, black, font_medium)  
            y_offset = 550  
            x_offset = 300  # Increased horizontal distance between keybinds
            move_up_width = font_medium.size("move up")[0]
            
            render_split_text("Move Up", 40, y_offset, dark_brown, font_medium)
            screen.blit(w_image, (40 + move_up_width + 10, y_offset))  # Position the image next to the text
            
            render_split_text("Move Down", 40, y_offset + 40, dark_brown, font_medium)
            screen.blit(s_image, (40 + move_up_width + 10, y_offset + 40))  # Position the image next to the text
            
            render_split_text("Move Left", 40 + x_offset, y_offset, dark_brown, font_medium)
            screen.blit(a_image, (40 + x_offset + move_up_width + 10, y_offset))  # Position the image next to the text
            
            render_split_text("Move Right", 40 + x_offset, y_offset + 40, dark_brown, font_medium)
            screen.blit(d_image, (40 + x_offset + move_up_width + 10, y_offset + 40))  # Position the image next to the text
            
            # Draw the back button at the bottom left corner
            screen.blit(back_button_size, (600, HEIGHT - back_button_size.get_height() + 10))

        def draw_slider(x, y, value, color, left_img, right_img):
            pygame.draw.line(screen, color, (x, y), (x + slider_length, y), slider_height)
            dot_x = x + (value / 100) * slider_length
            pygame.draw.circle(screen, color, (int(dot_x), y), slider_radius)
            
            # Display images further from the sliders
            screen.blit(left_img, (x - left_img.get_width() - 45, y - left_img.get_height() // 2))  # Changed offset to 30
            screen.blit(right_img, (x + slider_length + 50, y - right_img.get_height() // 2))  # Changed offset to 30

        def draw_checkbox(x, y, checked):
            pygame.draw.rect(screen, black, (x, y, checkbox_size, checkbox_size), 4)  # Thicker line
            if checked:
                screen.blit(checkbox_tick_img, (x, y))

        settings = load_settings()
        selected_option = None
        game_modes = ["easy", "medium", "hard"]

        # Initialize mixer and load music
        pygame.mixer.init()
        pygame.mixer.music.load('background_music.mp3')  # Replace with your music file
        pygame.mixer.music.set_volume(settings['volume']['music'] / 100)
        pygame.mixer.music.play(-1)  # Play the music in a loop

        running = True
        dragging_sfx = False
        dragging_music = False
        
        back_button_rect = pygame.Rect(600, 00, 200, 200)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    game_mode_x = 250  # Moved to the right
                    for mode in game_modes:
                        if game_mode_x <= x <= game_mode_x + checkbox_size and 160 <= y <= 160 + checkbox_size:
                            settings['game_mode'] = mode
                            selected_option = f"game_mode_{mode}"
                            save_settings(settings)
                        game_mode_x += checkbox_size + checkbox_margin
                    slider_x = (WIDTH - slider_length) // 2
                    if 350 - slider_radius <= y <= 350 + slider_radius and slider_x <= x <= slider_x + slider_length:
                        dragging_sfx = True
                    elif 450 - slider_radius <= y <= 450 + slider_radius and slider_x <= x <= slider_x + slider_length:
                        dragging_music = True
                    mouse_x, mouse_y = event.pos
                    # Check if the back button is pressed
                    if back_button_rect.collidepoint(mouse_x, mouse_y):
                        current_screen = 0  
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging_sfx = False
                    dragging_music = False
                elif event.type == pygame.MOUSEMOTION:
                    if dragging_sfx or dragging_music:
                        slider_x = (WIDTH - slider_length) // 2
                        slider_value = int((event.pos[0] - slider_x) / slider_length * 100)
                        slider_value = max(0, min(100, slider_value))
                        if dragging_sfx:
                            settings['volume']['sfx'] = slider_value
                            save_settings(settings)
                        elif dragging_music:
                            settings['volume']['music'] = slider_value
                            pygame.mixer.music.set_volume(slider_value / 100)
                            save_settings(settings)
                


               
            display(screen, settings, selected_option)
            pygame.display.flip()
            clock.tick(60)
        display(screen, settings, selected_option)

    # Scene 3 (Game)
    elif current_screen == 2:

        background = pygame.image.load("Untitled drawing.png")
        white_player = pygame.image.load("white-chess-piece.png")
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

    #coding for numbering how many powerups you pick uo 
        for slot in slots: 
            if (queenPUP_x, queenPUP_y) == slot:
                print_text(f"{queenPUP_counter}", text_font_smaller, (0,0,0), queenPUP_x + 55, queenPUP_y +8)
            if (rookPUP_x, rookPUP_y) == slot:
                print_text(f"{rookPUP_counter}", text_font_smaller, (0,0,0), rookPUP_x + 55, rookPUP_y +8)
            if(healthPUP_x, healthPUP_y) == slot:
                print_text(f"{healthPUP_counter}", text_font_smaller, (0,0,0), healthPUP_x + 55, healthPUP_y +8)
            if (laserPUP_x, laserPUP_y) == slot:
                print_text(f"{laserPUP_counter}", text_font_smaller, (0,0,0), laserPUP_x +55, laserPUP_y + 8)


        # if queenPUP_x == 190 and queenPUP_y == 620:
        #     print_text(f"{queenPUP_counter}", text_font_smaller, (0,0,0), 250, 630)
        
        # if rookPUP_x == 285 and rookPUP_y == 640:
        #     print_text(f"{rookPUP_counter}", text_font_smaller, (0,0,0), 330, 630)
        
        # if healthPUP_x == 370 and healthPUP_y == 640:
        #     print_text(f"{healthPUP_counter}", text_font_smaller, (0,0,0), 410, 630)

        # if laserPUP_x == 435 and laserPUP_y == 625:
        #     print_text(f"{laserPUP_counter}", text_font_smaller, (0,0,0), 490, 630)
        
    #drawing the store and what they can purchase by pressing E
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

    # Must be the last two lines
    # of the game loop
    pygame.display.flip()
    clock.tick(60)
    #---------------------------


pygame.quit()
