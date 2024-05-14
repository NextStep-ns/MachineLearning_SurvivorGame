import pygame
import random
import time

#-----------------------------------------------------------------------------------------------------------------------

# Définir une classe pour les carottes
class Carrot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y
        self.image = pygame.image.load('tiled/2909789.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

#-----------------------------------------------------------------------------------------------------------------------

    # Méthode pour faire réapparaître la carotte à une nouvelle position aléatoire
    def respawn(self, width, height):
        self.rect.topleft = (random.randint(0, width - 20), random.randint(0, height - 20))

#-----------------------------------------------------------------------------------------------------------------------

    def draw(self, surface):
        surface.blit(self.image, self.rect)