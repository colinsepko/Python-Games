"""
Implementing Gravity

This program will demonstrate a simple implementation of gravity in a game, 
the the player constantly jumping. Notice that using gravity makes the player
jump more realistic. The player goes up quickly, but falls slowly. 

"""
import pygame
import math
from dataclasses import dataclass

# Initialize Pygame
pygame.init()


# This is a data class, one way of storing settings and constants for a game.
# We will create an instance of the data class, but since there is only one of
# them, we could also use the class directly, like GameSettings.screen_width.
# You can check that the instance has the same values as the class:
#    settings = GameSettings()
#    assert GameSettings.screen_width == settings.screen_width
@dataclass
class GameSettings:
    """Class for keeping track of game settings."""
    screen_width: int = 500
    screen_height: int = 500
    player_size: int = 10
    player_x: int = 100 # Initial x position of the player
    gravity: float = 0.3 # acelleration, the change in velocity per frame
    jump_velocity: int = 15
    white: tuple = (255, 255, 255)
    black: tuple = (0, 0, 0)
    tick_rate: int = 30 # Frames per second

# Initialize game settings
settings = GameSettings()

# Initialize screen
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))

# Define player
player = pygame.Rect(settings.player_x, 
                     settings.screen_height - settings.player_size, 
                     settings.player_size, settings.player_size)

player_y_velocity = 0
player_x_velocity = 0
player_x_acceleration = 0
player_y_acceleration = 0
is_jumping = False

def get_grav(x, y, p_x, p_y, p):
    p/=10
    if p_x != 0:
        h = math.sqrt((p_x-x)**2 + (p_y-y)**2)
        return (p*(p_x-x)) / h**2, (p*(p_y-y)) / h**2
    else:
        return 0, p / (((p_y-settings.player_size)-y + 1)**2)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:

    # Handle events, such as quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Continuously jump. If the player is not jumping, initialize a new jump
    keys = pygame.key.get_pressed()

    if is_jumping is False and keys[pygame.K_SPACE]:
        # Jumping means that the player is going up. The top of the 
        # screen is y=0, and the bottom is y=SCREEN_HEIGHT. So, to go up,
        # we need to have a negative y velocity
        player_y_velocity = -1
        is_jumping = True

    # Update player position. Gravity is always pulling the player down,
    # which is the positive y direction, so we add GRAVITY to the y velocity
    # to make the player go up more slowly. Eventually, the player will have
    # a positive y velocity, and gravity will pull the player down.
    floor = get_grav(player.x, player.y, 0, 500, settings.gravity)
    top = get_grav(player.x, player.y, 0, 0, settings.gravity)
    planet_1_vec = get_grav(player.x, player.y, 250, 250, settings.gravity)
    player_x_acceleration = planet_1_vec[0]
    player_y_acceleration = planet_1_vec[1]
    print("" + str(player_x_acceleration) + ", " + str(player_y_acceleration))
    player_x_velocity += player_x_acceleration
    #player_x_velocity = min(10, player_x_velocity)
    player_y_velocity += player_y_velocity
    #player_y_velocity = min(10, player_y_velocity)
    player.x += player_x_velocity
    player.y += player_y_velocity

    # If the player hits the ground, stop the player from falling.
    # The player's position is measured from the top left corner, so the
    # bottom of the player is player.y + PLAYER_SIZE. If the bottom of the
    # player is greater than the height of the screen, the player is on the
    # ground. So, set the player's y position to the bottom of the screen
    # and stop the player from falling
    if player.bottom >= settings.screen_height:
        player.bottom = settings.screen_height 
        player_y_velocity = 0
        is_jumping = False
    # elif player.top <= 0:
    #     player.top = 0
    #     player_y_velocity = 0
    #     is_jumping = False


    # Draw everything
    screen.fill(settings.white)
    pygame.draw.circle(screen, (255, 0, 0), (250, 250), 50)
    pygame.draw.rect(screen, settings.black, player)

    pygame.display.flip()
    clock.tick(settings.tick_rate)

pygame.quit()
