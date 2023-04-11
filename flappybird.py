import pygame
import os

# Initialize Pygame
pygame.init()

# Load images
BIRD_IMAGE = pygame.image.load(os.path.join('sprites', 'bird-nyla.png'))
PIPE_IMAGE = pygame.image.load(os.path.join('sprites', 'pipe.png'))
BACKGROUND_IMAGE = pygame.image.load(os.path.join('sprites', 'background.png'))
GET_READY_IMAGE = pygame.image.load(os.path.join('sprites', 'getready.png'))

# Set up the game window
WINDOW_WIDTH = BACKGROUND_IMAGE.get_width()
WINDOW_HEIGHT = BACKGROUND_IMAGE.get_height()
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set the caption
pygame.display.set_caption("Flappy Bird")

# Clock object
clock = pygame.time.Clock()

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

# Create a Bird object
bird = Bird(50, 400)

# Show the "get ready" screen
game_started = False
while not game_started:
    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_started = True
                # Wait for a short delay
                pygame.time.wait(1000)

    # Draw the "get ready" screen
    game_window.blit(GET_READY_IMAGE, (100, 200))

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(60)

# Game loop
running = True
while running:
    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    # Update game objects
    bird.move()

    # Draw game objects
    game_window.blit(BACKGROUND_IMAGE, (0, 0))
    bird.draw()

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(60)

#Quit Pygame
pygame.quit()