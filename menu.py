import pygame as pg

class Menu():
    
    images = [pg.image.load('images/alien0' + str(number + 1) + '_01.bmp') for number in range(4)]

    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.settings.screen_width / 2, self.game.settings.screen_height / 2
        self.run_display = True
        self.cursor_rect = pg.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.font_name = pg.font.get_default_font()

    def draw_cursor(self):
        self.draw_text('*', self.cursor_rect.x, self.cursor_rect.y)

    def draw_text(self, text, x, y):
        font = pg.font.Font(self.font_name, 20)
        text_surface = font.render(text, True, self.game.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game.display.blit(text_surface, text_rect)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pg.display.update()
        self.game.reset_keys()

    
    def drawImage(self, number, x, y):
        rect = self.images[number].get_rect()
        rect.center = (x, y)
        self.game.display.blit(self.images[number], rect)


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Play"
        self.startx, self.starty = self.mid_w, self.mid_h + 100
        #add for other buttons here

    def display_menu(self):
        self.run_display = True

        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            r = - 120
            t = - 300
            for i in range(4):
                self.drawImage(i, self.game.settings.screen_width / 2 + r, self.game.settings.screen_height / 2 + t)
                t += 90

            self.draw_text('= 10 Points', self.game.settings.screen_width / 2 + 20, self.game.settings.screen_height / 2 - 300)
            self.draw_text('= 20 Points', self.game.settings.screen_width / 2 + 20, self.game.settings.screen_height / 2 - 210)
            self.draw_text('= 30 Points', self.game.settings.screen_width / 2 + 20, self.game.settings.screen_height / 2 - 120)
            self.draw_text('= 40 Points', self.game.settings.screen_width / 2 + 20, self.game.settings.screen_height / 2 - 30)
            self.draw_text('Main Menu', self.game.settings.screen_width / 2, 40)
            self.draw_text("Play", self.startx, self.starty)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        #For Scroll Menu
        if self.state == 'Play':
            self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def check_input(self):
        self.move_cursor()

        if self.game.PLAY_KEY:
            if self.state == 'Play':
                self.game.ongoing = True
                self.game.reset_keys()
                self.run_display = False