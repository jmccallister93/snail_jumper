import pygame, os
from sys import exit

#Set display score funciton
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

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

#Create surface varaiable for background image
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# #Create text surface
# score_surf = test_font.render('My Game', False, (64,64,64) ).convert()
# score_rect = score_surf.get_rect(center = (400, 50))

#Create snail surface and set rectangle
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(bottomright = (600, 300))


#Create player surface and set rectangle around
player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))

#Create player for load screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400,200))

#Create menu text
menu_title = test_font.render("Welcome to Snail Jumper", False, (111,196,169))
menu_title_rect = menu_title.get_rect(center = (400,50))
menu_cta = test_font.render("Press SPACE to Start", False, (111,196,169))
menu_cta_rect = menu_cta.get_rect(center = (400,350))


#Create gravity for jump
player_gravity = 0

#main game loop
while True:
    #Check for input close if quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

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
                    snail_rect.left = 800
                    start_time = int(pygame.time.get_ticks() / 1000)

    #Set active state                
    if game_active:
        #Call surface for background
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))

        # #Call surface for text
        # pygame.draw.rect(screen, ('#c0e8ec'), score_rect)
        # pygame.draw.rect(screen, ('#c0e8ec'), score_rect, 15)
        # screen.blit(score_surf,score_rect)
        score = display_score()

        #Create surface for snail reset if it goes off screen
        snail_rect.x -= 5
        if snail_rect.right <= 0: snail_rect.left = 800
        screen.blit(snail_surface, snail_rect)

        #Create surface for player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300    
        screen.blit(player_surf, player_rect)

        #Collision to end game
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
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
