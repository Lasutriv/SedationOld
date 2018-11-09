# The main engine of the game that runs all of the menu screens, game entering/exiting, and hardware communications.
# Tanner Fry
# tefnq2@mst.edu
import character
import devLib
import engineLib
import npc
import settings

import importlib
import logging
import os
import pygame
from pygame.locals import *


class Game:
    """Class. Used to handle the creation, modification, and deletion of all game assets."""

    def __init__(self):
        """
        Constructor. Used to initialize all handlers, timers, and other variables for the game to function properly.
        """
        # Initialize the game engine with necessary variables
        self.buff_handler = object  # The handler for the main character's buffs and debuffs
        self.character = pygame.sprite.Sprite  # The main character that the player will use
        self.clock = pygame.time.Clock()  # The frames per second
        self.clock.tick(settings.FPS)
        self.engine_handler = engineLib.EngineHandler(self)
        self.level_current = 1
        self.level_directions = ''  # The directions that the character can go to get to adjacent levels
        self.level_directions_down = 'None'  # The level number of the level below the current level
        self.level_directions_left = 'None'  # The level number of the level to the left of the current level
        self.level_directions_right = 'None'  # The level number of the level to the right of the current level
        self.level_directions_up = 'None'  # The level number of the level above the current level
        self.level_matrix = []  # A 2-d matrix representing a 'map' of the level each position is a sub-level
        self.level_matrix_location = [0, 0]  # The character's current location in the level matrix
        self.level_sub_current = 1
        self.level_sub_current_total = 0  # The number of total sub-levels in the current level
        self.level_sub_total = 0  # The number of total sub-levels
        self.level_total = settings.TOTAL_LEVELS
        self.popups = []
        self.running = False
        self.screen = pygame.Surface
        self.sprites_important = pygame.sprite.Group()
        self.sprites_active_walls = pygame.sprite.Group()
        self.sprites_walls = pygame.sprite.Group()
        self.state = 'Play'
        self.texts_to_display = []
        self.window = pygame.Surface

        # Initialize environment assets
        self.type_tiles = {}  # Used to correlate in game environment assets to specific images

        # Initialize government assets (In tab order)
        self.img_gov_leader_selected = pygame.Surface
        self.img_gov_leader_selected_rect = pygame.Rect
        self.img_gov_party_selected = pygame.Surface
        self.img_gov_party_selected_rect = pygame.Rect
        self.img_gov_judge_selected = pygame.Surface
        self.img_gov_judge_selected_rect = pygame.Rect
        self.img_gov_info_selected = pygame.Surface
        self.img_gov_info_selected_rect = pygame.Rect
        self.img_gov_map_selected = pygame.Surface
        self.img_gov_map_selected_rect = pygame.Rect

        # Initialize inventory assets (In tab order)
        self.img_inv_inv_base = pygame.Surface
        self.img_inv_inv_base_rect = pygame.Rect
        self.img_inv_inv_selected = pygame.Surface
        self.img_inv_inv_selected_rect = pygame.Rect
        self.img_inv_saves_selected = pygame.Surface
        self.img_inv_saves_selected_rect = pygame.Rect
        self.img_inv_opt_selected = pygame.Surface
        self.img_inv_opt_selected_rect = pygame.Rect
        self.img_inv_feed_selected = pygame.Surface
        self.img_inv_feed_selected_rect = pygame.Rect
        self.img_inv_exit_selected = pygame.Surface
        self.img_inv_exit_selected_rect = pygame.Rect

        # Initialize npc assets
        self.npc_squishy = object

    def game_new(self, file_save_name: str, character_name='None'):
        """
        The main function to set up a new game since the engine was started. Works with loaded games too.

        @param file_save_name: the name of the file to use for the engine to start up
        @param character_name: the name of the new character that the user customized
        @return: none
        @rtype: none
        """
        try:
            # Initialize assets for new game
            pygame.display.set_caption(settings.TITLE_GAME)
            self.screen = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            self.window = pygame.display.set_mode((self.engine_handler.gather_engine_info(self, 'calculate_window')), DOUBLEBUF)
            # NOTE: Reimport all libraries for easier code change and testing
            importlib.reload(engineLib)
            self.engine_handler.reimport_all()
            self.engine_handler.init_finish()

            # Gather information
            self.engine_handler.gather_engine_info(self, 'get_levels')

            # Generate new settings file for the character to use, whether from defaults or the character save
            if character_name != 'None':
                self.engine_handler.save_new_game(character_name, file_save_name)
            else:
                self.engine_handler.load_saved_game(file_save_name)
                character_name = settings.CHAR_NAME

            # Initialize all environment assets for new game
            # NOTE: these assets had to be initialized early due to performance issues
            environment_spritesheet = engineLib.SpriteSheet(settings.DIR_SPRITES_GAME_ENVI
                                                            + '/Ground_Grass_384_432_Spritesheet.png')
            self.type_tiles = {'GL0': environment_spritesheet.get_image(0, 0, 32, 32),
                               'GL1': environment_spritesheet.get_image(0, 32, 32, 32),
                               'GL2': environment_spritesheet.get_image(0, 64, 32, 32),
                               'GL3': environment_spritesheet.get_image(0, 96, 32, 32),
                               'GL4': environment_spritesheet.get_image(0, 128, 32, 32),
                               'GL5': environment_spritesheet.get_image(0, 160, 32, 32),
                               'GL6': environment_spritesheet.get_image(0, 192, 32, 32),
                               'GM0': environment_spritesheet.get_image(32, 32, 32, 32),
                               'GM1': environment_spritesheet.get_image(64, 32, 32, 32),
                               'GM2': environment_spritesheet.get_image(96, 32, 32, 32),
                               'GM3': environment_spritesheet.get_image(128, 32, 32, 32),
                               'GM4': environment_spritesheet.get_image(160, 32, 32, 32),
                               'GM5': environment_spritesheet.get_image(192, 32, 32, 32),
                               'GM6': environment_spritesheet.get_image(224, 32, 32, 32),
                               'GT0': environment_spritesheet.get_image(32, 0, 32, 32),
                               'GT1': environment_spritesheet.get_image(64, 0, 32, 32),
                               'GT2': environment_spritesheet.get_image(96, 0, 32, 32),
                               'GT3': environment_spritesheet.get_image(128, 0, 32, 32),
                               'GT4': environment_spritesheet.get_image(160, 0, 32, 32),
                               'GT5': environment_spritesheet.get_image(192, 0, 32, 32),
                               'GT6': environment_spritesheet.get_image(224, 0, 32, 32),
                               'GR0': environment_spritesheet.get_image(256, 0, 32, 32),
                               'GR1': environment_spritesheet.get_image(256, 32, 32, 32),
                               'GR2': environment_spritesheet.get_image(256, 64, 32, 32),
                               'GR3': environment_spritesheet.get_image(256, 96, 32, 32),
                               'GR4': environment_spritesheet.get_image(256, 128, 32, 32),
                               'GR5': environment_spritesheet.get_image(256, 160, 32, 32),
                               'GR6': environment_spritesheet.get_image(256, 192, 32, 32),
                               'HL0': environment_spritesheet.get_image(96, 240, 32, 32),
                               'HL1': environment_spritesheet.get_image(96, 272, 32, 32),
                               'HL2': environment_spritesheet.get_image(96, 304, 32, 32),
                               'HL3': environment_spritesheet.get_image(96, 336, 32, 32),
                               'HL4': environment_spritesheet.get_image(96, 368, 32, 32),
                               'HL5': environment_spritesheet.get_image(96, 400, 32, 32),
                               'HT0': environment_spritesheet.get_image(0, 336, 32, 32),
                               'HT1': environment_spritesheet.get_image(32, 336, 32, 32),
                               'HT2': environment_spritesheet.get_image(64, 336, 32, 32),
                               'HT3': environment_spritesheet.get_image(128, 240, 32, 32),
                               'HT4': environment_spritesheet.get_image(160, 240, 32, 32),
                               'HT5': environment_spritesheet.get_image(224, 240, 32, 32),
                               'HT6': environment_spritesheet.get_image(288, 336, 32, 32),
                               'HT7': environment_spritesheet.get_image(320, 336, 32, 32),
                               'HT8': environment_spritesheet.get_image(352, 336, 32, 32),
                               'HR0': environment_spritesheet.get_image(256, 240, 32, 32),
                               'HR1': environment_spritesheet.get_image(256, 272, 32, 32),
                               'HR2': environment_spritesheet.get_image(256, 304, 32, 32),
                               'HR3': environment_spritesheet.get_image(256, 336, 32, 32),
                               'HR4': environment_spritesheet.get_image(352, 368, 32, 32),
                               'HR5': environment_spritesheet.get_image(352, 400, 32, 32)}

            try:
                # Initialize all sprites within each sub-level that's within current selected level
                for i in range(1, self.level_sub_total - 1):  # TODO: Fix this hard code pos
                    row_current = 0
                    path_to_level = 'Levels/Level_' + str(self.level_current) \
                                    + '/Sub_Level_' + str(i) \
                                    + '.txt'
                    # Generate the new level across the screen
                    try:
                        with open(path_to_level, 'r') as file:
                            for line in file:
                                col_current = 0
                                data_from_file = line.split(' ')
                                for data in data_from_file:
                                    self.engine_handler.generate_level_walls(self, data, col_current,
                                                                             True, row_current, i)
                                    col_current += 1
                                row_current += 1
                    except FileNotFoundError:
                        logging.error('* Error - File not found within the current level: %s %s.',
                                      self.level_current, i)
            except Exception:
                logging.error('* Error - Unexpected.')


            # Initialize the character and other character assets for new game
            self.character = character.Character(character_name, file_save_name, self,  settings.SCREEN_WIDTH / 2,
                                                 settings.SCREEN_HEIGHT / 2)
            # NOTE: Test npc, will end up using a general platform for npc and assign personalities to them
            # NOTE: so they can give specific outcomes based on the given personality
            self.npc_squishy = npc.NPCSquishy('npc_squishy', self, settings.SCREEN_WIDTH / 1.5, settings.SCREEN_HEIGHT / 2)
            self.buff_handler = character.BuffHandler(self.character, self.screen)

            # Initialize UI images for new game
            # Inventory system
            img_dir = settings.DIR_SPRITES_UI + '/Inventory'
            self.img_inv_inv_base = pygame.image.load(img_dir + '/Inventory_Base.png').convert_alpha()
            self.img_inv_inv_base_rect = self.img_inv_inv_base.get_rect()
            self.img_inv_inv_selected = pygame.image.load(img_dir + '/Inventory_Selected.png').convert_alpha()
            self.img_inv_inv_selected_rect = self.img_inv_inv_selected.get_rect()
            self.img_inv_saves_selected = pygame.image.load(img_dir + '/Saves_Selected.png').convert_alpha()
            self.img_inv_saves_selected_rect = self.img_inv_saves_selected.get_rect()
            self.img_inv_opt_selected = pygame.image.load(img_dir + '/Options_Selected.png').convert_alpha()
            self.img_inv_opt_selected_rect = self.img_inv_opt_selected.get_rect()
            self.img_inv_feed_selected = pygame.image.load(img_dir + '/Feedback_Selected.png').convert_alpha()
            self.img_inv_feed_selected_rect = self.img_inv_feed_selected.get_rect()
            self.img_inv_exit_selected = pygame.image.load(img_dir + '/Exit_Selected.png').convert_alpha()
            self.img_inv_exit_selected_rect = self.img_inv_exit_selected.get_rect()
            # Government management
            img_dir = settings.DIR_SPRITES_UI + '/Government_Management'
            img_dir_menu = img_dir + '/Main_Menu'
            img_dir_judge = img_dir + '/Judge'
            self.img_gov_menu = pygame.image.load(img_dir + '/Main_Menu/Gov_Base.png').convert_alpha()
            self.img_gov_menu_rect = self.img_gov_menu.get_rect()
            # Government leader assets
            self.img_gov_leader_selected = pygame.image.load(img_dir_menu + '/Gov_Leader_Selected.png').convert_alpha()
            self.img_gov_leader_selected_rect = self.img_gov_leader_selected.get_rect()
            # Government party assets
            self.img_gov_party_selected = pygame.image.load(img_dir_menu + '/Gov_Party_Selected.png').convert_alpha()
            self.img_gov_party_selected_rect = self.img_gov_party_selected.get_rect()
            # Government judge assets
            self.img_gov_judge_selected = pygame.image.load(img_dir_menu + '/Gov_Judge_Selected.png').convert_alpha()
            self.img_gov_judge_selected_rect = self.img_gov_judge_selected.get_rect()
            # Government info assets
            self.img_gov_info_selected = pygame.image.load(img_dir_menu + '/Gov_Information_Selected.png').convert_alpha()
            self.img_gov_info_selected_rect = self.img_gov_info_selected.get_rect()
            # Government map assets
            self.img_gov_map_selected = pygame.image.load(img_dir_menu + '/Gov_Map_Selected.png').convert_alpha()
            self.img_gov_map_selected_rect = self.img_gov_map_selected.get_rect()

            # Generate assets and start the game
            print(self.level_sub_current)
            for sprite in self.sprites_walls:

                    if sprite.level_sub == self.level_sub_current:
                        sprite.add(self.sprites_active_walls)

            # self.level_matrix.lvl = self.engine_handler.generate_level_matrix(self.engine_main)
            self.engine_handler.generate_level_matrix(self)
            self.running = True
            self.game_run()
        except Exception:
            logging.error('* Error - Unexpected.')

    def game_run(self):
        """
        The main function to run the game loop.

        @return: a game state for the menu to handle or exiting the game
        @rtype: str
        """
        try:
            while self.running:
                if self.engine_handler.state == 'Game_Run':
                    self.game_events()
                    self.game_update()
                    self.game_draw()
                # TODO: The game might need to be paused while in inventory as it
                # CONT: might be too resource intensive or handle other game objects
                # CONT: while in the inventory
                elif self.engine_handler.state == 'Game_Inventory':
                    self.game_events()
                    self.game_update()
                    self.game_draw()
                elif self.engine_handler.state == 'Game_Government_Management':
                    self.game_events()
                    self.game_update()
                    self.game_draw()
        except Exception:
            logging.error('* Error - Unexpected.')

    def game_events(self):
        """
        The main function to handle events in the game.

        @return: none
        @rtype: none
        """
        try:
            # Handle events for the character, popups, buttons, other sprites,
            for event in pygame.event.get():
                self.engine_handler.handle_events(self, event, self.character,
                                                  self.sprites_important,
                                                  self.sprites_walls)

            # Handle movements of the character
            self.character.handle_keys()

            # Check for map rotation
            self.engine_handler.check_character_close_to_exit(self, self.character)

            # Update map if switching levels or sublevels
            if self.engine_handler.screen_switch is True:
                # Remove the now old sprites from the group to display
                for sprite in self.sprites_active_walls:
                    sprite.remove(self.sprites_active_walls)
                # Figure out which sprites to display
                for sprite in self.sprites_walls:
                    if sprite.level_sub == self.level_sub_current:
                        sprite.add(self.sprites_active_walls)
                self.engine_handler.generate_level_directions()
                self.engine_handler.screen_switch = False
        except Exception:
            logging.error('* Error - Unexpected.')

    def game_update(self):
        """
        The main function to update any 'side' information.

        @return: none
        @rtype: none
        """
        try:
            # Check extra sprite information to update
            self.sprites_important.update()
            # Check popups for purging
            if len(self.popups) > 0:
                new_popups = []
                for popup in self.popups:
                    if popup.active is False:
                        pass
                    else:
                        new_popups.append(popup)
                self.popups = new_popups
        except Exception:
            logging.error('* Error - Unexpected.')

    def game_draw(self):
        """
        The main function to draw all of the information, old or new.

        @return: none
        @rtype: none
        """
        try:
            # TODO: Add backgrounds, create an object with a draw function that
            # CONT: when the screen is changed to calculate the next screen, OR we
            # CONT: could load the level's backgrounds at the beginning so that
            # CONT: there isn't any hard computation, just referencing.
            # Draw background

            # Draw level
            self.screen.fill(settings.DARK_GRAY)
            # self.game_draw_grid()

            # Draw characters, objects, and walls
            self.sprites_important.draw(self.screen)
            self.sprites_active_walls.draw(self.screen)
            # Draw other things in front of the character or on top of

            # Draw character effects
            self.buff_handler.handle_events()
            # TODO: Should the sprites be separated? Is it harder to keep track?
            # CONT: Does there need to be a function to change the sprites from
            # CONT: groups?
            # self.sprites_walls.draw(self.screen)

            # Draw UI
            self.engine_handler.draw_ui_debug(self, self.screen, self.character)
            self.engine_handler.draw_ui_game(self.screen, self.character)

            # TODO: Should the game graphics be checked before the game runs and
            # CONT: then change an engine variable to display certain graphics
            # Draw other visuals based on graphics setting...
            # self.engine_handler.check_game_graphics(self.screen, True)

            # Draw inventory system
            # TODO: FINISH INVENTORY MOCK UP
            if self.engine_handler.state == 'Game_Inventory':
                # Cycle #
                #########
                # 1. move all image types to their location
                # 2. determine which to display based on user interaction with text
                # 3. draw inventory slots, then items
                # TODO: Create a list of these to loop through to change their
                # CONT: values? Create list where the imgs are initialized maybe?
                self.img_inv_inv_base_rect.x = self.character.rect.x + self.character.rect.width / 2 - 245
                self.img_inv_inv_base_rect.y = 45
                self.img_inv_inv_selected_rect.x = self.character.rect.x + self.character.rect.width / 2 - 245
                self.img_inv_inv_selected_rect.y = 45
                self.img_inv_saves_selected_rect.x = self.character.rect.x + self.character.rect.width / 2 - 245
                self.img_inv_saves_selected_rect.y = 45
                self.img_inv_opt_selected_rect.x = self.character.rect.x + self.character.rect.width / 2 - 245
                self.img_inv_opt_selected_rect.y = 45
                self.img_inv_feed_selected_rect.x = self.character.rect.x + self.character.rect.width / 2 - 245
                self.img_inv_feed_selected_rect.y = 45
                self.img_inv_exit_selected_rect.x = self.character.rect.x + self.character.rect.width / 2 - 245
                self.img_inv_exit_selected_rect.y = 45
                # Display inventory background animation based on the state; interaction with inventory
                if self.engine_handler.state_inventory == 'Base':
                    self.screen.blit(self.img_inv_inv_base, self.img_inv_inv_base_rect)
                elif self.engine_handler.state_inventory == 'Inventory':
                    self.screen.blit(self.img_inv_inv_selected, self.img_inv_inv_selected_rect)
                elif self.engine_handler.state_inventory == 'Saves':
                    self.screen.blit(self.img_inv_saves_selected, self.img_inv_saves_selected_rect)
                elif self.engine_handler.state_inventory == 'Options':
                    self.screen.blit(self.img_inv_opt_selected, self.img_inv_opt_selected_rect)
                elif self.engine_handler.state_inventory == 'Feedback':
                    self.screen.blit(self.img_inv_feed_selected, self.img_inv_feed_selected_rect)
                elif self.engine_handler.state_inventory == 'Exit':
                    self.screen.blit(self.img_inv_exit_selected, self.img_inv_exit_selected_rect)
                # TODO: Recode somewhere so we aren't constantly creating new text
                # TODO: every frame
                tab_selected = 'Inventory'
                tab_size = 18
                tab_y = 93
                text_color = settings.BLACK
                text_selected = engineLib.GameText('Title', tab_selected, 26, text_color, self.character.rect.x
                                                   + self.character.rect.width / 2 - 59, 48, True, False)
                text_inventory = engineLib.GameText('Tab_Inventory', 'Inventory', tab_size, text_color,
                                                    self.character.rect.x + self.character.rect.width / 2 - 221,
                                                    tab_y, True, False)
                text_saves = engineLib.GameText('Tab_Saves', 'Saves', tab_size, text_color, self.character.rect.x
                                                + self.character.rect.width / 2 - 110, tab_y, True, False)
                text_options = engineLib.GameText('Tab_Options', 'Options', tab_size, text_color,
                                                  self.character.rect.x + self.character.rect.width / 2 - 25,
                                                  tab_y, True, False)
                text_feedback = engineLib.GameText('Tab_Feedback', 'Feedback', tab_size, text_color,
                                                   self.character.rect.x + self.character.rect.width / 2 + 82,
                                                   tab_y, True, False)
                text_exit = engineLib.GameText('Tab_Exit', 'Exit', tab_size, text_color, self.character.rect.x
                                               + self.character.rect.width / 2 + 195, tab_y, True, False)
                self.texts_to_display = [text_selected, text_inventory, text_saves, text_options, text_feedback, text_exit]
                # Display text
                for text in self.texts_to_display:
                    text.draw(self.screen)
                # Draw inventory slots
                x_start = self.character.rect.x + self.character.rect.width / 2 - 240
                y_start = 140
                buffer_x = 10.5
                buffer_y = 10.5
                for i in range(12):  # number of slots for items
                    x_spacing = (i * 32) + buffer_x
                    for j in range(5):
                        y_spacing = (j * 32) + buffer_y
                        pygame.draw.lines(self.screen, settings.DARK_GRAY, True,
                                          ((x_start + x_spacing, y_start + y_spacing),
                                           (x_start + x_spacing, y_start + y_spacing + 32),
                                           (x_start + x_spacing + 32, y_start + y_spacing + 32),
                                           (x_start + x_spacing + 32, y_start + y_spacing)))
                        buffer_y += 7.5
                    buffer_y = 10.5
                    buffer_x += 7.5
                buffer_x = 12
                buffer_y = 10.5
                item_count = 0
                # Display inventory items
                # TODO: Should there be a loaded dict for the inventory items so it's faster with the imgs ready? yaaa
                # TODO: Change the loop to account for x amt of items that would push the next item to the second level in
                # CONT: the inventory system.
                for item in settings.CHAR_INVENTORY:
                    img = pygame.image.load(settings.DIR_SPRITES_GAME_INV + '/' + str(item) + '.png').convert_alpha()
                    img_rect = img.get_rect()
                    x_spacing = (item_count * 32) + buffer_x
                    y_spacing = (item_count * 0 * 32) + buffer_y
                    img_rect.x, img_rect.y = (x_start + x_spacing), (y_start + y_spacing)
                    self.screen.blit(img, img_rect)
                    buffer_x += 7.5
                    item_count += 1
            elif self.engine_handler.state == 'Game_Government_Management':
                # TODO: init assets based on user interaction
                # TODO: display assets based on handled events
                # all of the government handling will be in the enginehandler.handle_events() for now but
                # should the events be handled in individual files so that there isn't a ton of
                # cross referencing?
                self.img_gov_menu_rect.x, self.img_gov_menu_rect.y = 3, 3
                self.img_gov_leader_selected_rect.x, self.img_gov_leader_selected_rect.y = 3, 3
                self.img_gov_party_selected_rect.x, self.img_gov_party_selected_rect.y = 3, 3
                self.img_gov_judge_selected_rect.x, self.img_gov_judge_selected_rect.y = 3, 3
                self.img_gov_info_selected_rect.x, self.img_gov_info_selected_rect.y = 3, 3
                self.img_gov_map_selected_rect.x, self.img_gov_map_selected_rect.y = 3, 3
                if self.engine_handler.state_governmnet is 'Default':
                    self.screen.blit(self.img_gov_menu, self.img_gov_menu_rect)
                elif self.engine_handler.state_governmnet is 'Leader':
                    self.screen.blit(self.img_gov_leader_selected, self.img_gov_leader_selected_rect)
                elif self.engine_handler.state_governmnet is 'Party':
                    self.screen.blit(self.img_gov_party_selected, self.img_gov_party_selected_rect)
                elif self.engine_handler.state_governmnet is 'Judge':
                    self.screen.blit(self.img_gov_judge_selected, self.img_gov_judge_selected_rect)
                    # Display other judge assets for user interaction and handle the events
                    # in engine handler
                elif self.engine_handler.state_governmnet is 'Information':
                    self.screen.blit(self.img_gov_info_selected, self.img_gov_info_selected_rect)
                elif self.engine_handler.state_governmnet is 'Map':
                    self.screen.blit(self.img_gov_map_selected, self.img_gov_map_selected_rect)
            # Display important popups
            for popup in self.popups:
                popup.draw(self.screen)
            # Scale screen to the size of user's specified resolution
            # TODO: This line is causing issues regarding the updating of resolutions and other settings
            pygame.transform.scale(self.screen, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), self.window)
            # Pygame draws everything that has been sent to it's display which is represented by self.screen
            pygame.display.flip()
        except Exception:
            logging.error('* Error - Unexpected.')


