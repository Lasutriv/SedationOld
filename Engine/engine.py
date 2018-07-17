import animations
import character
import engineLib
import settings

import importlib
import os
import pygame


class Game:
    """Class. Used to handle the creation, modification, and deletion of all game assets."""
    def __init__(self):
        """
        Constructor. Used to initialize all handlers, timers, and other variables for the game to function properly.
        """
        # Initialize the game engine with necessary variables
        self.character = pygame.sprite.Sprite
        self.clock = pygame.time.Clock()
        self.engine_handler = engineLib.EngineHandler()
        self.level_current = 1
        self.level_directions = ''  # The directions that the character can go to get to adjacent levels
        self.level_directions_down = 'None'  # The level number of the level below the current level
        self.level_directions_left = 'None'  # The level number of the level to the left of the current level
        self.level_directions_right = 'None'  # The level number of the level to the right of the current level
        self.level_directions_up = 'None'  # The level number of the level above the current level
        self.level_matrix = []  # A 2-d matrix representing a 'map' of the level where each position in the matrix is a sub-level
        self.level_matrix_location = [0, 0]  # The character's current location in the level matrix
        self.level_sub_current = 1
        self.level_sub_current_total = 0  # The number of total sub-levels in the current level
        self.level_sub_total = 0  # The number of total sub-levels
        self.level_total = settings.TOTAL_LEVELS
        self.running = False
        self.screen = pygame.Surface
        self.sprites_all = pygame.sprite.Group()
        self.sprites_walls = pygame.sprite.Group()
        self.window = pygame.Surface

    # Main function to set up a NEW game
    def game_new(self, file_save_name: str, character_name='Caesar'):
        # Initialize assets for the NEW game
        self.engine_handler = engineLib.EngineHandler()
        self.screen = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.window = pygame.display.set_mode((self.engine_handler.gather_engine_info(self, 'calculate_window')))
        # NOTE: Reimport all libraries for easier code change and testing
        importlib.reload(engineLib)
        self.engine_handler.reimport_all()

        # Gather information
        self.engine_handler.gather_engine_info(self, 'get_levels')

        # Generate new settings file for the character to use, whether from defaults or the character save
        if character_name != 'Caesar':
            self.engine_handler.save_new_game(character_name, file_save_name)
        else:
            self.engine_handler.load_saved_game(file_save_name)
            character_name = settings.CHAR_NAME

        # Initialize other assets for the NEW game
        self.character = character.Character(character_name, file_save_name, self, settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2)
        self.sprites_all.add(self.character)
        pygame.display.set_caption(settings.TITLE_GAME)

        # Generate assets and start the game
        self.engine_handler.generate_level(self, self.level_current, self.level_sub_current)

        # self.level_matrix.lvl = self.engine_handler.generate_level_matrix(self.engine_main)
        self.engine_handler.generate_level_matrix(self)
        self.running = True
        self.game_run()

    # Main function to run the game
    def game_run(self):
        while self.running:
            self.game_events()
            self.game_update()
            self.game_draw()

    # Main function to handle events in the game
    def game_events(self):
        # Check events and handle them
        for event in pygame.event.get():
            self.engine_handler.handle_events(event, self, self.character, self.sprites_all, self.sprites_walls)
        # Grab movements
        self.character.handle_keys()
        # Check for map rotation
        self.engine_handler.check_character_close_to_exit(self, self.character)
        if self.engine_handler.screen_switch:
            self.engine_handler.generate_level_switch(self, self.character, self.sprites_all, self.sprites_walls)

    # Main function to update any information in the game
    def game_update(self):
        self.sprites_all.update()

    # NOTE: REMOVE LATER: A function to draw tile sizes.
    def game_draw_grid(self):
        for x in range(0, settings.SCREEN_WIDTH, settings.TILE_SIZE):
            pygame.draw.line(self.screen, settings.LIGHT_GRAY, (x, 0), (x, settings.SCREEN_HEIGHT))
        for y in range(0, settings.SCREEN_HEIGHT, settings.TILE_SIZE):
            pygame.draw.line(self.screen, settings.LIGHT_GRAY, (0, y), (settings.SCREEN_WIDTH, y))

    # Main function to draw all of the information, old and new
    def game_draw(self):
        # TODO: Add backgrounds, create an object with a draw function that when the screen is changed to calculate the next screen, OR we could load the level's
        # CONT: backgrounds at the beginning so that there isn't any hard computation, just referencing.
        # Draw background

        # Draw level
        self.screen.fill(settings.DARK_GRAY)
        # self.game_draw_grid()

        # Draw characters and objects
        self.sprites_all.draw(self.screen)
        # self.sprites_walls.draw(self.screen)
        print('Walls:', self.sprites_walls)

        # Draw UI
        self.engine_handler.draw_ui_debug(self, self.screen, self.character)
        self.engine_handler.draw_ui_game(self.screen, self.character)
        # Draw other visuals based on graphics setting...
        self.engine_handler.check_game_graphics(self.screen, True)
        # Display developer information
        self.engine_handler.DEV_time_handler.clock_board_print() # NOTE: Prints once due to performance issues
        # Scale screen to the size of user's window
        pygame.transform.scale(self.screen, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), self.window)
        pygame.display.flip()
        self.clock.tick(settings.FPS)


