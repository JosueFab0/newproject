import pygame


def draw_ui(screen, player, small_font, font):
    pygame.draw.rect(
        screen,
        (80, 80, 80),
        (20, 20, 400, 25)
    )

    pygame.draw.rect(
        screen,
        (60, 120, 255),
        (20, 20, int((player.xp / player.xp_needed) * 400), 25)
    )

    xp_text = small_font.render(
        "Nivel " + str(player.level) + "  XP: " + str(player.xp) + "/" + str(player.xp_needed),
        True,
        (255, 255, 255)
    )

    screen.blit(xp_text, (25, 22))

    coin_text = font.render(
        "Oro: " + str(player.gold),
        True,
        (255, 255, 255)
    )

    screen.blit(coin_text, (20, 60))


def draw_upgrade_menu(screen, font, small_font, upgrade_options):
    pygame.draw.rect(
        screen,
        (20, 20, 20),
        (340, 220, 600, 250)
    )

    title_text = font.render(
        "SUBISTE DE NIVEL",
        True,
        (255, 255, 255)
    )

    option_1_text = small_font.render(
        "1 / ENTER - " + upgrade_options[0],
        True,
        (255, 255, 255)
    )

    option_2_text = small_font.render(
        "2 - " + upgrade_options[1],
        True,
        (255, 255, 255)
    )

    screen.blit(title_text, (515, 260))
    screen.blit(option_1_text, (430, 330))
    screen.blit(option_2_text, (430, 380))