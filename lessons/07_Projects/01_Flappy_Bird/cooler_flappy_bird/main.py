import pygame, numpy, random, time
from pygame.locals import *

from pathlib import Path
images_folder = Path(__file__).parent / 'images'

class GameSetting:
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 600
    BACKGROUND_COLOR = (0,0,0)
    SPEED = 20
    GRAVITY = 2.5

    GROUND_WIDTH = 2 * SCREEN_HEIGHT
    GROUND_HEIGHT= 100

    PIPE_WIDTH = 80
    PIPE_HEIGHT = 500

    FRAME_RATE = 24

    IMAGES = {str(k)[1+len(str(images_folder)):str(k).find('.')]: pygame.image.load(k) if str(k)[-3:] == 'png' else None for k in images_folder.iterdir()}
    IMAGES['background'] = pygame.transform.scale(IMAGES['background'], (SCREEN_WIDTH, SCREEN_HEIGHT))

    BASE_Y = SCREEN_HEIGHT - IMAGES['base'].get_height()

    IMAGES['base'] = pygame.transform.scale(IMAGES['base'], (SCREEN_WIDTH, IMAGES['base'].get_height()))

    EASY, MEDIUM, HARD, DIE = 0,1,2,3
    BACKGROUNDS = ['background-tile', 'background-sunset', 'background-night', 'background-abandoned']
    
    TILE_WIDTH = IMAGES['background-tile'].get_width()
    for background in BACKGROUNDS:
        IMAGES[background] = pygame.transform.scale(IMAGES[background], (TILE_WIDTH, SCREEN_HEIGHT))

    TILE_LOCS = numpy.arange(0,SCREEN_WIDTH + TILE_WIDTH, TILE_WIDTH)
    TILE_RESET = TILE_LOCS[-1]

    NUM_TILES = len(TILE_LOCS)

    def __init__(self):
        self.difficulty = self.EASY
        self.background = self.BACKGROUNDS[self.difficulty]
        self.game_speed = 4
        self.pipe_gap = 150
        self.pipe_speed = 0

    def change_diff(self, higher_or_lower):
        if higher_or_lower:
            self.difficulty = min(self.difficulty+1, self.DIE)
        else:
            self.difficulty = max(self.difficulty-1, self.EASY)
        self.background = self.BACKGROUNDS[self.difficulty]

        match self.difficulty:
            case self.EASY:
                self.game_speed = 4
                self.pipe_gap = 150
                self.pipe_speed = 0
            case self.MEDIUM:
                self.game_speed = 6
                self.pipe_gap = 150
                self.pipe_speed = 0
            case self.HARD:
                self.game_speed = 10
                self.pipe_gap = 140
                self.pipe_speed = 1
            case self.DIE:
                self.game_speed = 20
                self.pipe_gap = 120
                self.pipe_speed = 2

class Bird(pygame.sprite.Sprite):
    def __init__(self, game_settings: GameSetting):
        super().__init__()
        self.settings = game_settings
        self.images = [self.settings.IMAGES[bird].convert_alpha() for bird in sorted([file_name for file_name in self.settings.IMAGES if file_name.find("bird") != -1])]

        for bird in sorted([file_name for file_name in self.settings.IMAGES if file_name.find("bird") != -1]):
            print(bird)
        
        self.speed = self.settings.SPEED

        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = self.settings.SCREEN_WIDTH/6, self.settings.SCREEN_HEIGHT/2
    
    def update(self):
        super().update()
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image + (self.settings.difficulty*3)]
        self.mask = pygame.mask.from_surface(self.image)
        self.speed += self.settings.GRAVITY
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -self.settings.SPEED

    def idle(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image + (self.settings.difficulty*3)]


class Pipe(pygame.sprite.Sprite):
    def __init__(self, game_settings: GameSetting, inverted, xpos, ysize, direction):
        super().__init__()

        self.settings = game_settings

        self.images = [pygame.transform.scale(self.settings.IMAGES[pipe].convert_alpha(), (self.settings.PIPE_WIDTH, self.settings.PIPE_HEIGHT)) for pipe in sorted([file_name for file_name in self.settings.IMAGES if file_name.find("pipe") != -1])]
        temp = self.images[1]
        self.images[1] = self.images[0]
        self.images[0] = temp
        self.image = self.images[0]
        self.direction = direction

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.images = [pygame.transform.flip(image, False, True) for image in self.images]
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = self.settings.SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= self.settings.game_speed
        if self.rect[0] < self.settings.SCREEN_WIDTH and self.settings.difficulty >= self.settings.HARD:
            self.rect[1] += (self.direction*self.settings.pipe_speed)
        self.image = self.images[self.settings.difficulty]


