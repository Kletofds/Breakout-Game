########################################
# Breakout Game
# Kelton Figurski
########################################

import pygame,time


# -------------- Classes -------------- #

# class for the paddle 
class Paddle(pygame.sprite.Sprite):

    # initialization function
    def __init__(self, color, width, height):

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()
        
    # function to move the platform to the left
    def move_left(self, pixels):
        self.rect.x -= pixels

        if self.rect.x < 0:
          self.rect.x = 0

    # function to move the platform to the right
    def move_right(self, pixels):
        self.rect.x += pixels

        if self.rect.x > 600:
          self.rect.x = 600
          
# class for the bricks
class Brick(pygame.sprite.Sprite):

    # initialization function
    def __init__(self, color, width, height):

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()
        
# class for the ball
class Ball(pygame.sprite.Sprite):

    # initialization function
    def __init__(self, color, width, height):

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()
        
        self.width = width
        self.height = height

        self.speed = [3, 3]

    # function that updates the position of the ball
    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH - self.width:
            self.speed[0] = -self.speed[0]

        if self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT - self.height:
            self.speed[1] = -self.speed[1]
            
        if self.rect.y > SCREEN_HEIGHT - self.height:
            screen.blit(game_over_text, game_over_text_rect)
            
            global GameOver
            GameOver = True
            
            global Run
            Run = False
        
# -------------- Main Code -------------- #

# initializes pygame
pygame.init()

# sets colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# creates the pygame screen
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

clock = pygame.time.Clock()

# sets the font of the text
font = pygame.font.SysFont("Arial", 24)

# saves text for game over
game_over_text = font.render("Game Over", True, WHITE)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.centerx = SCREEN_WIDTH / 2
game_over_text_rect.centery = SCREEN_HEIGHT / 2

# saves the text for if the user won
win_text = font.render("You Won", True, WHITE)
win_text_rect = game_over_text.get_rect()
win_text_rect.centerx = SCREEN_WIDTH / 2
win_text_rect.centery = SCREEN_HEIGHT / 2

# creates a sprite list for the bricks
bricks = pygame.sprite.Group()

# creates a sprite list for the rest of the objects
all_sprites_list = pygame.sprite.Group()

# creates the starting position of the paddle using the paddle class
paddle = Paddle(WHITE, 100, 10)
paddle.rect.x = 350
paddle.rect.y = 450

# creates the starting position of the ball using the ball class
ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

# adds the paddle and the ball to the sprite list
all_sprites_list.add(paddle)
all_sprites_list.add(ball)

# creates the bricks and adds them to the brick sprite list
for i in range(11):
    for q in (50, 80, 110, 140):
        brick = Brick(RED, 50, 20)
        
        brick.rect.x = 60 * i + 15
        brick.rect.y = q

        bricks.add(brick)
        all_sprites_list.add(brick)

Run = True # sets Run status to true
GameOver = False # sets GameOver(Lose) status to false
Win = False # sets the Win status to false

# Main Game Loop
while Run:
    # exits the loop if the user hits the exit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Run = False
            
    # moves the platform left or right if a/left or d/right are pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        paddle.move_left(5)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        paddle.move_right(5)
    
    # finds out how many bricks are left
    bricks_left = len(bricks)
    
    # ends the loop and sets the Win status to true if there are no bricks left
    if bricks_left == 0:
        Run = False
        Win = True
    
    # updates the position of the ball
    ball.update()

    # changes direction of ball if it hits platform
    if pygame.sprite.collide_rect(ball, paddle):
      ball.speed[1] = -ball.speed[1]

    # creates a list for the bricks that have collided with the ball
    brick_collision_list = pygame.sprite.spritecollide(ball, bricks, False)
    
    # removes bricks that have collided with the ball
    for brick in brick_collision_list:
        ball.speed[1] = -ball.speed[1]
        bricks.remove(brick)
        all_sprites_list.remove(brick)

    # draws the next screen
    screen.fill(BLACK)
    all_sprites_list.draw(screen)
    
    # Tells the user if they lost
    if GameOver:
        screen.blit(game_over_text, game_over_text_rect)
        
    # Tells the user if they won    
    if Win:
        screen.blit(win_text, game_over_text_rect)
    
    # updates the display
    pygame.display.flip()
    
    # sets frame rate to 60
    clock.tick(60)
    
# Waits so the user has time to view the text
if GameOver or Win:
    time.sleep(3)

pygame.quit()