class MainMenu:
    """Class. Used to work with the menu and keep smooth control flow."""
    def __init__(self, engine_game: object):
        """
        Constructor. Used to initialize the menu system and incorporate the engine for the game so we can run specific
        functions including the game itself.

        @param engine_game: the engine which controls the network/functions of the game when it starts after the menu
        @type engine_game: object
        """
        # Initialize the menu with the necessities
        pygame.display.set_caption(settings.TITLE_GAME)
        self.clock = pygame.time.Clock()
        self.clock.tick(30)
        self.engine_game = engine_game
        self.engine_handler = engineLib.EngineHandler(engine_game)  # Atm pretty useless in menu
        self.menu_handler = engineLib.MenuHandler(self)
        self.running = True
        self.sprites_all = pygame.sprite.Group()
        self.state = 'Main'

        # Initializing screen
        self.screen = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.window = pygame.display.set_mode((self.engine_handler.gather_engine_info(self.engine_game,
                                                                                      'calculate_window')))
        # Initialize sample character
        self.character_sample = character.Character('Caesar', 'Caesar.py', self.engine_game, 100,
                                                    settings.SCREEN_HEIGHT / 2)
        self.character_sample.collision_sets = 'Menu'
        self.character_sample.engine_menu = self
        self.character_name = 'Caesar'  # TODO: Is this variable useless?
        # Initialize menu images and screen assets
        # Feedback
        self.feedback_save_description = ''
        self.feedback_save_title = ''
        self.feedback_save_email = ''
        self.img_computer_interact_feedback = object
        # Main Menu
        self.img_menu_bg = pygame.image.load(settings.DIR_SPRITES_UI
                                             + '/Menu/Menu_Background_Interactive_Large.png').convert_alpha()
        self.img_menu_load_bg = pygame.image.load(settings.DIR_SPRITES_UI + '/Menu/Load/'
                                                  + 'Load_Background_Wood_With_Banners_Large.png').convert_alpha()
        self.menu_blit_bg_images = []
        self.menu_blit_layer_1_images = []
        # Initializing menu animations assets
        self.menu_animations = []
        # Initializing styling attributes
        self.menu_text_bg_color = settings.TRANSPARENT
        self.menu_text_color = settings.DEEP_GRAY
        # User attributes
        self.file_load_save = ''
        # Misc attributes
        self.buttons = []
        self.popups = []

        # Initializing dev tools after all other inits
        self.engine_dev = devLib.CharacterHandler(self, self.character_sample)

    # Menu setup

    def menu_start(self):
        """
        The setup of all other assets for the menu and game later..

        @return: none
        @rtype: none
        """
        try:
            # Run loading animation
            self.menu_loading()
            # Run menu handler and the menu screens via the handler, returns a state for either starting a
            # new game, loading an existing game, or exiting the menu.
            return self.menu_screen_handler()
        except Exception:
            logging.error('* Error - Unexpected.')

    # Menu Loading

    def menu_loading(self):
        """
        This function allows the programmer to load up assets, sprites, and other data/information needed to run
        the game smoothly before playing.

        @return: none
        @rtype: none
        """
        try:
            # Load specific assets that the menu handler will use later.
            self.menu_handler.init_finish()

            # Setup and display the loading animation for the game
            imgs = []
            for i in range(1, 11):
                imgs.append(pygame.image.load(settings.DIR_SPRITES_UI + '/Loading/Sprite_Loading_960_1280_Lightning_Effect'
                                              + str(i) + '.png').convert_alpha())
            img_index = 0
            img = imgs[img_index]
            img_rect = img.get_rect()
            loading = True
            timer_imgs = 0
            timer_imgs_trigger = 7

            while loading is True:
                timer_imgs += 1
                if timer_imgs == timer_imgs_trigger:
                    img_index += 1
                    timer_imgs = 0

                    # Check for end of imgs
                    if img_index == len(imgs) - 1:
                        img_index = 0

                        loading = False
                img = imgs[img_index]
                self.screen.fill(self.menu_text_color)
                self.screen.blit(img, img_rect)
                pygame.transform.scale(self.screen, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), self.window)
                pygame.display.flip()
        except Exception:
            logging.error('* Error - Unexpected.')

    # Menu Screens

    def menu_main(self):
        """
        The main menu screen to display all of the options to the user when they load the game.

        @return: none
        @rtype: none
        """
        try:
            # Set up background
            self.menu_blit_bg_images.append(self.img_menu_bg)
            # Set up title
            self.menu_animations.append(self.menu_handler.menu_anim_title)

            # Set up sample character
            self.sprites_all.add(self.character_sample)
            # Set up buttons
            button_load = engineLib.MenuButton(self, 'Load', 'Load', 35, self.menu_text_color, self.menu_text_bg_color,
                                               settings.SCREEN_WIDTH / 2 - 42, settings.SCREEN_HEIGHT / 2 - 45, True,
                                               False, False, True)
            button_exit = engineLib.MenuButton(self, 'Exit', 'Exit', 35, self.menu_text_color, self.menu_text_bg_color,
                                               settings.SCREEN_WIDTH / 2 - 33.5, settings.SCREEN_HEIGHT / 2 + 65, True,
                                               False, False, True)
            # Set the specific buttons that should be displayed
            self.buttons = [button_load, button_exit]
        except Exception:
            logging.error('* Error - Unexpected.')

    def menu_create_character(self):
        """
        The main menu screen to display all of the different settings and attributes of their starting character before
        the game is loaded.

        @return: none
        @rtype: none
        """
        try:
            self.state = 'Create_Character'
            # / 2 - 160 - 100 --> 160 = 10px * num_of_chars_in_question, 100 = 10px * num_of_chars_in_avg_names
            button_input_char_name = engineLib.MenuInteractiveText(self, 'Input_Create_Char_Name', 'Character Name: ',
                                                                   settings.SCREEN_WIDTH / 2 - 150,
                                                                   settings.SCREEN_HEIGHT / 2 - 30, 300, width=50,
                                                                   height=25)
            button_input_file_name = engineLib.MenuInteractiveText(self, 'Input_File_Save_Name', 'Save File Name: ',
                                                                   settings.SCREEN_WIDTH / 2 - 150,
                                                                   settings.SCREEN_HEIGHT / 2, 300, width=50, height=25)
            button_submit = engineLib.MenuButton(self, 'Submit', 'Submit', 35, self.menu_text_color,
                                                 self.menu_text_bg_color, settings.SCREEN_WIDTH - 195,
                                                 settings.SCREEN_HEIGHT - 95, True, False, False, True)
            button_back = engineLib.MenuButton(self, 'Back', 'Back', 35, self.menu_text_color, self.menu_text_bg_color, 99,
                                               settings.SCREEN_HEIGHT - 95, True, False, False, True)
            # Set the specific buttons that should be displayed
            self.buttons = [button_input_char_name, button_input_file_name, button_submit, button_back]
        except Exception:
            logging.error('* Error - Unexpected.')

    def menu_load(self):
        """
        A screen picked from the main menu to load an earlier saved game file.

        @return: none
        @rtype: none
        """
        try:
            # Set up assets for display
            self.menu_blit_bg_images.append(self.img_menu_load_bg)
            self.menu_animations.append(self.menu_handler.menu_anim_banners)
            # Create navigation bar with 30px between each selection
            button_cat_saves = engineLib.MenuButton(self, 'Load_Cat_Saves', 'Saves', 25, self.menu_text_color,
                                                    self.menu_text_bg_color, 103, 24, True, True, True, True)
            button_submit = engineLib.MenuButton(self, 'Submit', 'Submit', 35, self.menu_text_color,
                                                 self.menu_text_bg_color, settings.SCREEN_WIDTH - 195,
                                                 settings.SCREEN_HEIGHT - 95, True, True, False, True)
            # Misc
            button_back = engineLib.MenuButton(self, 'Back', 'Back', 35, self.menu_text_color, self.menu_text_bg_color, 90,
                                               settings.SCREEN_HEIGHT - 95, True, False, False, True)
            # Set the specific buttons that should be displayed
            self.buttons = [button_cat_saves, button_submit, button_back]
        except Exception:
            logging.error('* Error - Unexpected.')

    def menu_options(self):
        """
        A screen picked from the main menu or the pause menu to allow the viewing and changing of many options for how
        your game runs.

        @return: none
        @rtype: none
        """
        try:
            # Create navigation bar with 30px buffer between each selection
            button_cat_controls = engineLib.MenuButton(self, 'Options_Cat_Controls', 'Controls', 25, self.menu_text_color,
                                                       self.menu_text_bg_color, 50, 28, True, False, False, True)
            button_cat_game = engineLib.MenuButton(self, 'Options_Cat_Game', 'Game', 25, self.menu_text_color,
                                                   self.menu_text_bg_color, 190, 28, True, False, False, True)
            button_cat_sound = engineLib.MenuButton(self, 'Options_Cat_Sound', 'Sound', 25, self.menu_text_color,
                                                    self.menu_text_bg_color, 274, 28, True, False, False, True)
            button_cat_video = engineLib.MenuButton(self, 'Options_Cat_Video', 'Video', 25, self.menu_text_color,
                                                    self.menu_text_bg_color, 372, 28, True, False, False, True)
            # Misc
            button_back = engineLib.MenuButton(self, 'Back', 'Back', 35, self.menu_text_color, self.menu_text_bg_color, 90,
                                               settings.SCREEN_HEIGHT - 95, True, False, False, True)
            # Set the specific buttons that should be displayed
            self.buttons = [button_cat_controls, button_cat_game, button_cat_sound, button_cat_video, button_back]
        except Exception:
            logging.error('* Error - Unexpected.')

    def menu_help(self):
        """
        A screen picked from the main menu or the pause menu to allow the viewing of controls, lore help, or other kind
        of help the user may need.

        @return: none
        @rtype: none
        """
        try:
            # Create navigation bar with 30px buffer between each selection
            button_cat_categories = engineLib.MenuButton(self, 'Help_Cat_Cat', 'Categories', 25, self.menu_text_color,
                                                         self.menu_text_bg_color, 70, 22, True, False, True, True)
            # Misc
            button_back = engineLib.MenuButton(self, 'Back', 'Back', 35, self.menu_text_color, self.menu_text_bg_color, 90,
                                               settings.SCREEN_HEIGHT - 95, True, False, False, True)
            # Set the specific buttons that should be displayed
            self.buttons = [button_cat_categories, button_back]
        except Exception:
            logging.error('* Error - Unexpected.')

    def menu_feedback(self):
        """
        A screen picked from the main menu to allow the user to give specific feedback on the game, whether it's the
        physics engine that is acting up, the character's traits or skills, or anything that might need to be sent to
        myself for error handling.

        @return: none
        @rtype: none
        """
        try:
            # TODO: Finish design and send user feedback to remasteredworks.feedback@gmail.com
            # Initialize assets for display
            self.img_computer_interact_feedback = pygame.image.load(settings.DIR_SPRITES_UI
                                                                    + '/Menu/Feedback/Computer_Screen_Large'
                                                                    + '.png').convert_alpha()
            self.menu_blit_bg_images.append(self.img_menu_bg)
            self.menu_blit_layer_1_images.append(self.img_computer_interact_feedback)
            button_input_description = engineLib.MenuInteractiveText(self, 'Input_Feedback_Description', 'Bug description:',
                                                                     110, 120, 378, width=378, height=160)
            button_back = engineLib.MenuButton(self, 'Back', 'Back', 35, self.menu_text_color, self.menu_text_bg_color, 99,
                                               settings.SCREEN_HEIGHT - 95, True, False, False, True)
            # Set the specific buttons that should be displayed
            selfbuttons = [button_input_description, button_back]
        except Exception:
            logging.error('* Error - Unexpected.')

    # Sub Menu Screens

    def menu_options_video(self):
        """
        A screen picked from the options screen of the main menu or pause menu that allows the viewing of specific
        video settings for user to modify regarding the game.

        @return: none
        @rtype: none
        """
        try:
            # Create navigation bar with 30px buffer between each selection
            button_cat_controls = engineLib.MenuButton(self, 'Options_Cat_Controls', 'Controls', 25, self.menu_text_color,
                                                       self.menu_text_bg_color, 50, 28, True, False, False, True)
            button_cat_game = engineLib.MenuButton(self, 'Options_Cat_Game', 'Game', 25, self.menu_text_color,
                                                   self.menu_text_bg_color, 190, 28, True, False, False, True)
            button_cat_sound = engineLib.MenuButton(self, 'Options_Cat_Sound', 'Sound', 25, self.menu_text_color,
                                                    self.menu_text_bg_color, 274, 28, True, False, False, True)
            button_cat_video = engineLib.MenuButton(self, 'Options_Cat_Video', 'Video', 25, self.menu_text_color,
                                                    self.menu_text_bg_color, 372, 28, True, False, False, True)
            # Create video options, 10px space between each
            graphics_text = 'Graphics: [' + settings.GRAPHICS + ']'
            resolution_text = 'Resolution: [' + str(settings.WINDOW_WIDTH) + ', ' + str(settings.WINDOW_HEIGHT) + ']'
            button_graphics = engineLib.MenuButton(self, 'Options_Video_Graphics', graphics_text, 20, self.menu_text_color,
                                                   self.menu_text_bg_color, 50, 120, True, True, True, False)
            button_resolution = engineLib.MenuButton(self, 'Options_Video_Resolution', resolution_text, 20,
                                                     self.menu_text_color, self.menu_text_bg_color, 50, 90, True, True,
                                                     True, False)
            # Misc
            button_back = engineLib.MenuButton(self, 'Back', 'Back', 35, self.menu_text_color, self.menu_text_bg_color, 99,
                                               settings.SCREEN_HEIGHT - 95, True, False, False, True)
            self.buttons = [button_cat_controls, button_cat_game, button_cat_sound, button_cat_video, button_graphics,
                            button_resolution, button_back]
        except Exception:
            logging.error('* Error - Unexpected.')

    # Menu System - A system to update the view and catch any events on any of the menu screens and then handle those
    #               events appropriately whether it's launching the game, pausing the game, changing settings, or
    #               saving.

    def menu_screen_handler(self):
        """
        A function to handle switching between screens on the menu without hogging resources via recursion.

        @return: returns the state of the game so that the menu object can be tossed for proper resource management and
                 then the state is used to determine whether to start a new game, load a game, or exit the game
                 completely.
        @rtype: str
        """
        try:
            handler_running = True  # Only set to false when we are done with the menu
            while handler_running is True:
                old_state = self.state
                self.running = True
                # TODO: Until we have animations on every screen that resets the animation list, we have to cleanse the list
                # CONT: since it isn't rewritten
                # Cleanse any animations before new screen
                self.menu_animations = []
                self.menu_blit_bg_images = []
                self.menu_blit_layer_1_images = []
                if self.state == 'None':
                    self.menu_main()
                elif self.state == 'Main':
                    self.menu_main()
                elif self.state == 'Create_Character':
                    self.menu_create_character()
                elif self.state == 'Load':
                    self.menu_load()
                elif self.state == 'Options':
                    self.menu_options()
                elif self.state == 'Options_Video':
                    self.menu_options_video()
                elif self.state == 'Help':
                    self.menu_help()
                elif self.state == 'Feedback':
                    self.menu_feedback()
                elif self.state == 'Exit' or self.state == 'Load_New' or self.state == 'Load_Save':
                    # Log any information before the menu closes

                    # Close menu
                    print('[Debug - Info]: MainMenu.menu_screen_handler() is shutting down.')
                    handler_running = False
                # Continue running menu screen
                if self.state != 'None' and self.state != 'Exit' and self.state != 'Load_New' and self.state != 'Load_Save':
                    print('[Debug - Info]: Cleared sprites with top-lvl var-ref '
                          '\n\t\tengine_main_menu.state = \'' + self.state + '\'.')
                    self.menu_run()
                # Give feedback on the state
                if old_state != self.state:
                    print('[Debug - Info]: Changed state with top-lvl var-ref '
                          '\n\t\tengine_main_menu.state = \'' + self.state + '\'.')

            # Return the state so that the next action can be taken. States include 'Load_New', 'Load_Save', and 'Exit'
            return self.state
        except Exception:
            logging.error('* Error - Unexpected.')

    def menu_run(self):
        """
        A function that performs all of the tasks necessary for the menu to function properly.

        @return: none
        @rtype: none
        """
        try:
            while self.running:
                self.menu_events()
                self.menu_update()
                self.menu_draw()
        except Exception:
            logging.error('* Error - Unexpected.')

    def menu_events(self):
        """
        A function to handle all capture and handle all menu events for the menu to function properly.

        @return: none
        @rtype: none
        """
        try:
            for event in pygame.event.get():
                # Handle buttons, popups, and specific keys pressed
                self.menu_handler.handle_events(event)
            self.character_sample.handle_keys()
        except Exception:
            logging.error('* Error - Unexpected.')

    def menu_update(self):
        """
        A function that updates  all of the buttons if needed as well as the screen.

        @return: none
        @rtype: none
        """
        try:
            self.screen.fill(settings.WHITE)
            # TODO: Only update those.
            # Some input buttons require an update based on text input into them
            for button in self.buttons:
                button.update()
            # Update character
            self.sprites_all.update()

            # Update animations that are applied
            for animation in self.menu_animations:
                animation.update()

            # Check popups for purging
            if len(self.popups) > 0:
                new_popups = []
                for popup in self.popups:
                    if popup.active is False:
                        pass
                    else:
                        new_popups.append(popup)
                self.popups = new_popups
        except Exception:
            logging.error('* Error - Unexpected.')

    def menu_draw(self):
        """
        A function to draw all the buttons, visual effects, and scale the game
        screen to the specified resolution.

        @return: none
        @rtype: none
        """
        try:
            # Display backgrounds
            for image in self.menu_blit_bg_images:
                self.screen.blit(image, image.get_rect())
            # Display the sample character running across the screen
            self.sprites_all.draw(self.screen)
            # TODO: Debugging
            # CONT: for obj_interactable in objs:
            # CONT:     # Draw box around obj
            for obj in self.menu_handler.objs_interact:
                pygame.draw.lines(self.screen, settings.RED, True,
                                  ((obj.rect.x, obj.rect.y), (obj.rect.x, obj.rect.y + obj.rect.height),
                                   (obj.rect.x + obj.rect.width, obj.rect.y + obj.rect.height),
                                   (obj.rect.x + obj.rect.width, obj.rect.y)))
            # TODO: End of Debugging
            # Display overlays via options for the user
            for image in self.menu_blit_layer_1_images:
                rect = image.get_rect()
                if str(image) == '<Surface(1266x948x32 SW)>':  # Computer overlay
                    adjustment_computer_height = 15
                    rect.y = adjustment_computer_height
                self.screen.blit(image, rect)
            # Display specific visuals for sub menus
            self.menu_handler.draw_sub_menu_visuals(self.screen)
            # Display animations that are active
            for animation in self.menu_animations:
                animation.draw(self.screen)
            # Display information over visuals
            for button in self.buttons:
                button.draw(self.screen)
            for popup in self.popups:
                popup.draw(self.screen)
            # Display dev information
            # self.engine_dev.push_animation_to_screen()
            # Scale screen
            pygame.transform.scale(self.screen, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), self.window)
            pygame.display.flip()
        except Exception:
            logging.error('* Error - Unexpected.')


