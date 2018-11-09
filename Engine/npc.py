# The npc module that handles specific events, actions, and information from the game in relation to npcs.
# Tanner Fry
# tefnq2@mst.edu
import settings

import pygame


class NPCHandler(object):
    """Class. To handle events, actions, and information regarding the overview of all npcs in the game."""
    def __init__(self, engine_game: object):
        """
        Setting up the npc handler to keep npc load to a usable level.

        @param engine_game: the engine which controls the network of the game when it starts after the menu
        @type engine_game: object
        """
        self.active_npcs = []
        self.engine_game = engine_game
        self.max_npcs = 25

    def handler_cycle(self):
        """
        A function that performs the necessary cycle that the handler goes through to perform its checks and
        information gathering on the active and possible inactive npcs.

        @return: none
        @rtype: none
        """
        # Test any other npc extremities
        self.test_reached_npc_capacity()

    def test_reached_npc_capacity(self):
        """
        A function that calculates whether or not the current list of active npcs is above or below the desired
        threshhold.

        @return: none
        @rtype: none
        """
        if len(self.active_npcs) > self.max_npcs:
            print('[Debug - Error]: There are over 25 active NPCS. '
                  'There shouldn\'t be that many yet. '
                  'Check NPCHandler() class in npc.py.')
            # TODO: Determine a way to reduce the npc count based on priority


