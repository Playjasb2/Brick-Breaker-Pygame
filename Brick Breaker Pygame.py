
# Brick Breaker Pygame Version 2.0.1
import sys
import pygame

SCREEN_SIZE   = 640,480

# Object dimensions
BRICK_WIDTH   = 60
BRICK_HEIGHT  = 15
PADDLE_WIDTH  = 60
PADDLE_HEIGHT = 12
BALL_DIAMETER = 16
BALL_RADIUS   = BALL_DIAMETER / 2

MAX_PADDLE_X = SCREEN_SIZE[0] - PADDLE_WIDTH
MAX_BALL_X   = SCREEN_SIZE[0] - BALL_DIAMETER
MAX_BALL_Y   = SCREEN_SIZE[1] - BALL_DIAMETER

# Paddle Y coordinate
PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 10

# Color constants
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0,0,255)
GOLD = (200,200,0)
GREEN = (0,255,0)
SKY_BLUE = (0,239,255)
ORANGE = (255,154,0)
RED = (255,0,0)


# State constants
STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3
STATE_NEXT_LEVEL = 4
STATE_PAUSE = 5

class Bricka:

    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Brick Breaker Version 2.0.1")
        
        self.clock = pygame.time.Clock()

        if pygame.font:
            self.font = pygame.font.Font(None,30)
        else:
            self.font = None

#These define the initial constants at the very beginning and they are never resetted.
        self.lives = 3
        self.level = 1
        self.score = 0
        self.Paddle_Speed = 18

        self.init_game()

        
    def init_game(self):
        self.state = STATE_BALL_IN_PADDLE

        self.paddle   = pygame.Rect(300,PADDLE_Y,PADDLE_WIDTH,PADDLE_HEIGHT)
        self.ball     = pygame.Rect(300,PADDLE_Y - BALL_DIAMETER,BALL_DIAMETER,BALL_DIAMETER)

        if self.level == 1:
            self.ball_vel = [5,-5]
        elif self.level == 2:
            self.ball_vel = [6,-6]
        elif self.level == 3:
            self.ball_vel = [7,-7]
        elif self.level == 4:
            self.ball_vel = [8,-8]
        else:
            self.ball_vel = [9,-9]

        self.create_bricks()
        

    def create_bricks(self):
            y_ofs = 35
            self.bricks = []
            for i in range(7):
                x_ofs = 35
                for j in range(8):
                    self.bricks.append(pygame.Rect(x_ofs,y_ofs,BRICK_WIDTH,BRICK_HEIGHT))
                    x_ofs += BRICK_WIDTH + 10
                y_ofs += BRICK_HEIGHT + 5

    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, self.BRICK_COLOUR, brick)
        
    def check_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.paddle.left -= self.Paddle_Speed
            if self.paddle.left < 0:
                self.paddle.left = 0

        if keys[pygame.K_RIGHT]:
            self.paddle.left += self.Paddle_Speed
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        if keys[pygame.K_SPACE] and self.state == STATE_BALL_IN_PADDLE:
            self.ball_vel = self.ball_vel
            self.state = STATE_PLAYING
        elif keys[pygame.K_RETURN] and self.state == STATE_NEXT_LEVEL:
            self.level += 1
            self.init_game()
            self.level_difficulty()
        elif keys[pygame.K_RETURN] and (self.state == STATE_GAME_OVER or self.state == STATE_WON):
            self.init_game()
            self.lives = 3
            self.score = 0
            self.level = 1
            self.Paddle_Speed = 20
            self.ball_vel = [5,-5]

        if len(self.bricks) == 0:
            self.state = STATE_NEXT_LEVEL

        if keys[pygame.K_SPACE] and self.ball.top > self.paddle.top:
            if self.state == STATE_GAME_OVER and self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            else:
                self.state = STATE_GAME_OVER
                    
    def move_ball(self):
        self.ball.left += self.ball_vel[0]
        self.ball.top  += self.ball_vel[1]

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MAX_BALL_X:
            self.ball.left = MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]
        
        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top >= MAX_BALL_Y:            
            self.ball.top = MAX_BALL_Y
            self.ball_vel[1] = -self.ball_vel[1]

    def handle_collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                if self.BRICK_COLOUR == GOLD:
                    self.score += 3
                elif self.BRICK_COLOUR == RED:
                    self.score += 5
                elif self.BRICK_COLOUR == SKY_BLUE:
                    self.score += 8
                elif self.BRICK_COLOUR == ORANGE:
                    self.score += 10
                else:
                    self.score += (self.level*5)
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                break
            
        if self.ball.colliderect(self.paddle):
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            #The Code below shows when the user could win the game.
            elif self.lives == 0 and self.score >= 1500:
                self.state = STATE_WON
            elif self.lives == 0 and self.score < 1500:
                self.state = STATE_GAME_OVER

    def level_difficulty(self):
        if self.level == 2:
            self.Paddle_Speed = 16
            self.ball_vel = [6,-6]
            self.lives += 1
        elif self.level == 3:
            self.Paddle_Speed = 14
            self.ball_vel = [7,-7]
            self.lives += 2
        elif self.level == 4:
            self.Paddle_Speed = 12
            self.ball_vel = [8,-8]
            self.lives += 3
        else:
            self.Paddle_Speed = 10
            self.ball_vel = [9,-9]
            self.lives += 4

    def show_stats(self):
        if self.font:
            font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives) + " LEVEL: " + str(self.level), False, WHITE)
            self.screen.blit(font_surface, (205,5))

    def show_message(self,message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message,False, WHITE)
            x = (SCREEN_SIZE[0] - size[0]) / 2
            y = (SCREEN_SIZE[1] - size[1]) / 2
            self.screen.blit(font_surface, (x,y))
        
            
    def run(self):
        while 1:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit

            self.clock.tick(50)
            self.screen.fill(BLACK)
            self.check_input()
            
            if self.level == 1:
                self.BRICK_COLOUR = GOLD
            elif self.level == 2:
                self.BRICK_COLOUR = SKY_BLUE
            elif self.level == 3:
                self.BRICK_COLOUR = ORANGE
            elif self.level == 4:
                self.BRICK_COLOUR = RED
            else:
                self.BRICK_COLOUR = GREEN

            if self.state == STATE_PLAYING:
                self.move_ball()
                self.handle_collisions()
            elif self.state == STATE_BALL_IN_PADDLE:
                self.ball.left = self.paddle.left + self.paddle.width / 2
                self.ball.top  = self.paddle.top - self.ball.height
                self.show_message("PRESS SPACE TO LAUNCH THE BALL")
            elif self.state == STATE_GAME_OVER:
                self.show_message("GAME OVER. PRESS ENTER TO PLAY AGAIN")
            elif self.state == STATE_WON:
                self.show_message("YOU WON! PRESS ENTER TO PLAY AGAIN")
            elif self.state == STATE_NEXT_LEVEL:
                self.show_message("YOU WON THIS LEVEL! PRESS TO CONTINUE")
                
            self.draw_bricks()

            # Draw paddle
            pygame.draw.rect(self.screen, BLUE, self.paddle)

            # Draw ball
            pygame.draw.circle(self.screen, WHITE, (int(self.ball.left + BALL_RADIUS),int(self.ball.top + BALL_RADIUS)),int(BALL_RADIUS))

            self.show_stats()

            pygame.display.flip()

try:
    if __name__ == "__main__":
        Bricka().run()
except:
    print("The game has quit successfully! Thanks for playing our game!")
