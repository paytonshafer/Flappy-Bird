import pygame
import neat
import time
import os
import random
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROT = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2
        if d >= 16:
            d = 16
        if d < 0:
            d += 2
        
        self.y += d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROT:
                self.tilt = self.MAX_ROT
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

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
        
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rectangle = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotated_image, new_rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 250
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, True, True)
        self.PIPE_BOT = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_GAP(self,g):
        self.GAP = g

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOT, (self.x, self.bottom))

    def collide(self,bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bot_mask = pygame.mask.from_surface(self.PIPE_BOT)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bot_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bot_mask, bot_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        
        return False
        
class Base:
    VEl = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEl
        self.x2 -= self.VEl

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self,win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    base.draw(win)
    bird.draw(win)
    pygame.display.update()

def play_again(win,score):
    win.fill((0,0,0))
    scoretxt = STAT_FONT.render("Score:" + str(score), 1, (255,255,255) )
    text = STAT_FONT.render("Press any key to" , 1, (255,255,255))
    text2 = STAT_FONT.render("  play again,", 1, (255,255,255))
    text3 = STAT_FONT.render("click to quit!", 1, (255,255,255))
    win.blit(scoretxt,(0,0))
    win.blit(text,(0,50))
    win.blit(text2,(0,100))
    win.blit(text3,(0,150))
    pygame.display.update()

def diff(win):
    win.fill((0,0,0))
    easy = STAT_FONT.render("Press 1 for easy", 1, (255,255,255))
    med = STAT_FONT.render("Press 2 for medium", 1, (255,255,255))
    hard = STAT_FONT.render("Press 3 for hard", 1, (255,255,255))
    win.blit(easy,(0,0))
    win.blit(med,(0,50))
    win.blit(hard,(0,100))
    pygame.display.update()

def main():
    pygame.display.set_caption('Flappy Bird')
    bird = Bird(230,350)
    pipes = [Pipe(700)]
    base = Base(730)

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    diff(win)
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pipes[0].set_GAP(300)
                    start = False
                if event.key == pygame.K_2:
                    pipes[0].set_GAP(250)
                    start = False                
                if event.key == pygame.K_3:
                    pipes[0].set_GAP(200)
                    start = False

    qvar = False
    run = True 
    score = 0 
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                bird.jump()
            if event.type == pygame.QUIT:
                run = False
                qvar = False
        bird.move()
        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                qvar = True
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(700))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() <= 1:
            qvar = True 

        if bird.y + bird.img.get_height() >= 730:
            qvar = True

        base.move()
        draw_window(win, bird, pipes, base, score)

        if qvar:
            play_again(win, score)
        
            while qvar:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        qvar = False
                        run = True 
                        score = 0        
                        bird = Bird(230,350)
                        pipes = [Pipe(700)]
                        base = Base(730)
                        draw_window(win, bird, pipes, base, score)
                        pygame.display.update()      
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        qvar = False
                        run = False

    pygame.quit()
    quit()

if __name__=="__main__":
    main()