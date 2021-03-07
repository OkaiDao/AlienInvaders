#Jonathan Dao

import pygame as pg
from Ship import Ship
from Settings import Settings
from Alien import Alien, Aliens
import Game_Functions as GF
import time
from pygame.sprite import Group
from Scoreboard import Scoreboard
from menu import MainMenu
from Sound import Sound
#from Bullets import Bullets
from Game_Stats import GameStats
from Barrier import Barriers

class Game:

    def __init__(self):
        pg.init()
        #Screen Settings
        self.settings = Settings()
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        self.display = pg.Surface((self.settings.screen_width, self.settings.screen_height))
        self.window = pg.display.set_mode(((self.settings.screen_width, self.settings.screen_height)))
        ship_image = pg.image.load('images/ship.bmp')
        self.screen.fill(self.settings.bg_color)

        #Window Icon/Caption
        pg.display.set_caption("Alien Invasion")
        pg.display.set_icon(ship_image)
        self.ship_height = ship_image.get_rect().height

        #Misc
        self.ongoing = False
        self.UP_KEY, self.DOWN_KEY, self.PLAY_KEY, self.BACK_KEY = False, False, False, False
        self.sound = Sound(bg_music="sounds/startrektheme.wav")
        self.aliens = self.stats = self.sb = self.ship = None
        self.hs = 0
        self.startMenu = MainMenu(self)
        self.BLACK, self.WHITE = (60, 60, 60), (255, 255, 255) #not really black
        self.sound.play()
        self.sound.pause_bg()
        self.restart()

  
    def restart(self):
        self.startMenu.display_menu()
        alien_group = Group()
        self.stats = GameStats(settings = self.settings)
        self.sb = Scoreboard(game = self, sound = self.sound)
        self.barriers = Barriers(game = self)
        self.aliens = Aliens(settings = self.settings, screen = self.screen,
                            ship_height = self.ship_height, game = self, barriers = self.barriers)
        self.ship = Ship(game = self, sound = self.sound, aliens = self.aliens, barriers = self.barriers)
        self.aliens.add_ship(ship = self.ship)
        #Stats
        self.stats.high_score = self.hs
        self.sb.prep_high_score()

    def play(self):
        #Set false later
        #ongoing = True
        while self.ongoing:
            for event in pg.event.get():
                if event.type == pg.QUIT: 
                    self.startMenu.run_display = False
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pg.mouse.get_pos()
                    #Check Play Button
                elif event.type == pg.KEYDOWN: GF.check_keydown_events(event, self.settings, self.screen, self.ship)
                elif event.type == pg.KEYUP: GF.check_keyup_events(event, self.ship)

            self.ship.update()
            self.aliens.update()

            self.screen.fill(self.settings.bg_color)
            self.ship.update()
            self.ship.draw()
            self.barriers.draw()
            self.aliens.draw()
            self.sb.show_score()
            pg.display.update()
            if not self.sound.playing_bg: self.sound.unpause_bg()

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.PLAY_KEY, self.BACK_KEY = False, False, False, False

    def check_events(self):
    # Watch for keyboard and mouse events.
        for event in pg.event.get():
            #if event.type == pg.QUIT:
            #Do something
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.PLAY_KEY = True
                if event.key == pg.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pg.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pg.K_UP:
                    self.UP_KEY = True

    def reset(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.aliens.create_fleet()
            self.ship.centShip()
            time.sleep(0.5)
            self.ship.timer = Ship.timer
        else:
            self.stats.game_active = False
            self.sound.pause_bg()
            self.hs = self.stats.high_score
            self.restart()

def main():
    g = Game()
    #g.startMenu.display_menu()
    #if g.ongoing:
    #    g.play()

    g.play()

if __name__ == '__main__':
    main()

