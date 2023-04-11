import pygame
import os
import random

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.image = BIRD_IMAGE

    def jump(self):
        self.velocity = -10

    def move(self):
        self.velocity += 1
        self.y += self.velocity
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        elif self.y + self.image.get_height() > WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - self.image.get_height()
            self.velocity = 0
    
    def draw(self):
        game_window.blit(self.image, (self.x, self.y))

class Pipe:
    def __init__(self, x, y, is_top=True):
        self.x = x
        self.y = y
        self.is_top = is_top
        self.image = PIPE_IMAGE
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.velocity = -3
        self.scored = False

    def move(self):
        self.x += self.velocity

    def draw(self):
        if self.is_top:
            flip_pipe_image = pygame.transform.flip(self.image, False, True)
            game_window.blit(flip_pipe_image, (self.x, self.y))
        else:
            game_window.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.x < -self.width

    def collides_with(self, bird):
        if bird.x + bird.image.get_width() > self.x and bird.x < self.x + self.width:
            if self.is_top:
                return bird.y < self.y + self.height - 10
            else:
                return bird.y + bird.image.get_height() > self.y + 10
        return False

BIRD_IMAGE = pygame.image.load(os.path.join('sprites', 'bird.png'))
PIPE_IMAGE = pygame.image.load(os.path.join('sprites', 'pipe.png'))
BACKGROUND_IMAGE = pygame.image.load(os.path.join('sprites', 'background.png'))
GET_READY_IMAGE = pygame.image.load(os.path.join('sprites', 'getready.png'))
GAME_OVER_IMAGE = pygame.image.load(os.path.join('sprites', 'gameover.png'))

WINDOW_WIDTH = BACKGROUND_IMAGE.get_width()
WINDOW_HEIGHT = BACKGROUND_IMAGE.get_height()
BIRD_IMAGE = pygame.transform.scale(BIRD_IMAGE, (int(48), int(48)))
GET_READY_IMAGE = pygame.transform.scale(GET_READY_IMAGE, (int(WINDOW_WIDTH), int(WINDOW_HEIGHT)))
SPAWN_PIPE_EVENT = pygame.USEREVENT

game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pipes = []
scores = []
score = 0
highestscore = 0
game_running = True
game_over = False
game_started = False
clock = pygame.time.Clock()
bird = Bird(50, 400)

pygame.init()
pygame.display.set_caption("Flappy Bird")
pygame.time.set_timer(SPAWN_PIPE_EVENT, 1200)

def reset_game():
    global bird, pipes, score, game_over, BACKGROUND_IMAGE, PIPE_IMAGE
    bird = Bird(50, 400)
    pipes = []
    score = 0
    game_over = False
    pygame.time.set_timer(SPAWN_PIPE_EVENT, 1200)
    BACKGROUND_IMAGE = pygame.image.load(os.path.join('sprites', 'background.png'))
    PIPE_IMAGE = pygame.image.load(os.path.join('sprites', 'pipe.png'))

def draw_background():
    game_window.blit(BACKGROUND_IMAGE, (0, 0))

def draw_bird(bird):
    game_window.blit(bird.image, (bird.x, bird.y))

def draw_get_ready():
    game_window.blit(GET_READY_IMAGE, (0, 0))

def draw_pipes():
    pipe_gap = 150
    min_pipe_height = 100
    max_pipe_height = WINDOW_HEIGHT - min_pipe_height - pipe_gap
    pipe_height = random.randint(min_pipe_height, max_pipe_height)
    top_pipe = Pipe(WINDOW_WIDTH, pipe_height - PIPE_IMAGE.get_height(), True)
    bottom_pipe = Pipe(WINDOW_WIDTH, pipe_height + pipe_gap, False)
    pipes.append(top_pipe)
    pipes.append(bottom_pipe)

def draw_game():
    draw_background()
    draw_bird(bird)
    for pipe in pipes:
        pipe.draw()
    font = pygame.font.Font(None, 48)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    game_window.blit(score_text, (10, 10))

def event_game_start():
    global game_started
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_started = True
                pygame.time.wait(100)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game_started = True
            pygame.time.wait(100)

def event_game_over():
    global game_running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    reset_game()
                else:
                    bird.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                reset_game()
            else:
                bird.jump()
        elif event.type == SPAWN_PIPE_EVENT:
            draw_pipes()

def pipes_manager():
    global game_over, BACKGROUND_IMAGE, PIPE_IMAGE, pipes, score
    for pipe in pipes:
        pipe.move()
    pipes = [pipe for pipe in pipes if not pipe.off_screen()]
    for pipe in pipes:
        if not pipe.is_top and not pipe.scored and pipe.x < bird.x:
            pipe.scored = True
            score += 1
            if score >= 10:
                BACKGROUND_IMAGE = pygame.image.load(os.path.join('sprites', 'background-night.png'))
                PIPE_IMAGE = pygame.image.load(os.path.join('sprites', 'pipe-red.png'))
        if pipe.off_screen() and pipe.scored:
            pipes.remove(pipe)
    for pipe in pipes:
        if pipe.collides_with(bird):
            game_over = True

while not game_started:
    draw_get_ready()
    event_game_start()
    pygame.display.update()
    clock.tick(60)

while game_running:
    event_game_over()
    bird.move()
    pipes_manager()
    draw_game()
    if game_over:
        game_window.blit(GAME_OVER_IMAGE, (WINDOW_WIDTH/2 - GAME_OVER_IMAGE.get_width()/2, WINDOW_HEIGHT/2 - GAME_OVER_IMAGE.get_height()/2))
        scores.append(score)
        font = pygame.font.SysFont(None, 40)
        highestscore_max = max(scores)
        highestscore = font.render(f"Highest Score: {highestscore_max}", True, (255, 255, 255))
        game_window.blit(highestscore, (36, 280))
        pygame.display.update() 
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        reset_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    reset_game()
    pygame.display.update()
    clock.tick(60)
pygame.quit()