import pygame
import sys

#-----------------------------------------------------------------------------------------------------------------------
class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

        # Load images for different directions
        self.images = {
            'face': [pygame.image.load(f'tiled/Marche/Face/Anim_Face-{i}.png') for i in range(1, 4)],
            'dos': [pygame.image.load(f'tiled/Marche/Dos/Anim_Dos-{i}.png') for i in range(1, 4)],
            'gauche': [pygame.image.load(f'tiled/Marche/Gauche/Anim_Gauche-{i}.png') for i in range(1, 4)],
            'droite': [pygame.image.load(f'tiled/Marche/Droite/Anim_Droite-{i}.png') for i in range(1, 4)]
        }

        self.current_direction = 'face'
        self.current_image_index = 0
        self.animation_counter = 0
        self.animation_speed = 10  # Change this value to adjust the speed of animation
        self.image = self.images[self.current_direction][self.current_image_index]
        self.image = pygame.transform.scale(self.image, (350, 350))

        self.rect = self.image.get_rect()
        self.position = [self.x, self.y]

        self.speed = 20
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.3, 12)
        self.old_position = self.position.copy()
        self.life = 100
        self.max_health = 100
        self.last_update_time = pygame.time.get_ticks()
        self.inventory = []

    #-----------------------------------------------------------------------------------------------------------------------

    def life_update(self):
        """Update player's life."""
        now = pygame.time.get_ticks()
        elapsed_time = now - self.last_update_time

        if elapsed_time >= 1000:
            self.life_evolution(-2)
            self.last_update_time = now

    #-----------------------------------------------------------------------------------------------------------------------

    def life_evolution(self, amount):
        """Increase or decrease the player's life."""
        self.life = min(max(self.life + amount, 0), self.max_health)
        if self.life <= 0:
            self.death()

    #-----------------------------------------------------------------------------------------------------------------------

    def death(self):
        """Handle player's death."""
        print("Player has died.")
        pygame.quit()
        quit()

    #-----------------------------------------------------------------------------------------------------------------------

    def update_image(self):
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.current_image_index = (self.current_image_index + 1) % len(self.images[self.current_direction])
            self.image = self.images[self.current_direction][self.current_image_index]
            self.image = pygame.transform.scale(self.image, (350, 350))
            self.animation_counter = 0

    def move_left(self):
        self.current_direction = 'gauche'
        self.position[0] -= self.speed
        self.update_image()

    def move_right(self):
        self.current_direction = 'droite'
        self.position[0] += self.speed
        self.update_image()

    def move_up(self):
        self.current_direction = 'dos'
        self.position[1] -= self.speed
        self.update_image()

    def move_down(self):
        self.current_direction = 'face'
        self.position[1] += self.speed
        self.update_image()

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def update_walk_images(self, new_images):
        self.images = new_images
        self.current_image_index = 0
        self.image = self.images[self.current_direction][self.current_image_index]
        self.image = pygame.transform.scale(self.image, (350, 350))

    #-----------------------------------------------------------------------------------------------------------------------

    def save_location(self):
        self.old_position = self.position.copy()

    #-----------------------------------------------------------------------------------------------------------------------

    def get_image(self, x, y):
        """Get a specific image of a spreadsheet in function of the givens x and y."""
        image = pygame.Surface([30, 40])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 30, 40))
        return image

    #-----------------------------------------------------------------------------------------------------------------------

    def add_to_inventory(self, item):
        self.inventory.append(item)

    #-----------------------------------------------------------------------------------------------------------------------

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    #-----------------------------------------------------------------------------------------------------------------------

    def check_inventory(self, item):
        for object in self.inventory:
            if object == item:
                return True
        return False
