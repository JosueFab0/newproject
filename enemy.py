import pygame
import math
import random


class Enemy:

    def __init__(self, screen_width, screen_height):
        side = random.randint(1, 4)

        if side == 1:
            self.x = random.randint(0, screen_width)
            self.y = -30

        elif side == 2:
            self.x = random.randint(0, screen_width)
            self.y = screen_height + 30

        elif side == 3:
            self.x = -30
            self.y = random.randint(0, screen_height)

        else:
            self.x = screen_width + 30
            self.y = random.randint(0, screen_height)

        self.radius = 15
        self.speed = 1.2
        self.color = (180, 80, 80)

    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            dx /= distance
            dy /= distance

            enemy_speed_bonus = pygame.time.get_ticks() / 1000 * 0.02
            current_speed = self.speed + enemy_speed_bonus

            self.x += dx * current_speed
            self.y += dy * current_speed

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )


def separate_enemies(enemies):
    for i in range(len(enemies)):
        enemy_a = enemies[i]

        for j in range(i + 1, len(enemies)):
            enemy_b = enemies[j]

            dx = enemy_b.x - enemy_a.x
            dy = enemy_b.y - enemy_a.y

            distance = math.sqrt(dx ** 2 + dy ** 2)
            min_distance = enemy_a.radius + enemy_b.radius

            if distance < min_distance and distance != 0:
                overlap = min_distance - distance

                dx /= distance
                dy /= distance

                enemy_a.x -= dx * overlap / 2
                enemy_a.y -= dy * overlap / 2

                enemy_b.x += dx * overlap / 2
                enemy_b.y += dy * overlap / 2


def separate_enemy_from_player(enemy, player):
    dx = enemy.x - player.x
    dy = enemy.y - player.y

    distance = math.sqrt(dx ** 2 + dy ** 2)
    min_distance = player.radius + enemy.radius

    if distance < min_distance and distance != 0:
        overlap = min_distance - distance

        dx /= distance
        dy /= distance

        enemy.x += dx * overlap
        enemy.y += dy * overlap

        player.take_damage(1)