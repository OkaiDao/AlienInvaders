import pygame as pg
from pygame.sprite import Sprite
from timer import Timer
from Bullets import BulletFromShip
from pygame.sprite import Group

class Ship(Sprite):

    images = [pg.image.load('images/ship.bmp')]
    images_boom = [pg.image.load('images/boom' + str(i + 1) + '.bmp') for i in range(4)]
    timer_boom = Timer(frames = images_boom, wait = 100, looponce = True)
    timer = Timer(frames=images, wait=1000)
    
    def __init__(self, game, sound, aliens = None, barriers = None):
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.sound = sound
        self.game = game
        self.image = pg.image.load('images/ship.bmp') #Redundant
        self.rect = self.image.get_rect()
        self.screen_rect = game.screen.get_rect()
        self.center = 0
        self.centShip()
        self.movRight = False
        self.movLeft = False 
        self.aliens = aliens
        self.barriers = barriers

        #self.bullets = bullets
        self.shooting_bullets = False
        self.bullets_attempted = 0
        self.dead, self.wiped, self.timer_switched = False, False, False
        self.ship_group = Group()
        self.bulletKillAliens = Group()
        self.ship_group.add(self)
        self.timer = Ship.timer

    def add_bullet(self, game, x, y):
        self.bulletKillAliens.add(BulletFromShip(game = self.game, x = self.rect.centerx, y = self.rect.top))

    def bullet_group(self):
        return self.bulletKillAliens

    def group(self):
        return self.ship_group

    def centShip(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)

    def killed(self):
        if not self.dead and self.wiped: 
            self.dead = True
        if self.dead and not self.timer_switched:
            self.timer = Ship.timer_boom
            self.timer_switched = True

    def update(self):
        self.bulletKillAliens.update()
        if self.dead and self.timer_switched:
            if self.timer.frame_index() == len(Ship.images_boom) - 1:
                self.dead = False
                self.timer_switched = False
                self.wiped = True
                self.timer.reset()
                self.game.reset()

        bulletAlienCollisions = pg.sprite.groupcollide(self.aliens.group(), self.bulletKillAliens, False, True)
        
        if bulletAlienCollisions:
            for alien in bulletAlienCollisions:
                #alien.dead = True
                alien.killed()

        bulletBarrierCollisions = pg.sprite.groupcollide(self.barriers.group(), self.bulletKillAliens, True, True)

        if bulletBarrierCollisions:
            for barrier_block in bulletBarrierCollisions:
                barrier_block.damaged()

        if len(self.aliens.group()) == 0:
            self.bulletKillAliens.empty()
            self.settings.increase_speed()
            self.aliens.create_fleet()
            self.game.stats.level +=1
            self.game.sb.prep_level()

        delta = self.settings.ship_speed_factor
        if self.movRight and self.rect.right < self.screen_rect.right: self.center += delta
        if self.movLeft  and self.rect.left > 0: self.center -= delta
        if self.shooting_bullets and not self.dead:
            self.sound.shoot_bullet()
            #self.add_bullet(game = self.game, x = self.rect.centerx, y = self.rect.top)
            self.add_bullet(game = self.game, x = self.rect.x, y = self.rect.y)
            self.shooting_bullets = False
        self.rect.centerx = self.center

    def draw(self): 
        for bullet in self.bulletKillAliens:
            bullet.draw()
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
        #self.screen.blit(self.image, self.rect)
     