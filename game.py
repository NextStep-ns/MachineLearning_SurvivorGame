import pygame
import pytmx
import pyscroll
import sys
import random
from enum import Enum
from player import Player
from carrot import Carrot
from cow import Cow
from knife import Knife
from trap import Trap
import numpy as np

#-----------------------------------------------------------------------------------------------------------------------
class ActionMouvement(Enum):
    STAY=0
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    INTERACT = 5

SPEED = 360
SLOW_SPEED = 200
RED =(255,0,0)
GREY = (100,100,100)
CELL_SIZE=16

REWARD_TRAP = 0
REWARD_CARROT = 10
REWARD_KNIFE = 8
REWARD_COW = 40
REWARD_TIME = 0
#REWARD_DEAD = -100

BONUS_CARROT=25
BONUS_COW=100
BONUS_KNIFE=0

#-----------------------------------------------------------------------------------------------------------------------

class GameAI:
    """
    Creation of the Game class which is used to define the environment such as the character and the map itself.
    """
    def __init__(self):
        # ======================================= MAP INITILISATION ======================================
        #Initialize the map of size 900pixels and 600pixels with title "Survivor Simulator"
        self.width = 900
        self.heigth = 600
        pygame.init()
        self.font = pygame.font.Font('arial.ttf', 25)
        self.screen = pygame.display.set_mode((self.width, self.heigth))
        pygame.display.set_caption("Survivor Simulator")
        self.tmx_data = pytmx.util_pygame.load_pygame('tiled/Island_case/island_map.tmx')
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, (self.width, self.heigth))
        self.clock = pygame.time.Clock()
        self.reset()
        
    def reset(self):

        self.knife_holding_duration = 0
        self.start_ticks = pygame.time.get_ticks()
        self.frame_iteration=0
        # Initialize UI elements
        self.initialize_lifebar()

        # ======================================= OBJECT INIT ======================================
        # Initialize character and get its initial position
        player_position = self.tmx_data.get_object_by_name('Spawn_character')
        self.player = Player(player_position.x, player_position.y)
        self.map_layer.zoom = 1.2

        # Add obstacles to a list of obstacles
        self.walls = []

        for obj in self.tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Add obstacles to a list of obstacles
        self.water = []

        for obj in self.tmx_data.objects:
            if obj.type == 'water':
                self.water.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Add the player to the corresponding layer to be display on
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=2)
        self.group.add(self.player)

        #Initialize carrots
        self.carrot_group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=2)
        self.n_carrots=0

        # Initialize cows
        self.cow_group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)
        self.n_cows=0

        # Initialize knife
        self.knife_group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)
        self.n_knife = 0

        # Initialize knife
        self.trap_group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)

        # Detect sand layer
        self.sand_matrix = self.tmx_data.get_layer_by_name("sand").data

        # ======================================= FLAGS ======================================
        self.interaction_carrot = False
        self.interaction_cow = False
        self.interaction_knife = False
        self.interaction_trap = False
        self.Traps_exist = False
        self.Carrots_exist = False
        self.Cows_exist = False
        self.Knifes_exist = False
        """
        if not self.trap_group:
            self.spawn_item(1, "trap")"""

        if not self.cow_group:
            self.spawn_item(1, "cow")

        if not self.knife_group:
            self.spawn_item(1, "knife")

        if not self.carrot_group:
            self.spawn_item(1, "carrot")

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

#-----------------------------------------------------------------------------------------------------------------------

    def game_to_matrix_position(self, x, y):
        """
        Convert game coordinates (x, y) to matrix indices (i, j).
        """
        taille_case = CELL_SIZE  # Taille d'une case de la matrice
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
        self.current_time = (pygame.time.get_ticks()-self.start_ticks) // 1000  # Convert milliseconds to seconds
        time_text = self.font.render(f"Time: {self.current_time}", True, (0, 0, 0))
        self.screen.blit(time_text, (0, 50))  # Display at (0, 50) on the screen
        carrots_text = self.font.render(f"Carrots: {self.n_carrots}", True, (0, 0, 0))
        self.screen.blit(carrots_text, (0, 75))  # Display at (0, 50) on the screen
        cows_text = self.font.render(f"Cows: {self.n_cows}", True, (0, 0, 0))
        self.screen.blit(cows_text, (0, 100))  # Display at (0, 50) on the screen
        k_text = self.font.render(f"Cows: {self.n_cows}", True, (0, 0, 0))
        self.screen.blit(k_text, (0, 125))  # Display at (0, 50) on the screen
        game_text = self.font.render(f"Game: {self.n_games}", True, (0, 0, 0))
        self.screen.blit(game_text, (0, 150))  # Display at (0, 50) on the screen

        # Update the display
        pygame.display.flip()

