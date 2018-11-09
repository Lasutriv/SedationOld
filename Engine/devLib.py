# A collection of classes and functions to help debug the game code. When naming in the program, use DEV_xxx_xxx
# for the class and function names.
# Tanner Fry
# tefnq2@mst.edu
import time
import pygame


class CharacterHandler(object):

    def __init__(self, engine: object, character: object):
        self.character = character
        self.engine = engine

    def push_animation_to_screen(self):
        # Displays current character animation on the screen frame by frame nicely
        prev_x = 50  # Start display pos
        prev_y = 100  # Start display pos
        for image in self.character.images:
            rect = image.get_rect()
            rect.x = prev_x
            rect.y = prev_y

            prev_x += 96
            if self.character.direction == 'Left':
                image = pygame.transform.flip(image, True, False)
            self.engine.screen.blit(image, rect)
