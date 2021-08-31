import pygame
import os
import random

WIN_WIDTH = 570
WIN_HEIGHT = 800
pygame.font.init()



STAT_FONT = pygame.font.SysFont("comicsans", 50)
HEADING_FONT = pygame.font.SysFont("comicsans", 70)
TEXT_FONT = pygame.font.SysFont("comicsans", 30)

path = "imgs/" #path = "c:\GoogleDrive\Scarlett\pygame\flappy_bird\imgs"
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join(path, "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join(path, "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join(path, "bird3.png")))]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join(path, "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join(path, "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join(path, "bg.png")))




class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y, weights=None):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        self.weights = weights
        self.score = 0
        self.alive = True

    def jump(self):
        self.vel = -10.5  # y is always negative
        self.tick_count = 0 # when was the last jump
        self.height = self.y # where was the jump starting point

    def move(self):
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2
        # t=0 : vel = -10.5
        # t=1 : vel = -9
        # t=2 : vel = -5.5

        if d >= 16:
            d = 16 # limits the downward speed to 16
        if d<0:
            d -= 2 # hmm...

        self.y += d # update bird position

        # set tilt of the bird
        if d < 0 or self.y < self. height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL


    def draw(self, win):
        self.img_count += 1

        # use different bird annimations that it looks like the wings are going up or down
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # nose dive animation
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 300
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()

        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            # collision
            return True
        else:
            return False

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def draw_main_menu(win, bird):
    win.blit(BG_IMG, (0,0)) # draw background on top left position
    bird.draw(win)
    text = HEADING_FONT.render("Flappy Bird", 1, (255, 255, 255))
    win.blit(text, (120, 100))

    text = TEXT_FONT.render("Start normal game - Press SPACE", 1, (255, 255, 255))
    win.blit(text, (30, 250))

    text = TEXT_FONT.render("Start training AI - Press T", 1, (255, 255, 255))
    win.blit(text, (30, 300))

    text = TEXT_FONT.render("Quit Flappy birds - Press Q", 1, (255, 255, 255))
    win.blit(text, (30, 350))

    pygame.display.update()


def draw_normal_game(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0,0)) # draw background on top left position
    bird.draw(win)
    base.draw(win)
    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 50))
    pygame.display.update()


def draw_ai_game(win, swarm, pipes, base):
    win.blit(BG_IMG, (0,0)) # draw background on top left position
    for bird in swarm.birds:
        if bird.alive:
            bird.draw(win)
    base.draw(win)
    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Epoch: " + str(swarm.epoch), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Score: " + str(swarm.current_score) + "/" + str(swarm.best_score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 50))

    text = STAT_FONT.render("Birds alive: " + str(swarm.alive), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 90))

    pygame.display.update()