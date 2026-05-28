import pygame
import random
import math


class Loot:

    def __init__(self, x, y, loot_type, value):
        self.x = x
        self.y = y

        self.type = loot_type
        self.value = value

        self.radius = 8

        if self.type == "xp":
            self.color = (60, 120, 255)
        else:
            self.color = (230, 190, 40)

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )


def create_loot(x, y, loot_items):
    loot_chance = random.randint(1, 100)

    if loot_chance <= 45:
        loot_items.append(
            Loot(x, y, "xp", 25)
        )

    elif loot_chance <= 70:
        loot_items.append(
            Loot(x, y, "gold", 1)
        )


def collect_loot(player, loot_items):
    leveled_up = False

    for loot in loot_items[:]:
        dx = loot.x - player.x
        dy = loot.y - player.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < player.radius + loot.radius:

            if loot.type == "xp":
                if player.add_xp(loot.value):
                    leveled_up = True

            elif loot.type == "gold":
                player.gold += loot.value

            loot_items.remove(loot)

    return leveled_up