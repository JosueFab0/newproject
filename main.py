import pygame
import sys
import math
import random

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Granja en Peligro")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 26)

player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2
player_radius = 20
player_speed = 3
player_hp = 50
player_max_hp = 50

player_level = 1
player_xp = 0
xp_needed = 100

coins_collected = 0

last_direction_x = 1
last_direction_y = 0

enemies = []
bullets = []
loot_items = []

last_shot_time = 0
shoot_cooldown = 1000

last_spawn_time = 0
spawn_cooldown = 1500

game_state = "playing"
upgrade_options = []

bullet_piercing = False


def create_enemy():
    side = random.randint(1, 4)

    if side == 1:
        x = random.randint(0, SCREEN_WIDTH)
        y = -30
    elif side == 2:
        x = random.randint(0, SCREEN_WIDTH)
        y = SCREEN_HEIGHT + 30
    elif side == 3:
        x = -30
        y = random.randint(0, SCREEN_HEIGHT)
    else:
        x = SCREEN_WIDTH + 30
        y = random.randint(0, SCREEN_HEIGHT)

    enemy = {
        "x": x,
        "y": y,
        "radius": 15,
        "speed": 1.2
    }

    enemies.append(enemy)


def create_loot(x, y):
    loot_chance = random.randint(1, 100)

    if loot_chance <= 45:
        loot = {
            "x": x,
            "y": y,
            "radius": 8,
            "type": "xp",
            "value": 25
        }

        loot_items.append(loot)

    elif loot_chance <= 70:
        loot = {
            "x": x,
            "y": y,
            "radius": 8,
            "type": "gold",
            "value": 1
        }

        loot_items.append(loot)


def level_up():
    global game_state
    global upgrade_options

    upgrade_options = [
        "Disparar más rápido",
        "Balas atraviesan enemigos"
    ]

    game_state = "upgrade"


def apply_upgrade(option):
    global shoot_cooldown
    global bullet_piercing
    global game_state

    if option == 0:
        shoot_cooldown -= 150

        if shoot_cooldown < 250:
            shoot_cooldown = 250

    elif option == 1:
        bullet_piercing = True

    game_state = "playing"


def increase_xp(amount):
    global player_xp
    global player_level
    global xp_needed

    player_xp += amount

    if player_xp >= xp_needed:
        player_xp -= xp_needed
        player_level += 1

        if player_level < 10:
            xp_needed += 100
        else:
            xp_needed += 200

        level_up()


for i in range(10):
    create_enemy()


