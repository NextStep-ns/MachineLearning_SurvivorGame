import pygame

#-----------------------------------------------------------------------------------------------------------------------
# Définir une classe pour les carottes
class Cow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load('tiled/cow.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

#-----------------------------------------------------------------------------------------------------------------------

    # Méthode pour faire réapparaître la carotte à une nouvelle position aléatoire
    def respawn(self, x, y):
        self.rect.topleft = (x, y)
        print(self.rect.topleft)

#-----------------------------------------------------------------------------------------------------------------------

    def draw(self, surface):
        surface.blit(self.image, self.rect)