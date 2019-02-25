import pygame

def text_to_screen(screen, text, x, y, size = 25, color = (255, 255, 255), font_type = 'ARCADE.ttf'):
    try:
        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))
    except ValueError:
        print ("Font Error, saw it coming")
