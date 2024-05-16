import pygame

class Trap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load('tiled/trap.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = pygame.Rect(x+15, y-15, 15, 15)
        self.rect.topleft = (x, y)

#-----------------------------------------------------------------------------------------------------------------------

    # Méthode pour faire réapparaître la carotte à une nouvelle position aléatoire
    def respawn(self, x, y):
        self.rect.topleft = (x, y)
        print(self.rect.topleft)

#-----------------------------------------------------------------------------------------------------------------------

    def draw(self, surface):
        surface.blit(self.image, self.rect)