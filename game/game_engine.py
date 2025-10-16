import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine
WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 5  # score to win
        self.game_over = False
        self.winner_text = ""
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            return  # stop updates when game is over

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

        # check for game over
        if self.player_score >= self.winning_score:
            self.game_over = True
            self.winner_text = "PLAYER WINS"
            self.end_time = pygame.time.get_ticks()
        elif self.ai_score >= self.winning_score:
            self.game_over = True
            self.winner_text = "AI WINS"
            self.end_time = pygame.time.get_ticks()

    def render(self, screen):
        screen.fill((0, 0, 0))

        if not self.game_over:
            # draw paddles and ball
            pygame.draw.rect(screen, WHITE, self.player.rect())
            pygame.draw.rect(screen, WHITE, self.ai.rect())
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

            # draw scores
            player_text = self.font.render(str(self.player_score), True, WHITE)
            ai_text = self.font.render(str(self.ai_score), True, WHITE)
            screen.blit(player_text, (self.width//4, 20))
            screen.blit(ai_text, (self.width * 3//4, 20))
        else:
            # game over screen
            text_surface = self.font.render(self.winner_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width//2, self.height//2))
            screen.blit(text_surface, text_rect)

            # keep message visible for 3 seconds
            if pygame.time.get_ticks() - self.end_time > 3000:
                pygame.quit()
                exit()