running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if game_state == "upgrade":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    apply_upgrade(0)

                if event.key == pygame.K_2:
                    apply_upgrade(1)

                if event.key == pygame.K_RETURN:
                    apply_upgrade(0)

    if game_state == "playing":

        keys = pygame.key.get_pressed()

        move_x = 0
        move_y = 0

        if keys[pygame.K_w]:
            move_y -= 1
        if keys[pygame.K_s]:
            move_y += 1
        if keys[pygame.K_a]:
            move_x -= 1
        if keys[pygame.K_d]:
            move_x += 1

        if move_x != 0 or move_y != 0:
            distance = math.sqrt(move_x ** 2 + move_y ** 2)

            move_x /= distance
            move_y /= distance

            last_direction_x = move_x
            last_direction_y = move_y

            player_x += move_x * player_speed
            player_y += move_y * player_speed

        current_time = pygame.time.get_ticks()

        if current_time - last_spawn_time >= spawn_cooldown:
            last_spawn_time = current_time
            create_enemy()

        if current_time - last_shot_time >= shoot_cooldown:
            last_shot_time = current_time

            base_angle = math.atan2(last_direction_y, last_direction_x)

            angles = [
                base_angle - 0.25,
                base_angle,
                base_angle + 0.25
            ]

            for angle in angles:
                bullet = {
                    "x": player_x,
                    "y": player_y,
                    "dx": math.cos(angle),
                    "dy": math.sin(angle),
                    "radius": 6,
                    "speed": 8,
                    "piercing": bullet_piercing
                }

                bullets.append(bullet)

        enemy_speed_bonus = pygame.time.get_ticks() / 1000 * 0.02

        for enemy in enemies:
            dx = player_x - enemy["x"]
            dy = player_y - enemy["y"]

            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance != 0:
                dx /= distance
                dy /= distance

                current_enemy_speed = enemy["speed"] + enemy_speed_bonus

                enemy["x"] += dx * current_enemy_speed
                enemy["y"] += dy * current_enemy_speed

        for i in range(len(enemies)):
            enemy_a = enemies[i]

            for j in range(i + 1, len(enemies)):
                enemy_b = enemies[j]

                dx = enemy_b["x"] - enemy_a["x"]
                dy = enemy_b["y"] - enemy_a["y"]

                distance = math.sqrt(dx ** 2 + dy ** 2)
                min_distance = enemy_a["radius"] + enemy_b["radius"]

                if distance < min_distance and distance != 0:
                    overlap = min_distance - distance

                    dx /= distance
                    dy /= distance

                    enemy_a["x"] -= dx * overlap / 2
                    enemy_a["y"] -= dy * overlap / 2

                    enemy_b["x"] += dx * overlap / 2
                    enemy_b["y"] += dy * overlap / 2

        for enemy in enemies:
            dx = enemy["x"] - player_x
            dy = enemy["y"] - player_y

            distance = math.sqrt(dx ** 2 + dy ** 2)
            min_distance = player_radius + enemy["radius"]

            if distance < min_distance and distance != 0:
                overlap = min_distance - distance

                dx /= distance
                dy /= distance

                enemy["x"] += dx * overlap
                enemy["y"] += dy * overlap

                player_hp -= 1

        for bullet in bullets:
            bullet["x"] += bullet["dx"] * bullet["speed"]
            bullet["y"] += bullet["dy"] * bullet["speed"]

        for bullet in bullets[:]:
            if (
                bullet["x"] < -50 or
                bullet["x"] > SCREEN_WIDTH + 50 or
                bullet["y"] < -50 or
                bullet["y"] > SCREEN_HEIGHT + 50
            ):
                bullets.remove(bullet)

        for bullet in bullets[:]:
            for enemy in enemies[:]:

                dx = enemy["x"] - bullet["x"]
                dy = enemy["y"] - bullet["y"]

                distance = math.sqrt(dx ** 2 + dy ** 2)

                if distance < enemy["radius"] + bullet["radius"]:
                    create_loot(enemy["x"], enemy["y"])
                    enemies.remove(enemy)

                    if bullet in bullets and bullet["piercing"] == False:
                        bullets.remove(bullet)

                    break

        for loot in loot_items[:]:
            dx = loot["x"] - player_x
            dy = loot["y"] - player_y

            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance < player_radius + loot["radius"]:

                if loot["type"] == "xp":
                    increase_xp(loot["value"])

                elif loot["type"] == "gold":
                    coins_collected += loot["value"]

                loot_items.remove(loot)

    screen.fill((70, 120, 70))

    for loot in loot_items:

        if loot["type"] == "xp":
            color = (60, 120, 255)
        else:
            color = (230, 190, 40)

        pygame.draw.circle(
            screen,
            color,
            (int(loot["x"]), int(loot["y"])),
            loot["radius"]
        )

    pygame.draw.circle(
        screen,
        (240, 220, 170),
        (int(player_x), int(player_y)),
        player_radius
    )

    pygame.draw.rect(
        screen,
        (80, 80, 80),
        (int(player_x - 25), int(player_y + 30), 50, 8)
    )

    pygame.draw.rect(
        screen,
        (200, 50, 50),
        (int(player_x - 25), int(player_y + 30), int((player_hp / player_max_hp) * 50), 8)
    )

    for enemy in enemies:
        pygame.draw.circle(
            screen,
            (180, 80, 80),
            (int(enemy["x"]), int(enemy["y"])),
            enemy["radius"]
        )

    for bullet in bullets:
        pygame.draw.circle(
            screen,
            (250, 230, 80),
            (int(bullet["x"]), int(bullet["y"])),
            bullet["radius"]
        )

    pygame.draw.rect(screen, (80, 80, 80), (20, 20, 400, 25))
    pygame.draw.rect(screen, (60, 120, 255), (20, 20, int((player_xp / xp_needed) * 400), 25))

    xp_text = small_font.render("Nivel " + str(player_level) + "  XP: " + str(player_xp) + "/" + str(xp_needed), True, (255, 255, 255))
    screen.blit(xp_text, (25, 22))

    coin_text = font.render("Oro: " + str(coins_collected), True, (255, 255, 255))
    screen.blit(coin_text, (20, 60))

    if game_state == "upgrade":

        pygame.draw.rect(screen, (20, 20, 20), (340, 220, 600, 250))

        title_text = font.render("SUBISTE DE NIVEL", True, (255, 255, 255))
        option_1_text = small_font.render("1 - " + upgrade_options[0], True, (255, 255, 255))
        option_2_text = small_font.render("2 - " + upgrade_options[1], True, (255, 255, 255))

        screen.blit(title_text, (515, 260))
        screen.blit(option_1_text, (430, 330))
        screen.blit(option_2_text, (430, 380))

    pygame.display.flip()

    if player_hp <= 0:
        print("GAME OVER")
        running = False

pygame.quit()
sys.exit()