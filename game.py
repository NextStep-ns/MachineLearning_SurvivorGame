import pygame
import pytmx
import pyscroll
import sys
import random
import time
import xml.etree.ElementTree as ET
from player import Player
from carrot import Carrot
from cow import Cow

#-----------------------------------------------------------------------------------------------------------------------

class Game:
    """
    Creation of the Game class which is used to define the environment such as the character and the map itself.
    """
    def __init__(self):
        # ======================================= MAP INITILISATION ======================================
        #Initialize the map of size 900pixels and 600pixels with title "Survivor Simulator"
        self.width = 900
        self.heigth = 600
        self.screen = pygame.display.set_mode((self.width, self.heigth))
        pygame.display.set_caption("Survivor Simulator")
        tmx_data = pytmx.util_pygame.load_pygame('tiled/Island_case/island_map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, (self.width, self.heigth))

        # Initialize UI elements
        self.initialize_lifebar()

        # ======================================= OBJECT INIT ======================================
        # Initialize character and get its initial position
        player_position = tmx_data.get_object_by_name('Spawn_character')
        self.player = Player(player_position.x, player_position.y)
        map_layer.zoom = 2

        # Add obstacles to a list of obstacles
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Add the player to the corresponding layer to be display on
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)
        self.group.add(self.player)

        #Initialize carrots
        self.carrot_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)

        # Initialize cows
        self.cow_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)

        # Detect sand layer
        self.sand_matrix = tmx_data.get_layer_by_name("sand").data
        print(self.sand_matrix)

        # ======================================= FLAGS ======================================
        self.interaction_carotte = False
        self.interaction_cow = False
        self.Carrots_exist = False
        self.Cows_exist = False

#-----------------------------------------------------------------------------------------------------------------------

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

    def game_to_matrix_position(self, x, y):
        """
        Convert game coordinates (x, y) to matrix indices (i, j).
        """
        taille_case = 16  # Taille d'une case de la matrice
        i = y // taille_case
        j = x // taille_case
        return i, j

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
        life_percentage = self.player.life / self.player.max_health
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
                quit()

#-----------------------------------------------------------------------------------------------------------------------

    def collisions(self):

        # Necessary to update the position of the character in case of collision
        self.group.update()

        #if collision go back to old_position. collidelist() compare the self.player.feet rectangle and the self.walls one
        if self.player.feet.collidelist(self.walls) > -1:
            self.player.move_back()

#-----------------------------------------------------------------------------------------------------------------------

    def spawn_carrot(self, NbOfCarrots):
        if not self.Carrots_exist:
            for _ in range(NbOfCarrots):
                # Randomly generate carrot position until it's not colliding with any wall
                while True:
                    x = random.randint(0, len(self.sand_matrix)*16)
                    y = random.randint(0, len(self.sand_matrix)*16)
                    x_m,y_m=self.game_to_matrix_position(x, y)
                    carrot_rect = pygame.Rect(x, y, 20, 20)
                    if not (any(carrot_rect.colliderect(wall) for wall in self.walls))and (
                            self.sand_matrix[x_m][y_m] > 0):
                        break
                carrot = Carrot(x, y)
                self.carrot_group.add(carrot)
            self.carrot_group.update()

            print("carrots displayed")
            self.Carrots_exist = True

#-----------------------------------------------------------------------------------------------------------------------

    def update_carrots(self):

        if self.interaction_carotte:
            for carrot in self.carrot_group:
                while True:
                    x = random.randint(0, len(self.sand_matrix) * 16)
                    y = random.randint(0, len(self.sand_matrix) * 16)
                    x_m, y_m = self.game_to_matrix_position(x, y)
                    carrot_rect = pygame.Rect(x, y, 20, 20)
                    if not (any(carrot_rect.colliderect(wall) for wall in self.walls)) and (
                            self.sand_matrix[x_m][y_m] > 0):
                        break
                carrot.respawn(x, y)
                break
            self.interaction_carotte = False
            self.player.life += 5

#-----------------------------------------------------------------------------------------------------------------------

    def draw_carrots(self):
        # Dessinez chaque carotte dans le groupe de sprites sur la surface de jeu
        for carrot in self.carrot_group:
            self.group.add(carrot)

#-----------------------------------------------------------------------------------------------------------------------

    def collisions_carrot(self):

        # Necessary to update the position of the character in case of collision
        self.group.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                for carrot in self.carrot_group:
                    if carrot.rect.colliderect(self.player.rect):
                        self.interaction_carotte = True
                        return carrot

#-----------------------------------------------------------------------------------------------------------------------

    def spawn_cow(self, NbOfCows):
        if not self.Cows_exist:
            for _ in range(NbOfCows):
                # Randomly generate carrot position until it's not colliding with any wall
                while True:
                    x = random.randint(0, len(self.sand_matrix) * 16)
                    y = random.randint(0, len(self.sand_matrix) * 16)
                    x_m, y_m = self.game_to_matrix_position(x, y)
                    rect = pygame.Rect(x, y, 20, 20)
                    if not (any(rect.colliderect(wall) for wall in self.walls)) and (
                            self.sand_matrix[x_m][y_m] > 0):
                        break
                cow = Cow(x, y)
                self.cow_group.add(cow)
            self.cow_group.update()

            print("cows displayed")
            self.Cows_exist = True

#-----------------------------------------------------------------------------------------------------------------------

    def update_cows(self):

        if self.interaction_cow:
            for cow in self.cow_group:
                while True:
                    x = random.randint(0, len(self.sand_matrix) * 16)
                    y = random.randint(0, len(self.sand_matrix) * 16)
                    x_m, y_m = self.game_to_matrix_position(x, y)
                    rect = pygame.Rect(x, y, 20, 20)
                    if not (any(rect.colliderect(wall) for wall in self.walls))and (
                            self.sand_matrix[x_m][y_m] > 0):
                        break
                cow.respawn(x, y)
                break
            self.interaction_cow = False
            self.player.life += 20

#-----------------------------------------------------------------------------------------------------------------------

    def draw_cows(self):
        # Dessinez chaque carotte dans le groupe de sprites sur la surface de jeu
        for cow in self.cow_group:
            self.group.add(cow)

#-----------------------------------------------------------------------------------------------------------------------

    def collisions_cow(self):

        # Necessary to update the position of the character in case of collision
        self.group.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                for cow in self.cow_group:
                    if cow.rect.colliderect(self.player.rect):
                        self.interaction_cow = True
                        return cow

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
        :return: void
        """
        clock = pygame.time.Clock()
        running = True

        while running:
            self.player.save_location()
            self.handle_input()
            self.collisions()
            self.player.update()
            self.player.life_update()
            self.update_screen()

            # Check if player's life is zero
            if self.player.life <= 0:
                self.game_over()

            # Carrots
            self.spawn_carrot(1)
            self.draw_carrots()
            self.collisions_carrot() # carrots collision
            self.update_carrots()  # carrots update after collision

            # Cows
            self.spawn_cow(1)
            self.draw_cows()
            self.collisions_cow()  # cows collision
            self.update_cows()  # cow update after collision

            pygame.display.flip()

            # tick() used to control the number of time the code go through the while loop every seconds - 120 FPS
            clock.tick(240)
        pygame.quit()