#-----------------------------------------------------------------------------------------------------------------------

    def handle_input(self,action):
        """
        Link Machine learning actions to move the character with the corresponding functions
        :return: void
        """
        
        clock_wise = [ActionMouvement.RIGHT, ActionMouvement.DOWN, ActionMouvement.LEFT, ActionMouvement.UP,ActionMouvement.INTERACT]

        if np.array_equal(action, [1, 0, 0, 0]):
            new_dir = clock_wise[0] # GO RIGHT
            #print('RIGHT')
            self.player.move_right()
        
        if np.array_equal(action, [0, 1, 0, 0]):
            new_dir = clock_wise[1] # GO DOWN
            #print('DOWN')
            self.player.move_down()

        if np.array_equal(action, [0, 0, 1, 0]):
            new_dir = clock_wise[2] # GO LEFT
            #print('LEFT')
            self.player.move_left()

        if np.array_equal(action, [0, 0, 0, 1]):
            new_dir = clock_wise[3] # GO UP
            #print('UP')
            self.player.move_up()

        """if np.array_equal(action, [ 0, 0, 0, 0, 1]):
            new_dir = clock_wise[4] # INTERACT
            self.reward+=0
            print('INTERACT')"""

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

    def collisions_water(self,dir=None):

        # Necessary to update the position of the character in case of collision
        self.group.update()

        # if collision go back to old_position. collidelist() compare the self.player.feet rectangle and the self.walls one
        if self.player.feet.collidelist(self.water) > -1:
            self.player.life =-500
            self.player.image = pygame.image.load('tiled/drowning_character.png')
            self.player.image = pygame.transform.scale(self.player.image, (40, 40))
            self.reward -= 100
            return True

        else:
            self.player.sprite_sheet = pygame.image.load('tiled/aventurer_character(2).png')
            self.player.image = self.player.get_image(364, 1065)
            self.player.image.set_colorkey([0, 0, 0])

#-----------------------------------------------------------------------------------------------------------------------

    def is_collision(self,dir=None):
        # Necessary to update the position of the character in case of collision
        self.group.update()
        self.sand_array=np.array(self.sand_matrix)
        posx,posy=self.game_to_matrix_position(self.player.feet.center[0],self.player.feet.center[1])
        if posx>48:
            posx=48
        if posx<1:
            posx=1
        if posy>48:
            posy=48
        if posy<1:
            posy=1
        
        pos=[posx,posy]
        if dir==0:
            cell=[pos[0]+1,pos[1]]
        elif dir==1:
            cell=[pos[0],pos[1]+1]
        elif dir==2:
            cell=[pos[0]-1,pos[1]]
        elif dir==3:
            cell=[pos[0],pos[1]-1]

        if self.sand_array[int(cell[0]),int(cell[1])]==0:
            print("true")
            return True
        else:
            return False

#-----------------------------------------------------------------------------------------------------------------------

    def where_is_carrot(self,dir=None):
        carrot_list = list(self.carrot_group)
        carrot = carrot_list[0]
        carrot_posx,carrot_posy=carrot.x,carrot.y
        player_posx,player_posy=self.player.feet.center[0],self.player.feet.center[1]

        if dir==0:
            self.right=player_posx+CELL_SIZE<carrot_posx
            return self.right
        elif dir==1:
            self.down=player_posy+CELL_SIZE<carrot_posy
            return self.down
        elif dir==2:
            self.left = carrot_posx< player_posx-CELL_SIZE
            return self.left
        elif dir==3:
            self.up=carrot_posy< player_posy-CELL_SIZE
            return self.up

