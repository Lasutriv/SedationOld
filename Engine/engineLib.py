# The library of functions for the engine to use such as displaying sprites, changing files, moving sprites, and more.
# Tanner Fry
# tefnq2@mst.edu
import animations
import bindings
import character
import engine
import settings

from shutil import copy2
from typing import NewType
import importlib
import logging
import os
import pygame
import random

# Distinct Types #
# A group holds a collection of items just like a list. Groups for Pygame usually include sprites however.
Group = NewType('Group', list)


# noinspection PyDunderSlots
# ^-- Handles false warnings.
class EngineHandler:
    """Class. Used to handle in-game events, situations, and more."""
    def __init__(self, game):
        """
        Constructor. Used to initialize a handler object for parsing important actions and information from
                     the user.
        Note: Don't forget to call init_finish() when you're ready to start using the EngineHandler class.
        """
        self.engine_game = game
        # Game matrix variables
        self.screen_switch = False
        self.screen_switch_counter = settings.SCREEN_WIDTH
        self.screen_switch_counter_subtract = settings.SCREEN_WIDTH / 3
        self.screen_switch_dir = 'None'
        self.screen_switch_initial = True

        # Game ui animation variables

        # Game handling
        self.mouse_pos = ()
        self.state = 'None'
        self.state_inventory = 'Inventory'  # TODO: Change this to default as well
        self.state_governmnet = 'Default'

    def init_finish(self):
        """
        A function to finish late calls to create information and objects that might be based on other information that
        was needed in order to create said information.

        @return: none
        @rtype: none
        """
        self.state = 'Game_Run'

    # Handle Functions

    def handle_events(self, engine_game: object, event: object, character_main: object, sprites_all: Group,
                      sprites_walls: Group):
        """
        A function that handles specific keys, and mouse buttons, pressed while playing the game.

        @param engine_game: the engine which controls the network/functions of the game when it starts after the menu
        @type engine_game: object
        @param event: events from pygame that are triggered systematically via the keys, mouse, joystick or other
        @type event: object
        @param character_main: the character that the user is currently playing on
        @type character_main: object
        @param sprites_all: a collection of sprites representing every object or piece being displayed
        @type sprites_all: group
        @param sprites_walls: a collection of sprites representing every wall object being displayed
        @type sprites_walls: group
        @return: none
        @rtype: none
        """
        self.mouse_pos = pygame.mouse.get_pos()
        # Needed to fix the mouse position after the screen is scaled
        self.mouse_pos = (self.mouse_pos[0] / settings.RES_WIDTH_RATIO, self.mouse_pos[1] / settings.RES_HEIGHT_RATIO)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                if self.state == 'Game_Run':
                    sprites_all.empty()
                    sprites_walls.empty()
                    engine_game.state = 'Exit_To_Menu'
                    engine_game.running = False
                    print('[Debug - Info]: EngineHandler.handle_events() changed engine_game.running to False.')
                elif self.state == 'Game_Inventory':
                    self.state = 'Game_Run'
                    character_main.state = 'Idle'
                elif self.state == 'Game_Government_Management':
                    self.state = 'Game_Run'
                    character_main.state = 'Idle'
                else:
                    ask_you_sure = GamePopUp('Popup_State_Error', 'Error with engine state after \'ESC\' key. '
                                             'engine_game.state = ' + engine_game.state, 20, settings.DEEP_GRAY,
                                             'Exit To Main Menu', 15, settings.DEEP_GRAY, 'Exit To Desktop', 15,
                                             settings.DEEP_GRAY, 'Cancel', 15, settings.DEEP_GRAY, settings.LIGHT_GRAY,
                                             settings.BLACK, settings.SCREEN_WIDTH / 2 + 25,
                                             settings.SCREEN_HEIGHT / 2, True)
                    engine_game.popups.append(ask_you_sure)

            # NOTE: Debugging key action for a possible state
            elif event.key == pygame.K_c:
                if character_main.state == 'Idle':
                    character_main.state_changed = True
                    character_main.state = 'Crying'
                elif character_main.state == 'Crying':
                    character_main.state_changed = True
                    character_main.state = 'Idle'
            # NOTE: End of debugging key action

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == 'Game_Run':
                # Check whether the mouse click collided with the character's backpack
                if character_main.rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1]):
                    if 15 > (self.mouse_pos[0] - character_main.rect.x) > 0 \
                            and 74 > (self.mouse_pos[1] - character_main.rect.y) > 32 and character_main.direction == 'Right':
                        # TODO: Create inventory system such as what buttons and layout to show
                        self.state = 'Game_Inventory'
                        character_main.state = 'Inventory'
                    elif 15 > (character_main.rect.x + character_main.rect.width) - self.mouse_pos[0] > 0 \
                            and 74 > (self.mouse_pos[1] - character_main.rect.y) > 32 and character_main.direction == 'Left':
                        self.state = 'Game_Inventory'
                        character_main.state = 'Inventory'
            # Handle character inventory text and item clicking
            # We handle it here instead of the individual buttons so that it's faster to just check if's and else's
            # instead of doing function calls to handle events on each piece of text.
            elif self.state == 'Game_Inventory':
                for text in engine_game.texts_to_display:
                    if text.text_rect.collidepoint(self.mouse_pos[0], self.mouse_pos[1]):
                        if text.name == 'Tab_Inventory':
                            self.state_inventory = 'Inventory'
                        if text.name == 'Tab_Saves':
                            self.state_inventory = 'Saves'
                        if text.name == 'Tab_Options':
                            self.state_inventory = 'Options'
                        if text.name == 'Tab_Feedback':
                            self.state_inventory = 'Feedback'
                        if text.name == 'Tab_Exit':
                            self.state_inventory = 'Exit'
                            # TODO: Create a popup to ask if they want to exit the whole game or to the main screen
                            ask_you_sure = GamePopUp('Popup_Exit', 'Would you like to exit to the main menu or the game'
                                                     '?', 20, settings.DEEP_GRAY, 'Exit To Main Menu', 15,
                                                     settings.DEEP_GRAY, 'Exit To Desktop', 15, settings.DEEP_GRAY,
                                                     'Cancel', 15, settings.DEEP_GRAY, settings.LIGHT_GRAY,
                                                     settings.BLACK, settings.SCREEN_WIDTH / 2 + 25,
                                                     settings.SCREEN_HEIGHT / 2, True)
                            engine_game.popups.append(ask_you_sure)
            # Handle character inventory text and item clicking
            # We handle it here instead of the individual buttons so that it's faster to just check if's and else's
            # instead of doing function calls to handle events on each piece of text.
            elif self.state == 'Game_Government_Management':
                # TODO: If character clicks in location of the tabs then chage state_government
                # CONT: according to the tab
                if (self.mouse_pos[0] > 36 and self.mouse_pos[0] < 280) and (self.mouse_pos[1] > 73 and self.mouse_pos[1] < 98):
                    self.state_governmnet = 'Leader'
                elif (self.mouse_pos[0] > 286 and self.mouse_pos[0] < 540) and (self.mouse_pos[1] > 73 and self.mouse_pos[1] < 98):
                    self.state_governmnet = 'Party'
                elif (self.mouse_pos[0] > 549 and self.mouse_pos[0] < 696) and (self.mouse_pos[1] > 73 and self.mouse_pos[1] < 98):
                    self.state_governmnet = 'Judge'
                elif (self.mouse_pos[0] > 707 and self.mouse_pos[0] < 951) and (self.mouse_pos[1] > 73 and self.mouse_pos[1] < 98):
                    self.state_governmnet = 'Information'
                elif (self.mouse_pos[0] > 967 and self.mouse_pos[0] < 1245) and (self.mouse_pos[1] > 73 and self.mouse_pos[1] < 98):
                    self.state_governmnet = 'Map'

        # Handle popup events
        for popup in engine_game.popups:
            popup.handle_events(engine_game, engine_game.popups, event, self.mouse_pos)

    # Level Functions

    @staticmethod
    def change_level(engine_game: object, direction: str):
        """
        A function to change the level based off of which sub-level the character
        is on, their direction they were going, and which sub-level was in the
        direction they were going.

        @param engine_game: the engine which controls the network/functions of the game when it starts after the menu
        @type engine_game: object
        @param direction: the direction the character is facing and about to head into
        @type direction: str
        @return: none
        @rtype: none
        """
        if direction is 'Down':
            engine_game.level_sub_current = engine_game.level_directions_down
        elif direction is 'Left':
            engine_game.level_sub_current = engine_game.level_directions_left
        elif direction is 'Right':
            engine_game.level_sub_current = engine_game.level_directions_right
        elif direction is 'Up':
            engine_game.level_sub_current = engine_game.level_directions_up

    # TODO: Load the level into a list of already loaded assets so we don't call it as much
    def generate_level(self, engine_game: object, level_number: int, level_sub_number: int):
        """
        A function to generate the background as well as any kinds of assets in the level.

        @param engine_game: the engine which controls the network/functions of the game when it starts after the menu
        @type engine_game: object
        @param level_number: the level specified by engine
        @type level_number: int
        @param level_sub_number: the specific level, also named sub-level, inside of a specific level
        @type level_sub_number: int
        @return: none
        @rtype: none
        """
        # Screen size: 40 tiles wide by 30 tiles tall
        row_current = 0
        path_to_level = 'Levels/Level_' + str(level_number) + '/Sub_Level_' + str(level_sub_number) + '.txt'

        try:
            with open(path_to_level, 'r') as file:
                for line in file:
                    col_current = 0
                    data_from_file = line.split(' ')
                    for data in data_from_file:
                        self.generate_level_walls(engine_game, data, col_current, False, row_current)
                        col_current += 1
                    row_current += 1
        except FileNotFoundError:
            raise FileNotFoundError('File doesn\' exist.')
            engine_game.running = False

    def generate_level_directions(self):
        """
        A function to determine where the current exits are for the current level.
        It is called from the generate_level_matrix function to determine which levels
        are in each direction of where the current level is.

        @return: none
        @rtype: none
        """
        print('[Gather - Pending]: Generating level directions.')
        self.engine_game.level_directions = ''
        found_directions = False
        level_matrix_location = [0, 0]
        row = 0
        # Find current location
        for line in self.engine_game.level_matrix:
            col = 0
            for data in line:
                if data == self.engine_game.level_sub_current:
                    level_matrix_location = [row, col]
                col += 1
            row += 1
        # Update current location and determine level directions
        self.engine_game.level_matrix_location = level_matrix_location
        try:
            # Check for level left
            if '######' != self.engine_game.level_matrix[level_matrix_location[0] - 0][level_matrix_location[1] - 1]:
                self.engine_game.level_directions += 'Left'
                self.engine_game.level_directions_left = self.engine_game.level_matrix[level_matrix_location[0] - 0][level_matrix_location[1] - 1]
                found_directions = True
            # Check for level above
            if '######' != self.engine_game.level_matrix[level_matrix_location[0] - 1][level_matrix_location[1] - 0]:
                self.engine_game.level_directions += 'Up'
                self.engine_game.level_directions_up = self.engine_game.level_matrix[level_matrix_location[0] - 1][level_matrix_location[1] - 0]
                found_directions = True
            # Check for level right
            if '######' != self.engine_game.level_matrix[level_matrix_location[0] + 0][level_matrix_location[1] + 1]:
                self.engine_game.level_directions += 'Right'
                self.engine_game.level_directions_right = self.engine_game.level_matrix[level_matrix_location[0] + 0][level_matrix_location[1] + 1]
                found_directions = True
            # Check for level down
            if '######' != self.engine_game.level_matrix[level_matrix_location[0] + 1][level_matrix_location[1] + 0]:
                self.engine_game.level_directions += 'Down'
                self.engine_game.level_directions_down = self.engine_game.level_matrix[level_matrix_location[0] + 1][level_matrix_location[1] + 0]
                found_directions = True
            if found_directions is True:
                print('[Gather - Success]: Level directions found.')
            else:
                print('[Gather - Failed: Level directions not found.]')
        except:
            print(Exception)
            print('[Debug - Error]: Popped out of range on level_matrix?')
        print('[Debug - Info]: Surrounding Levels -', self.engine_game.level_directions)

    def generate_level_matrix(self, engine_game: object):
        """
        A function to gather the level matrix containing all of the sub-levels in a level.
        This allows the tracking of the character's location among all of the sub-levels within
        a level.

        @param engine_game: the engine which controls the network/functions of the game when it starts after the menu
        @type engine_game: object
        @return: none
        @rtype: none
        """
        data_counter = 0
        line_counter = 0
        path_to_matrix = 'Levels/Level_' + str(engine_game.level_current) + '/level_matrix.lvl'
        # Gather map length from file
        with open(path_to_matrix, 'r') as file:
            for _ in file:
                line_counter += 1
        # Set up level matrix height for each row in file
        level_matrix = [[] for row in range(line_counter)]  # [row][col] = ###### or LVL123
        line_counter = 0
        with open(path_to_matrix, 'r') as file:
            for line in file:
                data_from_line = line.split(' ')
                # Gather map width from file
                for _ in data_from_line:
                    data_counter += 1
                # Set up level matrix width for each col in file
                level_matrix[line_counter] = ['' for _ in range(data_counter)]
                data_counter = 0
                for data_other in data_from_line:
                    data_other = data_other.split('\n')
                    # Modify each level information in the matrix from what's in the file
                    if not '#' in data_other[0]:
                        data_other[0] = int(data_other[0].strip('LVL'))
                    level_matrix[line_counter][data_counter] = data_other[0]
                    data_counter += 1
                data_counter = 0
                line_counter += 1

        # Change data needed and then generate directions from current level
        engine_game.level_matrix = level_matrix
        self.generate_level_directions()

    def generate_level_walls(self, engine_game: object, data: str, col_current: int, level_switch: bool,
                             row_current: int, sub_level: int):
        """
        A function for generating all of the specific walls and pieces in a level.

        @param engine_game: the engine which controls the network/functions of the game when it starts after the menu
        @type engine_game: object
        @param data: the desired sprite, representing a tile for walls, that will be used for generation
        @type data: str
        @param col_current: an integer representing the tile's column location within the sub-level tile matrix
        @type col_current: int
        @param level_switch: the trigger for whether or not to modify how level generation works based on if we are
                             switching levels
        @type level_switch: bool
        @param row_current: an integer representing the tile's row location within the sub-level tile matrix
        @return: none
        @rtype: none
        """
        # Convert for pixel match in game
        x = 32 * col_current
        y = 32 * row_current
        type_tile = data.rstrip()
        if level_switch is None:
            # Move new level off the screen according to the direction the character is going
            if self.screen_switch_dir is 'Down':
                y += self.screen_switch_counter
            elif self.screen_switch_dir is 'Left':
                x -= self.screen_switch_counter
            elif self.screen_switch_dir is 'Right':
                x += self.screen_switch_counter
            elif self.screen_switch_dir is 'Up':
                y -= self.screen_switch_counter
            if type_tile == 'N/A' or type_tile == 'N/A\n' or type_tile == ' ':
                # Do nothing
                pass
            else:
                # Check all types of tiles against the given data and if one is found, init it
                TileSpriteInit(engine_game, type_tile, x, y, sub_level)
        else:
            if type_tile == 'N/A' or type_tile == 'N/A\n' or type_tile == ' ':
                # Do nothing
                pass
            else:
                # Check all types of tiles against the given data and if one is found, init it
                TileSpriteInit(engine_game, type_tile, x, y, sub_level)

    def load_saved_game(self, file_save_name: str):
        """
        A function to load a game, from the loading screen, that was previously saved.

        @param file_save_name: the name of the save file to be loaded. No need for '.py'
        @type file_save_name: str
        @return: none
        @rtype: none
        """
        file_path_full = 'Bin/Saves/' + file_save_name + '.py'
        # Make sure settings.py has a backup
        with open('settings.py', 'r') as file:
            lines = file.readlines()
        if (os.path.isfile('settings_defaults.py')) is not True:
            with open('settings_defaults.py', 'w') as file:
                file.writelines(lines)
            print('[Debug - Info]: Default settings backup started.')
        # Load settings from a save file into the engine file
        if (os.path.isfile('settings_defaults.py')) is True:
            print('[Debug - Info]: Default settings backup finished.')
            with open(file_path_full, 'r') as file:
                lines_new = file.readlines()
            with open('settings.py', 'w') as file:
                file.writelines(lines_new)
            print('[Debug - Info]: Character settings imported.')
        # Reload file
        importlib.reload(settings)

    def reload_default_settings(self):
        """
        A function to save the default settings back into the settings.py file.

        @return: none
        @rtype: none
        """
        if (os.path.isfile('settings_defaults.py')) is True:
            with open('settings_defaults.py', 'r') as file:
                lines = file.readlines()
            with open('settings.py', 'w') as file:
                file.writelines(lines)
            print('[Debug - Info]: \'settings.py\' was updated successfully from settings_defaults.py.')
        else:
            # Try to load settings from the backup.
            # NOTE: There should never be a rewrite to the 'settings_defaults.py' file in the Backup folder
            print('* [Debug - Error]: \'settings_defaults.py\' was not found when trying to rewrite settings. Retrying '
                  'from backups.')
            path_defaults_full = 'Bin/Backup/settings_defaults.py'
            if (os.path.isfile(path_defaults_full)) is True:
                with open(path_defaults_full, 'r') as file:
                    lines = file.readlines()
                with open('settings.py', 'w') as file:
                    file.writelines(lines)
                print('[Debug - Info]: \'settings.py\' was updated \'from Bin/Backup/settings_defaults.py '
                      '\'successfully.')
                # Copy from backup settings to a new settings_defaults file in Bin/
                try:
                    copy2('Bin/Backup/settings_defaults.py', 'Engine')
                except Exception as excep:
                    print('[Debug - Critical Error]: \'settings_defaults.py\' failed to copy from the backup folder. '
                          'Provide info to the developers via the feedback tab')
                    print('[Debug - Exception]: ' + str(excep))
            else:
                print('[Debug - Critical Error]: \'settings_defaults.py\' was not found in \'Bin/Backup/\'.')

    # TODO: Create the in-game pause menu features to save the game as well.
    def save_current_game(self, file_save_name: str):
        """
        A function to save a game that has already been saved before.

        @param file_save_name: the name of the file being saved. No need for '.py'
        @type file_save_name: str
        @return: none
        @rtype: none
        """
        path_saves_full = 'Bin/Saves/' + file_save_name + '.py'
        # Create save file from current settings
        with open('settings.py', 'r') as file:
            lines = file.readlines()
        with open(path_saves_full, 'w') as file:
            file.writelines(lines)
        print('[Debug - Info]:', file_save_name, 'saved.')

    def save_new_game(self, character_name: str, file_save_name: str):
        """
        A function to save a game that was just created.
        # NOTE: Later if coop is in the game we can list both character's being
        # NOTE: played and allow the user to select which character to save.

        @param character_name: the name that the user gave for their new character
        @type character_name: str
        @param file_save_name: the name of the file being saved. No need for '.py'
        @type file_save_name: str
        @return: none
        @rtype: none
        """
        path_saves_full = 'Bin/Saves/' + file_save_name + '.py'
        # Create a copy of default settings file and save it in Bin/Saves/ as well as in the main directory so that
        # we can copy back the defaults after the game is done.
        # NOTE: This could cause some bad corruption since the default settings have a chance to not be copied back to
        # NOTE: the settings.py file, thus leaving the previous character's settings still in the system
        with open('settings.py', 'r') as file:
            lines = file.readlines()
        # Create save file from default settings and a backup for default settings
        with open(path_saves_full, 'w') as file:
            file.writelines(lines)
        # TODO: The below two lines I don't think belong since we use settings_defaults for the system defaults and
        # CONT: those don't need to be changed.
        # with open('settings_defaults.py', 'w') as file:
        #     file.writelines(lines)
        # TODO: I don't think I need to update the settings again right here. We can just set the settings.CHAR_NAME
        # CONT: equal to the character_name given from game_new()
        # Update the new save file
        # self.update_settings('CHAR_NAME', character_name, 'string', file_location=path_saves_full)
        print('[Debug - Info]:', file_save_name, 'saved.')
        # Load the saved settings into the current engine settings
        # self.load_saved_game(file_save_name)

    # Misc Functions

    def check_character_close_to_exit(self, engine_game: object, character_main: object):
        """
        A function that determines how close the character is to a side of the screen.

        @param engine_game: the engine which controls the network/functions of the game when it starts after the menu
        @type engine_game: object
        @param character_main: the character that the user is currently playing as
        @type character_main: object
        @return: none
        @rtype: none
        """
        max_distance = 15
        if character_main.rect.x - max_distance > settings.SCREEN_WIDTH and 'Right' in engine_game.level_directions:
            if self.screen_switch is False:
                self.change_level(engine_game, 'Right')
                character_main.rect.x = 20
            self.screen_switch = True
            self.screen_switch_dir = 'Right'
        elif character_main.rect.x + max_distance < 0 and 'Left' in engine_game.level_directions:
            if self.screen_switch is False:
                self.change_level(engine_game, 'Left')
                character_main.rect.x = settings.SCREEN_WIDTH - 20
            self.screen_switch = True
            self.screen_switch_dir = 'Left'
        elif character_main.rect.y - max_distance > settings.SCREEN_HEIGHT and 'Down' in engine_game.level_directions:
            if self.screen_switch is False:
                self.change_level(engine_game, 'Down')
                character_main.rect.y = 20
            self.screen_switch = True
            self.screen_switch_dir = 'Down'
        elif character_main.rect.y + max_distance < 0 and 'Up' in engine_game.level_directions:
            if self.screen_switch is False:
                self.change_level(engine_game, 'Up')
                character_main.rect.y = settings.SCREEN_HEIGHT - 20
            self.screen_switch = True
            self.screen_switch_dir = 'Up'
        # Check if character is off screen or glitched
        if character_main.rect.x > settings.SCREEN_WIDTH + character_main.rect.width \
                or character_main.rect.x < 0 - character_main.rect.width \
                or character_main.rect.y > settings.SCREEN_HEIGHT + character_main.rect.height \
                or character_main.rect.y < 0 - character_main.rect.height:
            character_main.rect.x = settings.SCREEN_WIDTH / 2
            character_main.rect.y = settings.SCREEN_HEIGHT / 2

    def check_game_graphics(self, screen: object, in_game: bool):
        """
        A function to check the game graphics setting and perform actions based on whether the user is in game
        or not.

        @param screen: the surface that holds all of the menu and game images/pixels
        @type screen: object
        @param in_game: tells whether the program is in game or not
        @type in_game: bool
        @return: none
        @rtype: none
        """
        # Draw effects in the loading screen only if graphics are on high, otherwise the effects are all the time
        # because graphics don't really matter in this game
        return
        if settings.GRAPHICS == 'High' and in_game is False:
            for i in range(5):
                point_list = []
                for j in range(5):
                    rand_x = random.randrange(0 - 100, settings.SCREEN_WIDTH + 100)
                    rand_y = random.randrange(0 - 100, settings.SCREEN_HEIGHT + 100)
                    point_list.append((rand_x, rand_y))
                pygame.draw.polygon(screen, settings.LIGHT_GRAY, point_list, 1)
        elif settings.GRAPHICS == 'Medium':
            for i in range(5):
                point_list = []
                for j in range(5):
                    rand_x = random.randrange(0 - 100, settings.SCREEN_WIDTH + 100)
                    rand_y = random.randrange(0 - 100, settings.SCREEN_HEIGHT + 100)
                    point_list.append((rand_x, rand_y))
                pygame.draw.polygon(screen, settings.LIGHT_GRAY, point_list, 1)
        elif settings.GRAPHICS == 'Low':
            for i in range(10):
                point_list = []
                for j in range(5):
                    rand_x = random.randrange(0 - 100, settings.SCREEN_WIDTH + 100)
                    rand_y = random.randrange(0 - 100, settings.SCREEN_HEIGHT + 100)
                    point_list.append((rand_x, rand_y))
                pygame.draw.polygon(screen, settings.LIGHT_GRAY, point_list, 1)

    def draw_ui_debug(self, engine_game: object, screen: object, character_main: object):
        """
        A function to display debugging information to the programmer during engine creation/maintaining.

        @param engine_game: the engine which controls the network/functions of the game when it starts after the menu
        @type engine_game: object
        @param screen: the surface that holds all of the menu and game images/pixels
        @type screen: object
        @param character_main: the character which the user is playing at the moment
        @type character_main: object
        @return: none
        @rtype: none
        """
        # Info to display
        font_debug_info = pygame.font.Font('Bin/Fonts/Adventure_Merienda/Merienda-Regular.ttf', 15)
        font_level_surf = font_debug_info.render('Level: ' + str(engine_game.level_current) + ' of '
                                                 + str(engine_game.level_total), False, settings.WHITE,
                                                 settings.DARK_GRAY)
        font_level_sub_surf = font_debug_info.render('Sub Level: ' + str(engine_game.level_sub_current) + ' of '
                                                     + str(engine_game.level_sub_current_total) + '. Total: '
                                                     + str(engine_game.level_sub_total), False, settings.WHITE,
                                                     settings.DARK_GRAY)
        font_char_state_surf = font_debug_info.render('State: ' + character_main.state, False, settings.WHITE,
                                                      settings.DARK_GRAY)
        font_char_x_vel_surf = font_debug_info.render('X-Velocity: ' + str(character_main.x_velocity), False,
                                                      settings.WHITE, settings.DARK_GRAY)
        font_char_y_vel_surf = font_debug_info.render('Y-Velocity: ' + str(character_main.y_velocity), False,
                                                      settings.WHITE, settings.DARK_GRAY)
        font_char_jump_count_surf = font_debug_info.render('Jump Count: ' + str(character_main.jump_count), False,
                                                           settings.WHITE, settings.DARK_GRAY)
        # Character Collision help
        # pygame.draw.lines(screen, settings.RED, True, ((character_main.rect.x, character_main.rect.y),
        #   (character_main.rect.x, character_main.rect.y + character_main.rect.height),
        #   (character_main.rect.x + character_main.rect.width, character_main.rect.y + character_main.rect.height),
        #   (character_main.rect.x + character_main.rect.width, character_main.rect.y)))
        # Display ui
        screen.blit(font_level_surf, (5, 5))
        screen.blit(font_level_sub_surf, (5, 25))
        screen.blit(font_char_state_surf, (251, 5))
        screen.blit(font_char_x_vel_surf, (251, 25))  # 256 - 5 for the offset of 5 for the other debug info
        screen.blit(font_char_y_vel_surf, (251, 45))
        screen.blit(font_char_jump_count_surf, (251, 65))

    def draw_ui_game(self, screen: object, character_main: object):
        """
        A function to display in game character information while playing the game.

        @param screen: the surface that holds all of the menu and game images/pixels
        @type screen: object
        @param character_main: the character which the user is playing at the moment
        @type character_main: object
        @return: none
        @rtype: none
        """
        # Info to display such as character name and stats
        font_ui = pygame.font.Font('Bin/Fonts/Adventure_Merienda/Merienda-Regular.ttf', 15)
        font_ui_name = pygame.font.Font('Bin/Fonts/Adventure_Merienda/Merienda-Regular.ttf', 17)
        font_ui_char_name_surf = font_ui_name.render(settings.CHAR_NAME, True, settings.YELLOW)
        font_ui_char_name_rect = font_ui_char_name_surf.get_rect()
        font_ui_trait_endurance_surf = font_ui.render('Endurance: ' + str(character_main.trait_endurance), False,
                                                      settings.WHITE, settings.DARK_GRAY)
        # Ready all other elements of ui

        # Display ui system
        # Calculate name location
        if character_main.rect.width > font_ui_char_name_rect.width:
            x_new = character_main.rect.x + ((character_main.rect.width - font_ui_char_name_rect.width) / 2)
        else:
            x_new = character_main.rect.x - ((font_ui_char_name_rect.width - character_main.rect.width) / 2)

        # Finish and display
        buffer_due_to_buff_effect_images = 10
        screen.blit(font_ui_char_name_surf, (x_new, character_main.rect.y - font_ui_char_name_rect.height
                                             - buffer_due_to_buff_effect_images))
        screen.blit(font_ui_trait_endurance_surf, (5, 50))

    def gather_engine_info(self, engine_game: object, objective: str):
        """
        A function that gathers specific information for the engine.

        @param engine_game: the engine which controls the network/functions of the game when it starts after the menu
        @type engine_game: object
        @param objective: get_levels, get_spec_subs, calculate_window
        @type objective: str
        @return: none
        @rtype: none
        """
        if objective == 'get_levels':
            # Updates the total levels, total sub-levels of a level, and total sub-levels of the game
            counter_level_total = 0
            counter_level_sub_total = 0
            path_levels = 'Levels'
            path_level_sub = ''

            # Find items in the Levels folder
            for item in os.listdir(path_levels):
                # Split item for deeper condition checking
                item_split = item.split('_', maxsplit=1)
                # Check if item is a 'Level' directory
                if item_split[0] == 'Level' and item_split[1].isdigit() and os.path.isdir(os.path.join(path_levels,
                                                                                                       item)):
                    counter_level_total += 1
                    path_level_sub = path_levels + '/' + str(item)
                # Check the sub-levels in each level directory
                if path_level_sub != '':
                    for file in os.listdir(path_level_sub):
                        if 'Sub_Level' in file:
                            counter_level_sub_total += 1
                # Reset variables
                path_level_sub = ''

            # Change engine variables to reflect information gathered
            self.gather_engine_info(engine_game, 'get_total_sub_of_current_level')
            if 0 >= (counter_level_total or counter_level_sub_total):
                print('[Gather - Fail]: The calculation of the total levels and/or total sub-levels has failed to '
                      'finish properly.')
            else:
                engine_game.level_total = counter_level_total
                engine_game.level_sub_total = counter_level_sub_total
        # TODO: Refactor code below
        elif objective == 'get_total_sub_of_current_level':
            # Updates how many sub-levels are on the current level
            ctr_level_sub_total = 0
            path_spec_level = 'Levels/Level_' + str(engine_game.level_current)

            # Calculate specific sub levels
            for file in os.listdir(path_spec_level):
                if 'Sub_Level' in file:
                    ctr_level_sub_total += 1
            # Change engine variables to reflect information gathered
            if ctr_level_sub_total > 0:
                engine_game.level_sub_current_total = ctr_level_sub_total
            else:
                print('[Gather - Fail]: The calculation of the total sub-levels in the current level has failed to '
                      'finish properly.')
        elif objective == 'calculate_window':
            resolution_modes = pygame.display.list_modes(32)
            if not resolution_modes:
                print('[Gather - Fail]: There are no resolutions that support 32 pixel ratio.')
                self.update_settings('RES_WIDTH_RATIO', str(settings.WINDOW_WIDTH / settings.SCREEN_WIDTH), 'int')
                self.update_settings('RES_HEIGHT_RATIO', str(settings.WINDOW_HEIGHT / settings.SCREEN_HEIGHT), 'int')
                # TODO: Put pop-up message here signaling the user to restart the game to fix resolution querks.
                # TODO: Remember, we import 'settings0.py' so when it's changed it doesn't change the instance we have
                # CONT: open on import.
                return settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT
            else:
                # Check if user specified a different resolution
                if settings.RES_CHANGED is True:
                    print('[Gather - Success]: Resolution found but was changed by user, best is ('
                          + str(settings.WINDOW_WIDTH) + ', ' + str(settings.WINDOW_HEIGHT) + ')')
                    return settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT
                else:
                    print('[Gather - Success]: Resolution found, best is ' + str(resolution_modes[0]) + '.')
                    self.update_settings('WINDOW_WIDTH', str(resolution_modes[0][0]), 'int')
                    self.update_settings('WINDOW_HEIGHT', str(resolution_modes[0][1]), 'int')
                    self.update_settings('RES_WIDTH_RATIO', str(resolution_modes[0][0] / settings.SCREEN_WIDTH), 'int')
                    self.update_settings('RES_HEIGHT_RATIO', str(resolution_modes[0][1] / settings.SCREEN_HEIGHT),
                                         'int')
                    return resolution_modes[0]

    @staticmethod
    def reimport_all():
        """
        A function to reimport all files associated with the game. The only catch, this file needs its own reimport
        outside of this function use.

        @return: none
        @rtype: none
        """
        print('[Debug - Info]: Reloading imports.')
        importlib.reload(animations)
        importlib.reload(bindings)
        importlib.reload(character)
        importlib.reload(engine)
        importlib.reload(settings)

    def update_settings(self, setting: str, value: str, value_type='string', file_location='settings.py'):
        """
        A function to update the settings of the current game for the user.
        # TODO: There needs to be a separate settings file specified to the current user to hold all of their
        # CONT: own settings separately instead of one settings file as there will be multiple accounts on a
        # CONT: computer due to local coop probably being in the game.

        @param setting: the specific setting to change
        @type setting: str
        @param value: the new value of the desired setting
        @type value: str
        @param value_type: is either 'string', 'int', 'decimal', etc
        @type value_type: str
        @param file_location: the location of the file that is to be changed
        @type file_location: str
        @return: none
        @rtype: none

        Example:
        update_settings('RES_CHANGED', False, 'bool')
        """
        with open(file_location, 'r') as file:
            lines = file.readlines()
        # Find specific setting and split it
        line_counter = 0
        line_desired = 0
        line_changed = ''
        for line in lines:
            if line.find(setting) == 0:
                line_desired = line_counter
                split_line = line.split('=')
                if value_type is 'string':
                    line_changed = split_line[0] + '= \'' + value + '\'\n'
                elif value_type is 'bool':
                    line_changed = split_line[0] + '= ' + str(value) + '\n'
                else:
                    line_changed = split_line[0] + '= ' + value + '\n'
            line_counter += 1
        lines[line_desired] = line_changed

        # Change specific setting
        with open(file_location, 'w') as file:
            file.writelines(lines)
        importlib.reload(settings)
        print('[Debug - Info]: Setting = %s, Value = %s in %s' % (setting, value, file_location))