class NPCSquishy(pygame.sprite.Sprite):
    """
    Class. Creates an overall object to handle all interactions for a given npc.

    NOTE: Can we make this bare bones enough to use across all npcs and then each npc has a
    NOTE: personality tied to them? This is just concept at the moment
    """
    def __init__(self, name: str, engine_game: object, x: int, y: int):
        """
        Constructor.

        @param name: the name of the npc that the developer specified
        @type name: str
        @param engine_game: the engine which controls the network of the game when it starts after the menu
        @type engine_game: object
        @param x: the x location that the npc is to be initialized at
        @type x: int
        @param y: the y location that the character is to be initialized at
        @type y: int
        """
        self.engine_game = engine_game
        self.groups = engine_game.sprites_important
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.name = name
        self.health = 20
        self.state = 'None'
        self.state_changed = False  # Used to clear images list and change animation. Code clarity
        self.direction = ''
        self.falling = True  # NPC can take damage as well
        self.jumping = False  # Npc can try and get to higher places to reach character
        self.x_velocity = 0
        self.y_velocity = 0

        # Animation inits
        self.flipped_visually = False
        self.images = []
        self.images.append(pygame.image.load(settings.DIR_SPRITES_NPC
                                             + '/Squishy/Idle/Sprite_NPC_Base_96_Trimmed_Idle.png').convert_alpha())
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # NOTE: Might have to modify the width and height for proper collision testing later

        # Timers
        self.timer_images = 0
        self.timer_images_trigger = 0

    def handle_events(self):
        """
        A function to handle all of the keys for moving and interacting with the main network of the engine,
        whether that entails keys for moving/interacting with the npc or with in-game features.

        @return: none
        @rtype: none
        """
        # keys_pressed = pygame.key.get_pressed()
        # Handle interactions by possibly having a "view" distance and then aggro'ing after found

    def check_state(self):
        """
        A function to change the state based off of the npc's specific attributes affected by actions, traits,
        velocity, and set the images based on the state.

        @return: none
        @rtype: none
        """
        # Check actions and change state
        if self.x_velocity == 0 and self.y_velocity == 0 and self.state != 'Idle':
            self.state_changed = True
            self.state = 'Idle'
        # TODO: Fix the code below because as of right now anytime the user ins't 'running' and they move, their state
        # CONT: changes to running. Also the self.falling is used but the state is never changed to falling and we also
        # CONT: need to take into account jumping and then falling...
        elif (self.x_velocity > 0 or self.x_velocity < 0) and self.y_velocity == 0 and self.state != 'Running':
            self.state_changed = True
            self.state = 'Running'

        state_old = self.state
        # Change animation via state
        if self.state_changed:
            print('State changed from:', state_old, 'to', self.state)
            # Reset values since we are changing animations
            self.images.clear()
            self.image_index = 0
            self.state_changed = False
            self.timer_images = 0
            # TODO: A work around at the moment below
            if self.state == 'Idle':
                for i in range(1, 3):
                    self.images.append(pygame.image.load(settings.DIR_SPRITES_NPC
                                                         + '/Squishy/Breathing/Sprite_NPC_Base_96_Trimmed_Breathing' + str(i)
                                                         + '.png').convert_alpha())
            elif self.state == 'Running':
                for i in range(1, 7):
                    self.images.append(pygame.image.load(settings.DIR_SPRITES_NPC
                                                         + '/Squishy/Running/Sprite_NPC_Base_96_Trimmed_Running' + str(i)
                                                         + '.png').convert_alpha())

    def check_npc(self):
        """
        Check and update npc variables based on their state, traits, and velocity based on engine physics.

        @return: none
        @rtype: none
        """
        # TODO: Below
        # Check if an enemy is near, if so lets focus otherwise random movement

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
        elif self.falling is True:
            self.jumping = False
            self.rect.y += self.y_velocity
            self.y_velocity = self.y_velocity + settings.GRAVITY
            # Apply air resistance
            # if self.x_velocity > 0:
            #     self.x_velocity -= settings.AIR_RESISTANCE
            # elif self.x_velocity < 0:
            #     self.x_velocity += settings.AIR_RESISTANCE

        if self.jumping is False and self.falling is False:
            self.y_velocity = 0

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

        if len(wall_hit_list) > 0:
            for wall in wall_hit_list:
                # Check falling/walking into a wall from above
                if self.rect.collidepoint(wall.rect.midtop):
                    self.rect.bottom = wall.rect.top + 1  # 1 works perfectly
                    self.falling = False
                # Check falling into corner, lets clip through it
                if self.rect.collidepoint(wall.rect.topleft) and not self.rect.collidepoint(
                        wall.rect.midleft) and self.falling is True:
                    pass
                # Check falling into corner, lets clip through it
                if self.rect.collidepoint(wall.rect.topright) and not self.rect.collidepoint(
                        wall.rect.midright) and self.falling is True:
                    pass
                # Check hitting into a wall from above-left
                if self.rect.collidepoint(wall.rect.topleft) and not self.rect.collidepoint(wall.rect.midleft) \
                        and self.falling is False:
                    # Check if character is close to the corner of above-left and not trying to hang/climb down
                    # TODO: Create the ability for the character to hang on the tile if they are at an edge to hang on whether left or right
                    # TODO: NOTE - This could get intensive as it requires a function to determine if the character is at an edge.
                    self.rect.bottom = wall.rect.top + 1  # 1 works perfectly
                    self.falling = False
                # Check hitting into a wall from above-right
                if self.rect.collidepoint(wall.rect.topright) and not self.rect.collidepoint(wall.rect.midright) \
                        and self.falling is False:
                    # Check if character is close to the corner of above-right and not trying to hang/climb down
                    # TODO: Create the ability for the character to hang on the tile if they are at an edge to hang on
                    self.rect.bottom = wall.rect.top + 1  # 1 works perfectly
                    self.falling = False
                # Check hitting into a wall from the left
                if self.rect.collidepoint(wall.rect.midleft):
                    # Make sure new y velocity won't collide when going up
                    if self.rect.collidepoint(wall.rect.bottomright) or self.rect.collidepoint(wall.rect.midbottom):
                        self.rect.top = wall.rect.bottom + 1
                    elif self.rect.collidepoint(wall.rect.topright) or self.rect.collidepoint(wall.rect.midtop):
                        self.rect.bottom = wall.rect.top - 1
                    if not self.rect.collidepoint(wall.rect.midtop):
                        self.falling = True
                    # Check if movement would have went through wall
                    if self.rect.x + self.rect.width >= wall.rect.x:
                        self.rect.right = wall.rect.left + 1
                # Check hitting into a wall from the right
                elif self.rect.collidepoint(wall.rect.midright):
                    # Make sure new y velocity won't collide when going up
                    if self.rect.collidepoint(wall.rect.bottomleft) or self.rect.collidepoint(wall.rect.midbottom):
                        self.rect.top = wall.rect.bottom + 1
                    elif self.rect.collidepoint(wall.rect.topleft) or self.rect.collidepoint(wall.rect.midtop):
                        self.rect.bottom = wall.rect.top - 1
                    if not self.rect.collidepoint(wall.rect.midtop):
                        self.falling = True
                    # Check if movement would have went through wall
                    if self.rect.x <= wall.rect.x + wall.rect.width:
                        self.rect.left = wall.rect.right - 1
                # Check hitting into a wall from below
                if self.rect.collidepoint(wall.rect.midbottom):
                    self.y_velocity = 0
                    self.rect.top = wall.rect.bottom + 1
                    if not self.rect.collidepoint(
                            wall.rect.midtop) and self.falling is False:
                        self.falling = True
        # Check if not touching anything
        else:
            # Not doing anything
            if self.jumping is False and self.falling is False:
                self.falling = True

    def check_animation(self):
        """
        A function to change the animation and animation trigger for the looping of animations. This function bases the
        animation on a state rather than specific values from actions because those values need to be turned into one
        state after all scenarios are calculated.

        @return: none
        @rtype: none
        """
        self.timer_images += 1
        if self.state == 'Idle':
            self.timer_images_trigger = 6
        elif self.state == 'Running':
            self.timer_images_trigger = 10
        # Change animation image
        if self.timer_images >= self.timer_images_trigger:
            self.timer_images = 0
            # Make sure index isn't out of range
            if self.image_index == len(self.images) - 1:
                self.image_index = 0
            else:
                self.image_index += 1
            # Set image and check direction, flip accordingly
            self.image = self.images[self.image_index]
            if self.direction == 'Left':
                self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        """
        A function to finally update the character after performing most in-game tasks.

        @return: none
        @rtype: none
        """
        # Check which animation to use
        self.check_state()

        # Check and update npc variables
        self.check_npc()

        # Check collisions with new updates
        self.check_collision()

        # Recheck and run animation
        self.check_animation()
