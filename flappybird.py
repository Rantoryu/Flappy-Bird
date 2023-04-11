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

# Initialize Pygame
pygame.init()

# Load images
BIRD_IMAGE = pygame.image.load(os.path.join('sprites', 'bird-nyla.png'))
PIPE_IMAGE = pygame.image.load(os.path.join('sprites', 'pipe.png'))
BACKGROUND_IMAGE = pygame.image.load(os.path.join('sprites', 'background.png'))
GET_READY_IMAGE = pygame.image.load(os.path.join('sprites', 'getready.png'))
GAME_OVER_IMAGE = pygame.image.load(os.path.join('sprites', 'gameover.png'))

# Set up the game window
WINDOW_WIDTH = BACKGROUND_IMAGE.get_width()
WINDOW_HEIGHT = BACKGROUND_IMAGE.get_height()
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Alter Image
BIRD_IMAGE = pygame.transform.scale(BIRD_IMAGE, (int(32), int(32)))
GET_READY_IMAGE = pygame.transform.scale(GET_READY_IMAGE, (int(WINDOW_WIDTH), int(WINDOW_HEIGHT)))

# Pipes
SPAWN_PIPE_EVENT = pygame.USEREVENT

# Variables and objects
pipes = []
scores = []
score = 0
running = True
game_over = False
game_started = False
clock = pygame.time.Clock()
bird = Bird(50, 400)

# Set the caption / Window title
pygame.display.set_caption("Flappy Bird")
pygame.time.set_timer(SPAWN_PIPE_EVENT, 1200)

def reset_game():
    global bird, pipes, score, game_over
    bird = Bird(50, 400)
    pipes = []
    score = 0
    game_over = False
    pygame.time.set_timer(SPAWN_PIPE_EVENT, 0) # Stop timer
    pygame.time.set_timer(SPAWN_PIPE_EVENT, 1200) # Start timer again

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
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    game_window.blit(score_text, (10, 10))

while not game_started:
    draw_get_ready()
    # Handle Events
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

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(60)

# Game loop
while running:
    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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

    # Update game objects
    bird.move()

    # Move pipes
    for pipe in pipes:
        pipe.move()

    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if not pipe.off_screen()]

    # Add score for passing pipes
    for pipe in pipes:
        if not pipe.is_top and not pipe.scored and pipe.x < bird.x:
            pipe.scored = True
            score += 1
            if score >= 5:
                BACKGROUND_IMAGE = pygame.image.load(os.path.join('sprites', 'background-night.png'))
                BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))
        if pipe.off_screen() and pipe.scored:
            pipes.remove(pipe)

    # Check for collisions
    for pipe in pipes:
        if pipe.collides_with(bird):
            game_over = True

    draw_game()

    # Check if game is over
    if game_over:
        game_window.blit(GAME_OVER_IMAGE, (WINDOW_WIDTH/2 - GAME_OVER_IMAGE.get_width()/2, WINDOW_HEIGHT/2 - GAME_OVER_IMAGE.get_height()/2))
        pygame.display.update()
        scores.append(score)
        print("This session scores: ", scores)
        # Wait for the user to restart the game
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Restart game
                        bird = Bird(50, 400)
                        pipes = []
                        score = 0
                        game_over = False
                        pygame.time.set_timer(SPAWN_PIPE_EVENT, 1200)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Restart game
                    bird = Bird(50, 400)
                    pipes = []
                    score = 0
                    game_over = False
                    pygame.time.set_timer(SPAWN_PIPE_EVENT, 1200)
    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(60)


#Quit Pygame
pygame.quit()