class GameText(object):
    """Class. Used to create text to display in game."""
    def __init__(self, name: str, text: str, text_size: int, text_color: tuple,
                 x: int, y: int, active: bool, disabled: bool):
        """
        Constructor. Used to initialize texxt and set it up for being displayed.

        @param name: the name used to identify the button instead of creating another variable to represent the button
                     from others within a collection of buttons
        @type name: str
        @param text: the message that the button is trying to convey to the user
        @type text: str
        @param text_size: the text size of the message
        @type text_size: int
        @param text_color: the color that the message will be displayed in
        @type text_color: tuple
        @param background_color: the color behind all of the text and design on the pop-up
        @type background_color: tuple
        @param x: the desired horizontal location relative to the top left of the button
        @type x: int
        @param y: the desired vertical location relative to the top left of the button
        @type y: int
        @param active: the switch checked for whether a button should be displayed or not
        @type active: bool
        """
        # Text attributes
        self.text = text
        self.text_color = text_color
        self.text_size = text_size
        self.font = pygame.font.Font('Bin/Fonts/Adventure_Merienda/Merienda-Regular.ttf', self.text_size)
        self.text_image = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_image.get_rect()
        self.text_rect.x = x
        self.text_rect.y = y
        self.active = active
        self.disabled = disabled  # Usually False
        self.hover = False
        self.name = name
        self.rect = pygame.Rect(x, y, self.text_rect.width, self.text_rect.height)

    def draw(self, screen: object):
        """
        A function to update the button the screen every frame.

        @param screen: the display that the button is pushed to
        @type screen: object
        @return: none
        @rtype: none
        """
        if self.active:
            screen.blit(self.text_image, self.text_rect)


