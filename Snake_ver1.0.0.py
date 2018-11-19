# Pygame template - skeleton for a new pygame project
import pygame
import random
import os

WIDTH = 600
HEIGHT = 600
FPS = 10
global base
base = 50 # These are our basic units, everything is on a 12 * 12 grid with each unit being 50px * 50px
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DIF_GREEN = (128, 255, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
background = pygame.Surface((50, 50))
background.fill(BLACK)
background_rect = background.get_rect()

# Functions
def newApple(): # Creates an apple
    a = Apple()
    if collision(snake.posx, snake.posy, a.rect.x, a.rect.y): # if the apple somehow spawns within the snake
        a.kill() # It will kill itself
        newApple() # Then create a new apple
    else:      # If it doesn't spawn within the snake, then we're all good.
        all_sprites.add(a) 
        apples.add(a)

def prune(lst, length): # Prunes the last snake segment
    if len(lst) > (length - 1): # This checks if the snake segment exceeds its limit
        del lst[-1:] # This deletes the very last element

# Checks if two things are colliding or intersecting
def collision(x_lst, y_lst, x_coord, y_coord):
    in_bod = False
    for (x, y) in zip(x_lst, y_lst): # iterates through the two lists simultaneously
        if x_coord == x and y_coord == y: # if this is true, then it will break because it has no reason to continue checking.  This cuts down on run time
            in_bod = True
            break 
    return in_bod

def show_go_screen(): # "go" is shorthand for "Game over"
    draw_text(screen, "SNAKE!", 64, WIDTH / 2, HEIGHT / 4)
    if snake.length < 121:
        draw_text(screen, "Press a key to begin.  Your final length was {}" .format(snake.length), 18, WIDTH / 2, HEIGHT * 3 / 4)
    else:
        draw_text(screen, "Press a key to begin.  Your final length was {}.  You win!" .format(snake.length), 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
    
    
    
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


####################### CLASSES #############################

class Apple(pygame.sprite.Sprite): # Apple object
    global base
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(1,11)* base, random.randint(1,11)* base) # Randomly generates

class Player(pygame.sprite.Sprite):
    global base
    
    def __init__(self):
        # Generate snake head and snake itself
        self.posx = [] # X Snake segment position
        self.posy = [] # Y Snake segment position
        self.length = 5
        self.posx.append(base * 6) # Creates head
        self.posy.append(base * 6) # Creates head
        # ------------------
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (self.posx[0], self.posy[0])
        self.speedx = 50
        self.speedy = 0

    def update(self):
        # Controls
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] and self.speedx != 50:
            self.speedx = -50
            self.speedy = 0
        if keystate[pygame.K_RIGHT] and self.speedx != -50:
            self.speedx = 50
            self.speedy = 0
        if keystate[pygame.K_UP] and self.speedy != 50:
            self.speedy = -50
            self.speedx = 0
        if keystate[pygame.K_DOWN] and self.speedy != -50:
            self.speedy = 50
            self.speedx = 0
        # controls
        
        # Unshift the new snake head into the snake matricies
        xd = self.rect.x
        yd = self.rect.y
        self.posy = [yd] + self.posy
        self.posx = [xd] + self.posx
        # --------------------
        
        # Moving the head
        self.posx[0] += self.speedx
        self.posy[0] += self.speedy
        self.rect.x = self.posx[0]
        self.rect.y = self.posy[0]


class Body(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(DIF_GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x + 25, y + 25)

    def update(self):
        if collision(snake.posx, snake.posy, self.rect.x, self.rect.y) == False:
            self.kill()
           

all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
apples = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
player_bod = pygame.sprite.Group()

snake = Player()
all_sprites.add(snake)
player_sprites.add(snake)
newApple()

# Game loop
game_over = True
running = True
while running:
    clock.tick(FPS)
    
    if game_over:
        # Reset everything
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        player_sprites = pygame.sprite.Group()
        apples = pygame.sprite.Group()
        player_sprites = pygame.sprite.Group()
        player_bod = pygame.sprite.Group()
        snake = Player()
        all_sprites.add(snake)
        player_sprites.add(snake)
        newApple()
        snake.length = 5
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Apples collision detection
    hits = pygame.sprite.groupcollide(player_sprites, apples, False, True)
    if hits:
        newApple()
        snake.length += 1 # increases the length
    # ---------------------------

    # Check if snake is colliding with itself
    if collision(snake.posx[1:], snake.posy[1:], snake.posx[0], snake.posy[0]):
        game_over = True
    # ----------------------------------------
        
    # Creates new snake segments and deletes the very last snake segment
    for segment in range(len(snake.posx)):
        prune(snake.posx, snake.length)
        prune(snake.posy, snake.length)
        b = Body(snake.posx[segment-1],snake.posy[segment-1])
        all_sprites.add(b)
        player_bod.add(b)
    # ----------------------------------------
    
    # Out of bounds detection
    snake_head = {"x": snake.posx[0], "y": snake.posy[0]}
    if snake_head["x"] > WIDTH - 50 or snake_head["x"] < 25:
        game_over = True
    
    if snake_head["y"] > HEIGHT - 50 or snake_head["y"] < 25: 
        game_over = True
    
    # Win condition.  If the player exceeds the 11 * 11 grid or 121 snake segments, they win.
    if snake.length > 120:
        game_over = True
    # ----------------------------
    all_sprites.update()
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()