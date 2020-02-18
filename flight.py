# -*- coding: utf-8 -*-

import pygame
import time
from pygame.locals import *

screen_width = 480
screen_height = 852


class Hero(object):
    def __init__(self, screen):
        self.x = 190
        self.y = 740
        self.width = 100
        self.height = 110
        self.screen = screen
        self.image = pygame.image.load("./resources/flight-1.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.bullets = []

    def display_hero(self):
        self.screen.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            bullet.display()
            bullet.move()
            if bullet.judge():
                self.bullets.remove(bullet)

    def move_left(self):
        if self.x > 0:
            self.x -= 5

    def move_right(self):
        if self.x < (screen_width - self.width):
            self.x += 5

    def move_up(self):
        if self.y > self.height:
            self.y -= 5

    def move_down(self):
        if self.y < (screen_height - self.height):
            self.y += 5

    def fire(self):
        self.bullets.append(Bullet(self.screen, self.x, self.y))


class Bullet(object):
    def __init__(self, screen, x, y):
        self.x = x + 40
        self.y = y
        self.width = 15
        self.height = 15
        self.screen = screen
        self.image = pygame.image.load("./resources/bullet.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def display(self):
        self.screen.blit(self.image, (self.x, self.y - 20))

    def move(self):
        self.y -= 5

    def judge(self):
        if self.y <= 0:
            return True
        else:
            return False


class Enemy(object):
    def __init__(self, screen):
        self.x = 0
        self.y = 0
        self.screen = screen
        self.image = pygame.image.load("./resources/enemy.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.image = pygame.transform.rotate(self.image, 180)
        self.bullets = []
        self.direction = "right"

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    def fire(self):
        self.bullets.append(Bullet(self.screen, self.x, self.y))

    def move(self):
        if self.direction == "right":
            self.x += 5
        elif self.direction == "left":
            self.x -= 5

        if self.x > screen_width - 100:
            self.direction = "left"
        elif self.x <= 0:
            self.direction = "right"


def key_control(hero):
    for event in pygame.event.get():
        if event.type == QUIT:
            print("exit")
            exit()

    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_s] or key_pressed[K_DOWN]:
        print("down")
        hero.move_down()

    if key_pressed[K_w] or key_pressed[K_UP]:
        print("up")
        hero.move_up()

    if key_pressed[K_a] or key_pressed[K_LEFT]:
        print("left")
        hero.move_left()

    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        print("right")
        hero.move_right()


def main():
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    background = pygame.image.load("./resources/background.jpeg")
    background = pygame.transform.scale(background, (480, 852))

    hero = Hero(screen)
    enemy = Enemy(screen)

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)

        screen.blit(background, (0, 0))

        hero.display_hero()

        enemy.display()
        enemy.move()

        key_control(hero)

        pygame.display.update()

        time.sleep(0.01)


if __name__ == "__main__":
    main()