class GameButton(object):
    # TODO: FINISH THIS
    """Class. Used to created different kinds of buttons for the ui system in the game."""
    def __init__(self, engine_game: object, name: str, text: str, text_size: int, text_color: tuple,
                 background_color: tuple, x: int, y: int, active: bool, disabled: bool, dropdown: bool,
                 special: bool):
        """
        Constructor. Used to initialize a button and set it up for being displayed.

        @param engine_game: the engine which controls the network of the menu the game is originally started from
        @type engine_game: object
        @param name: the name used to identify the button instead of creating another variable to represent the button
                     from others within a collection of buttons
        @type name: str
        @param text: the message that the button is trying to convey to the user
        @type text: str
        @param text_size: the text size of the message
        @type text_size: int
        @param text_color: the color that the message will be displayed in
        @type text_color: tuple
        @param background_color: the color behind all of the text and design on the pop-up
        @type background_color: tuple
        @param x: the desired horizontal location relative to the top left of the button
        @type x: int
        @param y: the desired vertical location relative to the top left of the button
        @type y: int
        @param active: the switch checked for whether a button should be displayed or not
        @type active: bool
        @param dropdown: the switch checked for whether a button should display it's values that the dropdown contains
        @type dropdown: bool
        @param special: the switch checked for whether a button should be displayed with special visuals or not
        @type special: bool
        """
        # Text attributes
        self.text = text
        self.text_color = text_color
        self.text_size = text_size
        self.font = pygame.font.Font('Bin/Fonts/Adventure_Merienda/Merienda-Regular.ttf', self.text_size)
        self.text_image = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_image.get_rect()
        self.text_rect.x = x
        self.text_rect.y = y

        # Button attributes
        self.active = active
        self.dropdown = dropdown
        self.disabled = disabled  # Usually False
        self.hover = False
        self.name = name
        self.special = special
        # TODO: Does image need a conver_alpha() on it?
        if background_color == settings.TRANSPARENT:
            # Create a transparent background on the text's image
            self.image = pygame.Surface((self.text_rect.width, self.text_rect.height), pygame.SRCALPHA, 32)
        else:
            self.image = pygame.Surface((self.text_rect.width, self.text_rect.height))
            self.image.fill(background_color)
        self.rect = pygame.Rect(x, y, self.text_rect.width, self.text_rect.height)

        # Misc
        self.engine_game = engine_game

    def handle_events(self, event: object, mouse_pos: tuple):
        """
        A function that handles the events for the buttons in the menu section
        of the game.

        @param event: a specific action that pygame recognized from the user
        @type event: object
        @param mouse_pos: a collection of points representing the position of the mouse when the event occurred
        @type mouse_pos: tuple
        @return: none
        @rtype: none
        """
        # Check mouse pos for hover events
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.hover = True
            # Handle special buttons via their name
            if self.special:
                self.font.set_underline(True)
        else:
            self.hover = False
            self.font.set_underline(False)
        self.text_image = self.font.render(self.text, True, self.text_color)

        # Check mouse interaction with buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                pass

    def update(self):
        """
        A function to check various conditions for the button and prepare for next interaction

        @return: none
        @rtype: none
        """
        pass

    def draw(self, screen: object):
        """
        A function to draw buttons to the screen when called upon to do so, usually from a loop that iterates through
        a collection of buttons.

        @param screen: the display that the button is applied to
        @type screen: object
        @return: none
        @rtype: none
        """
        if self.active:
            screen.blit(self.image, self.rect)
            screen.blit(self.text_image, self.text_rect)


