import pygame
import button

from csv import reader, writer
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

show_statistics = False
background = True
show_main_menu = True

# main menu
screen_width = 1000
screen_height = 560
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_icon(pygame.image.load("assets/images/icons/icon_for_pygame_game.jpg"))

pygame.display.set_caption("Главное меню")
menu_bg = pygame.image.load("assets/images/background/menu_background.jpg").convert_alpha()
menu_font = pygame.font.Font("assets/fonts/Undertale-Battle-Font.ttf", 30)

# creating buttons
button_image = pygame.image.load("assets/images/background/button.png")

# in main menu
play_button = button.Button(380, 145, button_image, 1, 250, 60)
statistics_button = button.Button(380, 235, button_image, 1, 250, 60)
settings_button = button.Button(380, 325, button_image, 1, 250, 60)
exit_button = button.Button(380, 415, button_image, 1, 250, 60)

# in battle
pause_button_image = pygame.image.load("assets/images/icons/pause_button.png")
pause_button = button.Button(475, 10, pause_button_image, 1, 50, 50)

# end

# end of main menu
button_image = pygame.image.load("assets/images/background/button.png")

clock = pygame.time.Clock()
FPS = 60

# just colors
RED = (255, 0, 0)
GREEN = (173, 255, 47)
WHITE = (255, 255, 255)

intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# fighters
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]
# end

# sounds
warrior_sounds = [[pygame.mixer.Sound("assets/audio/warrior/sound_of_miss.mp3"),
                   pygame.mixer.Sound("assets/audio/warrior/sound_of_miss2.mp3"),
                   pygame.mixer.Sound("assets/audio/warrior/sound_of_miss3.mp3"),
                   pygame.mixer.Sound("assets/audio/warrior/sound_of_miss4.mp3"),
                   pygame.mixer.Sound("assets/audio/warrior/sound_of_miss5.mp3")],
                  [pygame.mixer.Sound("assets/audio/warrior/sound_of_hit.mp3")]]

magic_sounds = [[pygame.mixer.Sound("assets/audio/wizard/magic.wav"),
                 pygame.mixer.Sound("assets/audio/wizard/magic_attack2.mp3")]]
# end of sounds

# load images
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()
# end

WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# load fonts
count_font = pygame.font.Font("assets/fonts/Undertale-Battle-Font.ttf", 80)
score_font = pygame.font.Font("assets/fonts/Undertale-Battle-Font.ttf", 30)
# end

# fighters
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, warrior_sounds)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_sounds)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (screen_width, screen_height))
    screen.blit(scaled_bg, (0, 0))


def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))


def statistics_init():
    global bg_image
    global background

    if background:
        pygame.display.set_caption("Статистика персонажей")
        background = False


def main_menu_init():
    global background
    global show_main_menu
    global bg_image
    global show_statistics
    global run

    if background:
        pygame.mixer.music.load("assets/audio/background_music/music_in_main_menu.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
        pygame.display.set_caption("Главное меню")
        bg_image = pygame.image.load("assets/images/background/menu_background.jpg").convert_alpha()
        background = False

    draw_bg()

    if play_button.draw(screen):
        show_main_menu = False
        if not from_battle:
            pygame.mixer.music.load("assets/audio/background_music/Mortal Kombat.mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1, 0.0, 5000)

    elif statistics_button.draw(screen):
        show_statistics = True

    elif settings_button.draw(screen):
        pass

    elif exit_button.draw(screen):
        run = False

    if not from_battle:
        draw_text("Играть", menu_font, (255, 255, 255), 455, 155)

    else:
        draw_text("Продолжить", menu_font, (255, 255, 255), 420, 155)

    draw_text("Статистика", menu_font, (255, 255, 255), 425, 245)
    draw_text("Настройки", menu_font, (255, 255, 255), 430, 335)
    draw_text("Выход", menu_font, (255, 255, 255), 460, 425)


flag = True
run = True
move = True
from_battle = False

while run:
    clock.tick(FPS)

    if show_statistics:
        if flag:
            pygame.display.set_caption("Статистика")
            bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
            flag = False
            fighter_1.time_to_fight = False
            fighter_2.time_to_fight = False

        draw_bg()

        fighter_1.draw(screen)
        fighter_2.draw(screen)

        fighter_1.update()
        fighter_2.update()

    else:
        fighter_1.time_to_fight = True
        fighter_2.time_to_fight = True

        if show_main_menu:
            main_menu_init()

        elif not show_main_menu:
            if not background:
                bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
                background = True
                pygame.mixer.music.load("assets/audio/background_music/Mortal Kombat.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1, 0.0, 5000)

            draw_bg()

            draw_health_bar(fighter_1.health, 20, 20)
            draw_health_bar(fighter_2.health, 580, 20)
            draw_text(f"Игрок 1:    Счёт: {str(score[0])}", score_font, RED, 20, 60)
            draw_text(f"Игрок 2:    Счёт: {str(score[1])}", score_font, RED, 580, 60)

            if pause_button.draw(screen):
                from_battle = True
                show_main_menu = True

                main_menu_init()

            else:
                if move:
                    fighter_1.rect.x = 200
                    fighter_2.rect.x = 700
                    move = False

                if intro_count <= 0:
                    fighter_1.move(screen_width, screen_height, screen, fighter_2, round_over)
                    fighter_2.move(screen_width, screen_height, screen, fighter_1, round_over)

                else:
                    draw_text(str(intro_count), count_font, RED, screen_width / 2, screen_height / 3)

                    if (pygame.time.get_ticks() - last_count_update) >= 1000:
                        intro_count -= 1
                        last_count_update = pygame.time.get_ticks()

                fighter_1.update()
                fighter_2.update()

                fighter_1.draw(screen)
                fighter_2.draw(screen)

                if not round_over:
                    if not fighter_1.alive:
                        score[1] += 1
                        round_over = True
                        round_over_time = pygame.time.get_ticks()

                    elif not fighter_2.alive:
                        score[0] += 1
                        round_over = True
                        round_over_time = pygame.time.get_ticks()

                else:
                    screen.blit(victory_img, (360, 150))
                    if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                        round_over = False
                        intro_count = 3

                        print(fighter_1.jumps_count)
                        print(fighter_1.wins)
                        print(fighter_1.miss_counts)
                        print(fighter_1.hit_counts)

                        fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS,
                                            warrior_sounds)
                        fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS,
                                            magic_sounds)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not show_main_menu:
                show_main_menu = True
                from_battle = True
                main_menu_init()

    pygame.display.update()

pygame.quit()
