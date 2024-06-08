import json
import pygame

pygame.init()

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
    move_up_width = font_medium.size("move up")[0]  
    render_split_text("Move Up", 40, y_offset, dark_brown, font_medium)  
    render_split_text("Move Down", 40, y_offset + 40, dark_brown, font_medium)  
    render_split_text("Move Left A", 40 + move_up_width + 20, y_offset, dark_brown, font_medium)  
    render_split_text("Move Right D", 40 + move_up_width + 20, y_offset + 40, dark_brown, font_medium)
    
    # Draw the back button at the bottom left corner
    screen.blit(back_button_size, (600, HEIGHT - back_button_size.get_height() +10))

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
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_sfx = False
            dragging_music = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging_sfx:
                x, y = event.pos
                new_value = min(max((x - slider_x) / slider_length * 100, 0), 100)
                settings['volume']['sfx'] = int(new_value)
                save_settings(settings)
            elif dragging_music:
                x, y = event.pos
                new_value = min(max((x - slider_x) / slider_length * 100, 0), 100)
                settings['volume']['music'] = int(new_value)
                pygame.mixer.music.set_volume(settings['volume']['music'] / 100)
                save_settings(settings)
        elif event.type == pygame.KEYDOWN:
            if selected_option and selected_option.startswith("game_mode"):
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    current_mode_index = game_modes.index(settings['game_mode'])
                    settings['game_mode'] = game_modes[(current_mode_index + 1) % len(game_modes)]
                    save_settings(settings)

    screen.fill(tan)
    display(screen, settings, selected_option)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