class GamePopUp(object):
    """Class. Used to initialize pop-up messages while the menu screen is being used by the user."""

    def __init__(self, name: str, text: str, text_size: int, text_color: tuple,
                 text_left: str, text_left_size: int, text_left_color: tuple,
                 text_right: str, text_right_size: int, text_right_color: tuple,
                 text_middle: str, text_middle_size: int, text_middle_color: tuple,
                 background_color: tuple, border_color: tuple, x: int, y: int,
                 active: bool):
        """
        Constructor. Used to set up a pop-up for displaying information to the user and then requiring some
        kind of input for the pop-up to disappear.

        @param name: the name used to identify the pop-up instead of creating another variable to represent the pop-up
                     from others within a collection of pop-ups
        @type name: str
        @param text: the overall message that the pop-up is trying to convey to the user
        @type text: str
        @param text_size: the text size of the overall message
        @type text_size: int
        @param text_color: the color that the overall message will be displayed in
        @type text_color: tuple
        @param text_left: the text option a user can pick that will be on the left side of the pop-up message
        @type text_left: str
        @param text_left_size: the text size of the left hand side option
        @type text_left_size: int
        @param text_left_color: the color that the left hand side option will be displayed in
        @type text_left_color: tuple
        @param text_right: the text option a user can pick that will be on the right side of the pop-up message
        @type text_right: str
        @param text_right_size: the text size of the right hand side option
        @type text_right_size: int
        @param text_right_color: the color that the right hand size option will be displayed in
        @type text_right_color: tuple
        @param text_middle: the text option a user can pick that will be in the middle of the pop-up message
        @type text_middle: str
        @param text_middle_size: the text size of the middle option
        @type text_middle_size: int
        @param text_middle_color: the color that the middle option will be displayed in
        @type text_middle_color: tuple
        @param background_color: the color behind all of the text and design on the pop-up
        @type background_color: tuple
        @param border_color: the color that will be on the border, or edge, of the pop-up
        @type border_color: tuple
        @param x: the desired horizontal location relative to the top left of the pop-up
        @type x: int
        @param y: the desired vertical location relative to the top left of the pop-up
        @type y: int
        @param active: the switch checked for whether a pop-up should be displayed or not
        @type active: bool
        """
        # Main text attributes
        self.text = text
        self.text_color = text_color
        self.text_size = text_size
        self.font = pygame.font.SysFont('Consolas', self.text_size)
        self.text_image = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_image.get_rect()

        # Left text/button attributes
        self.text_left = text_left
        self.text_left_background = settings.DARK_GRAY
        self.text_left_color = text_left_color
        self.text_left_size = text_left_size
        self.text_left_font = pygame.font.SysFont('Consolas', self.text_left_size)
        self.text_left_image = self.text_left_font.render(self.text_left, True, self.text_left_color)
        self.text_left_rect = self.text_left_image.get_rect()

        # Right text/button attributes
        self.text_right = text_right
        self.text_right_background = settings.DARK_GRAY
        self.text_right_color = text_right_color
        self.text_right_size = text_right_size
        self.text_right_font = pygame.font.SysFont('Consolas', self.text_right_size)
        self.text_right_image = self.text_right_font.render(self.text_right, True, self.text_right_color)
        self.text_right_rect = self.text_right_image.get_rect()

        # Middle text/button attributes
        self.text_middle = text_middle
        self.text_middle_background = settings.DARK_GRAY
        self.text_middle_color = text_middle_color
        self.text_middle_size = text_middle_size
        self.text_middle_font = pygame.font.SysFont('Consolas', self.text_right_size)
        self.text_middle_image = self.text_middle_font.render(self.text_middle, True, self.text_middle_color)
        self.text_middle_rect = self.text_middle_image.get_rect()

        # Button attributes
        self.active = active
        self.border_color = border_color
        self.hover = False
        self.hover_left = False
        self.hover_right = False
        self.hover_middle = False
        self.height_buffer = 30
        self.simple_buffer = 10
        self.width_buffer = 20
        # The design formula, below, to help all code format correctly (draw out to understand)
        self.special_width_1_3 = (self.text_left_rect.width * (1 / 3))
        self.width = self.text_rect.width + self.width_buffer
        self.height = self.text_rect.height + (self.text_left_rect.height / 2) + (self.text_right_rect.height / 2) \
                      + self.height_buffer
        self.x = x - self.width / 2
        self.y = y - self.height / 2
        self.image = pygame.Surface((self.width, self.height))
        self.name = name
        self.image.fill(background_color)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Set locations after images are set up
        text_height_for_y = self.y + self.text_rect.height + 20
        self.special_width_2_3 = (self.text_left_rect.width * (2 / 3))
        self.text_rect.x = self.x + self.simple_buffer
        self.text_rect.y = self.y + self.simple_buffer
        self.text_left_rect.x = self.text_rect.x
        self.text_left_rect.y = text_height_for_y
        self.text_right_rect.x = self.text_rect.x + self.text_rect.width - self.text_right_rect.width
        self.text_right_rect.y = text_height_for_y
        self.text_middle_rect.x = (self.x + self.width / 2) - (self.text_middle_rect.width / 2)
        self.text_middle_rect.y = text_height_for_y

    def handle_events(self, engine_game: object, popups: list, event: object, mouse_pos: tuple):
        """
        A function that handles the events for pop-up messages wherever they may be running.

        @param engine_game:
        @type engine_game: object
        @param popups: a collection of all the pop-ups currently active due to user engagement
        @type popups: list
        @param event: a specific action that pygame recognized from the user
        @type event: object
        @param mouse_pos: a collection of points representing the position of the mouse when the event occurred
        @type mouse_pos: tuple
        @return: none
        @rtype: none
        """
        if self.active is True:
            # Check mouse pos for hover events
            if self.text_left_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.hover_left = True
                self.text_left_background = settings.DARK_GRAY
            else:
                self.hover_left = False
                self.text_left_background = settings.GRAY
            if self.text_right_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.hover_right = True
                self.text_right_background = settings.DARK_GRAY
            else:
                self.hover_right = False
                self.text_right_background = settings.GRAY
            if self.text_middle_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.hover_middle = True
                self.text_middle_background = settings.DARK_GRAY
            else:
                self.hover_middle = False
                self.text_middle_background = settings.GRAY
            self.text_left_image = self.text_left_font.render(self.text_left, True, self.text_left_color)
            self.text_right_image = self.text_right_font.render(self.text_right, True, self.text_right_color)
            self.text_middle_image = self.text_middle_font.render(self.text_middle, True, self.text_middle_color)

            # Check mouse interaction with buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.text_left_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if self.text_left == 'Ok' or self.text_left == 'Okay':
                        self.active = False
                        # TODO: Customize popup's for errors and maybe create a log with error's from certain popups.
                        # CONT: Do the same for the menu popups
                    elif self.text_left == 'Exit':
                        engine_game.running = False
                    elif self.text_left == 'Exit To Main Menu':
                        self.active = False
                        engine_game.running = False
                        engine_game.state = 'Exit_To_Menu'
                if self.text_right_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if self.text_right == 'Back' or self.text_right == 'Cancel' or self.text_right == 'Close':
                        self.active = False
                    # TODO: Make sure it exits pygame completely.
                    elif self.text_right == 'Exit To Desktop':
                        self.active = False
                        engine_game.sprites_all.empty()
                        engine_game.sprites_walls.empty()
                        engine_game.running = False
                        engine_game.state = 'Exit_To_Desktop'
                if self.text_middle_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if self.text_middle == 'Back' or self.text_middle == 'Cancel' or self.text_middle == 'Close' \
                            or self.text_middle == 'Okay':
                        self.active = False

    def update(self):
        """
        A function to check various conditions for the menu popup and prepare for next interaction

        @return: none
        @rtype: none
        """
        pass

    def draw(self, screen: object):
        """
        A function to draw a pop-up message's design and text to the screen for the user to interact with.

        @param screen: the display that will have the pop-up message's design and text pushed to
        @type screen: object
        @return: none
        @rtype: none
        """
        if self.active:
            # Draw layout
            screen.blit(self.image, self.rect)

            tweak_pixel_left = 3  # Used to tweak the button box
            tweak_pixel_right = 1  # Used to tweak the button box

            texts = [self.text_left, self.text_middle, self.text_right]
            backgrounds = [self.text_left_background, self.text_middle_background, self.text_right_background]
            rects = [self.text_left_rect, self.text_middle_rect, self.text_right_rect]
            for text, background, rect in zip(texts, backgrounds, rects):
                if text != '':
                    pygame.draw.polygon(screen, background,
                                        ((rect.x - tweak_pixel_left, rect.y),
                                         (rect.x - tweak_pixel_left, rect.y + rect.height),
                                         (rect.x + rect.width + tweak_pixel_right, rect.y + rect.height),
                                         (rect.x + rect.width + tweak_pixel_right, rect.y)))
                    pygame.draw.lines(screen, self.border_color, True,
                                      ((rect.x - tweak_pixel_left, rect.y),
                                       (rect.x - tweak_pixel_left, rect.y + rect.height),
                                       (rect.x + rect.width + tweak_pixel_right, rect.y + rect.height),
                                       (rect.x + rect.width + tweak_pixel_right, rect.y)))

            # Draw box around the whole popup
            pygame.draw.lines(screen, self.border_color, True, ((self.rect.x, self.rect.y),
                                                                (self.rect.x, self.rect.y + self.height),
                                                                (self.rect.x + self.width, self.rect.y + self.height),
                                                                (self.rect.x + self.width, self.rect.y)))

            # Draw the popup information
            screen.blit(self.text_image, self.text_rect)
            screen.blit(self.text_left_image, self.text_left_rect)
            screen.blit(self.text_right_image, self.text_right_rect)
            screen.blit(self.text_middle_image, self.text_middle_rect)


