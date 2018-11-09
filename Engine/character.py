# The character module that handles all interactions between the game, the engine itself and the character.
# Tanner Fry
# tefnq2@mst.edu
import settings

import pygame


class Character(pygame.sprite.Sprite):
    """Class. To handle events, actions, and information regarding the character and their impacts on the game."""
    def __init__(self, name: str, file_save_name: str, engine_game: object, x: int, y: int):
        """
        Setting up the character for movement, animations, displaying, and more.

        @param name: the name of the character that the user specified
        @type name: str
        @param file_save_name: the file name to load the settings from
        @type file_save_name: str
        @param engine_game: the engine which controls the network of the game when it starts after the menu
        @type engine_game: object
        @param x: the x location that the character is to be initialized at
        @type x: int
        @param y: the y location that the character is to be initialized at
        @type y: int
        """
        self.engine_game = engine_game
        self.engine_menu = object  # Used only for the sample character to access the menu object
        self.groups = engine_game.sprites_important
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.name = name
        self.file_save_name = file_save_name
        # Variables
        self.active_buffs = []  # The buffs that will be applied to the character, str
        self.collision_sets = 'None'  # Helps handle special collision sets based on the value
        self.direction = 'Right'  # Current direction the character is facing
        self.health = 100
        self.state = 'None'  # The state, or action, they are in: idle, running, jumping, climbing, etc
        self.state_changed = False
        self.jump_count = 0
        self.jump_strength = settings.JUMP_STRENGTH
        self.wall_jump_ratio_x = 2.5
        self.wall_jump_ratio_y = 0.8
        self.x_velocity = 0
        self.y_velocity = 0
        # Character Action Triggers
        self.blink = False  # NOTE: Note created yet
        self.climbing = False
        self.falling = True
        self.jumping = False
        self.running = False
        self.try_climb = False
        self.vortex = False  # NOTE: Note created yet
        self.walking = False
        # Character traits, these traits are only for new games and not loaded from files
        # NOTE: Sigmoid function example for scaling combat and other objects in relation to one another
        # NOTE: RawOdds = (1 + Skill) / ((1 + Skill) + (1 + Difficulty))
        # NOTE: AdjustedOdds = 1 / (1 + (e ^ ((RawOdds * Steepness) + Offset))) <-- Steepness = -10, Offset = 5
        self.trait_endurance = settings.CHAR_ENDURANCE
        self.trait_endurance_max = settings.CHAR_ENDURANCE_MAX
        self.trait_endurance_decrease_modifier = settings.CHAR_ENDURANCE_DECREASE_MODIFIER
        self.trait_endurance_increase_modifier = settings.CHAR_ENDURANCE_INCREASE_MODIFIER
        self.trait_endurance_decrease_time_modifier = settings.CHAR_ENDURANCE_DECREASE_TIME_MODIFIER
        self.trait_endurance_increase_time_modifier = settings.CHAR_ENDURANCE_INCREASE_TIME_MODIFIER
        self.trait_influence = settings.CHAR_INFLUENCE
        self.trait_influence_max = settings.CHAR_INFLUENCE_MAX
        self.trait_influence_decrease_modifier = settings.CHAR_INFLUENCE_DECREASE_MODIFIER
        self.trait_influence_increase_modifier = settings.CHAR_INFLUENCE_INCREASE_MODIFIER
        self.trait_influence_decrease_time_modifier = settings.CHAR_INFLUENCE_DECREASE_TIME_MODIFIER
        self.trait_influence_increase_time_modifier = settings.CHAR_INFLUENCE_INCREASE_TIME_MODIFIER
        self.trait_resolve = settings.CHAR_RESOLVE
        self.trait_resolve_max = settings.CHAR_RESOLVE_MAX
        self.trait_resolve_decrease_modifier = settings.CHAR_RESOLVE_DECREASE_MODIFIER
        self.trait_resolve_increase_modifier = settings.CHAR_RESOLVE_INCREASE_MODIFIER
        self.trait_resolve_decrease_time_modifier = settings.CHAR_RESOLVE_DECREASE_TIME_MODIFIER
        self.trait_resolve_increase_time_modifier = settings.CHAR_RESOLVE_INCREASE_TIME_MODIFIER
        self.trait_strength = settings.CHAR_STRENGTH
        self.trait_strength_max = settings.CHAR_STRENGTH_MAX
        self.trait_strength_decrease_modifier = settings.CHAR_STRENGTH_DECREASE_MODIFIER
        self.trait_strength_increase_modifier = settings.CHAR_STRENGTH_INCREASE_MODIFIER
        self.trait_strength_decrease_time_modifier = settings.CHAR_STRENGTH_DECREASE_TIME_MODIFIER
        self.trait_strength_increase_time_modifier = settings.CHAR_STRENGTH_INCREASE_TIME_MODIFIER
        # Images
        self.images = []
        self.images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE
                                             + '/Idle/Sprite_Char_Base_96_Trimmed_Idle.png').convert_alpha())
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = 64  # 66 is the base but we must keep it under 64 so the character can fit in small spaces
        self.rect.height = 90
        self.timer_climbing = 0
        self.timer_images = 0
        self.timer_images_trigger = 0
        self.timer_trait_endurance = 0

    def handle_keys(self):
        """
        A function to handle all of the keys for moving and interacting with the main network of the engine,
        whether that entails keys for moving/interacting with the character or with in-game features.

        @return: none
        @rtype: none
        """
        keys_pressed = pygame.key.get_pressed()

        # TODO: Create the handling of key bindings set by the user in 'bindings.py'
        # Handling keys for jumping
        if keys_pressed[pygame.K_SPACE] and self.trait_endurance > settings.REQ_JUMP_ENDURANCE and self.engine_game.engine_handler.state != 'Game_Inventory':
            if settings.DOUBLE_JUMP is False and not self.jumping and not self.falling:
                if self.jumping is False:
                    self.trait_endurance -= settings.REQ_JUMP_ENDURANCE
                self.jumping = True
                self.y_velocity = self.jump_strength
            elif settings.DOUBLE_JUMP is True and self.jump_count <= 2:
                if self.jumping is False:
                    self.trait_endurance -= settings.REQ_JUMP_ENDURANCE
                if self.jump_count is 0:
                    self.jump_count += 1
                    self.jumping = True
                    self.y_velocity = self.jump_strength
                elif self.jump_count is 1 and (self.y_velocity < 2 or self.falling is True):
                    self.jump_count += 1
                    self.jumping = True
                    self.y_velocity = self.jump_strength

        # Handling keys for setting up climbing
        if keys_pressed[pygame.K_LCTRL]:
            self.try_climb = True
        else:
            self.try_climb = False
            self.climbing = False

        # Handling keys while climbing
        if self.climbing is True and self.trait_endurance > settings.REQ_CLIMBING_ENDURANCE:
            if keys_pressed[pygame.K_w]:
                if self.y_velocity >= -settings.CAP_VELOCITY_CLIMB + settings.ACCELERATION:
                    self.y_velocity -= settings.ACCELERATION
            elif keys_pressed[pygame.K_s]:
                if self.y_velocity <= settings.CAP_VELOCITY_CLIMB - settings.ACCELERATION:
                    self.y_velocity += settings.ACCELERATION
            else:
                self.y_velocity = 0
            if keys_pressed[pygame.K_SPACE] and settings.WALL_RUN_JUMP is True:
                if self.direction == 'Right' and self.x_velocity >= -settings.CAP_VELOCITY_WALKING + settings.ACCELERATION:
                    self.climbing = False
                    self.jumping = True
                    # TODO: Change state to jumping whenever the jumping animation is created
                    self.state = 'Running'
                    self.state_changed = True
                    self.direction = 'Left'
                    self.x_velocity = -self.jump_strength / self.wall_jump_ratio_x
                    self.y_velocity = self.jump_strength / self.wall_jump_ratio_y
                elif self.direction == 'Left' and self.x_velocity <= settings.CAP_VELOCITY_WALKING - settings.ACCELERATION:
                    self.climbing = False
                    self.jumping = True
                    # TODO: Change state to jumping whenever the jumping animation is created
                    self.state = 'Running'
                    self.state_changed = True
                    self.direction = 'Right'
                    self.x_velocity = self.jump_strength / self.wall_jump_ratio_x
                    self.y_velocity = self.jump_strength / self.wall_jump_ratio_y
            # As the character continues to climb, their endurance depletes based off of two modifiers that the user
            # might be able to change later. One is for how much to decrease endurance and how often that should happen.
            self.timer_climbing += 1
            if self.timer_climbing == self.trait_endurance_decrease_time_modifier:
                self.trait_endurance -= self.trait_endurance_decrease_modifier
                self.timer_climbing = 0

        # Handling keys for movement on ground or in air
        if (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]) and self.climbing is False \
                and self.engine_game.engine_handler.state != 'Game_Inventory':
            self.direction = 'Right'

            # TODO: Make the running and walking fully incorporated with the hands gradually moving past the side.
            if keys_pressed[pygame.K_LSHIFT]:
                if self.x_velocity <= settings.CAP_VELOCITY_RUNNING - settings.ACCELERATION:
                    self.x_velocity += settings.ACCELERATION
            else:
                if self.x_velocity <= settings.CAP_VELOCITY_WALKING - settings.ACCELERATION:
                    self.x_velocity += settings.ACCELERATION
        if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]) and self.climbing is False \
                and self.engine_game.engine_handler.state != 'Game_Inventory':
            self.direction = 'Left'

            if keys_pressed[pygame.K_LSHIFT]:
                if self.x_velocity >= -settings.CAP_VELOCITY_RUNNING + settings.ACCELERATION:
                    self.x_velocity -= settings.ACCELERATION
            else:
                if self.x_velocity >= -settings.CAP_VELOCITY_WALKING + settings.ACCELERATION:
                    self.x_velocity -= settings.ACCELERATION

        # Handle keys for idle
        if self.state == 'Idle' and keys_pressed[pygame.K_g]:
            self.engine_game.engine_handler.state = 'Game_Government_Management'

    def check_var_change_state(self):
        """
        A function to change the state based off of the character's specific attributes affected by actions, traits,
        velocity, and set the images based on the state.

        @return: none
        @rtype: none
        """
        if 'Interacting' not in self.state:
            # Check actions and change state
            if self.x_velocity == 0 and self.y_velocity == 0 and self.state != 'Idle' and self.state != 'Crying':
                self.state = 'Idle'
                self.state_changed = True
            elif self.y_velocity > 0 and self.state != 'Climbing' and self.state != 'Falling':

                self.state = 'Falling'
                self.state_changed = True
            # TODO: Fix the code below because as of right now anytime the user ins't 'running' and they move, their state
            # CONT: changes to running. Also the self.falling is used but the state is never changed to falling and we also
            # CONT: need to take into account jumping and then falling...
            elif (self.x_velocity > 0 or self.x_velocity < 0) and self.y_velocity == 0:
                # Check velocity speed to determine state since user key input increases the character's velocity
                # NOTE: Above 9 units/sec has gained enough speed to increase the animation speed by changing states
                if (self.x_velocity > settings.CAP_VELOCITY_WALKING or self.x_velocity < -settings.CAP_VELOCITY_WALKING) \
                        and self.state != 'Running':
                    self.state = 'Running'
                    self.state_changed = True
                # TODO: Fix below code. State doesn't change back to walking after running and I tried to use the opposite
                # CONT: of the above for the 'Running' state
                if self.state != 'Walking' and self.state != 'Running':
                    self.state = 'Walking'
                    self.state_changed = True
            # TODO: Uncomment when there are falling animations
            if self.climbing and self.state != 'Climbing':
                self.state = 'Climbing'
                self.state_changed = True
            # elif self.y_velocity > 0:
            #     self.state_changed = True
            #     self.state = 'Falling'

        # Change animation via state
        if self.state_changed:
            self.images.clear()
            # Reset values since we are changing animations
            self.image_index = 0
            self.state_changed = False
            self.timer_images = 0
            if self.state == 'Idle':
                # No need for images facing left. We can just transform.flip the character
                for i in range(1, 5):
                    self.images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE
                                                         + '/Breathing/Sprite_Char_Base_96_Trimmed_Breathing' + str(i)
                                                         + '.png').convert_alpha())
            elif self.state == 'Climbing':
                for i in range(1, 4):
                    self.images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE
                                                         + '/Climbing/Sprite_Char_Base_96_Trimmed_Climbing' + str(i)
                                                         + '.png').convert_alpha())
            elif self.state == 'Crying':
                for i in range(1, 15):
                    self.images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE
                                                         + '/Crying/Sprite_Char_Base_96_Trimmed_Crying' + str(i)
                                                         + '.png').convert_alpha())
            elif self.state == 'Falling':
                for i in range(1, 3):
                    self.images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE
                                                         + '/Falling/Sprite_Char_Base_96_Trimmed_Falling' + str(i)
                                                         + '.png').convert_alpha())
            # TODO: Finish this for special menu interactions
            elif self.state == 'Interacting_With_Exit':
                for i in range(1, 9):
                    self.images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE
                                                         + '/Interacting/Feedback/Sprite_Char_Base_96_Trimmed'
                                                         + '_Interacting_Feedback' + str(i) + '.png').convert_alpha())
            elif self.state == 'Interacting_With_Feedback':
                for i in range(1, 9):
                    self.images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE
                                                         + '/Interacting/Feedback/Sprite_Char_Base_96_Trimmed'
                                                         + '_Interacting_Feedback' + str(i) + '.png').convert_alpha())
            elif self.state == 'Interacting_With_Help':
                for i in range(1, 9):
                    self.images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE
                                                         + '/Interacting/Feedback/Sprite_Char_Base_96_Trimmed'
                                                         + '_Interacting_Feedback' + str(i) + '.png').convert_alpha())
            elif self.state == 'Interacting_With_Load':
                for i in range(1, 9):
                    self.images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE
                                                         + '/Interacting/Feedback/Sprite_Char_Base_96_Trimmed'
                                                         + '_Interacting_Feedback' + str(i) + '.png').convert_alpha())
            elif self.state == 'Interacting_With_Options':
                for i in range(1, 9):
                    self.images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE
                                                         + '/Interacting/Feedback/Sprite_Char_Base_96_Trimmed'
                                                         + '_Interacting_Feedback' + str(i) + '.png').convert_alpha())
            elif self.state == 'Running' or self.state == 'Walking':
                # No need for images facing left. We can just transform.flip the character
                for i in range(1, 8):
                    self.images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE
                                                         + '/Running/Sprite_Char_Base_96_Trimmed_Running' + str(i)
                                                         + '.png').convert_alpha())
            print('State changed to ' + self.state)

    def check_character_apply_physics(self):
        """
        Apply physics to the character's velocity

        @return: none
        @rtype: none
        """
        # Gravity
        if self.jumping:
            self.falling = False
            self.rect.y -= self.y_velocity
            self.y_velocity = self.y_velocity - settings.GRAVITY
            if self.y_velocity < 0:
                self.falling = True
                self.jumping = False
                self.y_velocity = 0
            # Apply air resistance
            # if self.x_velocity > 0:
            #     self.x_velocity -= settings.AIR_RESISTANCE
            # elif self.x_velocity < 0:
            #     self.x_velocity += settings.AIR_RESISTANCE
        elif self.falling is True and self.climbing is False:
            self.jumping = False
            self.rect.y += self.y_velocity
            self.y_velocity = self.y_velocity + settings.GRAVITY
            # Apply air resistance
            # if self.x_velocity > 0:
            #     self.x_velocity -= settings.AIR_RESISTANCE
            # elif self.x_velocity < 0:
            #     self.x_velocity += settings.AIR_RESISTANCE

        if self.climbing:
            self.rect.y += self.y_velocity
            if settings.DOUBLE_JUMP is True:
                self.jump_count = 0
        elif self.jumping is False and self.falling is False:
            self.jump_count = 0
            self.y_velocity = 0

        # Update traits based on character interactions
        # Endurance
        if self.trait_endurance != self.trait_endurance_max:
            # Check to make sure the character isn't doing an activity
            if self.climbing is False and self.jumping is False:
                self.timer_trait_endurance += 1
                # Increase endurance due to resting or not performing extraneous activities
                if self.timer_trait_endurance == self.trait_endurance_increase_time_modifier:
                    self.trait_endurance += self.trait_endurance_increase_modifier
                    self.timer_trait_endurance = 0
        # NOTE: Trait checking
        # Influence
        # Resolve
        # Strength

        # Apply friction and air resistance
        if self.x_velocity > 0:
            # Apply friction
            if self.falling is False and self.jumping is False:
                self.x_velocity -= settings.FRICTION
            # Apply air resistance
            elif self.falling is True:
                self.x_velocity -= settings.AIR_RESISTANCE
            if self.x_velocity <= 0.4:
                self.x_velocity = 0
        elif self.x_velocity < 0:
            # Apply friction
            if self.falling is False and self.jumping is False:
                self.x_velocity += settings.FRICTION
            # Apply air resistance
            elif self.falling is True:
                self.x_velocity += settings.AIR_RESISTANCE
            if self.x_velocity >= -0.4:
                self.x_velocity = 0
        # Update character
        self.rect.x += self.x_velocity

    def check_collision(self):
        """
        A function to check the character against in game objects for collisions as well as updating other character
        variables.

        @return: none
        @rtype: none
        """
        wall_hit_list = pygame.sprite.spritecollide(self, self.engine_game.sprites_active_walls, False)

        # Check special collision sets
        if self.collision_sets != 'None':
            # Work with the sample character specifically for the interactive menu
            if self.collision_sets == 'Menu':
                if self.rect.y >= 735:
                    self.rect.y = 735
                    self.y_velocity = 0  # So the engine will register not falling
                    self.falling = False
                    self.jumping = False  # Used to update jump count
                    self.jump_count = 0

        # Check tile collision sets
        if len(wall_hit_list) > 0:
            for wall in wall_hit_list:
                # Check falling/walking into a wall from above
                if self.rect.collidepoint(wall.rect.midtop):
                    # Could fix, not important atm
                    self.rect.bottom = wall.rect.top + 1  # 1 works perfectly... don't ask cause idk
                    self.falling = False
                # Check falling into corner, lets clip through it
                if self.rect.collidepoint(wall.rect.topleft) and not self.rect.collidepoint(wall.rect.midleft) and self.falling is True:
                    pass
                # Check falling into corner, lets clip through it
                if self.rect.collidepoint(wall.rect.topright) and not self.rect.collidepoint(wall.rect.midright) and self.falling is True:
                    pass
                # Check hitting into a wall from above-left
                if self.rect.collidepoint(wall.rect.topleft) and not self.rect.collidepoint(wall.rect.midleft) \
                        and self.falling is False and self.climbing is False:
                    # Check if character is close to the corner of above-left and not trying to hang/climb down
                    # TODO: Create the ability for the character to hang on the tile if they are at an edge to hang on whether left or right
                    # TODO: NOTE - This could get intensive as it requires a function to determine if the character is at an edge.
                    self.rect.bottom = wall.rect.top + 1  # 1 works perfectly
                    self.falling = False
                # Check hitting into a wall from above-right
                if self.rect.collidepoint(wall.rect.topright) and not self.rect.collidepoint(wall.rect.midright) \
                        and self.falling is False and self.climbing is False:
                    # Check if character is close to the corner of above-right and not trying to hang/climb down
                    # TODO: Create the ability for the character to hang on the tile if they are at an edge to hang on
                    self.rect.bottom = wall.rect.top + 1  # 1 works perfectly
                    self.falling = False
                # Check hitting into a wall from the left
                if self.rect.collidepoint(wall.rect.midleft):
                    # Check climbing ability
                    if self.try_climb and self.trait_endurance > settings.REQ_CLIMBING_ENDURANCE:
                        self.climbing = True
                        # Make sure new y velocity won't collide when going up
                        if self.rect.collidepoint(wall.rect.bottomright) or self.rect.collidepoint(wall.rect.midbottom):
                            self.rect.top = wall.rect.bottom + 1
                        elif self.rect.collidepoint(wall.rect.topright) or self.rect.collidepoint(wall.rect.midtop):
                            self.rect.bottom = wall.rect.top - 1
                    else:
                        # Fall if climbing button is not pressed while against wall
                        self.climbing = False
                        if not self.rect.collidepoint(wall.rect.midtop):
                            self.falling = True
                    # Check if movement would have went through wall
                    if self.rect.x + self.rect.width >= wall.rect.x:
                        self.rect.right = wall.rect.left + 1
                # Check hitting into a wall from the right
                elif self.rect.collidepoint(wall.rect.midright):
                    # Check climbing ability
                    if self.try_climb and self.trait_endurance > settings.REQ_CLIMBING_ENDURANCE:
                        self.climbing = True
                        # Make sure new y velocity won't collide when going up
                        if self.rect.collidepoint(wall.rect.bottomleft) or self.rect.collidepoint(wall.rect.midbottom):
                            self.rect.top = wall.rect.bottom + 1
                        elif self.rect.collidepoint(wall.rect.topleft) or self.rect.collidepoint(wall.rect.midtop):
                            self.rect.bottom = wall.rect.top - 1
                    else:
                        # Fall if climbing button is not pressed while against wall
                        self.climbing = False
                        if not self.rect.collidepoint(wall.rect.midtop):
                            self.falling = True
                    # Check if movement would have went through wall
                    if self.rect.x <= wall.rect.x + wall.rect.width:
                        self.rect.left = wall.rect.right - 1
                # Check hitting into a wall from below
                if self.rect.collidepoint(wall.rect.midbottom):
                    self.y_velocity = 0
                    self.rect.top = wall.rect.bottom + 1
                    if not self.rect.collidepoint(wall.rect.midtop) and self.climbing is False and self.falling is False:
                        self.falling = True
        # Check if not touching anything
        else:
            # Climbing
            if self.climbing is True:
                self.climbing = False
            # Not doing anything
            if self.jumping is False and self.climbing is False and self.falling is False:
                self.falling = True

        # Check character's traits for specific tasks
        # Climbing
        if not self.trait_endurance > settings.REQ_CLIMBING_ENDURANCE:
            self.climbing = False

    def check_state_apply_animation(self):
        """
        A function to change the animation and animation trigger for the looping of animations. This function bases the
        animation on a state rather than specific values from actions because those values need to be turned into one
        state after all scenarios are calculated.

        @return: none
        @rtype: none
        """
        # TODO: Change what value is set to self.timer_images_trigger after all skills are implemented since the animation speed will
        # CONT: depend on how fast the character is going, which is based on their traits
        if self.state == 'Climbing':
            self.timer_images_trigger = settings.ANIM_CLIMBING_SPEED
        elif self.state == 'Jumping':
            self.timer_images_trigger = settings.ANIM_JUMPING_SPEED
        elif self.state == 'Falling':
            self.timer_images_trigger = settings.ANIM_FALLING_SPEED
        elif self.state == 'Interacting_With_Exit':
            self.timer_images_trigger = settings.ANIM_INTERACT_EXIT_SPEED
        elif self.state == 'Interacting_With_Feedback':
            self.timer_images_trigger = settings.ANIM_INTERACT_FEEDBACK_SPEED
        elif self.state == 'Interacting_With_Help':
            self.timer_images_trigger = settings.ANIM_INTERACT_HELP_SPEED
        elif self.state == 'Interacting_With_Options':
            self.timer_images_trigger = settings.ANIM_INTERACT_OPTIONS_SPEED
        # TODO: Create/fix this
        elif self.state == 'Inventory':
            pass
        elif self.state == 'Idle':
            # TODO: Make the idle animation slower if the endurance is closer to its maximum
            if self.trait_endurance < self.trait_endurance_max / 2:
                # Slow down the speed by half of the current speed. We subtract to the timer because it'll take a
                # shorter amount of time to loop enough to get to the next frame and vice versa for the speed at max
                # endurance
                self.timer_images_trigger = settings.ANIM_IDLE_SPEED - (settings.ANIM_IDLE_SPEED / 2)
            elif self.trait_endurance == self.trait_endurance_max:
                self.timer_images_trigger = settings.ANIM_IDLE_SPEED + (settings.ANIM_IDLE_SPEED / 2)
            else:
                self.timer_images_trigger = settings.ANIM_IDLE_SPEED
        elif self.state == 'Running':
            self.timer_images_trigger = settings.ANIM_RUNNING_SPEED
        elif self.state == 'Walking':
            self.timer_images_trigger = settings.ANIM_WALKING_SPEED
        self.timer_images += 1
        # Change animation image
        if self.timer_images >= self.timer_images_trigger:
            # Make sure index isn't out of range
            if self.image_index == len(self.images) - 1:
                self.image_index = 0
            else:
                self.image_index += 1
            self.timer_images = 0
        # Check direction and flip image if need be
        self.image = self.images[self.image_index]
        if self.direction == 'Left':
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        """
        A function to finally update the character after performing most in-game tasks.

        @return: none
        @rtype: none
        """
        # After events have been handled:
        self.check_var_change_state()

        self.check_character_apply_physics()

        # Check collisions with new updates
        self.check_collision()

        self.check_state_apply_animation()


