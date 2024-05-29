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
    "game_mode": "normal",
    "volume": {
        "sfx": 50,
        "music": 50
    },
    "keybinds": {
        "move_up": "W",
        "move_down": "S",
        "move_left": "A",
        "move_right": "D",
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

def draw_text(text, x, y, color=dark_brown):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

def display(screen, settings):
    screen.fill(tan)
    draw_text("PREFERENCES", WIDTH / 3, HEIGHT / 8)
    draw_text(f"Game Mode: {settings['game_mode']}", 20, 20)
    draw_text("Volume Settings:", 20, 60)
    draw_text(f"  SFX: {settings['volume']['sfx']}", 40, 100)
    draw_text(f"  Music: {settings['volume']['music']}", 40, 140)
    draw_text("Keybinds:", 20, 180)
    y_offset = 220
    for action, key in settings['keybinds'].items():
        draw_text(f"  {action}: {key}", 40, y_offset)
        y_offset += 40

settings = load_settings()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(tan)
    display(screen, settings)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