class MenuAnimation(object):
    """Class. Used to handle menu screen animations and when to draw them."""
    def __init__(self, image_count: int, image_directory: str, image_name: str, image_timer_trigger: int,
                 x: int, y: int):
        self.active = False  # Triggered to true when the animation is acalled into play
        self.images = []
        for i in range(1, image_count):
            self.images.append(pygame.image.load(image_directory + image_name + str(i) + '.png').convert_alpha())
        # Initialize important variables
        self.image = self.images[0]
        self.image_count = image_count
        self.image_directory = image_directory
        self.image_index = 0
        self.image_name = image_name
        self.image_rect = self.image.get_rect()
        self.image_rect.x = x
        self.image_rect.y = y
        self.image_timer = 0
        self.image_timer_trigger = image_timer_trigger

    def draw(self, screen):
        screen.blit(self.image, self.image_rect)

    def update(self):
        if self.image_timer >= self.image_timer_trigger:
            self.image_timer = 0
            # Update animation
            if len(self.images) - 1 > self.image_index:
                self.image_index += 1
            else:
                self.image_index = 0
        else:
            self.image_timer += 1
        # Update image
        self.image = self.images[self.image_index]


class MenuHandler(object):
    """Class. Used to handle specific events with the menu, display special
    visuals, and more."""
    def __init__(self, engine_menu: object):
        """
        Constructor. Used to initialize a handler object for parsing important actions and information from
                     the user.
        Note: Don't forget to call init_finish() when you're ready to start using the MenuHandler class.

        @param engine_menu: the engine which controls the network of the menu the game is originally started from
        @type engine_menu: object
        """
        self.engine_menu = engine_menu
        self.mouse_pos = ()

        # Initialize menu animations
        self.menu_anim_banners = object
        self.menu_anim_title = object
        # Initialize interact-able objects
        self.obj_interact_book_exit = MenuObjectInteract('Book_Exit', pygame.Rect(835, 705, 35, 105))
        self.obj_interact_book_options = MenuObjectInteract('Book_Options', pygame.Rect(800, 705, 35, 105))
        self.obj_interact_computer = MenuObjectInteract('Computer_Feedback', pygame.Rect(520, 750, 90, 65))
        self.obj_interact_teleporter = MenuObjectInteract('Teleporter_Load', pygame.Rect(690, 700, 90, 110))
        self.objs_interact = [self.obj_interact_book_exit, self.obj_interact_book_options, self.obj_interact_computer,
                              self.obj_interact_teleporter]

    def handle_events(self, event: object):
        """
        A function to handle different events in the via the menu.

        @param event: the pygame triggered event via the mouse/keyboard inputs
        @return: none
        @rtype: none
        """
        try:
            self.mouse_pos = pygame.mouse.get_pos()
            # Needed to fix the mouse position after the screen is scaled
            self.mouse_pos = (self.mouse_pos[0] / settings.RES_WIDTH_RATIO, self.mouse_pos[1] / settings.RES_HEIGHT_RATIO)

            # TODO: Create a popup asking if they're sure they want to exit
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pass
                    # self.running = False

                # Handle special character interaction with menu objects
                # NOTE: Might want to just port this over to the character so in-game object interaction
                # NOTE: can take place without an entirely new system.
                elif event.key == pygame.K_w:
                    char_center_x = self.engine_menu.character_sample.rect.x \
                             + (self.engine_menu.character_sample.rect.width / 2)
                    for obj in self.objs_interact:
                        # Check char location and determine interaction
                        if obj.rect.x < char_center_x < obj.rect.x + obj.rect.width:
                            # Change char animation set motion to load new assets for user interaction
                            if obj.name == 'Book_Exit':
                                self.engine_menu.character_sample.state = 'Interacting_With_Exit'
                                self.engine_menu.character_sample.state_changed = True
                            elif obj.name == 'Book_Options':
                                self.engine_menu.character_sample.state = 'Interacting_With_Options'
                                self.engine_menu.character_sample.state_changed = True
                            elif obj.name == 'Computer_Feedback':
                                self.engine_menu.character_sample.state = 'Interacting_With_Feedback'
                                self.engine_menu.character_sample.state_changed = True
                                self.engine_menu.state = 'Feedback'
                                self.engine_menu.running = False
                            elif obj.name == 'Teleporter_Load':
                                self.engine_menu.character_sample.state = 'Interacting_With_Load'
                                self.engine_menu.character_sample.state_changed = True
                            elif obj.name == 'Help_obj':  # TODO: Create this object
                                self.engine_menu.character_sample.state = 'Interacting_With_Help'
                                self.engine_menu.character_sample.state_changed = True
                elif event.key == pygame.K_s:
                    state = self.engine_menu.character_sample.state
                    if 'Interacting' in state:
                        self.engine_menu.running = False
                        self.engine_menu.state = 'Main'
                        self.engine_menu.character_sample.state = 'Idle'
                        self.engine_menu.character_sample.state_changed = True

            # Handle sample char switching interaction of objects
            state = self.engine_menu.character_sample.state
            if 'Interacting' in state:
                char_center_x = self.engine_menu.character_sample.rect.x
                # Display interact-able rect
                if self.obj_interact_computer.rect.x > char_center_x < \
                        (self.obj_interact_computer.rect.x + self.obj_interact_computer.rect.width):
                    self.engine_menu.character_sample.state = 'Idle'
                    self.engine_menu.character_sample.state_changed = True

            # Handle sample char screen switching
            # Going to create character, go to DIFFERENT screen
            if self.engine_menu.character_sample.rect.x < 0 and self.engine_menu.state != 'Create_Character':
                self.engine_menu.character_sample.rect.x = settings.SCREEN_WIDTH - 30
                self.engine_menu.state = 'Create_Character'
                self.engine_menu.running = False
            # Going to load, go to DIFFERENT screen
            elif 712 < self.engine_menu.character_sample.rect.x < 751 and self.engine_menu.state != 'Load' \
                    and self.engine_menu.character_sample.state == 'Interacting_With_Load':
                self.engine_menu.character_sample.rect.x = settings.SCREEN_WIDTH - 30
                self.engine_menu.state = 'Load'
                self.engine_menu.running = False
            # Going to feedback, STAY on menu screen
            # Going to options, STAY on menu screen
            # Going to help, STAY on menu screen
            # Going to exit, STAY on menu screen
            # TODO: Change, we should interact with objects on menu, not leave it except for loading
            # Going back to main FROM 'Create_Character' OR 'Load'
            elif self.engine_menu.character_sample.rect.x < 0 and (self.engine_menu.state == 'Create_Character'
                                                                   or self.engine_menu.state == 'Load'):
                # Place character in correct location, currently load is the only
                # interaction that changes the user's screen
                if self.engine_menu.character_sample.state == 'Interacting_With_Load':
                    self.engine_menu.character_sample.rect.x = 729  # Middle of loading pad
                self.engine_menu.character_sample.state = 'Idle'
                self.engine_menu.character_sample.rect.x = settings.SCREEN_WIDTH - 30
                self.engine_menu.state = 'Main'
                self.engine_menu.running = False

            # Handle extra events
            for button in self.engine_menu.buttons:
                button.handle_events(event, self.mouse_pos)
            for popup in self.engine_menu.popups:
                popup.handle_events(self.engine_menu, event, self.mouse_pos)
        except Exception:
            logging.info('Unexpected exception occured.', exc_info=True)

    def init_finish(self):
        """
        A function to import any other later information during a loading screen.

        @return: none
        @rtype: none
        """
        # Initialize assets for the load game menu screen
        self.menu_anim_banners = MenuAnimation(12, settings.DIR_SPRITES_UI + '/Menu/Load/',
                                               'Load_Banners_Outline_Large', 4, 7, 0)
        self.menu_anim_title = MenuAnimation(31, settings.DIR_SPRITES_UI + '/Menu/Title/',
                                             'Menu_Title_3X', 5, settings.SCREEN_WIDTH / 3 - 58,
                                             settings.SCREEN_HEIGHT / 4)

    def draw_sub_menu_visuals(self, screen: object):
        """
        A function to draw ui outlines and effects on all menus that come from the main menu.

        @param screen: the screen to blit the visuals to
        @type screen: object
        @return: none
        @rtype: none
        """
        # Set up top box for sub menus
        if self.engine_menu.state == 'Options' or self.engine_menu.state == 'Options_Video':
            pygame.draw.lines(screen, settings.DARK_GRAY, True, ((10, 25), (10, 65), (settings.SCREEN_WIDTH - 10, 65),
                                                                 (settings.SCREEN_WIDTH - 10, 25)), 1)

        self.draw_sub_menu_visuals_special(screen)

    def draw_sub_menu_visuals_special(self, screen: object):
        """
        A function to draw effects to show which dropdown selection the user is on, checks next to items that have been
        selected, and more.

        @param screen: the screen to blit the visuals to
        @type screen: object
        @return: none
        @rtype: none
        """
        # Create character
        if self.engine_menu.state == 'Create_Character':
            for btn in self.engine_menu.buttons:
                if (btn.name == 'Input_Create_Char_Name' or btn.name == 'Input_File_Save_Name') \
                        and btn.user_input != '' and btn.disabled is True:
                    # Display a check next to entered text
                    pygame.draw.lines(screen, settings.GREEN, False,
                                      ((btn.rect.x + btn.rect.width + 5, btn.rect.y + btn.rect.height - 7),
                                       (btn.rect.x + btn.rect.width + 8, btn.rect.y + btn.rect.height),
                                       (btn.rect.x + btn.rect.width + 10, btn.rect.y)), 2)
        # Load
        # Options controls
        # Options game
        # Options sound
        # Options video
        if self.engine_menu.state == 'Options_Video':
            for button in self.engine_menu.buttons:
                if button.name == 'Options_Video_Resolution' and button.hover:
                    pygame.draw.line(screen, settings.DARK_GRAY, (410, 60),
                                     (410, button.rect.y + button.rect.height / 2))
                    pygame.draw.line(screen, settings.DARK_GRAY, (410, button.rect.y + button.rect.height / 2),
                                     (350, button.rect.y + button.rect.height / 2))
                elif button.name == 'Options_Video_Graphics' and button.hover:
                    pygame.draw.line(screen, settings.DARK_GRAY, (410, 60),
                                     (410, button.rect.y + button.rect.height / 2))
                    pygame.draw.line(screen, settings.DARK_GRAY, (410, button.rect.y + button.rect.height / 2),
                                     (350, button.rect.y + button.rect.height / 2))
                else:
                    # TODO: Can this be fixed by just taking the for loop out and changing the below conditional statements to
                    # CONT: more elif statements?
                    for button in self.engine_menu.buttons:
                        # Show selection visuals if the dropdown buttons are active
                        if button.name[:7] == 'New_Res' and button.hover and button.active:
                            pygame.draw.line(screen, settings.DARK_GRAY, (410, 60),
                                             (410, button.rect.y + button.rect.height / 2))
                            pygame.draw.line(screen, settings.DARK_GRAY, (410, button.rect.y + button.rect.height / 2),
                                             (350, button.rect.y + button.rect.height / 2))
                        elif button.name[:15] == 'Choice_Graphics' and button.hover and button.active:
                            pygame.draw.line(screen, settings.DARK_GRAY, (410, 60),
                                             (410, button.rect.y + button.rect.height / 2))
                            pygame.draw.line(screen, settings.DARK_GRAY, (410, button.rect.y + button.rect.height / 2),
                                             (350, button.rect.y + button.rect.height / 2))
        # Help
        # Feedback


