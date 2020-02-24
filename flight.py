# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import random

screen_width = 480
screen_height = 852

hero_sprite_group = pygame.sprite.Group()
enemy_sprite_group = pygame.sprite.Group()

pygame.init()
pygame.mixer.init()

background_bgm = pygame.mixer.Sound("./resources/background.ogg")
fire_bgm = pygame.mixer.Sound("./resources/fire.ogg")
explosion_bgm = pygame.mixer.Sound("resources/explosion.ogg")

font = pygame.font.Font(None, 30)


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
        fire_bgm.play()
        self.bullets.add(Bullet(self.screen, self.rect.x, self.rect.y))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, *groups):
        super().__init__(*groups)
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
        self.screen = screen
        self.image = pygame.image.load("./resources/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, screen_width - self.rect.width)
        self.bullets = []

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
            return True
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

    return False


def check_hit_enemy_collide(hero, enemy):
    if len(hero.bullets) == 0:
        return False

    collide_list = pygame.sprite.spritecollide(enemy, hero.bullets, True)
    if len(collide_list) > 0:
        return True
    else:
        return False


def check_hero_enemy_collide(hero):
    if len(enemy_sprite_group) == 0:
        return False

    collide_list = pygame.sprite.spritecollide(hero, enemy_sprite_group, False)
    if len(collide_list) > 0:
        return True
    else:
        return False


def update_score(screen, score):
    score_text = font.render("Score : {}".format(score), 1, (0, 0, 0))
    score_text_pos = (5, 5)
    screen.blit(score_text, score_text_pos)


def main():
    score = 0
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    pygame.display.set_caption("Flight Game")

    background = pygame.image.load("./resources/background.jpeg")
    background = pygame.transform.scale(background, (480, 852))

    background_bgm.play()

    hero = Hero(screen)
    hero_sprite_group.add(hero)
    enemy = Enemy(screen)
    enemy_sprite_group.add(enemy)

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)

        screen.blit(background, (0, 0))
        update_score(screen, score)

        hero.display_hero()

        enemy.display()
        enemy.move()
        if enemy.rect.y > screen_height:
            enemy_sprite_group.remove(enemy)
            enemy = Enemy(screen)
            enemy_sprite_group.add(enemy)

        if check_hit_enemy_collide(hero, enemy):
            explosion_bgm.play()
            score += 1
            enemy_sprite_group.remove(enemy)
            enemy = Enemy(screen)
            enemy_sprite_group.add(enemy)

        if check_hero_enemy_collide(hero):
            die_text = font.render("You Die", 1, (0, 0, 0))
            die_text_pos = (screen_width / 2, screen_height / 2)
            screen.blit(die_text, die_text_pos)

        if  key_control(hero):
            return

        pygame.display.update()


if __name__ == "__main__":
    main()