def main():
    try:
        logging.basicConfig(level="INFO", format='%(asctime)s %(levelname)s %(message)s',
                            filename='Bin/Logs/logs.txt',
                            datefmt='%a, %d %b %Y %H:%M:%S')
        pygame.init()
        pygame.mixer.init()
        # Init pregame assets and settings
        # TODO: Start implementing sounds
        # sound_object = pygame.mixer.Sound('Bin/Sounds/test.ogg')
        # sound_object.set_volume(1.0)
        # sound_object.play()
        # NOTE: Dev debugging - Push game window to second monitor for easier use of debugging
        # os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the game screen
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (1920 + 300, 100)  # Suggested window location
        # NOTE: End Dev debugging
        logging.info('* Info - Starting pygame.')
        engine_game = Game()
        engine_main_menu = MainMenu(engine_game)

        # Menu state handler #

        # Start the menu for the game and find the user's next course of action which will be given as 'desired_state'.
        # NOTE: We handle the state outside so that we can grab any and all information needed.
        pygame_running = True
        while pygame_running is True:
            desired_state = engine_main_menu.menu_start()
            # TODO: Create a loading screen and find the best spot to start it as the system hangs a little
            # CONT: Issue tracker on github
            if desired_state == 'Load_New':
                # Start new game
                logging.info('* Info - New game is being loaded.')
                engine_game.sprites_important.remove(engine_main_menu.character_sample)
                engine_game.game_new(engine_main_menu.file_load_save, character_name=engine_main_menu.character_name)
                engine_main_menu.state = 'Main'
                logging.info('* Info - New game is being closed.')
            elif desired_state == 'Load_Save':
                # Load a saved game
                logging.info('* Info - Saved game is being loaded.')
                # Remove any unnecessary assets that a new game didn't have
                engine_game.sprites_important.remove(engine_main_menu.character_sample)
                engine_game.game_new(engine_main_menu.file_load_save)
                # After game was exited see if the engine wants to quit to main menu or not
                if engine_game.state == 'Exit_To_Desktop':
                    pygame_running = False
                elif engine_game.state == 'Exit_To_Menu':
                    engine_main_menu.state = 'Main'
                    engine_game.sprites_important.empty()
                    engine_game.sprites_walls.empty()
                else:
                    logging.error('* Error - Unexpected engine state: %s', engine_game.state)
                    exit()
                logging.info('* Info - Saved game is being closed.')
            elif desired_state == 'Exit':
                logging.info('* Info - Exiting menu.')
                pygame_running = False
            else:
                logging.error('* Error - engine_main_menu.menu_start() returned an invalid state.')

        logging.info('* End of main.')
        pygame.quit()
        return 0
    except Exception:
        logging.error('* Error - Unexpected.')


if __name__ == '__main__':
    main()
    logging.info('* Info - Exiting ' + settings.TITLE_GAME + '.')