class MenuObjectInteract(object):
    """
    Class. Creates the ability for the menu handler to easily interact with objects, that are
    already built into the art, and the user's character.
    """
    def __init__(self, name: str, rect: pygame.Rect):
        """
        Constructor. Used to set up an object that the menu handler can look at for information.

        @param name: the name of the object, such as 'Computer'
        @param rect: a pygame type that has an 'x', 'y', 'width', and a 'height'
        """
        self.name = name
        self.rect = rect


class MenuButton(object):
    """Class. Used to created different kinds of buttons for the ui system in the menu."""

    def __init__(self, engine_menu: object, name: str, text: str, text_size: int, text_color: tuple,
                 background_color: tuple, x: int, y: int, active: bool, disabled: bool, dropdown: bool,
                 special: bool):
        """
        Constructor. Used to initialize a button and set it up for being displayed.

        @param engine_menu: the engine which controls the network of the menu the game is originally started from
        @type engine_menu: object
        @param name: the name used to identify the button instead of creating another variable to represent the button from
                     others within a collection of buttons
        @type name: str
        @param text: the message that the button is trying to convey to the user
        @type text: str
        @param text_size: the text size of the message
        @type text_size: int
        @param text_color: the color that the message will be displayed in
        @type text_color: tuple
        @param background_color: the color behind all of the text and design on the pop-up
        @type background_color: tuple
        @param x: the desired horizontal location relative to the top left of the button
        @type x: int
        @param y: the desired vertical location relative to the top left of the button
        @type y: int
        @param active: the switch checked for whether a button should be displayed or not
        @type active: bool
        @param dropdown: the switch checked for whether a button should display it's values that the dropdown contains
        @type dropdown: bool
        @param special: the switch checked for whether a button should be displayed with special visuals or not
        @type special: bool
        """
        # Text attributes
        self.text = text
        self.text_color = text_color
        self.text_size = text_size
        self.font = pygame.font.Font('Bin/Fonts/Adventure_Merienda/Merienda-Regular.ttf', self.text_size)
        self.text_image = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_image.get_rect()
        self.text_rect.x = x
        self.text_rect.y = y

        # Button attributes
        self.active = active
        self.dropdown = dropdown
        self.disabled = disabled  # Usually False
        self.hover = False
        self.name = name
        self.special = special
        # TODO: Does image need a conver_alpha() on it?
        if background_color == settings.TRANSPARENT:
            # Create a transparent background on the text's image
            self.image = pygame.Surface((self.text_rect.width, self.text_rect.height), pygame.SRCALPHA, 32)
        else:
            self.image = pygame.Surface((self.text_rect.width, self.text_rect.height))
            self.image.fill(background_color)
        self.rect = pygame.Rect(x, y, self.text_rect.width, self.text_rect.height)

        # Misc
        self.engine_menu = engine_menu

    def handle_events(self, event: object, mouse_pos: tuple):
        """
        A function that handles the events for the buttons in the menu section of the game.

        @param event: a specific action that pygame recognized from the user
        @type event: object
        @param mouse_pos: a collection of points representing the position of the mouse when the event occurred
        @type mouse_pos: tuple
        @return: none
        @rtype: none
        """
        # TODO: Fix all button references to self.engine_menu.buttons and make sure it works
        buttons = self.engine_menu.buttons
        # Check mouse pos for hover events
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.hover = True
            # Handle special buttons via their name
            if self.special:
                self.font.set_underline(True)
        else:
            self.hover = False
            self.font.set_underline(False)
        self.text_image = self.font.render(self.text, True, self.text_color)

        # Check mouse interaction with buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                # Check state of menu
                if self.engine_menu.state == 'Main':
                    # Main menu buttons
                    if self.name == 'Start':
                        self.engine_menu.state = 'Create_Character'
                        self.engine_menu.running = False
                    elif self.name == 'Load':
                        self.engine_menu.state = 'Load'
                        self.engine_menu.running = False
                    elif self.name == 'Options':
                        self.engine_menu.state = 'Options'
                        self.engine_menu.running = False
                    elif self.name == 'Help':
                        self.engine_menu.state = 'Help'
                        self.engine_menu.running = False
                    elif self.name == 'Feedback':
                        self.engine_menu.state = 'Feedback'
                        self.engine_menu.running = False
                elif self.engine_menu.state == 'Create_Character':
                    # Character creation buttons
                    if self.name == 'Submit':
                        for btn in buttons:
                            if btn.name == 'Input_Create_Char_Name':
                                if btn.user_input != '':
                                    btn.disabled = True
                                    self.engine_menu.character_name = btn.user_input
                                    for button in buttons:
                                        if button.name == 'Input_File_Save_Name':
                                            if button.user_input != '':
                                                button.disabled = True
                                                self.engine_menu.file_load_save = button.user_input
                                                # Exit menu so the new game can start
                                                self.engine_menu.state = 'Load_New'
                                                self.engine_menu.running = False
                                else:
                                    # TODO: Add a popup telling the user to give a character name
                                    pass
                elif self.engine_menu.state == 'Load':
                    if self.name == 'Load_Cat_Saves':
                        # Open saves dropdown if clicked and disabled
                        if self.dropdown is True and self.disabled is True:
                            self.disabled = False
                            drop_down_offset = 80
                            padding = 5
                            saves_total = 0
                            # Grab all save files from folder
                            save_files = os.listdir('Bin/Saves/')
                            for save_file in save_files:
                                # Basic setup for proper values
                                new_text = save_file.strip('.py')
                                new_text_image = self.font.render(new_text, True, self.text_color)
                                new_text_rect = new_text_image.get_rect()
                                # Send it
                                new_x = 20
                                new_y = drop_down_offset + padding
                                new_button = MenuButton(self.engine_menu, 'Old_Save_' + str(saves_total), new_text, self.text_size,
                                                        self.text_color, (106, 49, 202), new_x, new_y, True, False, False, True)
                                # Check if button already exists
                                if new_button not in buttons:
                                    buttons.append(new_button)
                                drop_down_offset += self.text_size + padding
                                saves_total += 1
                        # Close saves dropdown if clicked and enabled
                        else:
                            self.disabled = True
                            new_buttons = []
                            for btn in buttons:
                                if btn.name[:8] != 'Old_Save':
                                    new_buttons.append(btn)
                                else:
                                    btn.active = False
                                    btn.disabled = True
                            buttons = new_buttons
                    elif self.name[:8] == 'Old_Save' and self.active is True and self.disabled is False:
                        for btn in buttons:
                            if btn.name == 'Submit':
                                btn.disabled = False
                        self.engine_menu.file_load_save = self.text
                    elif self.name == 'Submit' and self.disabled is False:
                        self.engine_menu.state = 'Load_Save'
                        self.engine_menu.running = False
                elif self.engine_menu.state == 'Options':
                    # Handle options buttons
                    if self.name == 'Options_Cat_Video':
                        self.engine_menu.state = 'Options_Video'
                        self.engine_menu.running = False
                elif self.engine_menu.state == 'Options_Video':
                    # Handle video resolution dropdown bar
                    if self.name == 'Options_Video_Resolution':
                        # Close resolutions dropdown if it's clicked on and not disabled
                        if self.dropdown is True and self.disabled is False:
                            self.disabled = True
                            # Close other resolution buttons in dropdown
                            new_buttons = []
                            for btn in buttons:
                                if btn.name[:7] != 'New_Res':
                                    new_buttons.append(btn)
                                else:
                                    btn.active = False
                                    btn.disabled = True
                            buttons = new_buttons
                        # Open resolutions dropdown if it's clicked on and disabled
                        else:
                            self.disabled = False
                            drop_down_offset = 0
                            padding = 5
                            total_resolutions = 0
                            # Grab supported resolutions
                            resolution_modes = pygame.display.list_modes(32)
                            for res in resolution_modes:
                                # Basic setup for proper values of new resolutions for dropdown
                                new_text = '(' + str(res[0]) + ', ' + str(res[1]) + ')'
                                new_text_image = self.font.render(new_text, True, self.text_color)
                                new_text_rect = new_text_image.get_rect()
                                # Send it
                                new_x = self.text_rect.x + self.text_rect.width - new_text_rect.width
                                new_y = self.text_rect.y + self.text_rect.height + drop_down_offset + padding
                                new_button = MenuButton(self.engine_menu, 'New_Res_' + str(total_resolutions), '(' + str(res[0]) + ', ' + str(res[1]) + ')', self.text_size,
                                                        self.text_color, settings.WHITE, new_x, new_y, True, False, False, False)
                                # Check if button already exists
                                if new_button not in buttons:
                                    buttons.append(new_button)
                                drop_down_offset += self.text_size + padding
                                total_resolutions += 1
                            # TODO: Create what's below
                            if total_resolutions > 5:
                                # Create a scroll wheel
                                pass
                            else:
                                # Don't create a scroll wheel
                                pass
                    elif self.name[:7] == 'New_Res' and self.active is True and self.disabled is False:
                        self.disabled = True
                        # Change values based on clicked button
                        strip_res_text = self.text.strip('()')
                        split_res = strip_res_text.split(', ')
                        # TODO: Fix the resolution use in the below code in order to better reflect option changes
                        # CONT: according involving the self.engine_menu.engine_handler.update_settings()
                        self.engine_menu.engine_handler.update_settings('WINDOW_WIDTH', split_res[0], 'int')
                        self.engine_menu.engine_handler.update_settings('WINDOW_HEIGHT', split_res[1], 'int')
                        self.engine_menu.engine_handler.update_settings('RES_WIDTH_RATIO', str((int(split_res[0]) / settings.SCREEN_WIDTH)), 'int')
                        self.engine_menu.engine_handler.update_settings('RES_HEIGHT_RATIO', str((int(split_res[1]) / settings.SCREEN_HEIGHT)), 'int')
                        self.engine_menu.engine_handler.update_settings('RES_CHANGED', True, 'bool')

                        # TODO: Reset screen and window to the appropriate resolution below. The line might not be correct
                        self.engine_menu.window = pygame.display.set_mode((self.engine_menu.engine_handler.gather_engine_info(self.engine_menu.engine_game, 'calculate_window')))
                        # Close all buttons on resolution drop down
                        new_buttons = []
                        for btn in buttons:
                            if btn.name[:7] == 'New_Res':
                                btn.active = False
                                btn.toggled = False
                            elif btn.name == 'Options_Video_Resolution':
                                btn.text = 'Resolution: [' + strip_res_text + ']'
                            else:
                                new_buttons.append(btn)
                        buttons = new_buttons
                    elif self.name == 'Options_Video_Graphics':
                        # Close graphics dropdown if it's clicked on and not disabled
                        if self.dropdown is True and self.disabled is False:
                            self.disabled = True
                            # Close other resolution buttons in dropdown
                            new_buttons = []
                            for btn in buttons:
                                if btn.name[:15] != 'Choice_Graphics':
                                    new_buttons.append(btn)
                                else:
                                    btn.active = False
                                    btn.disabled = True
                            buttons = new_buttons
                        # Open graphics dropdown if it's clicked on and disabled
                        else:
                            self.disabled = False
                            # Handle video graphics dropdown bar
                            drop_down_offset = 0
                            padding = 5
                            graphics_setting = ['Low', 'Medium', 'High', 'Extreme']
                            for setting in graphics_setting:
                                # Basic setup for proper values of each graphics setting in the dropdown
                                button_text = '(' + setting + ')'
                                button_image = self.font.render(button_text, True, settings.DARK_GRAY)
                                button_rect = button_image.get_rect()
                                button_x = self.rect.x + self.rect.width - button_rect.width
                                button_y = self.rect.y + self.rect.height + drop_down_offset + padding
                                button_graphics_setting = MenuButton(self.engine_menu, 'Choice_Graphics_' + setting, '(' + setting + ')', 20,
                                                                     self.text_color, settings.WHITE, button_x, button_y, True, False, False, False)
                                if button_graphics_setting not in buttons:
                                    buttons.append(button_graphics_setting)
                                drop_down_offset += self.text_size + padding
                    elif self.name[:15] == 'Choice_Graphics' and self.active is True and self.disabled is False:
                        self.disabled = True
                        # Change values in settings based on clicked button
                        strip_graphics_text = self.text.strip('()')
                        self.engine_menu.engine_handler.update_settings('GRAPHICS', strip_graphics_text, 'string')
                        new_buttons = []
                        for btn in buttons:
                            if btn.name[:15] == 'Choice_Graphics':
                                btn.active = False
                                btn.toggled = False
                            # Update the options video graphics with the new selected setting
                            elif btn.name == 'Options_Video_Graphics':
                                btn.text = 'Graphics: [' + strip_graphics_text + ']'
                            else:
                                new_buttons.append(btn)
                        buttons = new_buttons
                elif self.engine_menu.state == 'Feedback':
                    # TODO: Create button handling for feedback sub-menu
                    pass
                # Misc buttons
                if self.name == 'Back':
                    if self.engine_menu.state == 'Create_Character' or self.engine_menu.state == 'Load' or self.engine_menu.state == 'Options' or self.engine_menu.state == 'Help'\
                            or self.engine_menu.state == 'Feedback':
                        self.engine_menu.state = 'Main'
                        self.engine_menu.running = False
                    elif self.engine_menu.state == 'Options_Video':
                        self.engine_menu.state = 'Options'
                        self.engine_menu.running = False
                elif self.name == 'Exit':
                    self.engine_menu.state = 'Exit'
                    self.engine_menu.running = False

    def update(self):
        """
        A function to check various conditions for the button and prepare for next interaction

        @return: none
        @rtype: none
        """
        pass
    
    def draw(self, screen: object):
        """
        A function to draw buttons to the screen when called upon to do so, usually from a loop that iterates through
        a collection of buttons.

        @param screen: the display that the button is applied to
        @type screen: object
        @return: none
        @rtype: none
        """
        if self.active:
            screen.blit(self.image, self.rect)
            screen.blit(self.text_image, self.text_rect)


