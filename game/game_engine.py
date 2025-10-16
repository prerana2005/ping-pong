import pygame
import os
from .paddle import Paddle
from .ball import Ball

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

        # Scoring and states
        self.player_score = 0
        self.ai_score = 0
        self.winning_score = 5
        self.state = "PLAYING"  # PLAYING, GAME_OVER, REPLAY_MENU
        self.game_over_start_time = None
        self.winner_text = ""
        self.font = pygame.font.SysFont("Arial", 30)

        # --- Sound setup ---
        pygame.mixer.init()
        assets_path = os.path.join(os.path.dirname(__file__), "assets")
        self.sound_paddle = pygame.mixer.Sound(os.path.join(assets_path, "sound_paddle.wav"))
        self.sound_wall = pygame.mixer.Sound(os.path.join(assets_path, "sound_wall.wav"))
        self.sound_score = pygame.mixer.Sound(os.path.join(assets_path, "sound_score.wav"))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # --- GAME_OVER waiting ---
        if self.state == "GAME_OVER":
            if pygame.time.get_ticks() - self.game_over_start_time > 2000:
                self.state = "REPLAY_MENU"
            return

        # --- REPLAY_MENU input ---
        if self.state == "REPLAY_MENU":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                self.start_new_match(best_of=3)
            elif keys[pygame.K_2]:
                self.start_new_match(best_of=5)
            elif keys[pygame.K_3]:
                self.start_new_match(best_of=7)
            elif keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()
            return

        # --- PLAYING state ---
        if self.state == "PLAYING":
            self.ball.move(sound_wall=self.sound_wall)
            self.ball.check_collision(self.player, self.ai, sound_paddle=self.sound_paddle)

            if self.ball.x <= 0:
                self.ai_score += 1
                self.sound_score.play()
                self.ball.reset()
            elif self.ball.x >= self.width:
                self.player_score += 1
                self.sound_score.play()
                self.ball.reset()

            self.ai.auto_track(self.ball, self.height)

            if self.player_score >= self.winning_score:
                self.winner_text = "PLAYER WINS!"
                self.state = "GAME_OVER"
                self.game_over_start_time = pygame.time.get_ticks()
            elif self.ai_score >= self.winning_score:
                self.winner_text = "AI WINS!"
                self.state = "GAME_OVER"
                self.game_over_start_time = pygame.time.get_ticks()

    def start_new_match(self, best_of):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.winning_score = best_of // 2 + 1
        self.state = "PLAYING"

    def render(self, screen):
        screen.fill((0, 0, 0))

        if self.state == "PLAYING":
            pygame.draw.rect(screen, WHITE, self.player.rect())
            pygame.draw.rect(screen, WHITE, self.ai.rect())
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

            player_text = self.font.render(str(self.player_score), True, WHITE)
            ai_text = self.font.render(str(self.ai_score), True, WHITE)
            screen.blit(player_text, (self.width//4, 20))
            screen.blit(ai_text, (self.width*3//4, 20))

        elif self.state == "GAME_OVER":
            text_surface = self.font.render(self.winner_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width//2, self.height//2))
            screen.blit(text_surface, text_rect)

        elif self.state == "REPLAY_MENU":
            font = pygame.font.SysFont(None, 48)
            lines = [
                "Press 1: Best of 3",
                "Press 2: Best of 5",
                "Press 3: Best of 7",
                "Press ESC: Exit"
            ]
            for i, line in enumerate(lines):
                text = font.render(line, True, WHITE)
                rect = text.get_rect(center=(self.width//2, 250 + i*80))
                screen.blit(text, rect)
