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

def get_grav(x, y, p_x, p_y, p):
    p*=10
    if p_x != 0:
        h = math.sqrt((p_x-x)**2 + (p_y-y)**2)
        return 100*(p*(p_x-x)) / h**3, 100*(p*(p_y-y)) / h**3
    else:
        return 0, 50*p / ((p_y-y)**2)
    
def translate_velocity(x, y, p_x, p_y, min_dist):
    h = math.sqrt((p_x-x)**2 + (p_y-y)**2)
    if h < min_dist:
        return ((p_y-y)**2)/(h**2), ((p_x-x)**2)/(h**2)
    else:
        return 1, 1

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

class Planet:
    def __init__(self, x, y, size, p, moon=False, base_planet=None, start_xorbit=0, start_yorbit=0):
        self.x = x
        self.y = y
        self.size = size
        self.p = p
        self.moon = moon
        if moon:
            self.base_planet = base_planet
            self.x_vel = start_xorbit
            self.y_vel = start_yorbit

    def update(self, screen):
        color = (255, 0, 0)
        if self.moon:
            color = (0, 0, 255)
            temp = get_grav(self.x, self.y, self.base_planet.x, self.base_planet.y, self.base_planet.p)
            self.x_vel += temp[0]
            self.y_vel += temp[1]
            self.x += self.x_vel
            self.y += self.y_vel
        pygame.draw.circle(screen, color, (self.x, self.y), self.size)
        

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = settings.player_size
        self.x_vel = 0
        self.y_vel = 0
        self.x_acc = 0
        self.y_acc = 0
        self.show_vec = False
        self.on_surface = False
        self.pyplayer = pygame.Rect(self.x, self.y, self.size, self.size)

    def apply_physics(self, planets):
        self.x_acc = 0
        self.y_acc = 0
        floor = get_grav(self.x, self.y, 0, 500, settings.gravity)
        top = get_grav(self.x, self.y, 0, 0, -settings.gravity)
        self.y_acc += floor[1] + top[1]

        for planet in planets:
            planet_vec = get_grav(player.x, player.y, 250, 250, settings.gravity*2)
            self.x_acc += planet_vec[0]
            self.y_acc += planet_vec[1]

        print("" + str(self.x_acc) + ", " + str(self.y_acc))
        self.x_vel += self.x_acc
        self.y_vel += self.y_acc

        for planet in planets:
            vel = translate_velocity(player.x, player.y, planet.x, planet.y, planet.size)

            self.x_vel *= vel[0]
            self.y_vel *= vel[1]


    
    def update(self, screen, planets):
        keys = pygame.key.get_pressed()

        mouse = pygame.mouse.get_pressed()
        mouse_loc = pygame.mouse.get_pos()
        print(mouse_loc)

        if mouse[0]:
            self.x = mouse_loc[0]
            self.y = mouse_loc[1]

        if (self.y+self.size) >= settings.screen_height:
            self.y = settings.screen_height - self.size
            self.y_vel = 0
        elif self.y <= 10:
            self.y = 10
            self.y_vel = 0
        if (self.x+self.size) >= settings.screen_width:
            self.x = settings.screen_width - self.size
            self.x_vel = -self.x_vel
        elif self.x <= 0:
            self.x = 0 
            self.x_vel = -self.x_vel

        if keys[pygame.K_a]:
            self.x_vel = min(-3, self.x_vel)
        if keys[pygame.K_d]:
            self.x_vel = max(3, self.x_vel)
        if keys[pygame.K_w]:
            self.y_vel = min(-3, self.y_vel)
        if keys[pygame.K_s]:
            self.y_vel = max(3, self.y_vel)

        self.x += self.x_vel
        self.y += self.y_vel
        for planet in planets:
            h = math.sqrt((planet.x-self.x)**2 + (planet.y-self.y)**2)
            if h < planet.size:
                self.x = planet.x + (planet.size*(self.x-planet.x))/h
                self.y = planet.y + (planet.size*(self.y-planet.y))/h

        self.pyplayer.x = self.x
        self.pyplayer.y = self.y
        pygame.draw.rect(screen, settings.black, self.pyplayer)

    

# Initialize game settings
settings = GameSettings()

# Initialize screen
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))

# Main game loop
running = True
clock = pygame.time.Clock()

game_planets = [Planet(250, 250, 50, settings.gravity*2)]
game_planets.append(Planet(100, 250, 5, settings.gravity, True, game_planets[0], 0, 2))
game_planets.append(Planet(450, 400, 20, settings.gravity*5))

player = Player(settings.player_x, 100)

while running:

    # Handle events, such as quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Draw everything
    screen.fill(settings.white)

    for planet in game_planets:
        planet.update(screen)
    player.apply_physics(game_planets)
    player.update(screen, game_planets)

    pygame.display.flip()
    clock.tick(settings.tick_rate)

pygame.quit()
