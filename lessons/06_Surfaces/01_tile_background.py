"""
Example of loading a background image that is not as wide as the screen, and
tiling it to fill the screen.

"""
import random
import pygame

# Initialize Pygame
pygame.init()

from pathlib import Path
assets = Path(__file__).parent / 'images'

# Set up display
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tiled Background')

def make_tiled_bg(screen, bg_file):
    # Scale background to match the screen height
    
    bg_tile = pygame.image.load(bg_file).convert()
    
    background_height = screen.get_height()
    bg_tile = pygame.transform.scale(bg_tile, (bg_tile.get_width(), screen.get_height()))

    # Get the dimensions of the background after scaling
    background_width = bg_tile.get_width()

    # Make an image the is the same size as the screen
    image = pygame.Surface((screen.get_width(), screen.get_height()))

    # Tile the background image in the x-direction
    for x in range(0, screen.get_width(), background_width):
        image.blit(bg_tile, (x, 0))
        
    return image

def make_rainbow_bg(screen, tiles):

    # Make an image the is the same size as the screen
    image = pygame.Surface((screen.get_width(), screen.get_height()))

    tile = pygame.Surface((screen.get_width()/tiles, screen.get_height()))

    colors = [
    (255, 0, 0), (255, 69, 0), (255, 99, 71), (205, 92, 92), (220, 20, 60),
    (178, 34, 34), (139, 0, 0), (250, 128, 114), (233, 150, 122), (240, 128, 128),
    (188, 143, 143), (165, 42, 42), (255, 228, 225), (255, 182, 193), (255, 192, 203),
    (255, 105, 180), (255, 20, 147), (219, 112, 147), (199, 21, 133),

    (255, 165, 0), (255, 140, 0), (255, 127, 80), (255, 160, 122), (244, 164, 96),
    (255, 218, 185), (255, 228, 196), (255, 222, 173), (255, 228, 181), (245, 222, 179),
    (222, 184, 135), (210, 180, 140), (210, 105, 30), (205, 133, 63), (160, 82, 45),
    (139, 69, 19),

    (255, 255, 0), (255, 215, 0), (250, 250, 210), (255, 250, 205), (255, 255, 224),
    (240, 230, 140), (238, 232, 170), (189, 183, 107), (245, 245, 220), (255, 248, 220),
    (255, 235, 205), (250, 235, 215), (255, 239, 213), (253, 245, 230),

    (0, 128, 0), (0, 255, 0), (50, 205, 50), (0, 255, 127), (0, 250, 154),
    (124, 252, 0), (173, 255, 47), (127, 255, 0), (144, 238, 144), (152, 251, 152),
    (0, 100, 0), (34, 139, 34), (46, 139, 87), (60, 179, 113), (143, 188, 143),
    (128, 128, 0), (107, 142, 35), (154, 205, 50), (85, 107, 47), (240, 255, 240),
    (245, 255, 250),

    (0, 0, 255), (0, 0, 205), (0, 0, 139), (0, 0, 128), (65, 105, 225), (30, 144, 255),
    (0, 191, 255), (135, 206, 235), (135, 206, 250), (176, 224, 230), (173, 216, 230),
    (70, 130, 180), (95, 158, 160), (100, 149, 237), (123, 104, 238), (106, 90, 205),
    (72, 61, 139), (176, 196, 222),

    (75, 0, 130), (128, 0, 128), (148, 0, 211), (138, 43, 226), (153, 50, 204),
    (139, 0, 139), (186, 85, 211), (218, 112, 214), (238, 130, 238), (221, 160, 221),
    (216, 191, 216), (230, 230, 250), (147, 112, 219), (199, 21, 133), (255, 0, 255),
    (255, 0, 255),

    (255, 255, 255), (245, 245, 245), (255, 250, 250), (220, 220, 220), (211, 211, 211),
    (192, 192, 192), (169, 169, 169), (128, 128, 128), (105, 105, 105), (112, 128, 144),
    (47, 79, 79), (0, 0, 0), (240, 248, 255), (248, 248, 255), (240, 255, 255),
    (255, 240, 245), (255, 245, 238), (255, 250, 240), (255, 255, 240), (245, 255, 250),
    (250, 240, 230)
    ]



    # Tile the background image in the x-direction
    for x, color in zip(range(0, screen.get_width(), int(screen.get_width()/tiles)), [colors[random.randint(0,len(colors)-1)] for i in range(tiles)]):
        tile.fill(color)
        image.blit(tile, (x, 0))

        
    return image

background = make_rainbow_bg(screen, 6)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background,(0,0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
