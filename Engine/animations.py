import settings

import pygame
import os


# Character
# NOTE: Only need images for moving right as we can always mirron them with the pygame.transform.flip() function
# TODO: Because of the above note, refactor to not include direction facing in the below function names


def add_none_images(images: list):
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Sprite_Char_Base_96_Trimmed_Idle.png').convert_alpha())


def add_climbing_right_images(images: list):
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Climbing/Sprite_Char_Base_96_Trimmed_Climbing1.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Climbing/Sprite_Char_Base_96_Trimmed_Climbing2.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Climbing/Sprite_Char_Base_96_Trimmed_Climbing3.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Climbing/Sprite_Char_Base_96_Trimmed_Climbing4.png').convert_alpha())


def add_idle_right_images(images: list):
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Breathing/Sprite_Char_Base_96_Trimmed_Breathing1.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Breathing/Sprite_Char_Base_96_Trimmed_Breathing2.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Breathing/Sprite_Char_Base_96_Trimmed_Breathing3.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Breathing/Sprite_Char_Base_96_Trimmed_Breathing4.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Breathing/Sprite_Char_Base_96_Trimmed_Breathing5.png').convert_alpha())


def add_run_right_images(images: list):
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Running/Sprite_Char_Base_96_Trimmed_Running1.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Running/Sprite_Char_Base_96_Trimmed_Running2.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Running/Sprite_Char_Base_96_Trimmed_Running3.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Running/Sprite_Char_Base_96_Trimmed_Running4.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Running/Sprite_Char_Base_96_Trimmed_Running5.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Running/Sprite_Char_Base_96_Trimmed_Running6.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Running/Sprite_Char_Base_96_Trimmed_Running7.png').convert_alpha())


# UI



def add_health_bar_bubble_images(images: list):
    dir = settings.DIR_SPRITES_UI + '/Health_Bar/Effect_Bubble'
    path = dir + '/Sprite_Health_Bar_Bubble_Effect'
    count_files = find_files_png(dir)
    for i in range(count_files):
        images.append(pygame.image.load(path + str(i + 1) + '.png'))


# Game


def add_loading_images(images: list):
    images.append(pygame.image.load(settings.DIR_SPRITES_UI + '/Loading/Sprite_Loading_960_1280_Lightning_Effect1.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_UI + '/Loading/Sprite_Loading_960_1280_Lightning_Effect2.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_UI + '/Loading/Sprite_Loading_960_1280_Lightning_Effect3.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_UI + '/Loading/Sprite_Loading_960_1280_Lightning_Effect4.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_UI + '/Loading/Sprite_Loading_960_1280_Lightning_Effect5.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_UI + '/Loading/Sprite_Loading_960_1280_Lightning_Effect6.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_UI + '/Loading/Sprite_Loading_960_1280_Lightning_Effect7.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_UI + '/Loading/Sprite_Loading_960_1280_Lightning_Effect8.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_UI + '/Loading/Sprite_Loading_960_1280_Lightning_Effect9.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_UI + '/Loading/Sprite_Loading_960_1280_Lightning_Effect10.png').convert_alpha())
    images.append(pygame.image.load(settings.DIR_SPRITES_UI + '/Loading/Sprite_Loading_960_1280_Lightning_Effect11.png').convert_alpha())

def add_grass_images(images: list):
    pass

# Misc Functions


def find_files_png(path: str):
    """
    A function return the number of png files in a given path.

    :param path:
    :type path:
    :return:
    :rtype:
    """
    counter = 0
    # Find all files in directory
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.png'):
                counter += 1
    return counter