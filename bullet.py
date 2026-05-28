import pygame


class Bullet:

    def __init__(self, x, y, direction_x, direction_y, piercing=False):
        self.x = x
        self.y = y

        self.direction_x = direction_x
        self.direction_y = direction_y

        self.radius = 6
        self.speed = 8
        self.color = (250, 230, 80)

        self.piercing = piercing

    def update(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius
        )

    def is_outside_screen(self, screen_width, screen_height):
        return (
            self.x < -50 or
            self.x > screen_width + 50 or
            self.y < -50 or
            self.y > screen_height + 50
        )