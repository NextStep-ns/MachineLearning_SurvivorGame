import pygame

#-----------------------------------------------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):

    def __init__(self,x ,y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('tiled/aventurer_character(2).png')

        # Get a specific image of the spreadsheet
        self.image = self.get_image(364, 1065)

        # Transparency color set to black
        self.image.set_colorkey([0,0,0])

        # Create a rectangle around the character for collisions
        self.rect = self.image.get_rect()
        self.position = [x,y]
        print(self.position)

        self.speed = 1

        # Create a rectangle around the character's feet. Initialize at (0,0) that is topleft corner, the width and height
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.3, 12)

        # Keep in memory the old character position in case of collision
        self.old_position = self.position.copy()

        #HP of the player
        self.life=100
        self.max_health = 100

        # ======================================= LIFE BAR ======================================
        # Initialize the life bar
        self.lifebar_width = 200
        self.lifebar_height = 20
        self.lifebar_outer_rect = pygame.Rect(10, 10, self.lifebar_width, self.lifebar_height)
        self.lifebar_inner_rect = pygame.Rect(self.lifebar_outer_rect.left, self.lifebar_outer_rect.top + 2, 0,
                                              self.lifebar_height - 4)
        self.lifebar_color = (255, 0, 0)  # Red color

        # Load heart image
        self.heart_image = pygame.image.load('tiled/heart_lifebar.png')
        self.heart_height = self.lifebar_height + 10
        self.heart_image = pygame.transform.scale(self.heart_image, (self.heart_height, self.heart_height))
        self.heart_rect = self.heart_image.get_rect()
        self.heart_rect.topleft = (self.lifebar_outer_rect.left - 10, self.lifebar_outer_rect.top - 6)

        # Initialize the font
        self.font = pygame.font.Font(None, 36)

        # Initialize last update time
        self.last_update_time = pygame.time.get_ticks()

#-----------------------------------------------------------------------------------------------------------------------

    def save_location(self):
        """
        Keep in memory the old character position in case of collision
        :return: void
        """
        self.old_position = self.position.copy()

#-----------------------------------------------------------------------------------------------------------------------

    def move_right(self):
        self.position[0] += self.speed
    def move_left(self):
        self.position[0] -= self.speed
    def move_up(self):
        self.position[1] -= self.speed
    def move_down(self):
        self.position[1] += self.speed

#-----------------------------------------------------------------------------------------------------------------------

    def update(self):

        # Topleft corner of the rectange that surrounds the character
        self.rect.topleft = self.position

        #Bottom middle of the feet rectangle to match the position of the rect
        self.feet.midbottom = self.rect.midbottom

#-----------------------------------------------------------------------------------------------------------------------

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

#-----------------------------------------------------------------------------------------------------------------------

    def get_image(self, x, y):
        """
        Get a specific image of a spreadsheet in fucntion of the givens x and y
        :param x: x position of the desired image
        :param y: y position of the desired image
        :return: desired image
        """
        image = pygame.Surface([30,40])
        image.blit(self.sprite_sheet, (0,0), (x,y,30,40))
        return image

#-----------------------------------------------------------------------------------------------------------------------

    def life_evolution(self, change):
        """
        Method to increase or decrease player's life
        :param change: The amount by which the life should be changed
        :return: void
        """
        self.life += change
        if self.life > 100:
            self.life = 100
        elif self.life < 0:
            self.life = 0

#-----------------------------------------------------------------------------------------------------------------------

    def lifebar(self, group, screen):
        # Calculate elapsed time since last update
        now = pygame.time.get_ticks()
        elapsed_time = now - self.last_update_time

        # If 1 second has passed, decrease player's life by 1
        if elapsed_time >= 1000:
            self.life_evolution(-20)
            self.last_update_time = now

        # Update life bar
        life_percentage = self.life / self.max_health
        self.lifebar_inner_rect.width = int(self.lifebar_width * life_percentage - 2)
        self.lifebar_inner_rect.left = self.lifebar_outer_rect.left + 2

        # Display the different elements
        group.draw(screen)

        # Draw outer life bar
        pygame.draw.rect(screen, (0, 0, 0), self.lifebar_outer_rect, 2)

        # Draw inner life bar
        pygame.draw.rect(screen, self.lifebar_color, self.lifebar_inner_rect)

        screen.blit(self.heart_image, self.heart_rect)

        # Draw "Eat or Die" text
        text_surface = self.font.render("Eat or Die", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.lifebar_outer_rect.centerx, self.lifebar_outer_rect.centery))
        screen.blit(text_surface, text_rect)

