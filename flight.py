# -*- coding: utf-8 -*-

import pygame
import time
from pygame.locals import *
import random

screen_width = 480
screen_height = 852


class Hero(pygame.sprite.Sprite):
    def __init__(self, screen, *groups):
        super().__init__(*groups)
        self.width = 100
        self.height = 110
        self.screen = screen
        self.image = pygame.image.load("./resources/flight-1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = 190
        self.rect.y = 740
        self.bullets = pygame.sprite.Group()

    def display_hero(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.bullets.draw(self.screen)
        for bullet in self.bullets:
            bullet.move()
            if bullet.judge():
                self.bullets.remove(bullet)

    def move_left(self):
        if self.rect.x > 0:
            self.rect.x -= 5

    def move_right(self):
        if self.rect.x < (screen_width - self.width):
            self.rect.x += 5

    def move_up(self):
        if self.rect.y > self.height:
            self.rect.y -= 5

    def move_down(self):
        if self.rect.y < (screen_height - self.height):
            self.rect.y += 5

    def fire(self):
        self.bullets.add(Bullet(self.screen, self.rect.x, self.rect.y))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, *groups):
        super().__init__(*groups)
        # self.x = x + 40
        # self.y = y
        self.width = 15
        self.height = 15
        self.screen = screen
        self.image = pygame.image.load("./resources/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x + 40
        self.rect.y = y

    def display(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y - 20))

    def move(self):
        self.rect.y -= 5

    def judge(self):
        if self.rect.y <= 0:
            return True
        else:
            return False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, *groups):
        super().__init__(*groups)
        # self.x = 0
        # self.y = 0
        self.screen = screen
        self.image = pygame.image.load("./resources/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, screen_width - self.rect.width)
        self.bullets = []
        self.direction = "down"

    def display(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def fire(self):
        self.bullets.append(Bullet(self.screen, self.rect.x, self.rect.y))

    def move(self):
        self.rect.y += 5


def key_control(hero):
    for event in pygame.event.get():
        if event.type == QUIT:
            print("exit")
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_j:
                hero.fire()

    key_pressed = pygame.key.get_pressed()
    if key_pressed[K_s] or key_pressed[K_DOWN]:
        # print("down")
        hero.move_down()

    if key_pressed[K_w] or key_pressed[K_UP]:
        # print("up")
        hero.move_up()

    if key_pressed[K_a] or key_pressed[K_LEFT]:
        # print("left")
        hero.move_left()

    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        # print("right")
        hero.move_right()


def check_collide(hero, enemy):
    if len(hero.bullets) == 0:
        return False

    collide_list = pygame.sprite.spritecollide(enemy, hero.bullets, True)
    if len(collide_list) > 0:
        return True
    else:
        return False


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

        if check_collide(hero, enemy):
            enemy = Enemy(screen)

        key_control(hero)

        pygame.display.update()

        time.sleep(0.01)


if __name__ == "__main__":
    main()
