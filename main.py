import pygame, os
from sys import exit
from random import randint, choice

#Create player class
class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0 

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.05)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

#Create sprite class for sprites
class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = 210
		else:
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = 300

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

#Create Collision function
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True

#Set display score funciton
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

#Create obstacle movement function
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 8

            if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
            else: screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

#Collisions function
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True            

#Create player animation function
def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

#Initialize pygame
pygame.init()

#Set screen dimensions
screen = pygame.display.set_mode((800, 400))

#Set title
pygame.display.set_caption("Runner")

#Set clock object for frame rate
clock = pygame.time.Clock()

#Create font (type,size)
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

#Create activate game state
game_active = False

#Create score variable to store active score
score = 0

#Create start time for score
start_time = 0

#Create an instance of player class and add to group
player = pygame.sprite.GroupSingle()
player.add(Player())

#Create an instance of sprite class and add to group
obstacle_group = pygame.sprite.Group()

#Import background music
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops = -1)

#Create surface varaiable for background image
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# #Create text surface
# score_surf = test_font.render('My Game', False, (64,64,64) ).convert()
# score_rect = score_surf.get_rect(center = (400, 50))

#Create obstacles
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0 
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list=[]

#Create player surface and set rectangle around
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
#Set base gravity
player_gravity = 0

#Create player for load screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400,200))

#Create menu text
menu_title = test_font.render("Welcome to Snail Jumper", False, (111,196,169))
menu_title_rect = menu_title.get_rect(center = (400,50))
menu_cta = test_font.render("Press SPACE to Start", False, (111,196,169))
menu_cta_rect = menu_cta.get_rect(center = (400,350))

#Create timer for AI 
obstacle_timer = pygame.USEREVENT + 1 
pygame.time.set_timer(obstacle_timer, 900)

snail_animation_timer = pygame.USEREVENT +2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT +3
pygame.time.set_timer(fly_animation_timer,200)

#main game loop
while True:
    #Check for input close if quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        #Create surface for player

        if game_active:
            #Check for key input
            if player_rect.bottom >= 300:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player_rect.collidepoint(event.pos):
                        player_gravity = -20
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player_gravity = -20
        #Restart on space                
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    #snail_rect.left = 800
                    start_time = int(pygame.time.get_ticks() / 1000)
        #Obstacle loop
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
                # if randint(0,2):
                #     obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100), 300)))
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100), 210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]
    #Set active state                
    if game_active:
        #Call surface for background
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))

        # #Call surface for text
        #Create surface for player
        # pygame.draw.rect(screen, ('#c0e8ec'), score_rect)
        # pygame.draw.rect(screen, ('#c0e8ec'), score_rect, 15)
        # screen.blit(score_surf,score_rect)
        score = display_score()

        # #Create surface for snail reset if it goes off screen
        # snail_rect.x -= 5
        # if snail_rect.right <= 0: snail_rect.left = 800
        # screen.blit(snail_surface, snail_rect)

        # #Create surface for player
        # player_gravity += 1
        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300: player_rect.bottom = 300
        # player_animation()    
        # screen.blit(player_surf, player_rect)

        #Draw player class on the screen surface
        player.draw(screen)
        player.update()
        #Draw obstacle group
        obstacle_group.draw(screen)
        obstacle_group.update()
        #Check collision
        game_active = collision_sprite()

        # #obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #Collision to end game
        #if snail_rect.colliderect(player_rect):
         #   game_active = False
        # game_active = collisions(player_rect,obstacle_rect_list)

    else:
        #title screen after game over
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)

        #clear obstacles after game over
        obstacle_rect_list.clear()

        #Restart player at bottom of screen
        player_rect.midbottom = (80,300)
        player_gravity = 0 

        #Display score
        score_message  = test_font.render(f'Your Score: {score}', False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(menu_title,menu_title_rect)

        #Display score if score
        if score == 0:
            screen.blit(menu_cta,menu_cta_rect)
        else:
            screen.blit(score_message, score_message_rect)

    #Draw elements and update everything
    pygame.display.update()
    #Set frame rate ceiling
    clock.tick(60)