class MainMenu:
    """Class. Used to work with the menu and keep smooth control flow."""
    def __init__(self, engine_game: object):
        """
        Constructor. Used to initialize the menu system and incorporate the engine foor the game so we cann
                     run specific functions including the game itself.

        @param engine_game: the engine which controls the network/functions of the game when it starts after the menu
        @type engine_game: object
        """
        # Initialize the menu with the necessities
        pygame.display.set_caption(settings.TITLE_GAME)
        self.clock = pygame.time.Clock()
        self.engine_handler = engineLib.EngineHandler()
        self.engine_game = engine_game
        self.menu_handler = engineLib.MenuHandler(self)
        self.running = True
        self.state = 'None'

        # Initializing screen/snow
        self.screen = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.window = pygame.display.set_mode((self.engine_handler.gather_engine_info(self.engine_game, 'calculate_window')))
        self.snow_handler = engineLib.SnowHandler(self.screen)

        # Initializing styling attributes
        self.background_color = settings.DARK_GRAY
        self.menu_text_color = settings.DEEP_GRAY
        # User attributes
        self.character_name = ''
        self.file_load_save = ''
        # Misc attributes
        self.buttons = []
        self.popups = []
        self.sprites_all = pygame.sprite.Group()

    # Menu setup

    def menu_start(self):
        """
        The setup of all other assets for the menu and game later..

        @return: none
        @rtype: none
        """
        # Run loading animation
        self.menu_loading()
        # Run menu handler and the menu screens via the handler, returns a state for either starting a
        # new game, loading an existing game, or exiting the menu.
        return self.menu_state_handler()

    # Menu Loading

    def menu_loading(self):
        """
        This function allows the programmer to load up assets, sprites, and other data/information needed to run
        the game smoothly before playing.

        @return: none
        @rtype: none
        """
        images = []
        animations.add_loading_images(images)
        image_index = 0
        image = images[image_index]
        image_rect = image.get_rect()
        loading = True
        timer_images = 0
        timer_images_trigger = 7

        while loading is True:
            timer_images += 1
            if timer_images == timer_images_trigger:
                image_index += 1
                timer_images = 0

                # Check for end of images
                if image_index == len(images) - 1:
                    image_index = 0

                    loading = False
            image = images[image_index]
            self.screen.fill(self.menu_text_color)
            self.screen.blit(image, image_rect)
            pygame.transform.scale(self.screen, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), self.window)
            pygame.display.flip()

    # Menu Screens

    def menu_main(self):
        """
        The main menu screen to display all of the options to the user when they load the game.

        @return: none
        @rtype: none
        """
        self.character_sample = character.Character('Caesar', 'Caesar.py', self.engine_game, -100, settings.SCREEN_HEIGHT / 2)
        self.character_sample.state = 'Running'
        self.character_sample.state_changed = True
        self.character_sample.direction = 'Right'
        self.sprites_all.add(self.character_sample)
        self.button_start = engineLib.MenuButton(self, 'Start', 'Start', 35, self.menu_text_color, settings.WHITE, settings.SCREEN_WIDTH / 2 - 50, settings.SCREEN_HEIGHT / 2 - 100, True, False, False, True)
        self.button_load = engineLib.MenuButton(self, 'Load', 'Load', 35, self.menu_text_color, settings.WHITE, settings.SCREEN_WIDTH / 2 - 40, settings.SCREEN_HEIGHT / 2 - 45, True, False, False, True)
        self.button_options = engineLib.MenuButton(self, 'Options', 'Options', 35, self.menu_text_color, settings.WHITE, settings.SCREEN_WIDTH / 2 - 70, settings.SCREEN_HEIGHT / 2 + 10, True, False, False, True)
        self.button_help = engineLib.MenuButton(self, 'Help', 'Help', 35, self.menu_text_color, settings.WHITE, settings.SCREEN_WIDTH / 2 - 40, settings.SCREEN_HEIGHT / 2 + 65, True, False, False, True)
        self.button_feedback = engineLib.MenuButton(self, 'Feedback', 'Feedback', 35, self.menu_text_color, settings.WHITE, settings.SCREEN_WIDTH / 2 - 80, settings.SCREEN_HEIGHT / 2 + 120, True, False, False, True)
        self.button_exit = engineLib.MenuButton(self, 'Exit', 'Exit', 35, self.menu_text_color, settings.WHITE, settings.SCREEN_WIDTH / 2 - 40, settings.SCREEN_HEIGHT / 2 + 175, True, False, False, True)
        self.buttons = [self.button_start, self.button_load, self.button_options, self.button_help, self.button_feedback, self.button_exit]

    def menu_create_character(self):
        self.state = 'Create_Character'
        # / 2 - 160 - 100 --> 160 = 10px * num_of_chars_in_question, 100 = 10px * num_of_chars_in_avg_names
        self.button_input_char_name = engineLib.MenuButtonInput(self, 'Input_Create_Char_Name', 'Character Name: ', settings.SCREEN_WIDTH / 2 - 150, settings.SCREEN_HEIGHT / 2 - 30, width=50, height=25)
        self.button_input_file_name = engineLib.MenuButtonInput(self, 'Input_File_Save_Name', 'Save File Name: ', settings.SCREEN_WIDTH / 2 - 150, settings.SCREEN_HEIGHT / 2, width=50, height=25)
        self.button_submit = engineLib.MenuButton(self, 'Submit', 'Submit', 35, self.menu_text_color, settings.WHITE, settings.SCREEN_WIDTH - 195, settings.SCREEN_HEIGHT - 95, True, False, False, True)
        self.button_back = engineLib.MenuButton(self, 'Back', 'Back', 35, self.menu_text_color, settings.WHITE, 99, settings.SCREEN_HEIGHT - 95, True, False, False, True)
        self.buttons = [self.button_input_char_name, self.button_input_file_name, self.button_submit, self.button_back]

    def menu_load(self):
        """
        A screen picked from the main menu to load an earlier saved game file.

        @return: none
        @rtype: none
        """
        self.button_cat_saves = engineLib.MenuButton(self, 'Load_Cat_Saves', 'Saves', 25, self.menu_text_color, settings.UI_BANNER_BACKGROUND, 103, 30, True, True, True, True)
        self.button_submit = engineLib.MenuButton(self, 'Submit', 'Submit', 35, self.menu_text_color, settings.WHITE, settings.SCREEN_WIDTH - 195, settings.SCREEN_HEIGHT - 95, True, True, False, True)
        self.button_back = engineLib.MenuButton(self, 'Back', 'Back', 35, self.menu_text_color, settings.WHITE, 99, settings.SCREEN_HEIGHT - 95, True, False, False, True)
        self.buttons = [self.button_cat_saves, self.button_submit, self.button_back]

    def menu_options(self):
        """
        A screen picked from the main menu or the pause menu to allow the viewing and changing of many options for how your game runs.

        @return: none
        @rtype: none
        """
        # Create navigation bar with 30px buffer between each selection
        self.button_cat_controls = engineLib.MenuButton(self, 'Options_Cat_Controls', 'Controls', 25, self.menu_text_color, settings.WHITE, 50, 35, True, False, False, True)
        self.button_cat_game = engineLib.MenuButton(self, 'Options_Cat_Game', 'Game', 25, self.menu_text_color, settings.WHITE, 190, 35, True, False, False, True)
        self.button_cat_sound = engineLib.MenuButton(self, 'Options_Cat_Sound', 'Sound', 25, self.menu_text_color, settings.WHITE, 274, 35, True, False, False, True)
        self.button_cat_video = engineLib.MenuButton(self, 'Options_Cat_Video', 'Video', 25, self.menu_text_color, settings.WHITE, 372, 35, True, False, False, True)

        # Misc
        self.button_back = engineLib.MenuButton(self, 'Back', 'Back', 35, self.menu_text_color, settings.WHITE, 99, settings.SCREEN_HEIGHT - 95, True, False, False, True)
        self.buttons = [self.button_cat_controls, self.button_cat_game, self.button_cat_sound, self.button_cat_video, self.button_back]

    def menu_help(self):
        """
        A screen picked from the main menu or the pause menu to allow the viewing of controls, lore help, or other kind of help the user may need.

        @return: none
        @rtype: none
        """
        # Create navigation bar with 30px buffer between each selection
        self.button_cat_categories = engineLib.MenuButton(self, 'Help_Cat_Cat', 'Categories', 25, self.menu_text_color, settings.UI_BANNER_BACKGROUND, 70, 30, True, False, True, True)
        # Misc
        self.button_back = engineLib.MenuButton(self, 'Back', 'Back', 35, self.menu_text_color, settings.WHITE, 99, settings.SCREEN_HEIGHT - 95, True, False, False, True)
        self.buttons = [self.button_cat_categories, self.button_back]

    # TODO: Create a 'feedback' sub-menu
    def menu_feedback(self):
        """
        A screen picked from the main menu to allow the user to give specific feedback on the game, whether it's the
        physics engine that is acting up, the character's traits or skills, or anything that might need to be sent to
        myself for error handling.

        @return: none
        @rtype: none
        """
        self.button_submit = engineLib.MenuButton(self, 'Submit', 'Submit', 35, self.menu_text_color, settings.WHITE, settings.SCREEN_WIDTH - 195, settings.SCREEN_HEIGHT - 95, True, True, False, True)
        self.button_back = engineLib.MenuButton(self, 'Back', 'Back', 35, self.menu_text_color, settings.WHITE, 99, settings.SCREEN_HEIGHT - 95, True, False, False, True)
        self.buttons = [self.button_submit, self.button_back]

    # Sub Menu Screens

    def menu_options_video(self):
        """
        A screen picked from the options screen of the main menu or pause menu that allows the viewing of specific video settings for user to modify regarding
        the game.

        @return: none
        @rtype: none
        """
        # Create navigation bar with 30px buffer between each selection
        self.button_cat_controls = engineLib.MenuButton(self, 'Options_Cat_Controls', 'Controls', 25, self.menu_text_color, settings.WHITE, 50, 35, True, False, False, True)
        self.button_cat_game = engineLib.MenuButton(self, 'Options_Cat_Game', 'Game', 25, self.menu_text_color, settings.WHITE, 190, 35, True, False, False, True)
        self.button_cat_sound = engineLib.MenuButton(self, 'Options_Cat_Sound', 'Sound', 25, self.menu_text_color, settings.WHITE, 274, 35, True, False, False, True)
        self.button_cat_video = engineLib.MenuButton(self, 'Options_Cat_Video', 'Video', 25, self.menu_text_color, settings.WHITE, 372, 35, True, False, False, True)
        # Create video options, 10px space between each
        graphics_text = 'Graphics: [' + settings.GRAPHICS + ']'
        resolution_text = 'Resolution: [' + str(settings.WINDOW_WIDTH) + ', ' + str(settings.WINDOW_HEIGHT) + ']'
        self.button_graphics = engineLib.MenuButton(self, 'Options_Video_Graphics', graphics_text, 20, self.menu_text_color, settings.WHITE, 50, 120, True, True, True, False)
        self.button_resolution = engineLib.MenuButton(self, 'Options_Video_Resolution', resolution_text, 20, self.menu_text_color, settings.WHITE, 50, 90, True, True, True, False)
        # Misc
        self.button_back = engineLib.MenuButton(self, 'Back', 'Back', 35, self.menu_text_color, settings.WHITE, 99, settings.SCREEN_HEIGHT - 95, True, False, False, True)
        self.buttons = [self.button_cat_controls, self.button_cat_game, self.button_cat_sound, self.button_cat_video, self.button_graphics, self.button_resolution, self.button_back]

    # Menu System - A system to update the view and catch any events on any of the menu screens and then handle those events appropriately whether it's launching the game,
    #               pausing the game, changing settings, or saving.

    def menu_state_handler(self):
        """
        A function to handle switching between screens on the menu without hogging resources via recursion.

        @return: returns the state of the game so that the menu object can be tossed for proper resource management and
                 then the state is used to determine whether to start a new game, load a game, or exit the game completely.
        @rtype: str
        """
        handler_running = True
        while handler_running is True:
            self.running = True
            if self.state == 'None':
                self.state = 'Main'
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
                print('[Debug - Info]: MainMenu.menu_state_handler() is shutting down.')
                handler_running = False
            if self.state != 'None' and self.state != 'Exit' and self.state != 'Load_New' and self.state != 'Load_Save':
                self.menu_run()
            print('[Debug - Info]: State changed to \'' + self.state + '\'.')

        # Return the state so that the next action can be taken. States include 'Load_New', 'Load_Save', and 'Exit'
        return self.state

    def menu_run(self):
        """
        A function that performs all of the tasks necessary for the menu to function properly.

        @return: none
        @rtype: none
        """
        while self.running:
            self.menu_events()
            self.menu_update()
            self.menu_draw()

    def menu_events(self):
        """
        A function to handle all capture and handle all menu events for the menu to function properly.

        @return: none
        @rtype: none
        """
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()

            # Needed to fix the mouse position after the screen is scaled
            mouse_pos = (mouse_pos[0] / settings.RES_WIDTH_RATIO, mouse_pos[1] / settings.RES_HEIGHT_RATIO)

            # Check special keys, catch menu restart
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pass
                    # self.running = False

            # Handle buttons on menu
            for button in self.buttons:
                button.handle_events(self.buttons, event, mouse_pos)
            for popup in self.popups:
                popup.handle_events(self.engine_game, self.popups, event, mouse_pos)

    def menu_update(self):
        """
        A function that updates  all of the buttons if needed as well as the screen.

        @return: none
        @rtype: none
        """
        self.screen.fill(settings.WHITE)
        # Some input buttons require an update based on text input into them
        for button in self.buttons:
            button.update()

        # Handle sample character running across the screen. Sample character needs to be updated before the update() function due
        # to using the preset character template and conflicting issues via universal forces such as gravity, air resistance, and more.
        self.character_sample.state = 'Running'
        self.character_sample.falling = False
        self.character_sample.running = True
        self.character_sample.x_velocity = settings.CAP_VELOCITY_RUNNING + 10
        self.sprites_all.update()
        self.character_sample.rect.y = settings.SCREEN_HEIGHT - self.character_sample.rect.height
        if self.character_sample.rect.x > settings.SCREEN_WIDTH + 100:
            self.character_sample.rect.x = -100

    def menu_draw(self):
        """
        A function to draw all the buttons, visual effects, and scale the game screen to the specified resolution.

        @return: none
        @rtype: none
        """
        # Draw the sample character running across the screen
        self.sprites_all.draw(self.screen)
        # Draw specific visuals for sub menus
        self.menu_handler.draw_sub_menu_visuals(self.screen)
        # Draw other visuals based on graphics setting...
        self.engine_handler.check_game_graphics(self.screen, False)
        # Draw information over visuals
        for button in self.buttons:
            button.draw(self.screen)
        for popup in self.popups:
            popup.draw(self.screen)
        # Draw snow
        self.snow_handler.draw()
        # Scale screen
        pygame.transform.scale(self.screen, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), self.window)
        pygame.display.flip()
        self.clock.tick(30)


