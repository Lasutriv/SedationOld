import editorLib
import settings

import pygame
import os


class Editor(object):

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tile Editor")
        self.clock = pygame.time.Clock()
        self.level_loaded = False
        self.level_select = 0
        self.level_sub_select = 0
        self.running = False
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.tile_size = 32
        self.tile_selected = ''
        self.tile_selected_image = ''
        self.tile_selected_rect = ''
        # Setup
        self.sprites_all = pygame.sprite.Group()
        self.sprites_ground = pygame.sprite.Group()
        # Set up display
        self.editor_tab = editorLib.EditorTab(self.screen)
        self.tile_matrix = editorLib.TileMap(self, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        self.button_load = editorLib.Button(self, 'Load', 'Load', 'None', 15, 10, 840, override_text_x=30, override_width=74)
        self.button_input_level = editorLib.ButtonInput(self, self.tile_matrix, 'Input_Level', 'Specify Level: [Level:Sublevel]', 82, 815, 67, 25)
        self.button_transfer = editorLib.Button(self, 'Transfer', 'Transfer', 'None', 15, 10, 880)
        self.button_ask = editorLib.Button(self, 'Ask_To_Transfer', 'Are you sure you want to transfer the level matrix?',
                                           'Confirm/Deny', 15, settings.SCREEN_WIDTH / 2 - 160, settings.SCREEN_HEIGHT / 2)
        self.button_exit = editorLib.Button(self, 'Exit', 'Exit', 'None', 15, 10, 920, override_text_x=30, override_width=74)
        self.button_error = editorLib.Button(self, 'Tile_Error', 'Please select a tile before selecting a slot.', 'Error', 15,
                                             settings.SCREEN_WIDTH / 2 - 190 + 64, settings.SCREEN_HEIGHT / 2)
        self.buttons = [self.button_load, self.button_input_level, self.button_transfer, self.button_ask, self.button_exit, self.button_error]

    def editor_new(self):
        # TODO: Remove all content for new editor if called again
        # Empty self.sprites_all and self.buttons

        # Create new display
        # TODO: End of todo
        # Start the editor
        self.editor_run()

    def editor_run(self):
        self.running = True
        while self.running:
            self.editor_events()
            self.editor_update()
            self.editor_draw()
        pygame.quit()

    def editor_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pass
                    # self.running = False

            # Clicking on buttons
            for button in self.buttons:
                button.handle_events(event, self.buttons)

            # Clicking/working with the tile matrix
            self.tile_matrix.handle_events(self.editor_tab, event)

    def editor_update(self):
        self.sprites_all.update()
        for button in self.buttons:
            button.update()

    def editor_draw(self):
        self.screen.fill((0, 0, 0))
        self.tile_matrix.draw_grid(self.screen, self.tile_size)

        # Display the editor tab and other sprites
        self.sprites_all.draw(self.screen)
        self.editor_tab.draw(self.buttons)

        # Display buttons that are active
        for button in self.buttons:
            button.draw(self.screen)
            if button.name == 'Ask_To_Transfer':
                pass
        pygame.display.flip()


if __name__ == "__main__":
    # Center the game screen
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    editor_engine = Editor()
    editor_engine.editor_new()