class Buff(object):
    """Class."""
    def __init__(self, buff_name: str):
        """
        Constructor.

        @param buff_name: the name of the buff being created
        @type buff_name: str
        """
        # TODO: Should there be sound incorporated into the buff? Probably
        self.active = True
        self.buff_time_length = 0
        self.debuff_time_length = 0
        self.image = pygame.image.load('Bin/Sprites/Char_Base/Buff/Chamomile_Tea_96_Buff1.png').convert_alpha()
        self.image_rect = self.image.get_rect()
        self.image_timer = 0
        self.images_buff = []
        self.images_debuff = []
        self.index = 0
        self.name = buff_name
        self.timer_trigger = 0
        # The dictionary below is used due to performance issues with python. Everything must be as fast as possible
        # and hardcoded variables to change is better than reading files with statistics. Not sure about importing
        # though.
        # NOTE: Buff length 100 = 1 second
        self.dict_buffs = {
            'Chamomile Tea': {
                'Buff': {
                    'Influence': 2
                },
                'Debuff': {
                    'Resolve': -2
                },
                'Buff Time Length': 900,
                'DeBuff Time Length': 300,
                'Image Count': 15,
                'Image Buff Location': 'Bin/Sprites/Char_Base/Buff/Chamomile_Tea_96_Buff',
                'Image DeBuff Location': 'Bin/Sprites/Char_Base/Buff/Chamomile_Tea_96_DeBuff',
                'Image Timer Trigger': 7,
                'Type': 'Herbal'
            },
            'Dried Chamomile Leaves': {
                'Buff': {
                    'None': 0
                },
                'Debuff': {
                    'Endurance': -2,
                    'Influence': -2,
                    'Strength': -2
                },
                'Buff Time Length': 900,
                'DeBuff Time Length': 300,
                'Image Count': 10,
                'Image Buff Location': 'Bin/Sprites/Char_Base/Buff/Dried_Chamomile_Leaves_96_Buff',
                'Image DeBuff Location': 'Bin/Sprites/Char_Base/Buff/Dried_Chamomile_Leaves_96_DeBuff',
                'Image Timer Trigger': 7,
                'Type': 'Herbal'
            },
            'Helping Hand': {
                'Buff': {
                    'Endurance': 5,
                    'Influence': 5,
                    'Resolve': 5
                },
                'Debuff': {
                    'None': 0
                },
                'Buff Time Length': 900,
                'DeBuff Time Length': 300,
                'Image Count': 0,
                'Image Buff Location': '',
                'Image DeBuff Location': '',
                'Image Timer Trigger': 5,
                'Type': 'Spiritual'
            },
            'Odycopin': {
                'Buff': {
                    'Endurance': 5,
                    'Influence': 2,
                    'Resolve': 5
                },
                'Debuff': {
                    'Endurance': -10,
                    'Influence': -8,
                    'Resolve': -10
                },
                'Buff Time Length': 900,
                'DeBuff Time Length': 300,
                'Image Count': 0,
                'Image Buff Location': '',
                'Image DeBuff Location': '',
                'Image Timer Trigger': 5,
                'Type': 'Tech'
            }
        }
        # Finish setting up variables for the buff based on the dict above
        self.init_rest_of_buff()

    def init_rest_of_buff(self):
        """
        A function to use the dictionary of buffs to add in the appropriate images and other influence values.

        @return: none
        @rtype: none
        """
        for buff in self.dict_buffs:
            if self.name == buff:
                print('[Debug - Info]: Initializing', self.name, 'images.')
                buff = self.dict_buffs[buff]
                # Set the appropriate images
                for i in range(1, buff['Image Count']):
                    self.images_buff.append(pygame.image.load(buff['Image Buff Location'] + str(i) + '.png').convert_alpha())
                    self.images_debuff.append(pygame.image.load(buff['Image DeBuff Location'] + str(i) + '.png').convert_alpha())
                self.image = self.images_buff[self.index]
                self.buff_time_length = buff['Buff Time Length']
                self.debuff_time_length = buff['DeBuff Time Length']
                self.timer_trigger = buff['Image Timer Trigger']

    def reset_buff(self):
        """
        A function to reset the buff.

        @return: none
        """
        for buff in self.dict_buffs:
            if self.name == buff:
                print('[Debug - Info]: Resetting', self.name, '.')
                buff = self.dict_buffs[buff]
                # Reset only the values that change
                self.active = True
                self.buff_time_length = buff['Buff Time Length']
                self.debuff_time_length = buff['DeBuff Time Length']
                self.image = self.images_buff[0]
                self.image_timer = 0
                self.index = 0


