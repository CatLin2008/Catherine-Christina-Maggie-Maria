import json
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 650
SIZE = (WIDTH, HEIGHT)

# Initialize global variables
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
font = pygame.font.SysFont('Fira Sans Extra Condensed', 50)
dark_brown = 139, 69, 19
tan = 210, 180, 140
black = 0, 0, 0

# Initial settings
settings = {
    "game_mode": "easy",
    "volume": {
        "sfx": 50,
        "music": 50
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

def render_split_text(text, x, y, highlight_part, color=dark_brown):
    parts = text.split(":")
    rendered_text_1 = font.render(parts[0] + ":", True, highlight_part)
    screen.blit(rendered_text_1, (x, y))
    if len(parts) > 1:
        rendered_text_2 = font.render(parts[1], True, color)
        screen.blit(rendered_text_2, (x + rendered_text_1.get_width(), y))

def display(screen, settings, selected_option):
    screen.fill(tan)
    render_split_text("PREFERENCES", WIDTH / 3, HEIGHT / 8, dark_brown)
    
    game_mode_color = black if selected_option == "game_mode" else dark_brown
    render_split_text(f"Game Mode: {settings['game_mode']}", 20, 150, game_mode_color)
    
    volume_sfx_color = black if selected_option == "volume_sfx" else dark_brown
    volume_music_color = black if selected_option == "volume_music" else dark_brown
    render_split_text("Volume Settings:", 20, 200, dark_brown)
    render_split_text(f"SFX: {settings['volume']['sfx']}", 40, 250, volume_sfx_color)
    render_split_text(f"Music: {settings['volume']['music']}", 40, 300, volume_music_color)
    
    render_split_text("Keybinds:", 20, 350, dark_brown)
    y_offset = 400
    for action, key in settings['keybinds'].items():
        render_split_text(f"{action}: {key}", 40, y_offset, dark_brown)
        y_offset += 40

settings = load_settings()
selected_option = None
game_modes = ["easy", "medium", "hard"]

# Initialize mixer and load music
pygame.mixer.init()
pygame.mixer.music.load('background_music.mp3')  
pygame.mixer.music.set_volume(settings['volume']['music'] / 100)
pygame.mixer.music.play(-1)  

# Load the SFX sound
sfx_sound = pygame.mixer.Sound('coinsound.mp3')  

running = True
volume_change_direction = None  
volume_change_speed = 10  
hold_counter = 0  
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 20 < x < 200:
                if 150 < y < 200:
                    selected_option = "game_mode"
                elif 250 < y < 300:
                    selected_option = "volume_sfx"
                elif 300 < y < 350:
                    selected_option = "volume_music"
        elif event.type == pygame.KEYDOWN:
            if selected_option == "game_mode":
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    current_mode_index = game_modes.index(settings['game_mode'])
                    settings['game_mode'] = game_modes[(current_mode_index + 1) % len(game_modes)]
            elif selected_option == "volume_sfx":
                if event.key == pygame.K_UP:
                    volume_change_direction = 'up'
                elif event.key == pygame.K_DOWN:
                    volume_change_direction = 'down'
            elif selected_option == "volume_music":
                if event.key == pygame.K_UP:
                    volume_change_direction = 'up'
                elif event.key == pygame.K_DOWN:
                    volume_change_direction = 'down'
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                volume_change_direction = None

    # Handle continuous volume change
    if volume_change_direction:
        hold_counter += 1
        if hold_counter % 8 == 0:  
            if volume_change_direction == 'up':
                if selected_option == "volume_sfx" and settings['volume']['sfx'] < 100:
                    settings['volume']['sfx'] += volume_change_speed
                    sfx_sound.set_volume(settings['volume']['sfx'] / 100)
                    sfx_sound.play()  
                elif selected_option == "volume_music" and settings['volume']['music'] < 100:
                    settings['volume']['music'] += volume_change_speed
                    pygame.mixer.music.set_volume(settings['volume']['music'] / 100)
            elif volume_change_direction == 'down':
                if selected_option == "volume_sfx" and settings['volume']['sfx'] > 0:
                    settings['volume']['sfx'] -= volume_change_speed
                    sfx_sound.set_volume(settings['volume']['sfx'] / 100)
                    sfx_sound.play()  
                elif selected_option == "volume_music" and settings['volume']['music'] > 0:
                    settings['volume']['music'] -= volume_change_speed
                    pygame.mixer.music.set_volume(settings['volume']['music'] / 100)
            save_settings(settings)

    screen.fill(tan)
    display(screen, settings, selected_option)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
