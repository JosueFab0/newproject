import pygame
import math

from bullet import Bullet


class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.radius = 20
        self.speed = 3

        self.hp = 50
        self.max_hp = 50

        self.level = 1
        self.xp = 0
        self.xp_needed = 100

        self.gold = 0

        self.last_direction_x = 1
        self.last_direction_y = 0

        self.shoot_cooldown = 1000
        self.last_shot_time = 0

        self.bullet_piercing = False

    def update_movement(self):
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

            self.last_direction_x = move_x
            self.last_direction_y = move_y

            self.x += move_x * self.speed
            self.y += move_y * self.speed

    def shoot(self, bullets):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot_time >= self.shoot_cooldown:
            self.last_shot_time = current_time

            base_angle = math.atan2(
                self.last_direction_y,
                self.last_direction_x
            )

            angles = [
                base_angle - 0.25,
                base_angle,
                base_angle + 0.25
            ]

            for angle in angles:
                direction_x = math.cos(angle)
                direction_y = math.sin(angle)

                bullet = Bullet(
                    self.x,
                    self.y,
                    direction_x,
                    direction_y,
                    self.bullet_piercing
                )

                bullets.append(bullet)

    def add_xp(self, amount):
        self.xp += amount

        if self.xp >= self.xp_needed:
            self.xp -= self.xp_needed
            self.level += 1

            if self.level < 10:
                self.xp_needed += 100
            else:
                self.xp_needed += 200

            return True

        return False

    def apply_upgrade(self, option):
        if option == 0:
            self.shoot_cooldown -= 150

            if self.shoot_cooldown < 250:
                self.shoot_cooldown = 250

        elif option == 1:
            self.bullet_piercing = True

    def take_damage(self, amount):
        self.hp -= amount

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (240, 220, 170),
            (int(self.x), int(self.y)),
            self.radius
        )

        pygame.draw.rect(
            screen,
            (80, 80, 80),
            (int(self.x - 25), int(self.y + 30), 50, 8)
        )

        pygame.draw.rect(
            screen,
            (200, 50, 50),
            (
                int(self.x - 25),
                int(self.y + 30),
                int((self.hp / self.max_hp) * 50),
                8
            )
        )