def main():
    pygame.init()
    # Runs this if this is the main file
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the game screen
    print('[Debug - Info]: Starting pygame.')
    engine_game = Game()
    engine_main_menu = MainMenu(engine_game)
    print('[Debug]: Engine objects - ', engine_game, '\t', engine_main_menu)
    # Start the menu for the game and find the user's next course of action
    pygame_running = True
    while pygame_running is True:
        desired_state = engine_main_menu.menu_start()
        if desired_state == 'Load_New':
            # Start new game
            print('[Debug - Info]: New game being loaded.')
            engine_game.game_new(engine_main_menu.file_load_save, character_name=engine_main_menu.character_name)
            engine_main_menu.state = 'Main'
            print('[Debug - Info]: New game being closed.')
        elif desired_state == 'Load_Save':
            # Load a saved game
            print('[Debug - Info]: Saved game being loaded.')
            engine_game.game_new(engine_main_menu.file_load_save)
            engine_main_menu.state = 'Main'
            print('[Debug - Info]: Saved game being closed.')
        elif desired_state == 'Exit':
            print('[Debug - Info]: Exiting menu.')
            print('[Debug - Info]: Reloading default settings.')
            engine_game.engine_handler.rewrite_settings()
            pygame_running = False
        else:
            print('[Debug - Error]: engine_main_menu.menu_start() returned an invalid state.')
        print('[Debug - Info]: Reloading default settings.')
        engine_game.engine_handler.rewrite_settings()
    print('[Debug - Info]: End of main.')
    pygame.quit()


if __name__ == '__main__':
    main()
    print('[Debug - Info]: Exiting ' + settings.TITLE_GAME + '.')