class MenuInteractiveText(object):
    """Class. Used to represent a button, with input, inside of the editor that can be displayed."""
    def __init__(self, engine_menu: object, name: str, text_ask: str, x: int, y: int, max_width: int, width=50, height=50):
        """
        Constructor. Used to initialize the button's attributes.

        @param engine_menu: the engine which controls the network of the menu when its ran
        @type engine_menu: object
        @param name: the name that represents a specific button
        @type name: str
        @param text_ask: the text that the button will you to ask questions
        @type text_ask: str
        @param x: the desired location horizontally for the button regarding the top left of it
        @type x: int
        @param y: the desired location vertically for the button regarding the top left of it
        @type y: int
        @param width: the total width from left to right on the button
        @param height: the total height from bottom to top on the button
        """
        self._max_width = max_width
        self.engine_menu = engine_menu
        # Button attributes
        self.FONT = pygame.font.SysFont('Consolas', 15)  # depreciated
        self.font_ui = pygame.font.Font('Bin/Fonts/Adventure_Merienda/Merienda-Regular.ttf', 15)
        self.active = True
        self.disabled = True
        self.image = pygame.Surface((width, height))
        self.image.fill(settings.DARK_GRAY)
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.user_input = ''
        self.text_ask = text_ask
        self.text_image = self.font_ui.render(self.text_ask, True, settings.UI_FEEDBACK_TEXT)
        self.text_rect = pygame.Rect(x + 5, y + 5, width / 2, height / 2)

    def handle_events(self, event: object, mouse_pos: tuple):
        """
        A function to handle the actions of the user in regards to the button.

        @param event: the event that pygame was able to recognize based off of user interaction
        @type event: object
        @param mouse_pos: the position of the mouse when this function was called
        @type mouse_pos: tuple
        @return: none
        @rtype: none
        """
        # Handle the description for feedback
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and event.type == pygame.MOUSEBUTTONDOWN \
                and self.name == 'Input_Feedback_Description':
            if self.disabled is True:
                self.disabled = False
            else:
                self.disabled = True
        elif not self.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and event.type == pygame.MOUSEBUTTONDOWN \
                and self.name == 'Input_Feedback_Description':
            if self.disabled is True:
                self.disabled = False
            else:
                self.disabled = True
        if self.active and event.type == pygame.KEYDOWN and self.name == 'Input_Feedback_Description'\
                and self.disabled is False:
            if event.key == pygame.K_RETURN:
                # TODO: Finish cleansing work

                # Use input
                self.engine_menu.feedback_save_description = self.user_input
                self.disabled = True
            elif event.key == pygame.K_ESCAPE:
                self.user_input = ''
                self.disabled = True
            elif event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif event.key == pygame.K_TAB:
                self.disabled = True
                for button in self.engine_menu.buttons:
                    if button.name == 'Input_Feedback_Description':
                        button.disabled = False
            else:
                if self.user_input == self.text_ask:
                    self.user_input = ''
                # To get characters we use event.unicode
                self.user_input += event.unicode
            # Change the new text of the box to the user's input
            self.text_image = self.font_ui.render(self.text_ask + self.user_input, True, settings.UI_FEEDBACK_TEXT)

        # Handle events for buttons regarding character creation
        # NOTE: I separated these to further show the dire need to better modularize
        # NOTE: the buttons to be independent, self reliant, and get out and update information
        # NOTE: on itself only. It doesn't need to handle events of other buttons
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and event.type == pygame.MOUSEBUTTONDOWN\
                and (self.name == 'Input_Create_Char_Name' or self.name == 'Input_File_Save_Name'):
            # Only allow one box enabled at a time
            if self.name == 'Input_Create_Char_Name':
                for button in self.engine_menu.buttons:
                    if button.name == 'Input_File_Save_Name':
                        if self.disabled is True and button.disabled is True:
                            self.disabled = False
                        elif self.disabled is True and button.disabled is False:
                            self.disabled, button.disabled = False, True
                        elif self.disabled is False and button.disabled is True:
                            self.disabled = True
            elif self.name == 'Input_File_Save_Name':
                for button in self.engine_menu.buttons:
                    if button.name == 'Input_Create_Char_Name':
                        if self.disabled is True and button.disabled is True:
                            self.disabled = False
                        elif self.disabled is True and button.disabled is False:
                            self.disabled, button.disabled = False, True
                        elif self.disabled is False and button.disabled is True:
                            self.disabled = True
            # print('[Debug - Info]: ' + self.name + ' self.disabled = ' + str(self.disabled))
        # Gather input if the character name button is not disabled
        if self.active and event.type == pygame.KEYDOWN and self.name == 'Input_Create_Char_Name'\
                and self.disabled is False:
            if event.key == pygame.K_RETURN:
                # TODO: Finish cleansing work

                # Use input
                self.engine_menu.character_name = self.user_input
                self.disabled = True
            elif event.key == pygame.K_ESCAPE:
                self.user_input = ''
                self.disabled = True
            elif event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif event.key == pygame.K_TAB:
                self.disabled = True
                for button in self.engine_menu.buttons:
                    if button.name == 'Input_File_Save_Name':
                        button.disabled = False
            else:
                if self.user_input == self.text_ask:
                    self.user_input = ''
                # To get characters we use event.unicode
                self.user_input += event.unicode
            # Change the new text of the box to the user's input
            self.text_image = self.font_ui.render(self.text_ask + self.user_input, True, settings.UI_FEEDBACK_TEXT)
        # Gather input if the file save button is not disabled
        elif self.active and event.type == pygame.KEYDOWN and self.name == 'Input_File_Save_Name'\
                and self.disabled is False:
            if event.key == pygame.K_RETURN:
                # TODO: Finish cleansing work

                # Use input
                self.engine_menu.load_save_file = self.user_input
                self.disabled = True
            elif event.key == pygame.K_ESCAPE:
                self.user_input = ''
                self.disabled = True
            elif event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            # TODO: Fix the tab below. Currently the pressing of tab from the character name input button
            # CONT: also affects the event.key registering inside this button.
            elif event.key == pygame.K_TAB:
                pass
            else:
                if self.user_input == self.text_ask:
                    self.user_input = ''
                if event.key != pygame.K_TAB:
                    # To get characters we use event.unicode
                    self.user_input += event.unicode
            # Change the new text of the box to the user's input
            self.text_image = self.font_ui.render(self.text_ask + self.user_input, True, settings.UI_FEEDBACK_TEXT)

    def update(self):
        """
        A function to check various conditions for the button and prepare for next interaction

        @return: none
        @rtype: none
        """
        # Resize the box if the text is too long.
        width = max(self._max_width, self.text_image.get_width() + 10)
        if width > self._max_width:
            width = self._max_width
        self.rect.w = width
        self.image = pygame.Surface((width, self.rect.height))
        self.image.fill(settings.DARK_GRAY)

        # Limiting text size beyond max width
        if self.text_image.get_width() > self._max_width - 5:
            self.user_input = self.user_input[:-1]
            self.text_image = self.font_ui.render(self.text_ask + self.user_input, True, settings.UI_FEEDBACK_TEXT)

    def draw(self, screen: object):
        """
        A function to draw the buttons to the display

        @param screen: the display that has buttons and other visuals drawn to it
        @type screen: object
        @return: none
        @rtype: none
        """
        if self.active:
            screen.blit(self.image, self.rect)
            screen.blit(self.text_image, self.text_rect)
            # Line going around button
            # pygame.draw.lines(screen, settings.WHITE, True, (
            # (self.rect.x, self.rect.y),
            # (self.rect.x, self.rect.y + self.rect.height),
            # (self.rect.x + self.rect.width, self.rect.y + self.rect.height),
            # (self.rect.x + self.rect.width, self.rect.y)))
            # Line going around text/input
            # pygame.draw.lines(screen, settings.WHITE, True, (
            # (self.rect.x + 2, self.rect.y + 2),
            # (self.rect.x + 2, self.rect.y + self.rect.height - 3),
            # (self.rect.x + self.rect.width - 3,
            #  self.rect.y + self.rect.height - 3),
            # (self.rect.x + self.rect.width - 3, self.rect.y + 2)))