#-----------------------------------------------------------------------------------------------------------------------

    def where_is_cow(self, dir=None):
        cow_list = list(self.cow_group)
        cow = cow_list[0]
        cow_posx, cow_posy = cow.x, cow.y
        player_posx, player_posy = self.player.feet.center[0], self.player.feet.center[1]

        if dir == 0:
            self.right = player_posx + CELL_SIZE  < cow_posx
            return self.right
        elif dir == 1:
            self.down = player_posy + CELL_SIZE  < cow_posy
            return self.down
        elif dir == 2:
            self.left = cow_posx < player_posx - CELL_SIZE
            return self.left
        elif dir == 3:
            self.up = cow_posy < player_posy - CELL_SIZE
            return self.up

#-----------------------------------------------------------------------------------------------------------------------

    def where_is_knife(self, dir=None):
        knife_list = list(self.knife_group)
        knife = knife_list[0]
        knife_posx, knife_posy = knife.x, knife.y
        player_posx, player_posy = self.player.feet.center[0], self.player.feet.center[1]

        if dir == 0:
            self.right = player_posx + CELL_SIZE  < knife_posx
            return self.right
        elif dir == 1:
            self.down = player_posy + CELL_SIZE < knife_posy
            return self.down
        elif dir == 2:
            self.left = knife_posx < player_posx - CELL_SIZE
            return self.left
        elif dir == 3:
            self.up = knife_posy < player_posy - CELL_SIZE
            return self.up

        # -----------------------------------------------------------------------------------------------------------------------

    """def where_is_item(self,  group_, dir=None):
        list_ = list(group_)
        item = list_[0]
        item_posx, item_posy = item.x, item.y
        player_posx, player_posy = self.player.feet.center[0], self.player.feet.center[1]

        if dir == 0:
            self.right = player_posx + CELL_SIZE / 2 < item_posx
            return self.right
        elif dir == 1:
            self.down = player_posy + CELL_SIZE / 2 < item_posy
            return self.down
        elif dir == 2:
            self.left = item_posx < player_posx - CELL_SIZE / 2
            return self.left
        elif dir == 3:
            self.up = item_posy < player_posy - CELL_SIZE / 2
            return self.up"""

    #-----------------------------------------------------------------------------------------------------------------------

    def spawn_item(self, Nbr, item):
        exist_attr = f"{item.capitalize()}s_exist"
        group = getattr(self, f"{item}_group")
        obj_class = globals()[item.capitalize()]  # Récupère la classe Cow ou Carrot en fonction de l'argument 'item'

        if not getattr(self, exist_attr):
            for _ in range(Nbr):
                while True:
                    
                    x = random.randint(0, len(self.sand_matrix) * CELL_SIZE) - 1
                    y = random.randint(0, len(self.sand_matrix) * CELL_SIZE) - 1

                    x_m, y_m = self.game_to_matrix_position(x, y)
                    rect = pygame.Rect(x, y, 20, 20)
                    if not any(rect.colliderect(wall) for wall in self.walls) and self.sand_matrix[x_m][y_m] > 0:
                        break

                new_item = obj_class(x, y)
                group.add(new_item)
                setattr(self, exist_attr, True)
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
                    x = random.randint(0, len(self.sand_matrix) * CELL_SIZE) - 1
                    y = random.randint(0, len(self.sand_matrix) * CELL_SIZE) - 1
                    
                    x_m, y_m = self.game_to_matrix_position(x, y)
                    rect = pygame.Rect(x, y, 20, 20)
                    if not any(rect.colliderect(wall) for wall in self.walls) and self.sand_matrix[x_m][y_m] > 0:
                        break
                item_obj.respawn(x, y)
                break
            setattr(self, interaction, False)
            self.player.life += life_change

            if item == "cow":
                self.player.sprite_sheet = pygame.image.load('tiled/aventurer_character(2).png')
                self.player.image = self.player.get_image(364, 1065)
                self.player.image.set_colorkey([0, 0, 0])
                #self.knife_holding_duration += self.player.holding_knife_time()
                self.player.remove_from_inventory("knife")

            if item == "knife":
                self.player.image = pygame.image.load('tiled/personnage_couteau.png')
                self.player.image = pygame.transform.scale(self.player.image, (40, 40))

#-----------------------------------------------------------------------------------------------------------------------

    def draw_item(self, item):
        # Dessinez chaque élément dans le groupe de sprites sur la surface de jeu
        group = getattr(self, f"{item}_group")
        for obj in group:
            self.group.add(obj)

