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
    
def translate_velocity(x, y, p_x, p_y, perp=False):
    h = math.sqrt((p_x-x)**2 + (p_y-y)**2)
    if perp:
        return (p_x-x)/h, (p_y-y)/h
    else:
        return ((p_y-y)**2)/(h**2), ((p_x-x)**2)/(h**2)
"""
    if h < min_dist:
        return ((p_y-y)**2)/(h**2), ((p_x-x)**2)/(h**2)
    else:
        return 1, 1
"""

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
        self.curr_planet = None
        self.pyplayer = pygame.Rect(self.x, self.y, self.size, self.size)

    def apply_physics(self, planets):
        self.x_acc = -self.x_vel*abs(self.x_vel)/1000
        self.y_acc = -self.y_vel*abs(self.y_vel)/1000

        if self.on_surface:
            planet_vec = get_grav(self.x, self.y, self.curr_planet.x, self.curr_planet.y, self.curr_planet.p)
            self.x_acc += planet_vec[0]
            self.y_acc += planet_vec[1]
        else:
            floor = get_grav(self.x, self.y, 0, 500, settings.gravity)
            top = get_grav(self.x, self.y, 0, 0, -settings.gravity)
            self.y_acc += floor[1] + top[1]
            for planet in planets:
                planet_vec = get_grav(self.x, self.y, planet.x, planet.y, planet.p)
                self.x_acc += planet_vec[0]
                self.y_acc += planet_vec[1]

        self.x_vel += self.x_acc
        self.y_vel += self.y_acc

    
    def update(self, screen, planets):
        keys = pygame.key.get_pressed()

        mouse = pygame.mouse.get_pressed()
        mouse_loc = pygame.mouse.get_pos()

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
        if keys[pygame.K_SPACE] and self.on_surface:
            vel = translate_velocity(player.x, player.y, self.curr_planet.x, self.curr_planet.y, True)
            vel = translate_velocity(player.x, player.y, self.curr_planet.x, self.curr_planet.y, True)
            self.x_vel = -(settings.jump_velocity*vel[0])/5
            self.y_vel = -(settings.jump_velocity*vel[1])/5
            self.on_surface = False
            self.curr_planet = None
        if keys[pygame.K_q]:
            self.show_vec = not self.show_vec

        if self.on_surface:
            print("vel adjust")
            vel = translate_velocity(player.x, player.y, self.curr_planet.x, self.curr_planet.y)
            vel = translate_velocity(player.x, player.y, self.curr_planet.x, self.curr_planet.y)
            self.x_vel *= vel[0]
            self.y_vel *= vel[1]


        self.x += self.x_vel
        self.y += self.y_vel
        if not self.on_surface:
            for planet in planets:
                self.on_surface = False
                h = math.sqrt((planet.x-self.x)**2 + (planet.y-self.y)**2)
                if h < planet.size:
                    self.x = planet.x + (planet.size*(self.x-planet.x))/h
                    self.y = planet.y + (planet.size*(self.y-planet.y))/h
                    self.on_surface = True
                    self.curr_planet = planet
                    break
        else:
            h = math.sqrt((self.curr_planet.x-self.x)**2 + (self.curr_planet.y-self.y)**2)
            if h != self.curr_planet.size:
                self.x = self.curr_planet.x + (self.curr_planet.size*(self.x-self.curr_planet.x))/h
                self.y = self.curr_planet.y + (self.curr_planet.size*(self.y-self.curr_planet.y))/h

        self.pyplayer.x = self.x
        self.pyplayer.y = self.y
        pygame.draw.rect(screen, settings.black, self.pyplayer)
        if self.show_vec:
            pygame.draw.line(screen, (0,0,255), (self.x, self.y), (self.x+(5*self.x_vel), self.y))
            pygame.draw.line(screen, (0,0,255), (self.x, self.y), (self.x, self.y+(5*self.y_vel)))
            pygame.draw.line(screen, (255,0,0), (self.x, self.y), (self.x+(20*self.x_acc), self.y))
            pygame.draw.line(screen, (255,0,0), (self.x, self.y), (self.x, self.y+(20*self.y_acc)))

    

# Initialize game settings
settings = GameSettings()

# Initialize screen
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))

# Main game loop
running = True
clock = pygame.time.Clock()

game_planets = [Planet(250, 250, 50, settings.gravity*2)]
game_planets.append(Planet(100, 250, 20, settings.gravity/2, True, game_planets[0], 0, 2))
game_planets.append(Planet(450, 400, 30, settings.gravity*2))

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
    
    #screen.blit(pygame.transform.rotate(screen, 90), (0,0))
    player.apply_physics(game_planets)
    player.update(screen, game_planets)
    pygame.display.flip()
    clock.tick(settings.tick_rate)

pygame.quit()
