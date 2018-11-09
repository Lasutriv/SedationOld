#
# Tanner Fry
# tefnq2@mst.edu
import settings

import math
import os
import pygame


class TileMap(object):
    """
    Class. Used to handle the overall matrix of a level that is being worked on. Other
    functionality includes being able to place tiles, change specific levels, and
    delete tiles from the overall matrix of a level.
    """
    def __init__(self, editor_engine: object, screen_width: int, screen_height: int):
        """
        Constructor. Used to initialize the tile matrix object with it's variables so that
                     it can properly handle events and the functions built within it.

        @param editor_engine: the engine which controls the network of the editor when its ran
        @type editor_engine: object
        @param screen_width: the designated screen width that the settings file or the user specifies
        @type screen_width: int
        @param screen_height: the designed screen height that the settings file or the user specifies
        @type screen_height: int
        """
        self.editor_engine = editor_engine
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.default_sprite_sheet()

    def default_sprite_sheet(self):
        # TODO: Fix this predefined setup. The spritesheet size should be calculated (from name),
        # CONT: broken down into separate tiles, stored into objects that are placeable, place
        # CONT: those objects, save it, store it, and finally be able to transfer it.
        environment_spritesheet = SpriteSheet('Assets/Game_Environment/Ground_Grass_384_432_Spritesheet.png')
        self.tile_types = {'GL0': environment_spritesheet.get_image(0, 0, 32, 32),
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

    def handle_events(self, event: object):
        """
        A function to call other functions and handle the user's actions/movements/reactions while
        using the program.

        @param event: a specific action that pygame recognized from the user
        @type event: object
        @return: none
        @rtype: none
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handling tiles on matrix
            if event.pos[0] > settings.TAB_SIZE and self.editor_engine.tile_selected != '':
                # Divide by 32 then round down to find x tile slot. Then * 32 for it's pixel location
                tile_place_x = (math.floor((event.pos[0]) / settings.TILE_SIZE)) * settings.TILE_SIZE
                tile_place_y = (math.floor((event.pos[1]) / settings.TILE_SIZE)) * settings.TILE_SIZE
                if self.editor_engine.tile_selected == 'DELETE':
                    # TODO: Fix this as we don't delete the same way. We have to pop the sprite with the location we
                    # CONT: try to delete.
                    self.delete_tile(tile_place_x, tile_place_y)
                else:
                    self.place_tile(self.editor_engine.tile_selected, tile_place_x, tile_place_y)

    def change_tile_map(self, info_replace, tile_x, tile_y):
        """
        A function to change the contents of a cell in the matrix in a level.

        @param info_replace: the two-letter combination representing a specific tile in a cell on the matrix of a level
        @type info_replace: str
        @param tile_x: the desired horizontal location relative to the top left of the mouse click
        @type tile_x: int
        @param tile_y: the desired vertical location relative to the top left of the mouse click
        @type tile_y: int
        @return: none
        @rtype: none
        """
        # Change tile in the matrix of the level and save it
        if self.editor_engine.level_loaded is True:
            path_to_level = 'Levels/Level_' + str(self.editor_engine.level_select) + '/Sub_Level_' + str(self.editor_engine.level_sub_select) + '.txt'
            line_counter = 0
            data_counter = 0
            line_finished = ''
            lines_started = []
            lines_finished = []
            # Subtract by 3 because of 96pxtab
            pos_for_matrix = (tile_x / settings.TILE_SIZE) - 3, tile_y / settings.TILE_SIZE
            print('[Debug - Info]: The position in the matrix is (' + str(pos_for_matrix[0]) + ', '
                  + str(pos_for_matrix[1]) + ')')

            # Read file
            with open(path_to_level, 'r') as file:
                for line in file:
                    lines_started.append(line)
            # Change contents
            for line in lines_started:
                # Find row since we are going by lines at the moment
                if pos_for_matrix[1] == line_counter:
                    line = line.split(' ')
                    # Find col since we are going through a specific line's content
                    for data in line:
                        # Replace appropriate data
                        if pos_for_matrix[0] == data_counter:
                            line_finished = line_finished + info_replace + ' '
                        else:
                            line_finished = line_finished + data + ' '
                        data_counter += 1
                    # Fix up line and send it
                    # Check and see if last bit of data was at end of line or not
                    line_finished = (line_finished[:-1])
                    if line_finished[-1] == '\n':
                        pass
                    else:
                        line_finished = line_finished + '\n'
                    lines_finished.append(line_finished)
                    line_finished = ''
                else:
                    lines_finished.append(line)
                line_counter += 1
            # Write new file to update the change
            with open(path_to_level, 'w') as file:
                file.writelines(lines_finished)
            print('[Debug - Info]: The level has been loaded.')
        else:
            print('[Debug - Info]: A level wasn\'t loaded, therefore your tiles aren\'t being saved right now.')

    def load_tile_map(self):
        """
        A function to load a specific matrix from the levels folder onto the editor for editing.

        @return: none
        @rtype: none
        """
        print('[Debug - Info]: The tile specified tile matrix is being loaded from the specific level and sublevel '
              'folder.')
        # Setup info
        line_counter = 0
        path_to_level = 'Levels/Level_' + str(self.editor_engine.level_select) + '/Sub_Level_' + str(self.editor_engine.level_sub_select) + '.txt'
        # Wipe last tile matrix
        for sprite in self.editor_engine.sprites_all:
            self.editor_engine.sprites_all.remove(sprite)
        # Load tile matrix by reading a file that stores the tiles in a dictionary
        # style across a matrix
        try:
            with open(path_to_level, 'r') as file:
                for line in file:
                    data_counter = 0
                    data_from_line = line.split(' ')
                    for data in data_from_line:
                        if data == 'N/A' or data == 'N/A\n' or data == ' ':
                            # Do nothing
                            pass
                        else:
                            # Check all types of tiles against the given data and if one is found, init it
                            TileSpriteInit(self.editor_engine, data, (data_counter * settings.TILE_SIZE)
                                           + settings.TAB_SIZE, (line_counter * settings.TILE_SIZE))
                        data_counter += 1
                    line_counter += 1
                self.editor_engine.level_loaded = True
        except FileNotFoundError:
            print('[Debug - Error]: The sublevel of level 1 was not found. If you\'re looking to load a different level '
                  'then you need to change the first number submitted in the input box when loading a level.')

    def transfer_tile_map(self):
        """
        A function to transfer the current level being worked on to the Levels folder in the engine.

        @return: none
        @rtype: none
        """
        from shutil import copyfile
        # NOTE: use the change_tile_map to get ideas of how to do it
        path_to_project = os.path.realpath(__file__)
        path_to_project = path_to_project.strip('Tile_Editor\editorLib.py')
        path_to_project = path_to_project.replace('\\', '/')
        path_to_level = 'Levels/Level_' + str(self.editor_engine.level_select) + '/Sub_Level_' \
                        + str(self.editor_engine.level_sub_select) + '.txt'
        os.chdir('..')
        path_to_editor_level = path_to_project + '/Tile_Editor/' + path_to_level
        path_to_engine_level = path_to_project + '/Engine/' + path_to_level
        copyfile(path_to_editor_level, path_to_engine_level)
        os.chdir('Tile_Editor/')

    def place_tile(self, tile_selected: str, tile_x: int, tile_y: int):
        """
        A function that allows the addition of sprites to the tile matrix and puts
        them in a group so they can be displayed.

        @param tile_selected: the type of tile we will be placing onto the tile matrix and into the sprites_all group
        @type tile_selected: str
        @param tile_x: the desired horizontal location relative to the top left of the mouse click
        @type tile_x: int
        @param tile_y: the desired vertical location relative to the top left of the mouse click
        @type tile_y: int
        @return: none
        @rtype: none
        """
        # Change display to user
        TileSpriteInit(self.editor_engine, tile_selected, tile_x, tile_y)
        # Change and update the matrix
        self.change_tile_map(tile_selected, tile_x, tile_y)

    def delete_tile(self, tile_x, tile_y):
        """
        A function to remove tiles from the screen and the sprites_all group.

        @param tile_x: the desired x location to be deleted
        @type tile_x: int
        @param tile_y: the desired y location to be deleted
        @type tile_y: int
        @return: none
        @rtype: none
        """
        for sprite in self.editor_engine.sprites_all:
            if tile_x == sprite.rect.x and tile_y == sprite.rect.y:
                self.editor_engine.sprites_all.remove(sprite)
                # Delete tile from the matrix
                print('deleting tile')
                self.change_tile_map('NA', tile_x, tile_y)

    def draw_grid(self, screen: object, tile_size: int):
        """
        A function that apply's a colored grid across the screen display with a width equal
        to that of a tile for each cell in the grid so as to break up the matrix of a level
        for easier editing and understanding while making levels.

        @param screen: the display that all of the grid lines are applied to
        @type screen: object
        @param tile_size: the tile size for one individual tile
        @type tile_size: int
        @return: none
        @rtype: none
        """
        # Grid to see where tiles go, delete this after game is finished
        for x in range(settings.TAB_SIZE, self.screen_width, tile_size):
            pygame.draw.line(screen, settings.LIGHT_GRAY, (x, 0), (x, self.screen_height))
        for y in range(0, self.screen_height, tile_size):
            pygame.draw.line(screen, settings.LIGHT_GRAY, (settings.TAB_SIZE, y), (self.screen_width, y))


# TODO: Rename for better understanding?
class EditorTab(object):
    """Class. Used to represent the visuals for the tools/tiles available on the left side of the editor."""
    def __init__(self, editor_engine: object, screen: object, tile_map: object):
        """
        Constructor. Used to set up the tools/tiles object for manipulation during runtime.

        @param editor_engine: the engine which controls the network of the editor when its ran
        @type editor_engine: object
        @param screen: the display that all of the tools/tiles will be displayed to
        @type screen: object
        @param tile_map:
        @type tile_map:
        """
        # Max 2 cols 22 rows for the tab via 16x16 scaled to 48x48
        # 43 images total plus the delete
        self.editor_engine = editor_engine
        self.images = []  # Used to store the images that will be pushed to a tab holding them
        self._images_max = 43
        self.index_images = 0
        self.index_tabs_tile_types = 0  # Used to check if index_tiles caught up on next cycle tab tiles
        self.index_tiles = 0
        self.index_tiles_tab = 0
        self.old_index_tiles_tab = 0  # Used for comparison against the tab index for switching sprites
        self.screen = screen
        self.tab_count = 0
        self.tabs = []  # List of lists. The lists which are a list of images
        self.tile_map = tile_map

        self.calculate_tab_usage()

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if mouse clicked delete tile
            if 79 >= event.pos[0] >= 47 and 786 <= event.pos[1] <= 818:
                self.editor_engine.tile_selected = 'DELETE'
                print('Delete tile selected')
            for sprite in self.editor_engine.sprites_tab:
                # Check if mouse clicked on a sprite in the tab, if so it's selected
                if sprite.rect.collidepoint(event.pos) and sprite.active is True:
                    self.editor_engine.tile_selected = sprite.tile_type
                    # Handle arrow clicking on the tab section with the tiles
                elif 18 < event.pos[0] < 30 and 23 < event.pos[1] < 46:
                    # Start the left click animationand update the tab index for the tiles
                    self.editor_engine.anim_left_arrow.active = True
                    if self.editor_engine.editor_tab.index_tiles_tab - 1 >= 0:
                        self.editor_engine.editor_tab.index_tiles_tab -= 1
                    else:
                        self.editor_engine.editor_tab.index_tiles_tab = len(self.editor_engine.editor_tab.tabs) - 1
                elif 63 < event.pos[0] < 81 and 23 < event.pos[1] < 46:
                    # Start the right click animation and update the tab index for the tiles
                    self.editor_engine.anim_right_arrow.active = True
                    if self.editor_engine.editor_tab.index_tiles_tab + 1 < len(self.editor_engine.editor_tab.tabs):
                        self.editor_engine.editor_tab.index_tiles_tab += 1
                    else:
                        self.editor_engine.editor_tab.index_tiles_tab = 0

    def calculate_tab_usage(self):
        """
        A function to calculate the total amount of tabs that the spritesheet will use.

        @return: none
        @rtype: none
        """
        return_val = self.calculate_specific_tab()
        # Finished making tabs
        if return_val == 0:
            self.tabs.append(self.images)
            # Reset index tab
            self.index_tiles_tab = 0
        # Make another tab
        elif return_val == 1:
            self.tabs.append(self.images)
            self.tab_count += 1
            self.calculate_tab_usage()

    def calculate_specific_tab(self):
        """
        A function that calculates as many tabs needed for the spritesheet to be fully
        implemented into the tile tab.

        @return: none
        @rtype: none
        """
        self.images = []
        self.index_images = 0
        self.index_tiles = 0
        for tile_type in self.tile_map.tile_types:
            # Check make sure tile index is concurrent with tab tile type index
            if self.index_tiles >= self.index_tabs_tile_types:
                # Check tab bounds for max images
                if self.index_images <= self._images_max:
                    image = self.tile_map.tile_types[tile_type].convert_alpha()

                    # Calculate sprite location
                    # TODO: Group sprites together, but it seems hard to do
                    x, y = 0, 0
                    first_col_x = 15
                    # First column
                    if self.index_images <= 22:
                        x = first_col_x
                        y = 60 + (self.index_images * 33)
                    # Second column
                    else:
                        x = first_col_x + 32
                        y = (60 + ((self._images_max - self.index_images) * 33))

                    # Create tile sprite
                    TabSpriteInit(self.editor_engine, image, self.tab_count, tile_type, x, y)
                else:
                    self.index_tiles_tab += 1
                    return 1
                self.index_images += 1
                self.index_tabs_tile_types += 1
            self.index_tiles += 1

        return 0

    def update(self):
        """
        A function that updates the sprites on the tab if the tab index is ever changed.

        @return: none
        @rtype: none
        """
        # Check if tab was changed
        if self.index_tiles_tab != self.old_index_tiles_tab:
            # Check all sprites in tab group
            for sprite in self.editor_engine.sprites_tab:
                # Check if current sprite matches tab choice
                if sprite.tab_number == self.index_tiles_tab:
                    sprite.active = True
                else:
                    sprite.active = False
        else:
            # Make sure sprites on current tab are active
            for sprite in self.editor_engine.sprites_tab:
                if sprite.tab_number == self.index_tiles_tab:
                    sprite.active = True
                else:
                    sprite.active = False

    def draw(self):
        """
        A function to draw the tiles on the left side of the editor within a 64 pixel wide space starting
        all the way on the left.

        @return: none
        @rtype: none
        """
        # Display sprites who are active based on the chosen tab
        for sprite in self.editor_engine.sprites_tab:
            if sprite.active is True:
                self.editor_engine.screen.blit(sprite.image, sprite.rect)

        # If a tile is selected, display a border around it
        if self.editor_engine.tile_selected != '':
            if self.editor_engine.tile_selected == 'DELETE':
                pygame.draw.lines(self.editor_engine.screen, settings.RED, True, ((47, 786),
                                                                                  (47, 818),
                                                                                  (79, 818),
                                                                                  (79, 786)))
            else:
                for sprite in self.editor_engine.sprites_tab:
                    if sprite.tile_type == self.editor_engine.tile_selected:
                        pygame.draw.lines(self.editor_engine.screen, settings.RED, True, ((sprite.rect.x, sprite.rect.y),
                                                                                          (sprite.rect.x,
                                                                                           sprite.rect.y + 32),
                                                                                          (sprite.rect.x + 32,
                                                                                           sprite.rect.y + 32),
                                                                                          (sprite.rect.x + 32,
                                                                                           sprite.rect.y)))

        # Setup variables to check next cycle
        self.old_index_tiles_tab = self.index_tiles_tab


# TODO: Fix commenting
class TabSpriteInit(pygame.sprite.Sprite):
    """Class. Used to represent a tile sprite, in the tab section of the editor, for easier referencing. """
    def __init__(self, editor_engine: object, image: object, tab_number: int, tile_type: str, x: int,
                 y: int):
        """


        @param editor_engine:
        @param image:
        @param tab_number:
        @param tile_type:
        @param x:
        @param y:
        """
        self.active = False
        self.editor_engine = editor_engine
        self.groups = editor_engine.sprites_tab
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tab_number = tab_number
        self.tile_type = tile_type

    def update(self):
        """


        @return: none
        @rtype: none
        """
        pass

    def draw(self):
        """
        A function to draw the tab tile if it is active, aka if the tab that the
        tile to is selected, then the tile will display

        @return: none
        @rtype: none
        """
        if self.active is True:
            self.editor_engine.screen.blit(self.image, self.rect)


class Button(object):
    """Class. Used to represent a button within the editor that is being displayed."""
    def __init__(self, editor_engine: object, name: str, text: str, type: str, font_size: int, button_x: int, button_y: int,
                 **kwargs):
        """
        Constructor. Used to initialize the button's attributes.

        @param editor_engine: the engine which controls the network of the editor when its ran
        @type editor_engine: object
        @param name: the name that represents a specific button
        @type name: str
        @param text: the message that the button displays
        @type text: str
        @param type: the type of buttoon it can be, whether it's an error button, confirm, or confirm/deny
        @type type: str
        @param button_x: the desired location horizontally for the button regarding the top left of it
        @type button_x: int
        @param button_y: the desired location vertically for the button regarding the top left of it
        @type button_y: int
        @param width: the total width from left to right on the button
        @param height: the total height from bottom to top on the button
        """
        self.editor_engine = editor_engine
        # Base attributes
        self.active = False
        self.disabled = False
        self.font_size = font_size
        self.name = name
        self.type = type
        # Text attributes
        self.font = pygame.font.SysFont('Consolas', self.font_size)
        self.text = text
        self.text_image = self.font.render(text, True, settings.WHITE)
        self.text_rect = self.text_image.get_rect()
        # Visual attributes
        self.height = 0
        self.width = 0
        if type != 'None':
            self.height = (self.font_size * 2) + 15  # two lines of font and 5px of cushion between each line
        else:
            self.height = self.font_size + 10
        self.width = self.text_rect.width + 10
        for kw in kwargs:
            if kw == 'override_height':
                self.height = kwargs[kw]
            elif kw == 'override_width':
                self.width = kwargs[kw]
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(settings.DARK_GRAY)
        self.rect = pygame.Rect(button_x, button_y, self.width, self.height)
        self.text_rect.x = self.rect.x + 5
        self.text_rect.y = self.rect.y + 5
        for kw in kwargs:
            if kw == 'override_text_x':
                self.text_rect.x = kwargs[kw]

        # Determine type
        if type == 'Error':
            self.text_ok_image = self.font.render('Ok', True, settings.WHITE)
            self.text_ok_rect = self.text_ok_image.get_rect()
            self.text_ok_rect.x = self.rect.centerx - (self.text_ok_rect.width / 2)
            self.text_ok_rect.y = self.text_rect.y + self.font_size + 5
        elif type == 'Confirm':
            self.text_confirm_image = self.font.render('Confirm', True, settings.WHITE)
            self.text_confirm_rect = self.text_confirm_image.get_rect()
            self.text_confirm_rect.x = self.rect.centerx - (self.text_ok_rect.width / 2)
            self.text_confirm_rect.y = self.text_rect.y + self.font_size + 5
        elif type == 'Confirm/Deny':
            self.text_yes_image = self.font.render('Yes', True, settings.WHITE)
            self.text_yes_rect = self.text_yes_image.get_rect()
            self.text_yes_rect.x = self.text_rect.x + 5
            self.text_yes_rect.y = self.text_rect.y + self.font_size + 5
            self.text_no_image = self.font.render('No', True, settings.WHITE)
            self.text_no_rect = self.text_no_image.get_rect()
            self.text_no_rect.x = self.text_rect.x + self.text_rect.width - self.text_no_rect.width
            self.text_no_rect.y = self.text_rect.y + self.font_size + 5
        elif type == 'None':
            pass
        else:
            print('[Debug - Error]: Button type could not be found nor assigned. Was the button created correctly?')

    def handle_events(self, event: object, buttons: list):
        """
        A function to work with buttons and user triggered events and perform actions
        based on specific interactions of the two.

        @param event: the event that pygame was able to recognize based off of user interaction
        @type event: object
        @param buttons: a list of the active buttons that the game is cycling through to check the button's events
        @type buttons: list
        @return: none
        @rtype: none
        """
        # Check and see if mouse hits a specific button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.name == 'Exit':
                    self.editor_engine.running = False
                if self.name == 'Load':
                    self.editor_engine.button_input_level.active = not self.editor_engine.button_input_level.active
                if self.name == 'Transfer':
                    for button in buttons:
                        if button.name == 'Ask_To_Transfer':
                            button.active = True
                # Handle clicking on specific buttons based on their type
                if self.type == 'Error':
                    if self.text_ok_rect.collidepoint(event.pos):
                        if self.name == 'Tile_Error':
                            self.active = False
                elif self.type == 'Confirm':
                    if self.text_confirm_rect.collidepoint(event.pos):
                        pass
                if self.type == 'Confirm/Deny':
                    if self.text_yes_rect.collidepoint(event.pos):
                        if self.name == 'Ask_To_Transfer':
                            self.active = False
                            self.editor_engine.tile_map.transfer_tile_map()
                    elif self.text_no_rect.collidepoint(event.pos):
                        self.active = False
            # Display button error if user clicks with specified condition
            if self.name == 'Tile_Error' and event.pos[0] > settings.TAB_SIZE and self.editor_engine.tile_selected == '':
                self.active = True
            elif self.name == 'Tile_Error' and self.editor_engine.tile_selected != '':
                self.active = False

        # Set buttons active that need to be
        if self.name == 'Load' or self.name == 'Exit':
            self.active = True
        if self.name == 'Transfer':
            self.active = True
            if self.editor_engine.level_loaded is True:
                self.disabled = False
            else:
                self.disabled = True

        # Handle disabled buttons
        if self.disabled is True:
            self.text_image = self.font.render(self.text, True, settings.LIGHT_GRAY)
        elif self.disabled is False:
            self.text_image = self.font.render(self.text, True, settings.WHITE)

    def update(self):
        """
        A function to check various conditions for the button.

        @return: none
        @rtype: none
        """
        pass

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
            if self.type == 'Error':
                screen.blit(self.text_ok_image, self.text_ok_rect)
            elif self.type == 'Confirm':
                screen.blit(self.text_confirm_image, self.text_confirm_rect)
            elif self.type == 'Confirm/Deny':
                screen.blit(self.text_yes_image, self.text_yes_rect)
                screen.blit(self.text_no_image, self.text_no_rect)
            elif self.type == 'None':
                pass
            else:
                print('[Debug - Error]: Button type could not be found nor displayed. Was the button created correctly?')
            # Line going around button
            pygame.draw.lines(screen, settings.WHITE, True, (
            (self.rect.x, self.rect.y),
            (self.rect.x, self.rect.y + self.rect.height),
            (self.rect.x + self.rect.width, self.rect.y + self.rect.height),
            (self.rect.x + self.rect.width, self.rect.y)))


class ButtonInput(object):
    """Class. Used to represent a button, with input, inside of the editor that can be displayed."""
    def __init__(self, editor_engine: object, name: str, text_ask: str, x: int, y: int, width=50, height=50):
        """
        Constructor. Used to initialize the button's attributes.

        @param editor_engine: the engine which controls the network of the editor when its ran
        @type editor_engine: object
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
        self.editor_engine = editor_engine
        # Button attributes
        self.FONT = pygame.font.SysFont('Consolas', 15)
        self.active = False
        self.image = pygame.Surface((width, height))
        self.image.fill(settings.DARK_GRAY)
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.user_input = text_ask
        self.text_ask = text_ask
        self.text_image = self.FONT.render(self.text_ask, True, settings.WHITE)
        self.text_rect = pygame.Rect(x + 5, y + 5, width / 2, height / 2)

    def handle_events(self, event: object, buttons: list):
        """
        A function to handle the actions of the user in regards to the button.

        @param event: the event that pygame was able to recognize based off of user interaction
        @type event: object
        @param buttons: a collection of buttons usually used for interating through and modifying specific buttons.
                        NOTE: This param is kept to keep the looping of buttons working properly due to code overlap and
                        NOTE: not wanting to have repeatable code.
        @type buttons: list
        @return: none
        @rtype: none
        """
        if self.active and event.type == pygame.KEYDOWN:
            if self.name == 'Input_Level':
                if event.key == pygame.K_RETURN:
                    # Cleanse before sending user input to the level select button
                    # TODO: Create bettor error handling/input cleansing so that the program doesn't shut down
                    self.editor_engine.level_select, self.editor_engine.level_sub_select = self.user_input.split(':')
                    self.user_input = ''
                    # Load new matrix
                    self.editor_engine.tile_map.load_tile_map()
                elif event.key == pygame.K_ESCAPE:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                else:
                    if self.user_input == self.text_ask:
                        self.user_input = ''
                    # TODO: Figure out what event.unicode does and then write comments over it
                    self.user_input += event.unicode
                self.text_image = self.FONT.render('Specify Level: ' + self.user_input, True, settings.WHITE)

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


class Animation(object):
    """Class. Used to handle, change, and play images."""
    def __init__(self, active: bool, animation_sub_direction: str, first_file_no_ext: str,
                 image_count: int, screen: object, trigger: int, x: int, y: int):
        """
        Constructor. Used to initialize the animation for later use.

        @param active: default should be false
        @type active: bool
        @param animation_sub_direction: the directory name of the images
        @type animation_sub_direction: str
        @param first_file_no_ext: first file of the folder without integers or extensions
        @type first_file_no_ext: str
        @param image_count: the total image count of the directory
        @type image_count: int
        @param screen: the display we push the animation to
        @type screen: object
        @param trigger: the threshold for the engine tick rate counter
        @param x: the x coordinate for the animation
        @type x: int
        @param y: the y coordinate for the animation
        @type y: int
        """
        self.active = active
        self.dir = settings.DIR_SPRITES_ANIMATION + '/' + animation_sub_direction + '/'
        self.images = []
        self.index = 0
        self.index_timer = 0
        for i in range(1, image_count + 1):
            self.images.append(pygame.image.load(self.dir + first_file_no_ext + str(i) + '.png').convert_alpha())
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.screen = screen
        self.trigger = trigger

    def update_animation(self):
        """
        A function that updates the animation's image index based on whether the counter for the
        engine tick rate hits the image trigger.

        @return: none
        @rtype: none
        """
        if self.active is True:
            # Update index
            if self.index_timer >= self.trigger:
                self.index += 1
                # Check constraints and update
                if self.index == len(self.images):
                    self.index = 0
                    self.active = False
                self.image = self.images[self.index]
                self.index_timer = 0
            self.index_timer += 1

    def draw_animation(self):
        """
        A function that pushes the animation image to the display.

        @return: none
        @rtype: none
        """
        self.screen.blit(self.image, self.rect)


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


class TileSpriteInit(pygame.sprite.Sprite):
    """Class. Used to create sprites from game file images for later use and manipulation."""

    def __init__(self, editor_engine: object, type: str, x: int, y: int):
        """
        Constructor. Used to create a sprite and add it to the groups for drawing the level.

        @param editor_engine: the engine which controls the network/functions of the editor when it starts
        @type editor_engine: object
        @param x: the desired horizontal location for the sprite to be initiated at
        @type x: int
        @param y: the desired vertical location for the sprite to be initiated at
        @type y: int
        """
        # Width: 32 Height: 32
        for i in range(10000):
            if type in editor_engine.tile_map.tile_types:
                image = editor_engine.tile_map.tile_types[type]
            else:
                # print(' \'' + str(type) + '\'')
                return
        self.groups = editor_engine.sprites_all
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
