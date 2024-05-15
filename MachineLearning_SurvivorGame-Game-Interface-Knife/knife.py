import pygame
import random
import time
from player import Player

class Knife(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y
        self.image = pygame.image.load('tiled/knife.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.knife_exist = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_near(self, player):
        # Check if the player is near the knife
        return pygame.sprite.collide_rect(self, player)

    def pick_up(self, player, key):
        # If the player is near the knife and press Enter, pick it up
        if self.is_near(player) and key == pygame.K_RETURN:
            
            
            player.add_to_inventory("knife")
            self.knife_exist = False  # Mark the knife as not existing anymore
            self.kill()  # Remove the knife sprite from the group
