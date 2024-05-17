import pygame
import pytmx
import pyscroll
import sys
import random
from player import Player
from carrot import Carrot
from cow import Cow
from knife import Knife
from trap import Trap

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

        # Add obstacles to a list of obstacles
        self.water = []

        for obj in tmx_data.objects:
            if obj.type == 'water':
                self.water.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Add the player to the corresponding layer to be display on
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)
        self.group.add(self.player)

        #Initialize carrots
        self.carrot_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=2)

        # Initialize cows
        self.cow_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

        # Initialize knife
        self.knife_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

        # Initialize knife
        self.trap_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

        # Detect sand layer
        self.sand_matrix = tmx_data.get_layer_by_name("sand").data

        # ======================================= FLAGS ======================================
        self.interaction_carrot = False
        self.interaction_cow = False
        self.interaction_knife = False
        self.interaction_trap = False
        self.Traps_exist = False
        self.Carrots_exist = False
        self.Cows_exist = False
        self.Knifes_exist = False
        self.knifeflag=False
        
        self.interaction_water = False

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
        i = (y // taille_case)
        j = (x // taille_case)
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

        # Display time
        current_time = pygame.time.get_ticks() // 1000  # Convert milliseconds to seconds
        font = pygame.font.Font(None, 36)
        time_text = font.render(f"Time: {current_time}", True, (0, 0, 0))
        self.screen.blit(time_text, (800, 10))  # Display at (10, 10) on the screen

        # Update the display
        pygame.display.flip()

#-----------------------------------------------------------------------------------------------------------------------

    def handle_input(self):
        """
        Link keyboard actions to move the character with the corresponding functions
        :return: void
        """

        if self.pressed[pygame.K_UP]:
            self.player.move_up()
        elif self.pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif self.pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif self.pressed[pygame.K_RIGHT]:
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

    def collisions_water(self):

        # Necessary to update the position of the character in case of collision
        self.group.update()

        # if collision go back to old_position. collidelist() compare the self.player.feet rectangle and the self.walls one
        if self.player.feet.collidelist(self.water) > -1:
            self.player.life -= 0.5
            self.player.image = pygame.image.load('tiled/drowning_character.png')
            self.player.image = pygame.transform.scale(self.player.image, (40, 40))
            self.interaction_water = True

        else:
            if self.interaction_water:
                self.player.sprite_sheet = pygame.image.load('tiled/aventurer_character(2).png')
                self.player.image = self.player.get_image(364, 1065)
                self.player.image.set_colorkey([0, 0, 0])
                self.interaction_water = False


#-----------------------------------------------------------------------------------------------------------------------

    def spawn_item(self, Nbr, item):
        exist_attr = f"{item.capitalize()}s_exist"
        print(exist_attr)
        group = getattr(self, f"{item}_group")
        obj_class = globals()[item.capitalize()]  # Récupère la classe Cow ou Carrot en fonction de l'argument 'item'

        if not getattr(self, exist_attr):
            for _ in range(Nbr):
                while True:
                    x = random.randint(0, len(self.sand_matrix) * 16) - 1
                    y = random.randint(0, len(self.sand_matrix) * 16) - 1
                    x_m, y_m = self.game_to_matrix_position(x, y)
                    rect = pygame.Rect(x, y, 20, 20)
                    if not any(rect.colliderect(wall) for wall in self.walls) and self.sand_matrix[x_m][y_m] > 0:
                        break

                new_item = obj_class(x, y)
                group.add(new_item)
                setattr(self, exist_attr, True)
                print(f"{item}s displayed")
            group.update()

#-----------------------------------------------------------------------------------------------------------------------

    def update_item(self, life_change, item):

        interaction = f"interaction_{item}"
        group = getattr(self, f"{item}_group")
        if getattr(self, interaction):
            if item == "trap":
                self.interaction_trap = False
                self.player.life = 0
                return
            for item_obj in group:
                while True:
                    x = random.randint(0, len(self.sand_matrix) * 16) - 1
                    y = random.randint(0, len(self.sand_matrix) * 16) - 1
                    x_m, y_m = self.game_to_matrix_position(x, y)
                    rect = pygame.Rect(x, y, 20, 20)
                    if not any(rect.colliderect(wall) for wall in self.walls) and self.sand_matrix[x_m][y_m] > 0:
                        break
                if item=="knife":
                    if not self.knifeflag:
                        item_obj.respawn(2000, 2000)
                else:
                    item_obj.respawn(x,y)
                break
            setattr(self, interaction, False)
            self.player.life += life_change

            if item == "cow":
                print("im in cow")
                self.player.remove_from_inventory("knife")
                self.player.sprite_sheet = pygame.image.load('tiled/aventurer_character(2).png')
                self.player.image = self.player.get_image(364, 1065)
                self.player.image.set_colorkey([0, 0, 0])

            if item == "knife":
                print("pat",self.player.image)
                self.player.image = pygame.image.load('tiled/personnage_couteau.png')
                self.player.image = pygame.transform.scale(self.player.image, (40, 40))
                self.player.add_to_inventory("knife")
            
#-----------------------------------------------------------------------------------------------------------------------

    def draw_item(self, item):
        # Dessinez chaque élément dans le groupe de sprites sur la surface de jeu
        group = getattr(self, f"{item}_group")
        for obj in group:
            self.group.add(obj)

#-----------------------------------------------------------------------------------------------------------------------

    def collision_item(self, item, key):
        # Mettre à jour la position du personnage en cas de collision
        self.group.update()
        for obj in getattr(self, f"{item}_group"):
            if item == "cow":
                if obj.rect.colliderect(self.player.rect) and self.pressed[key] and self.player.check_inventory("knife"):
                    setattr(self, f"interaction_{item}", True)
                    for item_obj in getattr(self, "knife_group"):
                        while True:
                            x = random.randint(0, len(self.sand_matrix) * 16) - 1
                            y = random.randint(0, len(self.sand_matrix) * 16) - 1
                            x_m, y_m = self.game_to_matrix_position(x, y)
                            rect = pygame.Rect(x, y, 20, 20)
                            if not any(rect.colliderect(wall) for wall in self.walls) and self.sand_matrix[x_m][y_m] > 0:
                                break
                    item_obj.respawn(x,y)
                    return obj
                
            elif item == "trap":
                if obj.rect.colliderect(self.player.feet):
                    setattr(self, f"interaction_{item}", True)
                    return obj
                
            else:
                if obj.rect.colliderect(self.player.rect) and self.pressed[key]:
                    setattr(self, f"interaction_{item}", True)
                    return obj

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
            self.pressed = pygame.key.get_pressed()

            self.player.save_location()
            self.handle_input()
            self.collisions()
            self.collisions_water()
            self.player.update()
            self.player.life_update()
            self.update_screen()

            # Check if player's life is zero
            if self.player.life == 0:
                self.game_over()

            # Carrots
            if not self.carrot_group:
                self.spawn_item(1, "carrot")
            self.draw_item("carrot")
            self.collision_item("carrot", pygame.K_SPACE)  # carrots collision
            self.update_item(5, "carrot")  # carrots update after collision
            pygame.display.flip()

            # Cows
            if not self.cow_group:
                self.spawn_item(1, "cow")
            self.draw_item("cow")
            self.collision_item("cow", pygame.K_c)  # cows collision
            self.update_item(20, "cow")  # cow update after collision
            pygame.display.flip()

            # Knife
            if not self.knife_group:
                self.spawn_item(1, "knife")
            self.draw_item("knife")
            self.collision_item("knife", pygame.K_k)
            self.update_item(0, "knife")
            pygame.display.flip()

            # Trap
            if not self.trap_group:
                self.spawn_item(3, "trap")
            self.draw_item("trap")
            self.collision_item("trap", None)
            self.update_item(0, "trap")
            pygame.display.flip()

            # tick() used to control the number of time the code go through the while loop every seconds - 120 FPS
            clock.tick(120)
        pygame.quit()