class BuffHandler(object):
    """Class. To handle specific buffs and how they apply to the character based of the buff."""
    def __init__(self, character: object, screen: object):
        """
        Constructor.

        @param character: a reference to the object that the user is currently playing as
        @type character: object
        """
        self.active_buffs = []
        self.character = character
        self.image_timer = 0
        self.screen = screen
        # Check if there are any buffs to add right away
        self.update_buffs()
        # TODO: Create situational buffs such as a holy blessing for shielding oneself from fire for X amount of seconds
        # CONT: This 'holy blessing' can open a lot of possibilities such as getting to new areas unreachable before or
        # CONT: needing to get into a boss fight. The situational buffs should be somewhat easy to get because there
        # CONT: should be many different types of bosses that these buffs can be used for.
        """
        BUFF OUTLINE
            Herbal buffs: 
                Chamomile Tea - The herbal infusion of dried chamomile flowers. Two teaspoons of dried flower per cup 
                                of tea and then steeped for 5 - 10 minutes. "They say this is just as good as that Jane
                                I used to have for my anxiety." - Found in a medicine book in the game

            Spiritual buffs:
                Helping Hand - A low level buff cast by a priest and/or monk.

            Tech buffs [Cyber Era]:
                Odycopin - A highly advanced, and addictive, medicine to give character boosts
        """

    def handle_events(self):
        """
        A function to look at all active buffs and go through the appropriate steps for the buff handler.

        @return: none
        @rtype: none
        """
        # Apply buff effect to character, display them, and check for new ones
        self.apply_buff_effect()
        self.draw_buff_images()
        self.update_buffs()

    def apply_buff_effect(self):
        """
        A function that applies certain effects on the character's traits based on the buff name passed.

        @return: none
        @rtype: none
        """
        for buff in self.active_buffs:
            # Apply buff
            if buff.active is True and buff.buff_time_length != 0:
                # TODO: Add effect from buff to character
                pass
            # Apply debuff
            elif buff.active is False and buff.debuff_time_length != 0:
                # TODO: Add effect from debuff to character
                pass
            else:
                # Buff has finished it's effects on the character and is now going into passive mode
                pass

    def update_buffs(self):
        """
        A function to set new active buffs from the character's buff list.

        @return: none
        @rtype: none
        """
        # Find if there are any new buffs to add NOTE: Danger this could be resource intensive
        for buff_name in self.character.active_buffs:
            if len(self.active_buffs) == 0:
                # Creates a new buff and sets them to active
                print('[Debug - Info]:', buff_name, 'added.')
                self.active_buffs.append(Buff(buff_name))
            else:
                trigger = False  # If true then a match of a buff between two lists was accomplished
                for buff_object in self.active_buffs:
                    if buff_object.name == buff_name:
                        trigger = True
                # Create the new buff if there isn't a match
                if trigger is False:
                    print('[Debug - Info]:', buff_name, 'added.')
                    self.active_buffs.append(Buff(buff_name))

    def draw_buff_images(self):
        """
        A function to rotate through the image list and display the buff animations to the screen.

        @return: none
        @rtype: none
        """
        # Increment timer until it hits trigger for the specific buff object in the self.active_buffs list
        for buff in self.active_buffs:
            buff.image_timer += 1
            # Display buff images
            if buff.active is True and buff.buff_time_length != 0:
                if buff.image_timer >= buff.timer_trigger:
                    # Restart if at end of index after increment
                    if buff.index == len(buff.images_buff) - 1:
                        buff.index = 0
                    else:
                        buff.index += 1
                    buff.image_timer = 0
                    # Push appropriate image after cleansing
                    buff.image = buff.images_buff[buff.index]
                    if self.character.direction == 'Left':
                        buff.image = pygame.transform.flip(buff.image, True, False)

                # Update image location and display
                buff.image_rect = buff.image.get_rect()
                buff.image_rect.x = self.character.rect.x - 15
                buff.image_rect.y = self.character.rect.y - 15
                self.screen.blit(buff.image, buff.image_rect)

                # Since it was displayed, decrement the buff length
                buff.buff_time_length -= 1
            # Change to debuff if need be
            elif buff.active is True and buff.buff_time_length == 0:
                buff.active = False
            # Display debuff images
            elif buff.active is False and buff.debuff_time_length != 0:
                if buff.image_timer >= buff.timer_trigger:
                    # Restart if at end of index after increment
                    if buff.index == len(buff.images_debuff) - 1:
                        buff.index = 0
                    else:
                        buff.index += 1
                        buff.image_timer = 0
                    # Push appropriate image after cleansing
                    buff.image = buff.images_debuff[buff.index]
                    if self.character.direction == 'Left':
                        buff.image = pygame.transform.flip(buff.image, True, False)

                # Update image location and display
                buff.image_rect = buff.image.get_rect()
                buff.image_rect.x = self.character.rect.x - 15
                buff.image_rect.y = self.character.rect.y - 15
                self.screen.blit(buff.image, buff.image_rect)

                # Since it was displayed, decrement the debuff length
                buff.debuff_time_length -= 1
            else:
                # Buff has finished it's effects on the character and is now going into passive mode
                pass
