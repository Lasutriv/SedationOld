import animations
import bindings
import character
import devLib
import engine
import settings

from shutil import copy2
from typing import NewType
import importlib
import os
import pygame
import random

# Map
# EngineHandler Class
# Handle Functions
# Level Functions
# Misc Functions
# Snowflake Class
# GameButton Class
# MenuButton Class
# MenuButtonInput Class
# MenuPopUp Class
# TileSpriteInit Class
# SpriteSheet Class

# Distinct Types #
# A group holds a collection of items just like a list. Groups for Pygame usually include sprites however.
Group = NewType('Group', list)


# noinspection PyDunderSlots
# ^-- Handles false warnings.
class EngineHandler:
    """Class. Used to handle in-game events, situations, and more."""
    def __init__(self):
        """
        Constructor. Used to initialize a handler object for parsing important actions and information from
                     the user.
        """
        # Dev tools
        self.DEV_time_handler = devLib.TimeHandler()

        # Game matrix variables
        self.screen_switch = False
        self.screen_switch_counter = settings.SCREEN_WIDTH
        self.screen_switch_counter_subtract = settings.SCREEN_WIDTH / 3.84
        self.screen_switch_dir = 'None'
        self.screen_switch_initial = True

        # Game ui animation variables
        self.images_health_bar_bubble = []
        animations.add_health_bar_bubble_images(self.images_health_bar_bubble)
        self.image_index_health_bar_bubble = 0
        self.image_health_bar_bubble = self.images_health_bar_bubble[self.image_index_health_bar_bubble]
        self.image_health_bar_bubble_rect = self.image_health_bar_bubble.get_rect()
        self.image_health_bar_bubble_rect.x = 5
        self.image_health_bar_bubble_rect.y = 65
        self.timer_health_bar_bubble = 0
        self.timer_health_bar_bubble_trigger = 5
        # Game ground animation and spritesheet variables

    # Handle Functions

    def handle_events(self, event: object, engine_game: object, character_main: object, sprites_all: Group, sprites_walls: Group):
        """
        A function that handles specific keys pressed while playing the game.

        @param event: events from pygame that are triggered systematically via the keys, mouse, joystick or other
        @type event: object
        @param engine_game: the engine which controls the network/functions of the game when it starts after the menu
        @type engine_game: object
        @param character_main: the character that the user is currently playing on
        @type character_main: object
        @param sprites_all: a collection of sprites representing every object or piece being displayed
        @type sprites_all: group
        @param sprites_walls: a collection of sprites representing every wall object being displayed
        @type sprites_walls: group
        @return: none
        @rtype: none
        """
        if event.type == pygame.KEYUP:
            # TODO: Remove the 't', 'y', and 'u' keys as they were for level testing
            if event.key == pygame.K_t:
                engine_game.level_current += 1
                if engine_game.level_current > settings.TOTAL_LEVELS:
                    engine_game.level_current = 1
                # Generate new level and refresh the characteristics of the level and redraw it
                sprites_all.empty()
                sprites_walls.empty()
                self.generate_level(engine_game, engine_game.level_current, engine_game.level_sub_current)
                sprites_all.add(character_main)
            if event.key == pygame.K_y:
                engine_game.level_sub_current -= 1
                if engine_game.level_sub_current < 1:
                    engine_game.level_sub_current = engine_game.levels_sub_current
                # Generate new level and refresh the characteristics of the level and redraw it
                sprites_all.empty()
                sprites_walls.empty()
                self.generate_level(engine_game, engine_game.level_current, engine_game.level_sub_current)
                sprites_all.add(character_main)
            if event.key == pygame.K_u:
                engine_game.level_sub_current += 1
                if engine_game.level_sub_current > engine_game.level_sub_total:
                    engine_game.level_sub_current = 1
                # Generate new level and refresh the characteristics of the level and redraw it
                sprites_all.empty()
                sprites_walls.empty()
                self.generate_level(engine_game, engine_game.level_current, engine_game.level_sub_current)
                sprites_all.add(character_main)
            # TODO: Create pause menu handling
            if event.key == pygame.K_ESCAPE:
                sprites_all.empty()
                sprites_walls.empty()
                engine_game.running = False
                print('[Debug - Info]: EngineHandler.handle_events() changed engine_game.running to False.')
            # TODO: Create inventory system
            if event.key == pygame.K_i:
                # Generate inventory menu
                pass

    # Level Functions

    def change_level(self, engine_game: object, direction: str):
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
            print('[Debug - Error]: File doesn\'t exist.')
            engine_game.running = False

    def generate_level_directions(self, engine_game: object):
        """
        A function to determine where the current exits are for the current level.
        It is called from the generate_level_matrix function to determine which levels
        are in each direction of where the current level is.

        @param engine_game: the engine which controls the network/functions of the game when it starts after the menu
        @type engine_game: object
        @return: none
        @rtype: none
        """
        engine_game.level_directions = ''
        level_matrix_location = [0, 0]
        row = 0
        # Find current location
        for line in engine_game.level_matrix:
            col = 0
            for data in line:
                if data == engine_game.level_sub_current:
                    level_matrix_location = [row, col]
                col += 1
            row += 1
        # Update current location and determine level directions
        engine_game.level_matrix_location = level_matrix_location
        try:
            # Check for level left
            if '######' != engine_game.level_matrix[level_matrix_location[0] - 0][level_matrix_location[1] - 1]:
                engine_game.level_directions += 'Left'
                engine_game.level_directions_left = engine_game.level_matrix[level_matrix_location[0] - 0][level_matrix_location[1] - 1]
            # Check for level above
            if '######' != engine_game.level_matrix[level_matrix_location[0] - 1][level_matrix_location[1] - 0]:
                engine_game.level_directions += 'Up'
                engine_game.level_directions_up = engine_game.level_matrix[level_matrix_location[0] - 1][level_matrix_location[1] - 0]
            # Check for level above
            if '######' != engine_game.level_matrix[level_matrix_location[0] + 0][level_matrix_location[1] + 1]:
                engine_game.level_directions += 'Right'
                engine_game.level_directions_right = engine_game.level_matrix[level_matrix_location[0] + 0][level_matrix_location[1] + 1]
            # Check for level above
            if '######' != engine_game.level_matrix[level_matrix_location[0] + 1][level_matrix_location[1] + 0]:
                engine_game.level_directions += 'Down'
                engine_game.level_directions_down = engine_game.level_matrix[level_matrix_location[0] + 1][level_matrix_location[1] + 0]
        except:
            print('[Ddebug - Error]: Probably popped out of range on level_matrix.')
        print('[Debug - Info]: Surrounding Levels -', engine_game.level_directions)

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
        self.generate_level_directions(engine_game)

    def generate_level_switch(self, engine_game: object, character_main: object, sprites_all: Group, sprites_walls: Group):
        """
        A function that visually swipes the current sub-level away from the new sub-level. The level and sub-level should
        already be defined by this point.

        @param engine_game: the engine which controls the network/functions of the game when it starts after the menu
        @type engine_game: object
        @param character_main: the character that the user is currently playing with
        @type character_main: object
        @param sprites_all: a collection of sprites representing all of the sprites in the game
        @type sprites_all: pygame.sprite.Group()
        @param sprites_walls: a collection of sprites representing the walls
        @type sprites_walls: pygame.sprite.Group()
        @return: none
        @rtype: none
        """
        # Setup level switching
        if self.screen_switch_counter < 0:
            self.screen_switch_counter = 0
        # TODO: Fix level switching speed by better use of function calls and data rewriting. Only write once and then move the already written sprites instead
        # CONT: of rewriting them in different locations
        # Generate whole level on first call
        if self.screen_switch_initial is True:
            for sprite in sprites_walls:
                sprite.kill()
            row_current = 0
            path_to_level = 'Levels/Level_' + str(engine_game.level_current) + '/Sub_Level_' + str(engine_game.level_sub_current) + '.txt'

            # Generate the new level across the screen
            try:
                with open(path_to_level, 'r') as file:
                    for line in file:
                        col_current = 0
                        data_from_file = line.split(' ')
                        for data in data_from_file:
                            self.generate_level_walls(engine_game, data, col_current, True, row_current)
                            col_current += 1
                        row_current += 1
            except FileNotFoundError:
                print('[Debug - Error]: File doesn\'t exist.')
                engine_game.running = False
            self.screen_switch_initial = False
        else:
            # TODO: BROKEN, FIX ASAP
            x, y = 0, 0
            # Move level acccordingly
            if self.screen_switch_dir is 'Down':
                y -= self.screen_switch_counter
            elif self.screen_switch_dir is 'Left':
                x -= self.screen_switch_counter
            elif self.screen_switch_dir is 'Right':
                x += self.screen_switch_counter
            elif self.screen_switch_dir is 'Up':
                y += self.screen_switch_counter
            for sprite in sprites_walls:
                sprite.rect.x = x
                sprite.rect.y = y
        # Reset variables once done switching sub levels and generate a new
        if self.screen_switch_counter == 0:
            self.screen_switch = False
            self.screen_switch_counter = settings.SCREEN_WIDTH
            self.screen_switch_dir = 'None'
            self.screen_switch_initial = True
            # Find new directions to exit based on new sub level
            self.generate_level_directions(engine_game)
        else:
            self.screen_switch_counter -= self.screen_switch_counter_subtract
        # Add back important sprites that aren't the background

    def generate_level_walls(self, engine_game: object, data: str, col_current: int, level_switch: bool, row_current: int):
        """
        A function for generating all of the specific walls and pieces in a level.

        @param engine_game: the engine which controls the network/functions of the game when it starts after the menu
        @type engine_game: object
        @param data: the desired sprite, representing a tile for walls, that will be used for generation
        @type data: str
        @param col_current: an integer representing the tile's column location within the sub-level tile matrix
        @type col_current: int
        @param level_switch: the trigger for whether or not to modify how level generation works based on if we are switching levels
        @type level_switch: bool
        @param row_current: an integer representing the tile's row location within the sub-level tile matrix
        @return: none
        @rtype: none
        """
        # Convert for pixel match in game
        x = 32 * col_current
        y = 32 * row_current
        # TODO: Can the whole concept of level_switching not be in this function? Maybe in the change level function or where
        # CONT: this is called from when level switching occurs.
        type = data.rstrip()
        if level_switch:
            # Apply a new location for all sprites off the screen
            if self.screen_switch_dir is 'Down':
                y += self.screen_switch_counter
            elif self.screen_switch_dir is 'Left':
                x += self.screen_switch_counter
            elif self.screen_switch_dir is 'Right':
                x -= self.screen_switch_counter
            elif self.screen_switch_dir is 'Up':
                y -= self.screen_switch_counter
            if type == 'N/A' or type == 'N/A\n' or type == ' ':
                # Do nothing
                pass
            else:
                # Check all types of tiles against the given data and if one is found, init it
                TileSpriteInit(engine_game, type, x, y)
        else:
            if type == 'N/A' or type == 'N/A\n' or type == ' ':
                # Do nothing
                pass
            else:
                # Check all types of tiles against the given data and if one is found, init it
                TileSpriteInit(engine_game, type, x, y)

    def load_saved_game(self, file_save_name: str):
        """
        A function to load a game that was previously saved.

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

    def rewrite_settings(self):
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
            print('[Debug - Info]: \'settings.py\' was updated successfully.')
        else:
            # Try to load settings from the backup.
            # NOTE: There should never be a rewrite to the 'settings_defaults.py' file in the Backup folder
            print('[Debug - Error]: \'settings_defaults.py\' was not found when trying to rewrite settings. Retrying '
                  'from backups.')
            path_defaults_full = 'Bin/Backup/settings_defaults.py'
            if (os.path.isfile(path_defaults_full)) is True:
                with open(path_defaults_full, 'r') as file:
                    lines = file.readlines()
                with open('settings.py', 'w') as file:
                    file.writelines(lines)
                print('[Debug - Info]: \'settings.py\' was updated \'from Bin/Backup/\'successfully.')
                # Copy from backup settings to a new settings_defaults file in Bin/
                try:
                    copy2('Bin/Backup/settings_defaults.py', 'Engine')
                except Exception as excep:
                    print('[Debug - Critical Error]: \'settings_defaults.py\' failed to copy from the backup folder. Provide info to the developers via the feedback tab')
                    print('[Debug - Exception]: ' + str(excep))
            else:
                print('[Debug - Critical Error]: \'settings_defaults.py\' was not found in \'Bin/Backup/\'.')

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
        # TODO NOTE: This could cause some bad corruption since the default settings have a chance to not be copied back to
        # CONT NOTE: the settings.py file, thus leaving the previous character's settings still in the system
        with open('settings.py', 'r') as file:
            lines = file.readlines()
        # Create save file from default settings and a backup for default settings
        with open(path_saves_full, 'w') as file:
            file.writelines(lines)
        with open('settings_defaults.py', 'w') as file:
            file.writelines(lines)
        # Update the new save file
        self.update_settings('CHAR_NAME', character_name, file_location=path_saves_full)
        # Load the saved settings into the current engine settings
        self.load_saved_game(file_save_name)

    # TODO: Create the in-game pause menu features to save the game.
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
        if character_main.rect.x > settings.SCREEN_WIDTH + character_main.rect.width or character_main.rect.x < 0 - character_main.rect.width or character_main.rect.y > settings.SCREEN_HEIGHT + character_main.rect.height or character_main.rect.y < 0 - character_main.rect.height:
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
        # Draw effects in the loading screen only if graphics are on high, otherwise the effects are all the time because graphics don't really matter
        # in this game
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
        font_debug_info = pygame.font.SysFont('Consolas', 15)
        font_level_surf = font_debug_info.render('Level: ' + str(engine_game.level_current) + ' of '
                                                 + str(engine_game.level_total), False, settings.WHITE, settings.DARK_GRAY)
        font_level_sub_surf = font_debug_info.render('Sub Level: ' + str(engine_game.level_sub_current) + ' of '
                                                     + str(engine_game.level_sub_current_total) + '. Total: '
                                                     + str(engine_game.level_sub_total), False, settings.WHITE,
                                                     settings.DARK_GRAY)
        font_char_state_surf = font_debug_info.render('State: ' + character_main.state, False, settings.WHITE,
                                                      settings.DARK_GRAY)
        font_char_x_vel_surf = font_debug_info.render('X-Velocity: ' + str(character_main.x_velocity), False, settings.WHITE,
                                                      settings.DARK_GRAY)
        font_char_y_vel_surf = font_debug_info.render('Y-Velocity: ' + str(character_main.y_velocity), False, settings.WHITE,
                                                      settings.DARK_GRAY)
        font_char_jump_count_surf = font_debug_info.render('Jump Count: ' + str(character_main.jump_count), False,
                                                           settings.WHITE, settings.DARK_GRAY)
        # Collision help
        pygame.draw.lines(screen, settings.RED, True, ((character_main.rect.x, character_main.rect.y),
                                                            (character_main.rect.x, character_main.rect.y + character_main.rect.height),
                                                            (character_main.rect.x + character_main.rect.width, character_main.rect.y + character_main.rect.height),
                                                            (character_main.rect.x + character_main.rect.width, character_main.rect.y)))
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
        # Info to display
        font_ui = pygame.font.SysFont('Consolas', 15)
        font_ui_name = pygame.font.SysFont('Consolas', 18)
        font_ui_char_name_surf = font_ui_name.render(settings.CHAR_NAME, True, settings.YELLOW)
        font_ui_char_name_rect = font_ui_char_name_surf.get_rect()
        font_ui_trait_endurance_surf = font_ui.render('Endurance: ' + str(character_main.trait_endurance), False, settings.WHITE, settings.DARK_GRAY)
        # Ready all other elements of ui

        # Calculate which image to use in the bubble effect on health bar
        self.timer_health_bar_bubble += 1
        if self.timer_health_bar_bubble == self.timer_health_bar_bubble_trigger:
            self.image_index_health_bar_bubble += 1
            self.timer_health_bar_bubble = 0
            if self.image_index_health_bar_bubble == len(self.images_health_bar_bubble) - 1:
                self.image_index_health_bar_bubble = 0
        self.image_health_bar_bubble = self.images_health_bar_bubble[self.image_index_health_bar_bubble]

        # Display ui system
        # Get images and place them in their appropriate position
        # TODO: Create a SpriteSheets location with all other images and use code to import so it's less
        # CONT: files - importing, possibly, function calls, and more if the code can be more centralized.
        # CONT: More isn't always best.
        health_bar_sprite_sheet = SpriteSheet('Bin/Sprites/User_Interface/Health_Bar/Health_Bar_Sprite_Sheet.png')
        health_bar_full_left = health_bar_sprite_sheet.get_image(0, 0, 16, 16)
        health_bar_full_middle = health_bar_sprite_sheet.get_image(16, 0, 16, 16)
        health_bar_full_right = health_bar_sprite_sheet.get_image(32, 0, 16, 16)
        # NOTE: Base health is 100. Each health tile is 16 pixels wide so that's 12.5 pixels of health per tile for 8 tiles.
        if character_main.health >= 13:
            screen.blit(health_bar_full_left, (5, 75))
        if character_main.health >= 26:
            screen.blit(health_bar_full_middle, (21, 75))
        if character_main.health >= 39:
            screen.blit(health_bar_full_middle, (37, 75))
        if character_main.health >= 52:
            screen.blit(health_bar_full_middle, (53, 75))
        if character_main.health >= 65:
            screen.blit(health_bar_full_middle, (69, 75))
        if character_main.health >= 78:
            screen.blit(health_bar_full_middle, (85, 75))
        if character_main.health >= 92:
            screen.blit(health_bar_full_middle, (101, 75))
        if character_main.health >= 100:
            screen.blit(health_bar_full_right, (117, 75))
        screen.blit(self.image_health_bar_bubble, self.image_health_bar_bubble_rect)
        # Calculate name location
        if (character_main.rect.width > font_ui_char_name_rect.width):
            x_new = character_main.rect.x + ((character_main.rect.width - font_ui_char_name_rect.width) / 2)
        else:
            x_new = character_main.rect.x - ((font_ui_char_name_rect.width - character_main.rect.width) / 2)
        screen.blit(font_ui_char_name_surf, (x_new, character_main.rect.y - font_ui_char_name_rect.height))
        screen.blit(font_ui_trait_endurance_surf, (5, 50))

    def draw_ui_pause(self):
        """
        A function that draws the pause menu with the specified character that is in game. The ui should
        use variables from the specified character's settings file.

        @return: none
        @rtype: none
        """
        pass

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
        # TODO: Delete the game setting for total levels and calculate the total within the engine
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
                if item_split[0] == 'Level' and item_split[1].isdigit() and os.path.isdir(os.path.join(path_levels, item)):
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
            if 0 > (counter_level_total or counter_level_sub_total):
                print('[Gather - Fail]: The calculation of the total levels and/or total sub-levels has failed to finish properly.')
            else:
                engine_game.level_total = counter_level_total
                engine_game.level_sub_total = counter_level_sub_total
        # TODO: Refactor code below
        elif objective == 'get_total_sub_of_current_level':
            # Updates how many sub-levels are on the current level
            counter_level_sub_current_total = 0
            path_spec_level = 'Levels/Level_' + str(engine_game.level_current)

            # Calculate specific sub levels
            for file in os.listdir(path_spec_level):
                if 'Sub_Level' in file:
                    counter_level_sub_current_total += 1
            # Change engine variables to reflect information gathered
            if counter_level_sub_current_total > 0:
                engine_game.level_sub_current_total = counter_level_sub_current_total
            else:
                print('[Gather - Fail]: The calculation of the total sub-levels in the current level has failed to finish properly.')
        elif objective == 'calculate_window':
            resolution_modes = pygame.display.list_modes(32)
            if not resolution_modes:
                print('[Gather - Fail]: There are no resolutions that support 32 pixel ratio.')
                self.update_settings('RES_WIDTH_RATIO', str(settings.WINDOW_WIDTH / settings.SCREEN_WIDTH), 'int')
                self.update_settings('RES_HEIGHT_RATIO', str(settings.WINDOW_HEIGHT / settings.SCREEN_HEIGHT), 'int')
                # TODO: Put pop-up message here signaling the user to restart the game to fix resolution querks.
                # TODO: Remember, we import 'settings0.py' so when it's changed it doesn't change the instance we have open on import.
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
                    self.update_settings('RES_HEIGHT_RATIO', str(resolution_modes[0][1] / settings.SCREEN_HEIGHT), 'int')
                    return resolution_modes[0]

    def reimport_all(self):
        '''
        A function to reimport all files associated with the game. The only catch, this file needs its own reimport outside of
        this function use.

        @return: none
        @rtype: none
        '''
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
        @return: none
        @rtype: none
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


class MenuHandler(object):
    """Class. Used to handle specific events with the menu, display special visuals, and more."""
    def __init__(self, engine_menu: object):
        """
        Constructor. Used to initialize a handler object for parsing important actions and information from
                     the user.

        @param engine_menu: the engine which controls the network of the menu the game is originally started from
        @type engine_menu: object
        """
        self.engine_menu = engine_menu

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
            pygame.draw.lines(screen, settings.DARK_GRAY, True, ((10, 25), (10, 65), (settings.SCREEN_WIDTH - 10, 65), (settings.SCREEN_WIDTH - 10, 25)), 1)
        # Customize visuals
        # Help/Load selection and view boxes for sub menus
        if self.engine_menu.state == 'Help' or self.engine_menu.state == 'Load':
            image_banner_header = pygame.image.load(settings.DIR_SPRITES_UI + '/Menu/Menu_Banner_Header_New.png').convert_alpha()
            image_banner_header_rect = image_banner_header.get_rect()
            image_banner_header_rect.x, image_banner_header_rect.y = 10, 25
            image_banner_tab = pygame.image.load(settings.DIR_SPRITES_UI + '/Menu/Menu_Banner_Tab.png').convert_alpha()
            image_banner_tab_rect = image_banner_tab.get_rect()
            image_banner_tab_rect.x, image_banner_tab_rect.y = 10, 70
            image_banner_main = pygame.image.load(settings.DIR_SPRITES_UI + '/Menu/Menu_Banner_Main.png').convert_alpha()
            image_banner_main_rect = image_banner_main.get_rect()
            image_banner_main_rect.x, image_banner_main_rect.y = 270, 70
            screen.blit(image_banner_header, image_banner_header_rect)
            screen.blit(image_banner_tab, image_banner_tab_rect)
            screen.blit(image_banner_main, image_banner_main_rect)
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
                if (btn.name == 'Input_Create_Char_Name' or btn.name == 'Input_File_Save_Name') and btn.user_input != '' \
                        and btn.disabled is True:
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
                    pygame.draw.line(screen, settings.DARK_GRAY, (410, 60), (410, button.rect.y + button.rect.height / 2))
                    pygame.draw.line(screen, settings.DARK_GRAY, (410, button.rect.y + button.rect.height / 2), (350, button.rect.y + button.rect.height / 2))
                elif button.name == 'Options_Video_Graphics' and button.hover:
                    pygame.draw.line(screen, settings.DARK_GRAY, (410, 60), (410, button.rect.y + button.rect.height / 2))
                    pygame.draw.line(screen, settings.DARK_GRAY, (410, button.rect.y + button.rect.height / 2), (350, button.rect.y + button.rect.height / 2))
                else:
                    # TODO: Can this be fixed by just taking the for loop out and changing the below conditional statements to
                    # CONT: more elif statements?
                    for button in self.engine_menu.buttons:
                        # Show selection visuals if the dropdown buttons are active
                        if button.name[:7] == 'New_Res' and button.hover and button.active:
                            pygame.draw.line(screen, settings.DARK_GRAY, (410, 60), (410, button.rect.y + button.rect.height / 2))
                            pygame.draw.line(screen, settings.DARK_GRAY, (410, button.rect.y + button.rect.height / 2), (350, button.rect.y + button.rect.height / 2))
                        elif button.name[:15] == 'Choice_Graphics' and button.hover and button.active:
                            pygame.draw.line(screen, settings.DARK_GRAY, (410, 60), (410, button.rect.y + button.rect.height / 2))
                            pygame.draw.line(screen, settings.DARK_GRAY, (410, button.rect.y + button.rect.height / 2), (350, button.rect.y + button.rect.height / 2))
        # Help
        # Feedback


class SnowHandler(object):

    def __init__(self, screen):
        self.screen = screen
        self.list_flakes = []
        for i in range(200):
            x = random.randrange(0, settings.SCREEN_WIDTH)
            y = random.randrange(0, settings.SCREEN_HEIGHT)
            self.list_flakes.append([x, y])

    def draw(self):
        # Process each snow flake in the list
        for i in range(len(self.list_flakes)):

            # Draw the snow flake
            pygame.draw.circle(self.screen, settings.DARK_GRAY, self.list_flakes[i], 2)
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

class GameButton(object):
    """Class. Used to created different kinds of buttons for the ui system in the game."""
    def __init__(self):
        """
        Constructor. Used to initialize a button and set it up for being displayed.

        """
        pass

    def handle_events(self):
        pass

    def update(self):
        """
        A function to check various conditions for the button.

        @return: none
        @rtype: none
        """
        pass


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
        self.font = pygame.font.SysFont('Consolas', self.text_size)
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
        self.image = pygame.Surface((self.text_rect.width, self.text_rect.height))
        self.image.fill(background_color)
        self.rect = pygame.Rect(x, y, self.text_rect.width, self.text_rect.height)

        # Misc
        self.engine_menu = engine_menu

    def handle_events(self, buttons: list, event: object, mouse_pos: tuple):
        """
        A function that handles the events for the buttons in the menu section of the game.

        @param buttons: a collection of all the buttons currently active due to user engagement
        @type buttons: list
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
                    # TODO: Check for dropdown first as all buttons now have an attribute to determine whether they are dropdown buttons or not
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
                                # Basic setup for proper values
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
                        strip_res = self.text.strip('()')
                        split_res = strip_res.split(', ')
                        self.engine_menu.engine_handler.update_settings('WINDOW_WIDTH', split_res[0], 'int')
                        self.engine_menu.engine_handler.update_settings('WINDOW_HEIGHT', split_res[1], 'int')
                        self.engine_menu.engine_handler.update_settings('RES_WIDTH_RATIO', str((int(split_res[0]) / settings.SCREEN_WIDTH)), 'int')
                        self.engine_menu.engine_handler.update_settings('RES_HEIGHT_RATIO', str((int(split_res[1]) / settings.SCREEN_HEIGHT)), 'int')
                        self.engine_menu.engine_handler.update_settings('RES_CHANGED', True, 'bool')
                        self.engine_menu.window = pygame.display.set_mode((self.engine_menu.engine_handler.gather_engine_info(self.engine_menu.engine_game, 'calculate_window')))
                        # Close all buttons on resolution drop down
                        new_buttons = []
                        for btn in buttons:
                            if btn.name[:7] == 'New_Res':
                                btn.active = False
                                btn.toggled = False
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
                                # Basic setup for proper values
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
                        strip_graphics = self.text.strip('()')
                        self.engine_menu.engine_handler.update_settings('GRAPHICS', strip_graphics, 'string')
                        # Close buttons and dropdow bar
                        new_buttons = []
                        for btn in buttons:
                            if btn.name[:15] == 'Choice_Graphics':
                                btn.active = False
                                btn.toggled = False
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
        A function to check various conditions for the button.

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
            # Line going around button
            # pygame.draw.lines(screen, settings.WHITE, True, (
            #     (self.rect.x, self.rect.y),
            #     (self.rect.x, self.rect.y + self.rect.height),
            #     (self.rect.x + self.rect.width, self.rect.y + self.rect.height),
            #     (self.rect.x + self.rect.width, self.rect.y)))


