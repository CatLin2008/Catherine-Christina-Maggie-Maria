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
enemy_health = 100
dummy_x = WIDTH/2
dummy_y = HEIGHT/2
bullet_life = 200
death = False

# points system
points = 0
bullet_hit = 10
enemy_kill = 200

#queen powerup location
queenPUP_x = random.randrange(0, 750)
queenPUP_y = random.randrange(60, 500)
queenPUP_list = [
    pygame.Rect(queenPUP_x, queenPUP_y, 2, 5)
]
queenPUP_counter = 0

#health powerup location
healthPUP_x = random.randrange(0, 800)
healthPUP_y = random.randrange(60, 500)
healthPUP_list = [
    pygame.Rect(healthPUP_x, healthPUP_y, 2, 5)
]
healthPUP_counter = 0

#laser powerup location
laserPUP_x = random.randrange(0, 800)
laserPUP_y = random.randrange(60, 500)
laserPUP_list = [
    pygame.Rect(laserPUP_x, laserPUP_y, 2, 5)
]
laserPUP_counter = 0

#rook powerup location
rookPUP_x = random.randrange(0, 800)
rookPUP_y = random.randrange(60, 500)
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
    (110, 620),
    (190, 620), 
    (280, 620), 
    (360, 620), 
    (430, 620), 
    (500, 620),
    (570, 620)
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
# distance calculator
def calc_dist(x1, y1, x2, y2):
    a = y2 - y1
    b = x2 - x1
    return (a**2 + b**2)**0.5

#locations for the powerups within the store for later purchases used
queen_in_store = pygame.Rect(og_purchase_x, og_purchase_y, purchase_slots_width, purchase_slots_height)
laser_in_store = pygame.Rect(225, og_purchase_y, purchase_slots_width, purchase_slots_height)
rookPUP_in_store = pygame.Rect(425, og_purchase_y, purchase_slots_width, purchase_slots_height)
health_in_store = pygame.Rect(625, og_purchase_y, purchase_slots_width, purchase_slots_height)

#defining what a powerup should do when colliding the player
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
            angle = math.atan2(mouse_y - player_y, mouse_x - player_x) # chatgpt
            dx, dy = [bullet_speed * math.cos(angle), bullet_speed * math.sin(angle)] # chatgpt
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

     #adding a key press on E to open the store
    if keys[101]:  
        if not e_key_pressed:
            store_open = not store_open
            e_key_pressed = True
    else:
        e_key_pressed = False

    # Catherine's bullet & point system

    for b in player_bullets:
        b[0] += b[2]
        b[1] += b[3]
        b[4] -= 1
        
    player_bullets_alive = []
    for b in player_bullets:
        if b[4] >= 0:
            player_bullets_alive.append(b)
        bullet_to_enemy_dist = calc_dist(b[0], b[1], dummy_x, dummy_y)
        if bullet_to_enemy_dist <= 40:
            b[4] = -1
            enemy_health -= 10
            points += bullet_hit
    player_bullets = player_bullets_alive

    if enemy_health <= 0:
        death = True
        points += enemy_kill

    print(enemy_health)




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
    # DRAWING

    # background
    screen.fill((255, 255, 255))  # always the first drawing command

    # background image
    screen.blit(background, (0,0))

    # draw the pawn image
    screen.blit(white_player, (player_x, player_y))
    # dummy enemy
    if death == False:
        pygame.draw.circle(screen, (255, 0, 0), (dummy_x, dummy_y), 25)
    else:
        dummy_x = 0
        dummy_y = 0


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

    for slot in slots: 
        if (queenPUP_x, queenPUP_y) == slot:
            print_text(f"{queenPUP_counter}", text_font_smaller, (0,0,0), queenPUP_x + 55, queenPUP_y +8)
        if (rookPUP_x, rookPUP_y) == slot:
            print_text(f"{rookPUP_counter}", text_font_smaller, (0,0,0), rookPUP_x + 55, rookPUP_y +8)
        if(healthPUP_x, healthPUP_y) == slot:
            print_text(f"{healthPUP_counter}", text_font_smaller, (0,0,0), healthPUP_x + 55, healthPUP_y +8)
        if (laserPUP_x, laserPUP_y) == slot:
         print_text(f"{laserPUP_counter}", text_font_smaller, (0,0,0), laserPUP_x +55, laserPUP_y + 8)
    

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
