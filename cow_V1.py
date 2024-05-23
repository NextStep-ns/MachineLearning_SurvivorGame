import pygame

#-----------------------------------------------------------------------------------------------------------------------
# Définir une classe pour les carottes
class Cow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        width = 300
        height = 300
        self.images = {
            'vache_alive': [pygame.transform.scale(pygame.image.load(f'Tiled/Vache/Vache-{i}.png'), (width, height)) for i in range(1, 4)],
            'vache_mort': [pygame.transform.scale(pygame.image.load(f'Tiled/Vache/Mort/mort-{i}.png'), (width, height)) for i in range(1, 4)]
        }
        self.current_image_list = self.images['vache_alive']
        self.current_image_index = 0
        self.current_image_index1 = 0
        self.image = self.current_image_list[self.current_image_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_counter = 0
        self.animation_counter1 = 0

        self.image_duration = 20
        self.image_duration1 = 10
        self.dead_animation_done = False  # New flag for dead animation

#-----------------------------------------------------------------------------------------------------------------------

    # Méthode pour faire réapparaître la carotte à une nouvelle position aléatoire
    def respawn(self, x, y):
        self.rect.topleft = (x, y)
#-----------------------------------------------------------------------------------------------------------------------

    def animate(self, animation_type='alive'):
            if animation_type == 'dead':
                self.current_image_list = self.images['vache_mort']
                while not self.dead_animation_done:
                    self.animation_counter1 += 1
                    if self.animation_counter1 >= self.image_duration1:
                        self.animation_counter1 = 0
                        self.current_image_index1 = (self.current_image_index1 + 1) % len(self.current_image_list)
                        self.image = self.current_image_list[self.current_image_index1]
                        print('uuuuuuuuuuuuuuuuuuuuu',self.current_image_index1)
                        
                        if self.current_image_index1 == len(self.current_image_list) - 1:
                            self.dead_animation_done = True
                    
            else:
                self.dead_animation_done = False  # Reset flag when not dead
                self.current_image_list = self.images['vache_alive']
                self.animation_counter += 1
                if self.animation_counter >= self.image_duration:
                    self.animation_counter = 0
                    self.current_image_index = (self.current_image_index + 1) % len(self.current_image_list)
                    self.image = self.current_image_list[self.current_image_index]
                        
                
                
                