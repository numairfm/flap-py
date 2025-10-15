import pygame
import random

pygame.init()
screen_x = 500
screen_y = 800
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
running = True
start_game = False
delta = 0
JUMP_POWER = -12 
GRAVITY = 0.56
TERMINAL_VELOCITY = 20

plr_position = pygame.Vector2((screen.get_width() / 2) - 150, screen.get_height() / 2)
start_plr_position = pygame.Vector2((screen.get_width() / 2) - 150, screen.get_height() / 2)
plr_y_vel = 0


on_ground = False
jump = True

box_size = (40, 40)
box = pygame.Rect(0, 0, *box_size)

rnd_num = random.random() * 100
pillar_size = (100, 600)
top_pillar = pygame.Rect(0, 0, *pillar_size)
bottom_pillar = pygame.Rect(0, 0, *pillar_size)
spawn_offset = 0
PIL_SPEED = -4

score = 0

top_pillar.center = pygame.Vector2((screen.get_width() / 2) + 300, ((screen.get_height() / 2) - 425) + rnd_num + spawn_offset)
bottom_pillar.center = pygame.Vector2((screen.get_width() / 2) + 300, ((screen.get_height() / 2) + 425) + rnd_num + spawn_offset)
start_top_pillar = pygame.Vector2((screen.get_width() / 2) + 300, ((screen.get_height() / 2) - 425) + rnd_num + spawn_offset)
start_bottom_pillar = pygame.Vector2((screen.get_width() / 2) + 300, ((screen.get_height() / 2) + 425) + rnd_num + spawn_offset)

font = pygame.font.SysFont("Arial", 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("white")
    pygame.draw.rect(screen, "red", box)
    
    pygame.draw.rect(screen, "green", top_pillar)
    pygame.draw.rect(screen, "blue", bottom_pillar)
    
    if not start_game:
        rnd_num = random.random() * 100
        plr_position = start_plr_position.copy()
        top_pillar.center = start_top_pillar.copy()
        bottom_pillar.center = start_bottom_pillar.copy()
        plr_y_vel = 0
        score = 0
        
        text_surface = font.render(f"Press the UP arrow to start!", True, (0,0,0))
        screen.blit(text_surface, (35, 50))
    else:
        text_surface = font.render(f"Score: {score}", True, (0,0,0))
        screen.blit(text_surface, (50, 50))
        
    # Input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and jump == True:
        plr_y_vel = JUMP_POWER
        jump = False
        on_ground = False
        # GAME BASICALLY STARTS HERE
        start_game = True
    if not keys[pygame.K_UP]:
        jump = True
        
    # Gravity
    if not on_ground and start_game == True:
        plr_y_vel += GRAVITY
        if plr_y_vel > TERMINAL_VELOCITY:
            plr_y_vel = TERMINAL_VELOCITY
        
    plr_position.y += plr_y_vel
    box.center = plr_position
    
    # Ground Collision
    if box.bottom >= screen.get_height():
        box.bottom = screen.get_height()
        plr_position.y = box.centery
        plr_y_vel = 0
        on_ground = True
        start_game = False
    else:
        on_ground = False
    
    # Pillar collision
    if box.colliderect(top_pillar) or box.colliderect(bottom_pillar):
        start_game = False
    
    if start_game:
        top_pillar.x += PIL_SPEED
        bottom_pillar.x += PIL_SPEED
        
        if top_pillar.right < 0:
            rnd_num = random.random() * 100
            spawn_offset = 100 if rnd_num > 50 else -100
            top_pillar.x = screen.get_width() + 100
            bottom_pillar.x = screen.get_width() + 100  
            top_pillar.centery = ((screen.get_height() / 2) - 425) + rnd_num + spawn_offset
            bottom_pillar.centery = ((screen.get_height() / 2) + 425) + rnd_num + spawn_offset
            score += 1
    
    pygame.display.flip()
        
    delta = clock.tick(60) / 1000

pygame.quit()
