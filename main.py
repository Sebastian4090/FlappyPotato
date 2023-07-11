import pygame
from random import randint, choice
from sys import exit


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450))

def create_pipe():
    random_pipe_pos = choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (300, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (300, random_pipe_pos - 105))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if player_rect.colliderect(pipe):
            death_sound.play()
            return False

        if player_rect.top <= -100 or player_rect.bottom >= 450:
            return False

    return True

def rotate_player(player):
    new_player = pygame.transform.rotozoom(player, -player_movement * 5, 1)
    return new_player

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center=(144,50))
        screen.blit(score_surface, score_rect)

    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {(int(score))}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {(int(high_score))}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(144, 425))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency = 44100, size = 32, channels = 1, buffer = 256)
pygame.init()
screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.ttf",20)

Icon = pygame.image.load("icon.ico").convert_alpha()
pygame.display.set_caption("FlappyPotato")
pygame.display.set_icon(Icon)

# Game Variables
gravity = 0.25
player_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load("sprites/background-day.png").convert()
floor_surface = pygame.image.load("sprites/base.png").convert()
player = pygame.image.load("sprites/potato.png").convert_alpha()
player_rect = player.get_rect(center = (100,256))
floor_x_pos = 0

pipe_surface = pygame.image.load("sprites/pipe-green.png").convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,randint(1000,2000))
pipe_height = [200, 300, 400]

game_over_surface = pygame.image.load("sprites/message.png").convert()
game_over_rect = game_over_surface.get_rect(center = (144, 256))

flap_sound = pygame.mixer.Sound("audio/wing.wav")
death_sound = pygame.mixer.Sound("audio/hit.wav")
score_sound = pygame.mixer.Sound("audio/point.wav")
score_sound_countdown = 100

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                player_movement = 0
                player_movement -= 6
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                player_rect.center = (100, 256)
                player_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())


    # Background
    screen.blit(bg_surface, (0,0))
    floor_x_pos -= 1
    if game_active:
        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Player
        rotated_player = rotate_player(player)
        screen.blit(rotated_player, player_rect)
        player_movement += gravity
        player_rect.centery += player_movement
        game_active = check_collision(pipe_list)

        score += 0.01
        score_display("main_game")
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")

    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0





    pygame.display.update()
    clock.tick(60)