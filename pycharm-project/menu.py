import pygame
import button

pygame.init()

screen_width = 1000
screen_height = 560
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Главное меню")
menu_bg = pygame.image.load("assets/images/background/menu_background.jpg").convert_alpha()
menu_font = pygame.font.Font("assets/fonts/Undertale-Battle-Font.ttf", 30)

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
button_image = pygame.image.load("assets/images/background/button.png")


def draw_bg():
    scaled_bg = pygame.transform.scale(menu_bg, (screen_width, screen_height))
    screen.blit(scaled_bg, (0, 0))


def draw_button(x, y, width, height, color):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


play_button = button.Button(380, 165, button_image, 1)
statistics_button = button.Button(380, 255, button_image, 1)
exit_button = button.Button(380, 345, button_image, 1)

running = True
while running:
    draw_bg()

    if play_button.draw(screen):
        print(1)

    elif statistics_button.draw(screen):
        print(2)

    elif exit_button.draw(screen):
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_text("Играть", menu_font, (255, 255, 255), 455, 175)
    draw_text("Статистика", menu_font, (255, 255, 255), 425, 265)
    draw_text("Выход", menu_font, (255, 255, 255), 460, 355)

    pygame.display.update()

pygame.quit()
