import pygame
import sys
import math

from player import Player
from enemy import Enemy, separate_enemies, separate_enemy_from_player
from loot import create_loot, collect_loot
from ui import draw_ui, draw_upgrade_menu

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Granja en Peligro")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 26)

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

enemies = []
bullets = []
loot_items = []

last_spawn_time = 0
spawn_cooldown = 1500

game_state = "playing"

upgrade_options = [
    "Disparar más rápido",
    "Balas atraviesan enemigos"
]

for i in range(10):
    enemies.append(
        Enemy(SCREEN_WIDTH, SCREEN_HEIGHT)
    )

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if game_state == "upgrade":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    player.apply_upgrade(0)
                    game_state = "playing"

                if event.key == pygame.K_2:
                    player.apply_upgrade(1)
                    game_state = "playing"

                if event.key == pygame.K_RETURN:
                    player.apply_upgrade(0)
                    game_state = "playing"

    if game_state == "playing":

        player.update_movement()
        player.shoot(bullets)

        current_time = pygame.time.get_ticks()

        if current_time - last_spawn_time >= spawn_cooldown:
            last_spawn_time = current_time

            enemies.append(
                Enemy(SCREEN_WIDTH, SCREEN_HEIGHT)
            )

        for enemy in enemies:
            enemy.update(player)

        separate_enemies(enemies)

        for enemy in enemies:
            separate_enemy_from_player(enemy, player)

        for bullet in bullets:
            bullet.update()

        for bullet in bullets[:]:

            if bullet.is_outside_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                bullets.remove(bullet)

        for bullet in bullets[:]:

            for enemy in enemies[:]:

                dx = enemy.x - bullet.x
                dy = enemy.y - bullet.y

                distance = math.sqrt(dx ** 2 + dy ** 2)

                if distance < enemy.radius + bullet.radius:

                    create_loot(enemy.x, enemy.y, loot_items)

                    enemies.remove(enemy)

                    if bullet in bullets and bullet.piercing == False:
                        bullets.remove(bullet)

                    break

        if collect_loot(player, loot_items):
            game_state = "upgrade"

    screen.fill((70, 120, 70))

    for loot in loot_items:
        loot.draw(screen)

    player.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)

    draw_ui(screen, player, small_font, font)

    if game_state == "upgrade":
        draw_upgrade_menu(screen, font, small_font, upgrade_options)

    pygame.display.flip()

    if player.hp <= 0:
        print("GAME OVER")
        running = False

pygame.quit()
sys.exit()