class PipePair():
    def __init__(self, game_settings: GameSetting, xpos, size):
        self.settings = game_settings
        direction = (random.randint(0,1)*2)-1
        if size > 250:
            direction = 1
        elif size < 150:
            direction = -1
        self.pipe = Pipe(self.settings, False, xpos, size, direction)
        self.pipe_inverted = Pipe(self.settings, True, xpos, self.settings.SCREEN_HEIGHT - size - self.settings.pipe_gap, direction)

    def get_pipes(self, inverted):
        if inverted:
            return self.pipe_inverted
        else:
            return self.pipe

class Ground(pygame.sprite.Sprite):
    def __init__(self, game_settings: GameSetting, xpos):
        super().__init__()
        self.settings = game_settings
        self.image = self.settings.IMAGES['base'].convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = self.settings.BASE_Y

    def update(self):
        self.rect[0] -= self.settings.game_speed
        if self.rect[0] < -self.rect[2]:
            self.rect[0] += 2*self.rect[2]
        
class Game:
    def __init__(self, game_settings: GameSetting):
        pygame.init()
        self.settings = game_settings
        self.screen = pygame.display.set_mode((game_settings.SCREEN_WIDTH, game_settings.SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.settings.IMAGES['message'] = self.settings.IMAGES['message'].convert_alpha()
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        tile_locs = self.settings.TILE_LOCS.copy()
    
        player = Bird(self.settings)
        player_group = pygame.sprite.GroupSingle(player)

        ground_group = pygame.sprite.Group()
        for loc in [0, self.settings.SCREEN_WIDTH]:
            ground = Ground(self.settings, loc)
            ground_group.add(ground)

        pipe_group = pygame.sprite.Group()

        begin = True
        self.running = True
        while begin:

            self.clock.tick(self.settings.FRAME_RATE)

            self.screen.fill(self.settings.BACKGROUND_COLOR)

            for event in pygame.event.get():
                if event.type == QUIT:
                    begin = False
                    self.running = False
                    print("Quitting from menu")
                if event.type == KEYDOWN:
                    if event.key == K_SPACE or event.key == K_UP:
                        player.bump()
                        begin = False
                    if event.key == K_RIGHT:
                        self.settings.change_diff(True)
                    if event.key == K_LEFT:
                        self.settings.change_diff(False)

            if not self.running and not begin:
                print("Breaking menu loop")
                pygame.quit()
                break

            for i, loc in enumerate(tile_locs):
                self.screen.blit(self.settings.IMAGES[self.settings.background], (tile_locs[i], 0))
            self.screen.blit(self.settings.IMAGES['message'], (120, 150))


            player.idle()
            ground_group.update()

            player_group.draw(self.screen)
            ground_group.draw(self.screen)

            pygame.display.flip()
            pygame.display.update()

        if self.running:
            for i in range (2):
                pipes = PipePair(self.settings, self.settings.SCREEN_WIDTH * i + 800, random.randint(100, 300))
                pipe_group.add(pipes.get_pipes(False))
                pipe_group.add(pipes.get_pipes(True))

        while self.running:
            self.clock.tick(self.settings.FRAME_RATE)

            self.screen.fill(self.settings.BACKGROUND_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    print("Quitting mid game")
                if event.type == KEYDOWN:
                    if event.key == K_SPACE or event.key == K_UP:
                        player.bump()

            if not self.running:
                print("Breaking game loop")
                pygame.quit()
                break

            tile_locs -= (1 + self.settings.difficulty)

            for i, loc in enumerate(tile_locs):
                if loc < -self.settings.TILE_WIDTH:
                    tile_locs[i] += self.settings.TILE_RESET + self.settings.TILE_WIDTH
                self.screen.blit(self.settings.IMAGES[self.settings.background], (tile_locs[i], 0))

            if pipe_group.sprites()[0].rect[0] < -pipe_group.sprites()[0].rect[2]:
                pipe_group.remove(pipe_group.sprites()[0])
                pipe_group.remove(pipe_group.sprites()[0])

                pipes = PipePair(self.settings, self.settings.SCREEN_WIDTH * 2, random.randint(100, 300))
                pipe_group.add(pipes.get_pipes(False))
                pipe_group.add(pipes.get_pipes(True))


            player_group.update()
            pipe_group.update()
            ground_group.update()

            player_group.draw(self.screen)
            pipe_group.draw(self.screen)
            ground_group.draw(self.screen)

            # flip() the display to put your work on screen
            pygame.display.flip()
            pygame.display.update()

            if (pygame.sprite.groupcollide(player_group, ground_group, False, False, pygame.sprite.collide_mask) or
                pygame.sprite.groupcollide(player_group, pipe_group, False, False, pygame.sprite.collide_mask)):
                time.sleep(1)
                self.running = False

if __name__ == "__main__":
    game = Game(GameSetting())
    while pygame.get_init():
        game.run()
    pygame.quit()