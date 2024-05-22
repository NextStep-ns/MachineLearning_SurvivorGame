import pygame

#-----------------------------------------------------------------------------------------------------------------------
# Définir une classe pour les carottes
class Cow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 50
        self.heigth = 50
        self.rect_size = 20
        self.image = pygame.image.load('tiled/cow.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.heigth))
        self.rect = pygame.Rect(self.x+self.width/2 - self.rect_size/2, self.y+self.heigth/2 - self.rect_size/2, self.rect_size, self.rect_size)
        self.rect.topleft = (self.x, self.y)

#-----------------------------------------------------------------------------------------------------------------------

    # Méthode pour faire réapparaître la carotte à une nouvelle position aléatoire
    def respawn(self, x, y):
        self.rect.topleft = (x, y)
        self.x=x
        self.y=y
        print(self.rect.topleft)

#-----------------------------------------------------------------------------------------------------------------------

    def draw(self, surface):
        surface.blit(self.image, self.rect)