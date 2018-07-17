import animations
import settings

import pygame


class Character(pygame.sprite.Sprite):

    def __init__(self, name: str, file_save_name: str, engine_game: object, x: int, y: int):
        """
        A class to handle events, actions, and information regarding the character and their impacts on the game.

        @param name: the name of the character that the user specified
        @type name: str
        @param file_save_name: the file name to load the settings from
        @type file_save_name: str
        @param engine_game: the engine which controls the network of the game when it starts after the menu
        @type engine_game: object
        @param x: the x location that the character is to be initially at
        @type x: int
        @param y: the y location that the character is to be initially at
        @type y: int
        """
        self.engine_game = engine_game
        self.groups = engine_game.sprites_all
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.name = name
        self.file_save_name = file_save_name
        # Variables
        self.direction = 'Right'
        self.health = 100
        self.state = 'None'
        self.state_changed = False
        self.jump_count = 0
        self.jump_strength = settings.JUMP_STRENGTH
        self.x_velocity = 0
        self.y_velocity = 0
        # Character Actions
        self.blink = False
        self.climbing = False
        self.falling = True
        self.jumping = False
        self.running = False
        self.try_climb = False
        self.vortex = False
        self.walking = False
        # Character traits, these traits are only for new games and not loaded from files
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
        self.images.append(pygame.image.load(settings.DIR_SPRITES_CHAR_BASE + '/Idle/Sprite_Char_Base_96_Trimmed_Idle.png').convert_alpha())
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
        whether that entails keys for moving/interacting with the character and in-game features.

        @return: none
        @rtype: none
        """
        keys_pressed = pygame.key.get_pressed()

        # TODO: Create the handling of key bindings set by the user in 'bindings.py'
        # Handling keys for jumping
        if keys_pressed[pygame.K_SPACE] and self.trait_endurance > settings.REQ_JUMP_ENDURANCE:
            if settings.DOUBLE_JUMP is False and not self.jumping and not self.falling:
                if self.jumping is False:
                    self.trait_endurance -= self.jump_strength
                self.jumping = True
                self.y_velocity = self.jump_strength
            elif settings.DOUBLE_JUMP is True and self.jump_count <= 2:
                if self.jumping is False:
                    self.trait_endurance -= self.jump_strength
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
                    self.x_velocity = -self.jump_strength / 3
                    self.y_velocity = self.jump_strength / 1.2
                elif self.direction == 'Left' and self.x_velocity <= settings.CAP_VELOCITY_WALKING - settings.ACCELERATION:
                    self.climbing = False
                    self.jumping = True
                    # TODO: Change state to jumping whenever the jumping animation is created
                    self.state = 'Running'
                    self.state_changed = True
                    self.direction = 'Right'
                    self.x_velocity = self.jump_strength / 3
                    self.y_velocity = self.jump_strength / 1.2
            # As the character continues to climb, their endurance depletes based off of two modifiers that the user might be able to change later.
            # One is for how much to decrease endurance and how often that should happen.
            self.timer_climbing += 1
            if self.timer_climbing == self.trait_endurance_decrease_time_modifier:
                self.trait_endurance -= self.trait_endurance_decrease_modifier
                self.timer_climbing = 0

        # Handling keys for movement on ground or in air
        if (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]) and self.climbing is False and self.jumping is False:
            self.direction = 'Right'
            # TODO: Make the running and walking fully incorporated.
            if keys_pressed[pygame.K_LSHIFT]:
                if self.x_velocity <= settings.CAP_VELOCITY_RUNNING - settings.ACCELERATION:
                    self.x_velocity += settings.ACCELERATION
            else:
                if self.x_velocity <= settings.CAP_VELOCITY_WALKING - settings.ACCELERATION:
                    self.x_velocity += settings.ACCELERATION
        if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]) and self.climbing is False and self.jumping is False:
            self.direction = 'Left'
            if keys_pressed[pygame.K_LSHIFT]:
                if self.x_velocity >= -settings.CAP_VELOCITY_RUNNING + settings.ACCELERATION:
                    self.x_velocity -= settings.ACCELERATION
            else:
                if self.x_velocity >= -settings.CAP_VELOCITY_WALKING + settings.ACCELERATION:
                    self.x_velocity -= settings.ACCELERATION

    def check_character(self):
        """
        Check and update character variables based on their state, traits, and velocity.

        @return: none
        @rtype: none
        """
        # Check states
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

        # Check character states and change traits accordingly
        # Endurance
        if self.trait_endurance != self.trait_endurance_max:
            # Check to make sure the character isn't doing an activity
            if self.climbing is False and self.falling is False and self.jumping is False:
                self.timer_trait_endurance += 1
                # Increase endurance due to resting or not performing extraneous activities
                if self.timer_trait_endurance == self.trait_endurance_increase_time_modifier:
                    self.trait_endurance += self.trait_endurance_increase_modifier
                    self.timer_trait_endurance = 0
        # NOTE: Trait location check
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
        A function to check the character against in game objects for collisions as well as updating other character variables.

        @return: none
        @rtype: none
        """
        wall_hit_list = pygame.sprite.spritecollide(self, self.engine_game.sprites_walls, False)

        if len(wall_hit_list) > 0:
            for wall in wall_hit_list:
                # Check falling/walking into a wall from above
                if self.rect.collidepoint(wall.rect.midtop):
                    self.rect.bottom = wall.rect.top + 1  # 1 works perfectly
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

    def check_state(self):
        """
        A function to change the state based off of the character's specific attributes affected by actions, traits, and velocity.

        @return: none
        @rtype: none
        """
        # Check actions and change state
        if self.x_velocity == 0 and self.y_velocity == 0 and self.state != 'Idle':
            self.state_changed = True
            self.state = 'Idle'
        # TODO: Fix the code below because as of right now anytime the user ins't 'running' and they move, their state changes to
        # CONT: running. Also the self.falling is used but the state is never changed to falling and we also need to take into
        # CONT: account jumping and then falling...
        elif (self.x_velocity > 0 or self.x_velocity < 0) and self.y_velocity == 0 and self.state != 'Running':
            self.state_changed = True
            self.state = 'Running'
        # TODO: Uncomment when there are falling animations
        if self.climbing and self.state != 'Climbing':
            self.state_changed = True
            self.state = 'Climbing'
        # elif self.y_velocity > 0:
        #     self.state_changed = True
        #     self.state = 'Falling'

        # Change animation via state
        if self.state_changed:
            self.images.clear()
            # Reset values since we are changing animations
            self.image_index = 0
            self.timer_images = 0
            if self.state == 'Idle':
                # No need for images facing left. We can just transform.flip the character
                animations.add_idle_right_images(self.images)
            elif self.state == 'Running':
                # No need for images facing left. We can just transform.flip the character
                animations.add_run_right_images(self.images)
            elif self.state == 'Climbing':
                animations.add_climbing_right_images(self.images)
            self.state_changed = False

    def check_animation(self):
        """
        A function to change the animation and animation trigger for the looping of animations. This function bases the animation on a state rather than
        specific values from actions because those values need to be turned into one state after all scenarios are calculated.

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
        elif self.state == 'Idle':
            # TODO: Make the idle animation slower if the endurance is closer to its maximum
            if self.trait_endurance < self.trait_endurance_max / 2:
                # Slow down the speed by half of the current speed. We subtract to the timer because it'll take a shorter
                # amount of time to loop enough to get to the next frame and vice versa for the speed at max endurance
                self.timer_images_trigger = settings.ANIM_IDLE_SPEED - (settings.ANIM_IDLE_SPEED / 2)
            elif self.trait_endurance == self.trait_endurance_max:
                self.timer_images_trigger = settings.ANIM_IDLE_SPEED + (settings.ANIM_IDLE_SPEED / 2)
            else:
                self.timer_images_trigger = settings.ANIM_IDLE_SPEED
        elif self.state == 'Running':
            self.timer_images_trigger = settings.ANIM_RUNNING_SPEED
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

    # TODO: Create a setup for creating a character when 'New Game' is selected
    def setup_traits(self, new_character=True):
        """
        A function to figure out specific modifiers based on a loaded file, or a new character, and the statistics/traits
        of the character.

        @param new_character: determines whether to load defaults or not
        @type new_character: bool
        @return: none
        @rtype: none
        """
        if new_character is True:
            pass
            # TODO: Start a character setup that then saves and loads the new character created.
        else:
            pass
            # TODO: Create a file to store a character's complete game state.

    def update(self):
        """
        A function to finally update the character after performing most in-game tasks.

        @return: none
        @rtype: none
        """
        # Check which animation to use
        self.check_state()

        # Check and update character variables
        self.check_character()

        # Check collisions with new updates
        self.check_collision()

        # Recheck and run animation
        self.check_animation()
