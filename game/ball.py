import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        # Predict next position
        next_x = self.x + self.velocity_x
        next_y = self.y + self.velocity_y

        # Update Y first and bounce off top/bottom
        self.y = next_y
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1

        # Apply horizontal motion separately (collision handled externally)
        self.x = next_x

    def check_collision(self, player, ai):
        ball_rect = self.rect()

        # --- Player paddle collision ---
        if ball_rect.colliderect(player.rect()):
            # Place the ball flush with the paddle edge
            self.x = player.rect().right
            self.velocity_x = abs(self.velocity_x)  # Ensure it moves right

        # --- AI paddle collision ---
        elif ball_rect.colliderect(ai.rect()):
            self.x = ai.rect().left - self.width
            self.velocity_x = -abs(self.velocity_x)  # Ensure it moves left

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