class MenuButtonInput(object):
    """Class. Used to represent a button, with input, inside of the editor that can be displayed."""
    def __init__(self, engine_menu: object, name: str, text_ask: str, x: int, y: int, width=50, height=50):
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
        self.engine_menu = engine_menu
        # Button attributes
        self.FONT = pygame.font.SysFont('Consolas', 15)
        self.active = True
        self.disabled = True
        self.image = pygame.Surface((width, height))
        self.image.fill(settings.DARK_GRAY)
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.user_input = ''
        self.text_ask = text_ask
        self.text_image = self.FONT.render(self.text_ask, True, settings.WHITE)
        self.text_rect = pygame.Rect(x + 5, y + 5, width / 2, height / 2)

    def handle_events(self, buttons: list, event: object, mouse_pos: tuple):
        """
        A function to handle the actions of the user in regards to the button.

        @param buttons: a collection of all the buttons currently being displayed
        @type buttons: list
        @param event: the event that pygame was able to recognize based off of user interaction
        @type event: object
        @param mouse_pos: the position of the mouse when this function was called
        @type mouse_pos: tuple
        @return: none
        @rtype: none
        """
        # Clicking on a button
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and event.type == pygame.MOUSEBUTTONDOWN:
            # Only allow one box enabled at a time
            if self.name == 'Input_Create_Char_Name':
                for button in buttons:
                    if button.name == 'Input_File_Save_Name':
                        if self.disabled is True and button.disabled is True:
                            self.disabled = False
                        elif self.disabled is True and button.disabled is False:
                            self.disabled, button.disabled = False, True
                        elif self.disabled is False and button.disabled is True:
                            self.disabled = True
            elif self.name == 'Input_File_Save_Name':
                for button in buttons:
                    if button.name == 'Input_Create_Char_Name':
                        if self.disabled is True and button.disabled is True:
                            self.disabled = False
                        elif self.disabled is True and button.disabled is False:
                            self.disabled, button.disabled = False, True
                        elif self.disabled is False and button.disabled is True:
                            self.disabled = True
            # print('[Debug - Info]: ' + self.name + ' self.disabled = ' + str(self.disabled))
        if self.active and event.type == pygame.KEYDOWN:
            # Gather input if button is not disabled
            if self.name == 'Input_Create_Char_Name' and self.disabled is False:
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
                    for button in buttons:
                        if button.name == 'Input_File_Save_Name':
                            button.disabled = False
                else:
                    if self.user_input == self.text_ask:
                        self.user_input = ''
                    # To get characters we use event.unicode
                    self.user_input += event.unicode
                # Change the new text of the box to the user's input
                self.text_image = self.FONT.render(self.text_ask + self.user_input, True, settings.WHITE)
            # Gather input if the button is not disabled
            elif self.name == 'Input_File_Save_Name' and self.disabled is False:
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
                self.text_image = self.FONT.render(self.text_ask + self.user_input, True, settings.WHITE)

    def update(self):
        """
        A function to check various conditions for the button.

        @return: none
        @rtype: none
        """
        # Resize the box if the text is too long.
        width = max(15, self.text_image.get_width() + 10)
        self.rect.w = width
        self.image = pygame.Surface((width, self.rect.height))
        self.image.fill(settings.DARK_GRAY)

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
            pygame.draw.lines(screen, settings.WHITE, True, (
            (self.rect.x, self.rect.y),
            (self.rect.x, self.rect.y + self.rect.height),
            (self.rect.x + self.rect.width, self.rect.y + self.rect.height),
            (self.rect.x + self.rect.width, self.rect.y)))
            # Line going around text/input
            pygame.draw.lines(screen, settings.WHITE, True, (
            (self.rect.x + 2, self.rect.y + 2),
            (self.rect.x + 2, self.rect.y + self.rect.height - 3),
            (self.rect.x + self.rect.width - 3,
             self.rect.y + self.rect.height - 3),
            (self.rect.x + self.rect.width - 3, self.rect.y + 2)))


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
        self.text_left_color = text_left_color
        self.text_left_size = text_left_size
        self.text_left_font = pygame.font.SysFont('Consolas', self.text_left_size)
        self.text_left_image = self.text_left_font.render(self.text_left, True, self.text_left_color)
        self.text_left_rect = self.text_left_image.get_rect()

        # Right text/button attributes
        self.text_right = text_right
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
        self.height = self.text_rect.height + (self.text_left_rect.height / 2) + (self.text_right_rect.height / 2) + self.height_buffer
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

    def handle_events(self, engine_menu: object, popups: list, event: object, mouse_pos: tuple):
        """
        A function that handles the events for pop-up messages wherever they may be running.

        @param engine_menu:
        @type engine_menu: object
        @param popups: a collection of all the pop-ups currently active due to user engagement
        @type popups: list
        @param event: a specific action that pygame recognized from the user
        @type event: object
        @param mouse_pos: a collection of points representing the position of the mouse when the event occurred
        @type mouse_pos: tuple
        @return: none
        @rtype: none
        """
        # Check mouse pos for hover events
        if self.text_left_rect.collidepoint(mouse_pos):
            self.hover_left = True
            # Handle special buttons via their name
            self.text_left_font.set_underline(True)
        else:
            self.hover_left = False
            self.text_left_font.set_underline(False)
        if self.text_right_rect.collidepoint(mouse_pos):
            self.hover_right = True
            # Handle special buttons via their name
            self.text_right_font.set_underline(True)
        else:
            self.hover_right = False
            self.text_right_font.set_underline(False)
        self.text_left_image = self.text_left_font.render(self.text_left, True, self.text_left_color)
        self.text_right_image = self.text_right_font.render(self.text_right, True, self.text_right_color)

        # Check mouse interaction with buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.text_left_rect.collidepoint(mouse_pos):
                if self.text_left == 'Ok':
                    self.active = False
                    # TODO: Customize popup's for errors and maybe create a log with error's from certain popups
                elif self.text_left == 'Exit':
                    engine_menu.running = False
            if self.text_right_rect.collidepoint(mouse_pos):
                if self.text_right == 'Cancel':
                    self.active = False
                elif self.text_right == 'Close':
                    self.active = False
            # Remove button popup from popups if not active
            if not self.active:
                new_popups = []
                for popup in popups:
                    # Exclude this popup from the popup group and append.
                    if popup.name == self.name:
                        pass
                    else:
                        new_popups.append(popup)
                popups = new_popups
                print('[Debug - Info]: Popup removed. Remaining: ', popups)

    def update(self):
        """
        A function to check various conditions for the menu pop-uo.

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
            screen.blit(self.image, self.rect)
            screen.blit(self.text_image, self.text_rect)
            screen.blit(self.text_left_image, self.text_left_rect)
            screen.blit(self.text_right_image, self.text_right_rect)

            # Draw box around the whole popup
            pygame.draw.lines(screen, self.border_color, True, ((self.rect.x, self.rect.y), (self.rect.x, self.rect.y + self.height),
                                                                (self.rect.x + self.width, self.rect.y + self.height), (self.rect.x + self.width, self.rect.y)))


class TileSpriteInit(pygame.sprite.Sprite):
    """Class. Used to create sprites from game file images for later use and manipulation."""

    def __init__(self, engine_game: object, type: str, x: int, y: int):
        """
        Constructor. Used to create a sprite and add it to the groups for drawing the level.

        @param engine_game: the engine which controls the network/functions of the game when it starts after the menu
        @type engine_game: object
        @param x: the desired horizontal location for the sprite to be initiated at
        @type x: int
        @param y: the desired vertical location for the sprite to be initiated at
        @type y: int
        """
        # Width: 32 Height: 32
        # TODO: Create a hiearchy of elifs for 'g' or 'h' so that it takes less time to get through the loop
        # CONT: Is this coded effeciently?
        environment_spritesheet = SpriteSheet(settings.DIR_SPRITES_GAME_ENVI + '/Ground_Grass_384_432_Spritesheet.png')
        type_tiles = {'GL0': environment_spritesheet.get_image(0, 0, 32, 32), 'GL1': environment_spritesheet.get_image(0, 32, 32, 32),
                      'GL2': environment_spritesheet.get_image(0, 64, 32, 32), 'GL3': environment_spritesheet.get_image(0, 96, 32, 32),
                      'GL4': environment_spritesheet.get_image(0, 128, 32, 32), 'GL5': environment_spritesheet.get_image(0, 160, 32, 32),
                      'GL6': environment_spritesheet.get_image(0, 192, 32, 32), 'GM0': environment_spritesheet.get_image(32, 32, 32, 32),
                      'GM1': environment_spritesheet.get_image(64, 32, 32, 32), 'GM2': environment_spritesheet.get_image(96, 32, 32, 32),
                      'GM3': environment_spritesheet.get_image(128, 32, 32, 32), 'GM4': environment_spritesheet.get_image(160, 32, 32, 32),
                      'GM5': environment_spritesheet.get_image(192, 32, 32, 32), 'GM6': environment_spritesheet.get_image(224, 32, 32, 32),
                      'GT0': environment_spritesheet.get_image(32, 0, 32, 32), 'GT1': environment_spritesheet.get_image(64, 0, 32, 32),
                      'GT2': environment_spritesheet.get_image(96, 0, 32, 32), 'GT3': environment_spritesheet.get_image(128, 0, 32, 32),
                      'GT4': environment_spritesheet.get_image(160, 0, 32, 32), 'GT5': environment_spritesheet.get_image(192, 0, 32, 32),
                      'GT6': environment_spritesheet.get_image(224, 0, 32, 32), 'GR0': environment_spritesheet.get_image(256, 0, 32, 32),
                      'GR1': environment_spritesheet.get_image(256, 32, 32, 32), 'GR2': environment_spritesheet.get_image(256, 64, 32, 32),
                      'GR3': environment_spritesheet.get_image(256, 96, 32, 32), 'GR4': environment_spritesheet.get_image(256, 128, 32, 32),
                      'GR5': environment_spritesheet.get_image(256, 160, 32, 32), 'GR6': environment_spritesheet.get_image(256, 192, 32, 32),
                      'HL0': environment_spritesheet.get_image(96, 240, 32, 32), 'HL1': environment_spritesheet.get_image(96, 272, 32, 32),
                      'HL2': environment_spritesheet.get_image(96, 304, 32, 32), 'HL3': environment_spritesheet.get_image(96, 336, 32, 32),
                      'HL4': environment_spritesheet.get_image(96, 368, 32, 32), 'HL5': environment_spritesheet.get_image(96, 400, 32, 32),
                      'HT0': environment_spritesheet.get_image(0, 336, 32, 32), 'HT1': environment_spritesheet.get_image(32, 336, 32, 32),
                      'HT2': environment_spritesheet.get_image(64, 336, 32, 32), 'HT3': environment_spritesheet.get_image(128, 240, 32, 32),
                      'HT4': environment_spritesheet.get_image(160, 240, 32, 32), 'HT5': environment_spritesheet.get_image(224, 240, 32, 32),
                      'HT6': environment_spritesheet.get_image(288, 336, 32, 32), 'HT7': environment_spritesheet.get_image(320, 336, 32, 32),
                      'HT8': environment_spritesheet.get_image(352, 336, 32, 32), 'HR0': environment_spritesheet.get_image(256, 240, 32, 32),
                      'HR1': environment_spritesheet.get_image(256, 272, 32, 32), 'HR2': environment_spritesheet.get_image(256, 304, 32, 32),
                      'HR3': environment_spritesheet.get_image(256, 336, 32, 32), 'HR4': environment_spritesheet.get_image(352, 368, 32, 32),
                      'HR5': environment_spritesheet.get_image(352, 400, 32, 32)}
        for i in range(10000):
            if type in type_tiles:
                image = type_tiles[type]
            else:
                print(' \'' + str(type) + '\'')
                return
        self.groups = engine_game.sprites_all, engine_game.sprites_walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


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
