import settings

import math
import os
import pygame


class TileSpriteInit(pygame.sprite.Sprite):
    """Class. Used to represent tiles as sprites for easier handling within the editor engine."""
    # TODO: Add a parameter for groups and then parse the groups so that the sprite can be completely unique
    def __init__(self, engine_editor: object, image_file_name: str, tile_x: int, tile_y: int):
        """
        Constructor. Used to initialize the sprite with its properties and add it to it's respective groups

        @param engine_editor: the engine which controls the network of the editor when its ran
        @type engine_editor: object
        @param image_file_name:
        @type image_file_name: str
        @param tile_x: the desired horizontal location relative to the top left of the mouse click
        @type tile_x: int
        @param tile_y: the desired vertical location relative to the top left of the mouse click
        @type tile_y: int
        """
        self.groups = engine_editor.sprites_all, engine_editor.sprites_ground
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.image.load(os.path.join(settings.DIR_SPRITES_ASSETS, image_file_name)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = tile_x
        self.rect.y = tile_y


class TileMap(object):
    """
    Class. Used to handle the overall matrix of a level that is being worked on. Other
    functionality includes being able to place tiles, change specific levels, and
    delete tiles from the overall matrix of a level.
    """
    def __init__(self, engine_editor: object, screen_width: int, screen_height: int):
        """
        Constructor. Used to initialize the tile matrix object with it's variables so that
                     it can properly handle events and the functions built within it.

        @param engine_editor: the engine which controls the network of the editor when its ran
        @type engine_editor: object
        @param screen_width: the designated screen width that the settings file or the user specifies
        @type screen_width: int
        @param screen_height: the designed screen height that the settings file or the user specifies
        @type screen_height: int
        """
        self.engine_editor = engine_editor
        self.screen_height = screen_height
        self.screen_width = screen_width

    def handle_events(self, editor_tab: object, event: object):
        """
        A function to call other functions and handle the user's actions/movements/reactions while
        using the program.

        @param editor_tab: a class representing the visual aspects of a split section on the left
                           side of the editor
        @type editor_tab: object
        @param event: a specific action that pygame recognized from the user
        @type event: object
        @return: none
        @rtype: none
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handling tiles on matrix
            if event.pos[0] > settings.TAB_SIZE and self.engine_editor.tile_selected != '':
                # Divide by 32 then round down to find x tile slot. Then * 32 for it's pixel location
                tile_place_x = (math.floor((event.pos[0]) / settings.TILE_SIZE)) * settings.TILE_SIZE
                tile_place_y = (math.floor((event.pos[1]) / settings.TILE_SIZE)) * settings.TILE_SIZE
                if self.engine_editor.tile_selected == 'DELETE':
                    self.delete_tile(tile_place_x, tile_place_y)
                else:
                    self.place_tile(self.engine_editor.tile_selected, tile_place_x, tile_place_y)

            # Selecting tiles from legend
            # TODO: Could we not think of an idea to import a spritesheet and display it and then add
            # CONT: what was clicked on into the editor? It would overall take a lot less code.
            if (0 < event.pos[0] < settings.TILE_SIZE) and (0 < event.pos[1] < settings.TILE_SIZE):
                self.engine_editor.tile_selected = 'DELETE'
                print('Deletion selected.')
            if editor_tab.image_base_grass_rect.collidepoint(event.pos[0], event.pos[1]):
                self.engine_editor.tile_selected = 'Base_Grass'
                editor_tab.tile_selected_image = pygame.image.load('Assets/Ground_Basic_Grass_32.png').convert_alpha()
                editor_tab.tile_selected_rect = pygame.Rect(32, 0, 32, 32)
            elif editor_tab.image_base_dark_gray_rect.collidepoint(event.pos[0], event.pos[1]):
                self.engine_editor.tile_selected = 'Base_Background'
                editor_tab.tile_selected_image = pygame.image.load('Assets/Ground_Dark_Gray_32.png').convert_alpha()
                editor_tab.tile_selected_rect = pygame.Rect(0, 32, 32, 32)
            if self.engine_editor.tile_selected != 'DELETE':
                print('[Debug - Info]: ', self.engine_editor.tile_selected + ' selected.')

    def change_tile_matrix(self, info_replace, tile_x, tile_y):
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
        if self.engine_editor.level_loaded is True:
            path_to_level = 'Levels/Level_' + str(self.engine_editor.level_select) + '/Sub_Level_' + str(self.engine_editor.level_sub_select) + '.txt'
            line_counter = 0
            data_counter = 0
            line_finished = ''
            lines_started = []
            lines_finished = []
            # Subtract by 3 because of 96pxtab
            pos_for_matrix = (tile_x / settings.TILE_SIZE) - 3, tile_y / settings.TILE_SIZE

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
                    if (line_finished[-1] == '\n'):
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
        else:
            print('[Debug - Info]: A level wasn\'t loaded, therefore your tiles aren\'t being saved right now.')

    def load_tile_matrix(self):
        """
        A function to load a specific matrix from the levels folder onto the editor for editing.

        @return: none
        @rtype: none
        """
        # Setup info
        line_counter = 0
        path_to_level = 'Levels/Level_' + str(self.engine_editor.level_select) + '/Sub_Level_' + str(self.engine_editor.level_sub_select) + '.txt'
        # Wipe last tile matrix
        for sprite in self.engine_editor.sprites_all:
            self.engine_editor.sprites_all.remove(sprite)
        # Load tile matrix
        with open(path_to_level, 'r') as file:
            for line in file:
                data_counter = 0
                data_from_line = line.split(' ')
                for data in data_from_line:
                    if data == 'NA' or data == 'NA\n':
                        # Nothing in spot, paint nothing to grid
                        pass
                    if data == 'BG' or data == 'BG\n':
                        # We add 64 because of the tab window being 64 pixels wide for the controls
                        self.place_tile('Base_Grass', (data_counter * settings.TILE_SIZE) + settings.TAB_SIZE, (line_counter * settings.TILE_SIZE))
                    if data == 'BB' or data == 'BB\n':
                        # Base background, black/gray?, paint tile to grid
                        self.place_tile('Base_Background', (data_counter * settings.TILE_SIZE) + settings.TAB_SIZE, (line_counter * settings.TILE_SIZE))
                    data_counter += 1
                line_counter += 1
            self.engine_editor.level_loaded = True

    def transfer_tile_matrix(self):
        """
        A function to transfer the current level being worked on to the Levels folder in the engine.

        @return: none
        @rtype: none
        """
        from shutil import copyfile
        # NOTE: use the change_tile_matrix to get ideas of how to do it
        path_to_project = os.path.realpath(__file__)
        path_to_project = path_to_project.strip('Tile_Editor\editorLib.py')
        path_to_project = path_to_project.replace('\\', '/')
        path_to_level = 'Levels/Level_' + str(self.engine_editor.level_select) + '/Sub_Level_' + str(self.engine_editor.level_sub_select) + '.txt'
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
        if tile_selected == 'Base_Grass':
            self.info_replace = 'BG'
            TileSpriteInit(self.engine_editor, 'Ground_Basic_Grass_32.png', tile_x, tile_y)
        elif tile_selected == 'Base_Background':
            self.info_replace = 'BB'
            TileSpriteInit(self.engine_editor, 'Ground_Dark_Gray_32.png', tile_x, tile_y)
        # Change and update the matrix
        self.change_tile_matrix(self.info_replace, tile_x, tile_y)

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
        for sprite in self.engine_editor.sprites_all:
            if tile_x == sprite.rect.x and tile_y == sprite.rect.y:
                self.engine_editor.sprites_all.remove(sprite)
                # Delete tile from the matrix
                print('deleting tile')
                self.change_tile_matrix('NA', tile_x, tile_y)

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
    def __init__(self, screen: object):
        """
        Constructor. Used to set up the tools/tiles object for manipulation during runtime.

        @param screen: the display that all of the tools/tiles will be displayed to
        @type screen: object
        """
        self.screen = screen
        # Assets used to display tiles in the editor tab to click on and use for selection.
        self.image_base_grass = pygame.image.load('Assets/Ground_Basic_Grass_32.png').convert_alpha()
        self.image_base_grass_rect = pygame.Rect(32, 0, 32, 32)
        self.image_base_dark_gray = pygame.image.load('Assets/Ground_Dark_Gray_32.png').convert_alpha()
        self.image_base_dark_gray_rect = pygame.Rect(0, 32, 32, 32)

    def draw(self, buttons: list):
        """
        A function to draw the tiles on the left side of the editor within a 64 pixel wide space starting
        all the way on the left.

        @param buttons: a collection of buttons that are currently handling events
        @type buttons: list
        @return: none
        @rtype: none
        """
        # Display the sprites tool bar on the left side which is used to make the matrix.
        self.screen.blit(self.image_base_grass, (self.image_base_grass_rect.x, self.image_base_grass_rect.y))
        self.screen.blit(self.image_base_dark_gray, (self.image_base_dark_gray_rect.x, self.image_base_dark_gray_rect.y))
        for button in buttons:
            button.draw(self.screen)


class Button(object):
    """Class. Used to represent a button within the editor that is being displayed."""
    def __init__(self, engine_editor: object, name: str, text: str, type: str, font_size: int, button_x: int, button_y: int,
                 **kwargs):
        """
        Constructor. Used to initialize the button's attributes.

        @param engine_editor: the engine which controls the network of the editor when its ran
        @type engine_editor: object
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
        self.engine_editor = engine_editor
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
        @return: none
        @rtype: none
        """
        # Check and see if mouse hits a specific button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.name == 'Exit':
                    self.engine_editor.running = False
                if self.name == 'Load':
                    self.engine_editor.button_input_level.active = not self.engine_editor.button_input_level.active
                if self.name == 'Transfer':
                    for button in buttons:
                        if button.name == 'Ask_To_Transfer':
                            button.active = True
                            print(self.name, ' set active to ', self.active)
                # Handle clicking on specific buttons based on their type
                if self.type == 'Error':
                    if self.text_ok_rect.collidepoint(event.pos):
                        if self.name == 'Tile_Error':
                            self.active = False
                            print(self.name, ' set active to ', self.active)
                elif self.type == 'Confirm':
                    if self.text_confirm_rect.collidepoint(event.pos):
                        pass
                if self.type == 'Confirm/Deny':
                    if self.text_yes_rect.collidepoint(event.pos):
                        if self.name == 'Ask_To_Transfer':
                            self.active = False
                            print(self.name, ' set active to ', self.active)
                            self.engine_editor.tile_matrix.transfer_tile_matrix()
                    elif self.text_no_rect.collidepoint(event.pos):
                        self.active = False
                        print(self.name, ' set active to ', self.active)
            # Display button error if user clicks with specified condition
            if self.name == 'Tile_Error' and event.pos[0] > settings.TAB_SIZE and self.engine_editor.tile_selected == '':
                self.active = True
                print(self.name, ' set active to ', self.active)
            elif self.name == 'Tile_Error' and self.engine_editor.tile_selected != '':
                self.active = False
                print(self.name, ' set active to ', self.active)

        # Set buttons active that need to be
        if self.name == 'Load' or self.name == 'Exit':
            self.active = True
        if self.name == 'Transfer':
            self.active = True
            if self.engine_editor.level_loaded is True:
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
    def __init__(self, engine_editor: object, tile_matrix_handler: object, name: str, text_ask: str, x: int, y: int, width=50, height=50):
        """
        Constructor. Used to initialize the button's attributes.

        @param engine_editor: the engine which controls the network of the editor when its ran
        @type engine_editor: object
        @param tile_matrix_handler: the handler for loading, editing, and saving the tile matrix within each level
        @type tile_matrix_handler: object
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
        self.engine_editor = engine_editor
        self.tile_matrix_handler = tile_matrix_handler
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
        @param buttons: a collection of buttons usually used for interating through and modifying specific buttons
        @type buttons: list
        @return: none
        @rtype: none
        """
        if self.active and event.type == pygame.KEYDOWN:
            if self.name == 'Input_Level':
                if event.key == pygame.K_RETURN:
                    # Cleanse before sending user input to the level select button
                    # TODO: Create bettor error handling/input cleansing so that the program doesn't shut down
                    self.engine_editor.level_select, self.engine_editor.level_sub_select = self.user_input.split(':')
                    self.user_input = ''
                    # Load new matrix
                    self.tile_matrix_handler.load_tile_matrix()
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