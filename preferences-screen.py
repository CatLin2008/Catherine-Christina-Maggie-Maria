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

def text(text, x, y, color=dark_brown):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

def display(screen, settings):
    screen.fill(tan)
    text("PREFERENCES", WIDTH / 3, HEIGHT / 8)
    text(f"Game Mode: {settings['game_mode']}", 20, 150)
    text("Volume Settings:", 20, 200)
    text(f"  SFX: {settings['volume']['sfx']}", 40, 250)
    text(f"  Music: {settings['volume']['music']}", 40, 300)
    text("Keybinds:", 20, 350)
    y_offset = 400
    for action, key in settings['keybinds'].items():
        text(f"  {action}: {key}", 40, y_offset)
        y_offset += 40

settings = load_settings()
selected_option = None
game_modes = ["easy", "medium", "hard"]

running = True
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
        elif event.type == pygame.KEYDOWN and selected_option is not None:
            if selected_option == "game_mode":
                current_mode_index = game_modes.index(settings['game_mode'])
                settings['game_mode'] = game_modes[(current_mode_index + 1) % len(game_modes)]
            elif selected_option == "volume_sfx":
                if event.key == pygame.K_UP and settings['volume']['sfx'] < 100:
                    settings['volume']['sfx'] += 10
                elif event.key == pygame.K_DOWN and settings['volume']['sfx'] > 0:
                    settings['volume']['sfx'] -= 10
            elif selected_option == "volume_music":
                if event.key == pygame.K_UP and settings['volume']['music'] < 100:
                    settings['volume']['music'] += 10
                elif event.key == pygame.K_DOWN and settings['volume']['music'] > 0:
                    settings['volume']['music'] -= 10
            selected_option = None
            save_settings(settings)

    screen.fill(tan)
    display(screen, settings)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