#-----------------------------------------------------------------------------------------------------------------------

    def collision_item(self, item, action):
        # Mettre à jour la position du personnage en cas de collision
        self.group.update()
        for obj in getattr(self, f"{item}_group"):
            if item == "cow":
                if obj.rect.colliderect(self.player.rect):
                    if self.player.check_inventory("knife"):
                        setattr(self, f"interaction_{item}", True)
                        self.reward+=REWARD_COW
                        self.n_cows += 1
                        return obj
                    #else:
                        #self.reward-=20

            elif item == "trap":
                if obj.rect.colliderect(self.player.feet):
                    setattr(self, f"interaction_{item}", True)
                    self.reward-=REWARD_TRAP
                    self.game_over_var=True
                    return obj

            elif item == "carrot":
                if obj.rect.colliderect(self.player.feet):
                    setattr(self, f"interaction_{item}", True)
                    self.reward+=REWARD_CARROT
                    self.n_carrots+=1
                    return obj

            elif item == "knife":
                if obj.rect.colliderect(self.player.feet):
                    setattr(self, f"interaction_{item}", True)
                    self.player.add_to_inventory("knife")
                    self.reward+=REWARD_KNIFE
                    self.n_knife += 1
                    return obj

#-----------------------------------------------------------------------------------------------------------------------

    def game_over(self):
        """
        Function to display game over message and quit the game
        """
        game_over_font = pygame.font.Font('arial.ttf', 72)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()
        pygame.time.delay(3000)  # Pause for 3 seconds before quitting
        pygame.quit()
        sys.exit()

#-----------------------------------------------------------------------------------------------------------------------

    def display_carrot_pos(self):
        """
        Function to display the agents action
        """
        self.right_box = pygame.Rect(799, 499, 50, 50)
        self.down_box = pygame.Rect(748, 550, 50, 50)
        self.left_box = pygame.Rect(698, 499, 50, 50)
        self.up_box = pygame.Rect(748, 448, 50, 50)
        if self.right:
            pygame.draw.rect(self.screen,RED,self.right_box)
        else:
            pygame.draw.rect(self.screen,GREY,self.right_box)
        if self.down:
            pygame.draw.rect(self.screen,RED,self.down_box)
        else:
            pygame.draw.rect(self.screen,GREY,self.down_box)
        if self.left:
            pygame.draw.rect(self.screen,RED,self.left_box)
        else:
            pygame.draw.rect(self.screen,GREY,self.left_box)
        if self.up:
            pygame.draw.rect(self.screen,RED,self.up_box)
        else:
            pygame.draw.rect(self.screen,GREY,self.up_box)
        pygame.display.flip()
#-----------------------------------------------------------------------------------------------------------------------
    
    def play_step(self,action,n_games):
        self.n_games=n_games
        self.reward=0
        self.frame_iteration+=1
        self.game_over_var=False
        self.player.save_location()
        self.handle_input(action)
        self.display_carrot_pos()
        self.collisions()
        self.collisions_water()
        self.player.update()
        self.player.life_update()
        self.update_screen()

        # Check if player's life is zero or if iterations too long
        if self.player.life <= 0:
            self.game_over_var=True
            #self.reward += REWARD_DEAD


        # Carrots
        if not self.carrot_group:
            self.spawn_item(1, "carrot")
        self.draw_item("carrot")
        self.collision_item("carrot",action)  # carrots collision
        self.update_item(BONUS_CARROT, "carrot")  # carrots update after collision
        pygame.display.flip()

        # Cows
        if not self.cow_group:
            self.spawn_item(1, "cow")
        self.draw_item("cow")
        self.collision_item("cow", action)  # cows collision
        self.update_item(BONUS_COW, "cow")  # cow update after collision
        pygame.display.flip()

        # Knife
        if not self.knife_group:
            self.spawn_item(1, "knife")
        self.collision_item("knife", action)
        self.update_item(BONUS_KNIFE, "knife")
        self.draw_item("knife")
        pygame.display.flip()

        # Trap
        """if not self.trap_group:
            self.spawn_item(3, "trap")
        self.draw_item("trap")
        self.collision_item("trap", None)
        self.update_item(0, "trap")
        pygame.display.flip()
        """

        self.clock.tick(SPEED)
        self.reward += REWARD_TIME

        return self.reward, self.game_over_var,self.n_carrots, self.n_cows, self.n_knife