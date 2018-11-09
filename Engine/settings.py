# Loaded settings defaults
# Tanner Fry
# tefnq2@mst.edu

# NOTE: If any setting is added into this file then please double check that it is added into the settings_defaults.py
# NOTE: file as well as the Bin/Backups/settings_defaults.py file
# Colors base
RED = (255, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
VIOLET = (148, 0, 211)
# Colors alt
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
DEEP_GRAY = (16, 16, 16)
DARK_GRAY = (105, 105, 105)
DARKER_GRAY = (174, 174, 174)
GRAY = (180, 180, 180)
LIGHT_GRAY = (211, 211, 211)
PURPLE = (106, 49, 202)
TAN = (210, 180, 140)
WHITE = (255, 255, 255)

TRANSPARENT = (255, 255, 255)

# Colors for the UI
UI_BANNER_BACKGROUND = PURPLE
UI_BANNER_FOREGROUND = WHITE
UI_FEEDBACK_TEXT = DARKER_GRAY

# File/folder locations
# TODO: Finish directory changes to streamline the ease of location changing later.
# CONT: Change any directories with the name 'Test' in it and add from them any of the
# CONT: sprites we will be using.
DIR_SPRITES_CHAR_BASE = 'Bin/Sprites/Char_Base'
DIR_SPRITES_GAME_ENVI = 'Bin/Sprites/Game_Environment'
DIR_SPRITES_GAME_INV = 'Bin/Sprites/Game_Inventory_Items'
DIR_SPRITES_NPC = 'Bin/Sprites/NPCs/Test'
DIR_SPRITES_UI = 'Bin/Sprites/User_Interface'

# Game
# Novice Casual Master Godlike
DIFFICULTY = 'Casual'
FPS = 60
GRAPHICS = 'High'
TITLE_GAME = 'Sedation'
TOTAL_LEVELS = 2
TOTAL_LEVEL_ASSETS = 0  # Tells how many blocks a tile map level will be using. Could use to optimize for bigger maps

# Game obstacle endurance requirements
REQ_CLIMBING_ENDURANCE = 2
REQ_JUMP_ENDURANCE = 5

# Project
CREATED = 'January 14th, 2018'
RELEASED = 'TBD'
CREATOR = 'Tanner Fry'
VERSION = '0.0.7'

# Window
# Tiles - 40 squares by 30 squares
TILE_SIZE = 32
GRID_WIDTH = 40
GRID_HEIGHT = 30
RES_CHANGED = True
# 1.125 1080/960
RES_HEIGHT_RATIO = 0.9375
# 1.5 1920/1280
RES_WIDTH_RATIO = 1.125
SCREEN_HEIGHT = 960
SCREEN_WIDTH = 1280
WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1440

# Character - At bottom due to extensive variable amount
# TODO: Rename character settings that don't have 'CHAR_' in front of them. Remember to do the same for any file using settings.py
ACCELERATION = 3
ANIM_CLIMBING_SPEED = 5
ANIM_INTERACT_EXIT_SPEED = 3
ANIM_INTERACT_FEEDBACK_SPEED = 3
ANIM_INTERACT_HELP_SPEED = 3
ANIM_INTERACT_OPTIONS_SPEED = 3
ANIM_JUMPING_SPEED = 0
ANIM_FALLING_SPEED = 0
ANIM_IDLE_SPEED = 8
ANIM_RUNNING_SPEED = 2
ANIM_WALKING_SPEED = 3
CAP_VELOCITY_WALKING = 9
CAP_VELOCITY_RUNNING = 12
CAP_VELOCITY_CLIMB = CAP_VELOCITY_WALKING / 1.2
CHAR_NAME = 'Lasutriv'
CHAR_INVENTORY = ['Bowl_Half', 'Bowl_Full']
JUMP_STRENGTH = 15
# Cosmic forces
AIR_RESISTANCE = 1
GRAVITY = 1
FRICTION = 0.7
'''
Character traits: These are all defaults!
    1. Agility - A trait representing the character's ability to perform physical tasks.
        A. The Decrease Modifier represents how much to decrease endurance after every tick which is based on the endurance_decrease_time_modifier.
        B. The Decrease Time Modifier represents the tick rate, or code loops ran, before the decrease modifier is applied.
        C. The Increase Modifier represents how much to increase endurance after every tick which is based on the endurance_increase_time_modifier.
        D. The Increase Time Modifier represents the tick rate, or code loops ran, before the increase modifier is applied.
        E. Situations:
            a. Passive
            b. Non-Passive
    2. Endurance - A trait representing the character's ability to last longer while running, climbing, attacking, blocking, jumping, or more.
        A. " "...
    3. Influence - A trait representing the character's ability to sway other NPC's opinions in game.
        A. " "...
        B. Situations:
            a. Passive
                - Swaying citizen's opinions. A higher influence will allow the character to handle emigration easier.
                - 
            b. Non-Passive
                - Bartering with other nations, cities, towns, villages, or tribes.
                - Bartering with other NPCs.
                -
    4. Resolve - A trait representing the character's ability to push themselves beyond their limits in certain situations.
        A. " "...
        B. Situations:
            a. Combat
                - Character health is critical. Upon a death dealing hit, the character will get a percentage of health back. If the percentage
                  is not enough to deal with the remaining damage after calculations then the character will die.
            b. Non-Combat
                - Endurance running out while climbing/hanging. A higher resolve will let the character push onwards for a very brief period of time.
                - 
    5. Strength - A trait representing the character's measure of how strong a character is.
        A. " "...
        B. Situations:
            a. Combat
                - How hard melee attacks hit
                - How fast weapon switching handles
            b. Non-Combat
                - Maximum weight
                - Moving objects
'''
# Character traits
CHAR_ENDURANCE = 50
CHAR_ENDURANCE_MAX = 50
CHAR_INFLUENCE = 5
CHAR_INFLUENCE_MAX = 5
CHAR_RESOLVE = 5
CHAR_RESOLVE_MAX = 5
CHAR_STRENGTH = 5
CHAR_STRENGTH_MAX = 5

# Character trait modifiers
CHAR_ENDURANCE_DECREASE_MODIFIER = 1
CHAR_ENDURANCE_DECREASE_TIME_MODIFIER = 5
CHAR_ENDURANCE_INCREASE_MODIFIER = 1
CHAR_ENDURANCE_INCREASE_TIME_MODIFIER = 4
CHAR_INFLUENCE_DECREASE_MODIFIER = 1
CHAR_INFLUENCE_DECREASE_TIME_MODIFIER = 60
CHAR_INFLUENCE_INCREASE_MODIFIER = 1
CHAR_INFLUENCE_INCREASE_TIME_MODIFIER = 60
CHAR_RESOLVE_DECREASE_MODIFIER = 1
CHAR_RESOLVE_DECREASE_TIME_MODIFIER = 15
CHAR_RESOLVE_INCREASE_MODIFIER = 1
CHAR_RESOLVE_INCREASE_TIME_MODIFIER = 15
CHAR_STRENGTH_DECREASE_MODIFIER = 1
CHAR_STRENGTH_DECREASE_TIME_MODIFIER = 15
CHAR_STRENGTH_INCREASE_MODIFIER = 1
CHAR_STRENGTH_INCREASE_TIME_MODIFIER = 15

# Character specializations: Special skills that could possibly become unlocked after dedication and use of specific
#                            traits and in-game actions.
#   - BLINK is a type of transportation/time travel that allows the character to cover an amount of distance based on the
#           expertise of the specialization.
#   - WALL_RUN_JUMP is a type of speed jumping that allows the character to jump from a wall and have their jump count
#                   reset back to 0 allowing the character to continue their jumps until endurance is exhausted or the
#                   obstacle is accomplished.
BLINK = False
DOUBLE_JUMP = True
WALL_RUN_JUMP = True
TUMBLE = False
