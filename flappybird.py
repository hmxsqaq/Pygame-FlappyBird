import os
import sys
import random
import pygame

# static
WIDTH = 288
HEIGHT = 512
FPS = 30

# material
IMG = {}
for img in os.listdir('./img'):
    name, extension = os.path.splitext(img)
    path = os.path.join('./img', img)
    IMG[name] = pygame.image.load(path)
LAND_Y = HEIGHT - IMG['land'].get_height()

# initialize
pygame.init()
pygame.display.set_caption('Flappy Bird(Python ver) -- By 徽墨行深')
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.frames = [0]*5 + [1]*5 + [2]*5 + [1]*5
        self.idx = 0

        self.images = IMG['protagonist']
        self.image = IMG['protagonist'][self.frames[self.idx]]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.range = [y-6, y+6]
        self.idle_speed = -1

        self.gravity = 1
        self.y_velocity = -11
        self.y_maxvelocity = 15

        self.rotate_velocity = -3
        self.maxrotate = -90
        self.rotate = 45

    def fly(self):
        self.idx += 1
        self.idx %= len(self.frames)
        self.image = self.images[self.frames[self.idx]]

    def idle(self):
        self.fly()
        self.rect.y += self.idle_speed
        if self.rect.y <= self.range[0] or self.rect.y >= self.range[1]:
            self.idle_speed *= -1

    def interact(self, flag=False):
        self.fly()
        if flag:
            self.rotate = 45
            self.y_velocity = -11
        self.y_velocity = min(self.y_velocity+self.gravity, self.y_maxvelocity)
        self.rect.y += self.y_velocity
        self.rotate = max(self.rotate+self.rotate_velocity, self.maxrotate)
        self.image = pygame.transform.rotate(self.image, self.rotate)

    def die(self):
        if self.rect.centery <= LAND_Y-4:
            self.rect.y += self.y_maxvelocity
            self.rotate = self.maxrotate
            self.image = self.images[self.frames[self.idx]]
            self.image = pygame.transform.rotate(self.image, self.rotate)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, reverse=False):
        pygame.sprite.Sprite.__init__(self)
        self.images = IMG['pipe']
        if reverse:
            self.image = self.images[1]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = y
        else:
            self.image = self.images[0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.top = y
        self.velocity = -4

    def update(self):
        self.rect.x += self.velocity

    def iscrashed(self, pos):
        if self.rect.collidepoint(pos):
            return True
        else:
            return False


class Button:
    def __init__(self, name, x, y):
        self.image = IMG[name]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def ispressed(self, pos):
        if self.rect.collidepoint(pos):
            return True
        else:
            return False
# main


def random_method():
    IMG['background'] = IMG[random.choice(['bg_day', 'bg_night'])]
    protagonist_type = random.choice(['0', '1', '2'])
    IMG['protagonist'] = [IMG['bird'+protagonist_type+'_0'],
                          IMG['bird'+protagonist_type+'_1'],
                          IMG['bird'+protagonist_type+'_2']]
    pipe_type = random.choice(['1', '2'])
    IMG['pipe'] = [IMG['pipe'+pipe_type+'_up'],
                   IMG['pipe'+pipe_type+'_down']]


def show_score(score):
    score_str = str(score)
    score_width = IMG['0'].get_width()*1.1
    score_x = (WIDTH-score_width*len(score_str))/2
    score_y = HEIGHT*0.1
    for number in score_str:
        SCREEN.blit(IMG[number], (score_x, score_y))
        score_x += score_width


def menu():
    title_x = (WIDTH - IMG['title'].get_width())/2
    title_y = HEIGHT/4
    land_x = 0
    button_play_x = (WIDTH - IMG['button_play'].get_width())/2
    button_play_y = (HEIGHT + IMG['button_play'].get_height())/2
    button_play = Button('button_play', button_play_x, button_play_y)
    protagonist = Bird(
        (WIDTH - IMG['bird0_1'].get_width())/2, (LAND_Y + IMG['bird0_1'].get_height())/2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and button_play.ispressed(event.pos):
                return

        SCREEN.blit(IMG['background'], (0, 0))
        if -land_x >= IMG['land'].get_width() - WIDTH:
            land_x = 0
        land_x -= 4
        SCREEN.blit(IMG['land'], (land_x, LAND_Y))
        SCREEN.blit(protagonist.image, protagonist.rect)
        SCREEN.blit(IMG['title'], (title_x, title_y))
        SCREEN.blit(button_play.image, button_play.rect)

        protagonist.idle()

        pygame.display.update()
        CLOCK.tick(FPS)


def begin():
    land_x = 0
    tutorial_x = (WIDTH - IMG['tutorial'].get_width())/2
    tutorial_y = (HEIGHT - IMG['tutorial'].get_height())/2
    ready_x = (WIDTH - IMG['text_ready'].get_width())/2
    ready_y = HEIGHT/4

    protagonist = Bird(tutorial_x - IMG['bird0_1'].get_width()/2, tutorial_y)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return

        SCREEN.blit(IMG['background'], (0, 0))
        if -land_x >= IMG['land'].get_width() - WIDTH:
            land_x = 0
        land_x -= 4
        SCREEN.blit(IMG['land'], (land_x, LAND_Y))
        SCREEN.blit(protagonist.image, protagonist.rect)
        SCREEN.blit(IMG['text_ready'], (ready_x, ready_y))
        SCREEN.blit(IMG['tutorial'], (tutorial_x, tutorial_y))
        show_score(0)

        protagonist.idle()

        pygame.display.update()
        CLOCK.tick(FPS)


def gameplay():
    land_x = 0
    protagonist = Bird(
        (WIDTH - IMG['tutorial'].get_width())/2 - IMG['bird0_1'].get_width()/2, (HEIGHT - IMG['tutorial'].get_height())/2)

    pipe_number = 4
    pipe_dis = 150
    pipe_gap = 100
    pipe_group = pygame.sprite.Group()
    for i in range(pipe_number):
        pipe_y = random.uniform(LAND_Y*0.3, LAND_Y*0.9)
        pipe_up = Pipe(WIDTH+i*pipe_dis, pipe_y, False)
        pipe_down = Pipe(WIDTH+i*pipe_dis, pipe_y-pipe_gap, True)
        pipe_group.add(pipe_up)
        pipe_group.add(pipe_down)

    score = 0

    while True:
        flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                flag = True

        SCREEN.blit(IMG['background'], (0, 0))
        pipe_group.draw(SCREEN)
        if -land_x >= IMG['land'].get_width() - WIDTH:
            land_x = 0
        land_x -= 4
        SCREEN.blit(IMG['land'], (land_x, LAND_Y))
        SCREEN.blit(protagonist.image, protagonist.rect)

        temp_pipeup = pipe_group.sprites()[0]
        temp_pipedown = pipe_group.sprites()[1]
        new_pipe_x = temp_pipeup.rect.x+pipe_number*pipe_dis
        if temp_pipeup.rect.right < 0:
            pipe_y = random.uniform(LAND_Y*0.3, LAND_Y*0.9)
            new_pipeup = Pipe(new_pipe_x, pipe_y, False)
            new_pipedown = Pipe(new_pipe_x, pipe_y-pipe_gap, True)
            pipe_group.add(new_pipeup)
            pipe_group.add(new_pipedown)
            temp_pipeup.kill()
            temp_pipedown.kill()

        protagonist.interact(flag)
        pipe_group.update()

        score_range = [protagonist.rect.centerx, protagonist.rect.centerx+4]
        if pipe_group.sprites()[0].rect.centerx > score_range[0] and pipe_group.sprites()[0].rect.centerx < score_range[1]:
            score += 1
        show_score(score)

        if protagonist.rect.centery <= 0 or protagonist.rect.centery >= LAND_Y:
            trans = {'protagonist': protagonist,
                     'pipe_group': pipe_group,
                     'score': score}
            return trans
        for j in range(3):
            if pipe_group.sprites()[j].iscrashed(protagonist.rect.center):
                trans = {'protagonist': protagonist,
                         'pipe_group': pipe_group,
                         'score': score}
                return trans
        pygame.display.update()
        CLOCK.tick(FPS)


def result(trans):
    protagonist = trans['protagonist']
    pipe_group = trans['pipe_group']
    score = trans['score']
    over_x = (WIDTH - IMG['text_game_over'].get_width())/2
    over_y = HEIGHT/3
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return
        SCREEN.blit(IMG['background'], (0, 0))
        pipe_group.draw(SCREEN)
        SCREEN.blit(protagonist.image, protagonist.rect)
        protagonist.die()
        SCREEN.blit(IMG['land'], (0, LAND_Y))
        SCREEN.blit(IMG['text_game_over'],(over_x,over_y))
        show_score(score)
        
        pygame.display.update()
        CLOCK.tick(FPS)


def main():
    random_method()
    menu()
    while True:
        begin()
        trans = gameplay()
        result(trans)
        random_method()

main()