class MenuPopUp(object):
    """Class. Used to initialize pop-up messages while the menu screen is being used by the user."""

    def __init__(self, name: str, text: str, text_size: int, text_color: tuple,
                 text_left: str, text_left_size: int, text_left_color: tuple,
                 text_right: str, text_right_size: int, text_right_color: tuple,
                 background_color: tuple, border_color: tuple, x: int, y: int,
                 active: bool):
        """
        Constructor. Used to set up a pop-up for displaying information to the user and then requiring some
        kind of input for the pop-up to disappear.

        @param name: the name used to identify the pop-up instead of creating another variable to represent the pop-up from
                     others within a collection of pop-ups
        @type name: str
        @param text: the overall message that the pop-up is trying to convey to the user
        @type text: str
        @param text_size: the text size of the overall message
        @type text_size: int
        @param text_color: the color that the overall message will be displayed in
        @type text_color: tuple
        @param text_left: the text option a user can pick that will be on the left side of the pop-up message
        @type text_left: str
        @param text_left_size: the text size of the left hand side option
        @type text_left_size: int
        @param text_left_color: the color that the left hand side option will be displayed in
        @type text_left_color: tuple
        @param text_right: the text option a user can pick that will be on the right side of the pop-up message
        @type text_right: str
        @param text_right_size: the text size of the right hand side option
        @type text_right_size: int
        @param text_right_color: the color that the right hand size option will be displayed in
        @type text_right_color: tuple
        @param background_color: the color behind all of the text and design on the pop-up
        @type background_color: tuple
        @param border_color: the color that will be on the border, or edge, of the pop-up
        @type border_color: tuple
        @param x: the desired horizontal location relative to the top left of the pop-up
        @type x: int
        @param y: the desired vertical location relative to the top left of the pop-up
        @type y: int
        @param active: the switch checked for whether a pop-up should be displayed or not
        @type active: bool
        """
        # Main text attributes
        self.text = text
        self.text_color = text_color
        self.text_size = text_size
        self.font = pygame.font.SysFont('Consolas', self.text_size)
        self.text_image = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_image.get_rect()

        # Left text/button attributes
        self.text_left = text_left
        self.text_left_background = settings.DARK_GRAY
        self.text_left_color = text_left_color
        self.text_left_size = text_left_size
        self.text_left_font = pygame.font.SysFont('Consolas', self.text_left_size)
        self.text_left_image = self.text_left_font.render(self.text_left, True, self.text_left_color)
        self.text_left_rect = self.text_left_image.get_rect()

        # Right text/button attributes
        self.text_right = text_right
        self.text_right_background = settings.DARK_GRAY
        self.text_right_color = text_right_color
        self.text_right_size = text_right_size
        self.text_right_font = pygame.font.SysFont('Consolas', self.text_right_size)
        self.text_right_image = self.text_right_font.render(self.text_right, True, self.text_right_color)
        self.text_right_rect = self.text_right_image.get_rect()

        # Button attributes
        self.active = active
        self.border_color = border_color
        self.hover = False
        self.hover_left = False
        self.hover_right = False
        self.height_buffer = 30
        self.simple_buffer = 10
        self.width_buffer = 20
        self.special_width_1_3 = (self.text_left_rect.width * (1 / 3))  # The design formula to help all code format correctly (draw out to understand)
        self.width = self.text_rect.width + self.width_buffer
        self.height = self.text_rect.height + (self.text_left_rect.height / 2) + (self.text_right_rect.height / 2) \
                      + self.height_buffer
        self.x = x - self.width / 2
        self.y = y - self.height / 2
        self.image = pygame.Surface((self.width, self.height))
        self.name = name
        self.image.fill(background_color)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Set locations after images are set up
        self.special_width_2_3 = (self.text_left_rect.width * (2 / 3))
        self.text_rect.x = self.x + self.simple_buffer
        self.text_rect.y = self.y + self.simple_buffer
        self.text_left_rect.x = self.text_rect.x
        self.text_left_rect.y = self.y + self.text_rect.height + 20
        self.text_right_rect.x = self.text_rect.x + self.text_rect.width - self.text_right_rect.width
        self.text_right_rect.y = self.y + self.text_rect.height + 20

    def handle_events(self, engine_menu: object, event: object, mouse_pos: tuple):
        """
        A function that handles the events for pop-up messages wherever they may be running.

        @param engine_menu: the engine which controls the network of the menu the game is originally started from
        @type engine_menu: object
        @param event: a specific action that pygame recognized from the user
        @type event: object
        @param mouse_pos: a collection of points representing the position of the mouse when the event occurred
        @type mouse_pos: tuple
        @return: none
        @rtype: none
        """
        if self.active:
            # Check mouse pos for hover events
            if self.text_left_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.hover_left = True
            else:
                self.hover_left = False

            if self.text_right_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.hover_right = True
            else:
                self.hover_right = False
            self.text_left_image = self.text_left_font.render(self.text_left, True, self.text_left_color)
            self.text_right_image = self.text_right_font.render(self.text_right, True, self.text_right_color)

            # Check mouse interaction with buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.text_left_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if self.text_left == 'Ok' or self.text_left == 'Okay':
                        self.active = False
                    elif self.text_left == 'Exit':
                        engine_menu.running = False
                if self.text_right_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    if self.text_right == 'Back' or self.text_right == 'Cancel' or self.text_right == 'Close' \
                            or self.text_right == 'Okay':
                        self.active = False

    def update(self):
        """
        A function to check various conditions for the menu popup and prepare for next interaction

        @return: none
        @rtype: none
        """
        pass

    def draw(self, screen: object):
        """
        A function to draw a pop-up message's design and text to the screen for the user to interact with.

        @param screen: the display that will have the pop-up message's design and text pushed to
        @type screen: object
        @return: none
        @rtype: none
        """
        # Draw layout
        screen.blit(self.image, self.rect)

        tweak_pixel_left = 3  # Used to tweak the button box
        tweak_pixel_right = 1  # Used to tweak the button box

        texts = [self.text_left, self.text_right]
        backgrounds = [self.text_left_background, self.text_right_background]
        rects = [self.text_left_rect, self.text_right_rect]
        for text, background, rect in zip(texts, backgrounds, rects):
            if text != '':
                # TODO: This uses the text_middle_background, we need it to be interactive
                pygame.draw.polygon(screen, background,
                                    ((rect.x - tweak_pixel_left, rect.y),
                                     (rect.x - tweak_pixel_left, rect.y + rect.height),
                                     (rect.x + rect.width + tweak_pixel_right, rect.y + rect.height),
                                     (rect.x + rect.width + tweak_pixel_right, rect.y)))
                pygame.draw.lines(screen, self.border_color, True,
                                  ((rect.x - tweak_pixel_left, rect.y),
                                   (rect.x - tweak_pixel_left, rect.y + rect.height),
                                   (rect.x + rect.width + tweak_pixel_right, rect.y + rect.height),
                                   (rect.x + rect.width + tweak_pixel_right, rect.y)))

        # Draw box around the whole popup
        pygame.draw.lines(screen, self.border_color, True, ((self.rect.x, self.rect.y),
                                                            (self.rect.x, self.rect.y + self.height),
                                                            (self.rect.x + self.width, self.rect.y + self.height),
                                                            (self.rect.x + self.width, self.rect.y)))

        # Draw the popup information
        screen.blit(self.text_image, self.text_rect)
        screen.blit(self.text_left_image, self.text_left_rect)
        screen.blit(self.text_right_image, self.text_right_rect)
        screen.blit(self.text_middle_image, self.text_middle_rect)


class TileSpriteInit(pygame.sprite.Sprite):
    """Class. Used to create sprites from game file images for later use and manipulation."""

    def __init__(self, engine_game: object, type: str, x: int, y: int, level_sub: int):
        """
        Constructor. Used to create a sprite and add it to the groups for drawing the level.

        @param engine_game: the engine which controls the network/functions of the game when it starts after the menu
        @type engine_game: object
        @param x: the desired horizontal location for the sprite to be initiated at
        @type x: int
        @param y: the desired vertical location for the sprite to be initiated at
        @type y: int
        @param level_sub: the sub level that the sprite is created for
        @type level_sub: int
        """
        # Width: 32 Height: 32
        # TODO: Create a hiearchy of elifs for 'g' or 'h' so that it takes less time to get through the loop
        # CONT: Is this coded effeciently?
        for i in range(10000):
            if type in engine_game.type_tiles:
                image = engine_game.type_tiles[type]
            else:
                return
        self.level_sub = level_sub
        self.groups = engine_game.sprites_walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class SnowHandler(object):
    """
    Class. Creates the ability to handle a bunch of particles for a snow
    effect.
    """
    # NOTE: Depreciated
    def __init__(self, main_menu: object, screen: object):
        """
        Constructor. used to set up the snowflakes before visualization.

        @param screen: the display that the snowflakes are pushed to
        @type screen: object
        """
        self.main_menu = main_menu
        self.screen = screen
        self.list_flakes = []
        for i in range(200):
            x = random.randrange(0, settings.SCREEN_WIDTH)
            y = random.randrange(0, settings.SCREEN_HEIGHT)
            self.list_flakes.append([x, y])

    def draw(self):
        """
        A function to cycle through the snowflakes, changing each one's
        position every loop, and then displaying them
        to the screen.

        @return:
        """
        # NOTE: Resource intensive AF 4 random numbers 200 times
        # TODO: Create snow animation rather than hard coding snowflakes and looping
        # Process each snow flake in the list
        for i in range(200):

            # Draw the snow flake
            pygame.draw.circle(self.screen, settings.DARK_GRAY,
                               self.list_flakes[i], 2)
            if self.main_menu.state == 'Main':
                self.list_flakes[i][0] += random.randrange(-5, 5)
                self.list_flakes[i][1] += random.randrange(1, 5)
            else:
                self.list_flakes[i][0] += random.randrange(-5, 5)
                self.list_flakes[i][1] += random.randrange(1, 5)

            # If the snow flake has moved off the bottom of the screen
            if self.list_flakes[i][1] > settings.SCREEN_HEIGHT:
                # Reset it just above the top
                y = random.randrange(-50, -10)
                self.list_flakes[i][1] = y
                # Give it a new x position
                x = random.randrange(0, settings.SCREEN_WIDTH)
                self.list_flakes[i][0] = x


class SpriteSheet(object):
    """Class. Used to grab images out of a sprite sheet."""
    def __init__(self, file_name: str):
        """
        Constructor. Used to initialize the SpriteSheet for later use.

        @param file_name: the full file location of the sprite sheet relative the engineLib.py file
        @type file_name: str
        """
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x: int, y: int, width: int, height: int):
        """
        Accessor. Grab a single image out of a larger sprite sheet Pass in the x, y location of the sprite
        and the width and height of the sprite.

        @param x: the starting position horizontally of a specific image relative to the top left of the sprite sheet
        @type x: int
        @param y: the starting position vertically of a specific image relative to the top left of the sprite sheet
        @type y: int
        @param width: the total width of the sprite relative to the desired x passed
        @type width: int
        @param height: the total height of the sprite relative to the desired y value
        @type height: int
        @return: a surface that hasn't been converted into a sprite but can still be displayed to the screen. This
                 can help with performance if used correctly as it will cut down on pygame calls, functions varaibles,
                 and functionality as a whole.
        @rtype: surface
        """
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
        image.set_colorkey(settings.BLACK)

        # Return the image
        return image
