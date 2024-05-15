import pygame
import pytmx
import pyscroll
from player import Player
import sys
from carrot import Carrot
import random
import time

#-----------------------------------------------------------------------------------------------------------------------

class Game:
    """
    Creation of the Game class which is used to define the environment such as the character and the map itself.
    """

    def __init__(self):
        
        #Initialize the map of size 900pixels and 600pixels with title "Survivor Simulator"
        self.width = 900
        self.heigth = 600
        self.screen = pygame.display.set_mode((self.width, self.heigth))
        pygame.display.set_caption("Survivor Simulator")
        tmx_data = pytmx.util_pygame.load_pygame('tiled/Island_case/first_level_map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        # Initialize UI elements
        self.initialize_lifebar()

        # Initialize character and get its initial position
        player_position = tmx_data.get_object_by_name('Spawn_character')
        self.player = Player(player_position.x, player_position.y)
        self.map_layer.zoom = 2

        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, (self.width, self.heigth))


        # Add obstacles to a list of obstacles
        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == 'collision' or obj.type =='obstacle':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=2)
        self.group.add(self.player)
        
        #Initialize carrots

        self.carrot_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)
       
        # ======================================= FLAGS ======================================
        self.interaction_carotte = False
        self.Carrots_exist = False

    def initialize_lifebar(self):
        """
        Initialize the life bar and heart image.
        """
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

#-----------------------------------------------------------------------------------------------------------------------

    def handle_input(self):
        """
        Link keyboard actions to move the character with the corresponding functions
        :return: void
        """
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
        if pressed[pygame.K_DOWN]:
            self.player.move_down()
        if pressed[pygame.K_LEFT]:
            self.player.move_left()
        if pressed[pygame.K_RIGHT]:
            self.player.move_right()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

#-----------------------------------------------------------------------------------------------------------------------


    def update_screen(self):
        """
        Update the game screen.
        """
        # Camera centered on the character
        self.group.center(self.player.rect.center)

        # Draw the map and player
        self.group.draw(self.screen)

        # Update life bar
        life_percentage = self.player.life / 100
        self.lifebar_inner_rect.width = int(self.lifebar_width * life_percentage - 2)
        self.lifebar_inner_rect.left = self.lifebar_outer_rect.left + 2

        # Draw outer life bar
        pygame.draw.rect(self.screen, (0, 0, 0), self.lifebar_outer_rect, 2)

        # Draw inner life bar
        pygame.draw.rect(self.screen, self.lifebar_color, self.lifebar_inner_rect)

        # Draw heart image
        self.screen.blit(self.heart_image, self.heart_rect)

        # Draw "Eat or Die" text
        text_surface = self.font.render("Eat or Die", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.lifebar_outer_rect.centerx, self.lifebar_outer_rect.centery))
        self.screen.blit(text_surface, text_rect)

        # Update the display
        pygame.display.flip()
        
#-----------------------------------------------------------------------------------------------------------------------

    def collisions(self):

        # Necessary to update the position of the character in case of collision
        self.group.update()

        # If collision, go back to old_position. collidelist() compares the self.player.feet rectangle and the self.walls one
        if self.player.feet.collidelist(self.walls) > -1:
            self.player.move_back()


#-----------------------------------------------------------------------------------------------------------------------

# Spawn pas parfait, il y a toujours des carrottes dans l'eau mais je capte pas pk /:    

    def spawn_carrot(self, NbOfCarrots):
        if not self.Carrots_exist:
            for _ in range(NbOfCarrots):
                # Randomly generate carrot position until it's not colliding with any wall
                while True:
                    x = random.randint(0, self.width - 20)
                    y = random.randint(0, self.heigth - 20)
                    carrot_rect = pygame.Rect(x, y, 20, 20)
                    if not any(carrot_rect.colliderect(wall) for wall in self.walls):
                        break
    
                carrot = Carrot(x, y)
                self.carrot_group.add(carrot)
            self.carrot_group.update()
    
            print("carrots displayed")
            self.Carrots_exist = True


#-----------------------------------------------------------------------------------------------------------------------

    def update_carrots(self):
        self.carrot_group.update()
        if self.interaction_carotte:
            time.sleep(3)
            for carrot in self.carrot_group.sprites():
                carrot.respawn(self.width, self.heigth)
            self.interaction_carotte = False

#-----------------------------------------------------------------------------------------------------------------------

    def draw_carrots(self):
        # Dessinez chaque carotte dans le groupe de sprites sur la surface de jeu
        for carrot in self.carrot_group:
            self.group.add(carrot)

#-----------------------------------------------------------------------------------------------------------------------   

    def game_over(self):
        """
        Function to display game over message and quit the game
        """
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()
        pygame.time.delay(3000)  # Pause for 3 seconds before quitting
        pygame.quit()
        sys.exit()    

#-----------------------------------------------------------------------------------------------------------------------

    def run(self):
        """
        While running loop to call all the functions until the user quit the game window.
        """
        clock = pygame.time.Clock()
        running = True

        while running:
            self.player.save_location()
            self.handle_input()
            self.collisions()
            self.player.update()
            self.player.life_update() # Update player's life
            self.update_screen()  # Update the game screen
            if self.player.life <= 0: # Check if player's life is zero
                self.game_over()
            # Carrots
            self.spawn_carrot(5)
            self.update_carrots()
            self.draw_carrots()
            pygame.display.flip()
            clock.tick(120)  # tick() used to control the number of times the code goes through the while loop every second - 120 FPS
        pygame.quit()

