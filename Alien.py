import pygame as pg
from pygame.sprite import Sprite
from pygame.sprite import Group
from timer import Timer
from Bullets import BulletFromAlien
from random import randint

class Aliens:
    def __init__(self, settings, screen, ship_height, game, barriers):
        self.settings = settings
        self.aliens = Group()
        self.screen = screen
        self.game = game
        self.ship_height = ship_height
        self.barriers = barriers
        self.ship_group = Group()
        self.bulletKillShip = Group()
        self.last_bullet_shot = pg.time.get_ticks()
        self.create_fleet()
        self.ship = None

    def create_fleet(self):
        settings, screen = self.settings, self.screen
        alien = Alien(parent = self, settings = settings, game = self.game, screen = self.screen)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        rows_per_screen = self.rows_per_screen(settings = settings, alien_height = alien_height)
        aliens_per_row = self.aliens_per_row(settings = settings, alien_width = alien_width)
        #self.aliens.add(alien)

        for y in range(rows_per_screen):
            for x in range(aliens_per_row):
                if (y < 3):
                    alien = Alien(parent = self, settings = settings, game = self.game, screen = screen, number = y , x = alien_width * (4 +  1.5 * x), y = alien_height * (1 + y))
                else:
                    alien = Alien(parent = self, settings = settings, game = self.game, screen = screen, number = 3 , x = alien_width * (4 + 1.5 * x), y = alien_height * (1 + y))
                self.aliens.add(alien)

    def aliens_per_row(self, settings, alien_width):
        space_x = settings.screen_width - 2 * alien_width
        return int(space_x / (2 * alien_width))

    def add(self, alien): self.aliens.add(alien)

    def remove(self, alien): self.aliens.aliens.remove(alien)

    def add_bullet(self, game, x, y):
        self.bulletKillShip.add(BulletFromAlien(game = game, x = x, y = y))

    def change_direction(self):
        for alien in self.aliens:
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def rows_per_screen(self, settings, alien_height): return 5

    def group(self):
        return self.aliens

    def add_ship(self, ship):
        self.ship = ship
        self.ship_group.add(self.ship)

    def empty(self): 
        self.aliens.empty()

    def remove(self, alien): 
        self.aliens.remove(alien)


    def check_edges(self):
        #for alien in self.aliens:
        for alien in self.aliens.sprites():
            if alien.check_edges(): return True
        return False

    def check_aliens_bottom(self):
        r = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom > r.bottom:
                return True
        return False

    def alienShootsTime(self):
        now = pg.time.get_ticks()
        if now > self.last_bullet_shot + self.settings.alien_bullets_every * 1000:
            li = self.aliens.sprites()
            length = len(li)
            shooter = li[randint(1, length - 1)]
            self.add_bullet(game = self.game, x = shooter.x + 34, y = shooter.y)
            self.last_bullet_shot = now

    def update(self):
        self.aliens.update()
        self.bulletKillShip.update()
        bulletCollisions = pg.sprite.groupcollide(self.bulletKillShip,  self.ship.group(), True, False)

        if bulletCollisions:
            self.ship.dead = True
            self.ship.killed()

        #Barrier
        bulletBarrierCollisions = pg.sprite.groupcollide(self.barriers.group(), self.bulletKillShip, True, True)
        
        if bulletBarrierCollisions:
            for barrier_block in bulletBarrierCollisions:
                barrier_block.damaged()

        #for bullet in self.bulletKillShip.copy():
        #    if bullet.rect.bottom <= 0:
        #        self.bulletKillShip.remove(bullet)

        for bullet in self.bulletKillShip.copy():
            if bullet.rect.top >= self.screen.get_rect().height:
                self.bulletKillShip.remove(bullet)

        self.alienShootsTime()

        if self.check_edges():
            self.change_direction()
        if self.check_aliens_bottom() or pg.sprite.spritecollideany(self.game.ship, self.aliens):
            self.game.reset()
            return

        for alien in self.aliens.copy():
            alien.update()
            #if alien.rect.bottom <= 0 or alien.reallydead: self.aliens.remove(alien)
            if alien.rect.bottom >= self.screen.get_rect().height or alien.reallydead:
                self.aliens.remove(alien)

    def draw(self):
        for alien in self.aliens.sprites(): 
            alien.draw()
        for bullet in self.bulletKillShip:
            bullet.draw()

class Alien(Sprite):
    
    images = [[pg.image.load('images/alien0' + str(number + 1) + '_0' +str(i + 1) + '.bmp') for i in range(4)] for number in range(4)]
    images_boom = [pg.image.load('images/boom' + str(i + 1) + '.bmp') for i in range(4)]
    timers = []

    for i in range(4):
        timers.append(Timer(frames = images[i], wait = 300))
    timer_boom = Timer(frames = images_boom, wait = 100, looponce = True)

    def __init__(self, parent, settings, game, screen, number = 0, x = 0, y = 0, speed = 0):
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.game = game
        self.number = number
        self.aliens = parent
        self.dead = False
        self.reallydead = False
        self.timer = Alien.timers[number]
        self.rect = self.timer.imagerect().get_rect()
        self.rect.x = self.x = x
        self.rect.y = self.y = y
        self.x = float(self.rect.x)
        self.speed = speed
        self.timer_switched = False
        self.update_requests = 0

    def check_edges(self):
        r, rscreen = self.rect, self.screen.get_rect()
        return r.right >= rscreen.right or r.left <= 0
    
    def killed(self):
        if not self.dead and not self.reallydead:
            self.dead = True
        if self.dead and not self.timer_switched:
            self.timer = Timer(frames = Alien.images_boom, wait = 400, looponce = True)
            self.timer_switched = True
            self.game.stats.score += self.settings.alien_points #* len(self.aliens)
            self.game.sb.check_high_score(self.game.stats.score)
            self.game.sb.prep_score()

    def update(self):
        
        delta = self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x += delta
        self.x = self.rect.x

        if self.dead and self.timer_switched:
            if self.timer_boom.frame_index() == len(Alien.images_boom) - 1:
                self.dead = False
                self.timer_switched = False
                self.reallydead = True
                self.aliens.remove(self)
                self.timer.reset()


    def draw(self):
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)