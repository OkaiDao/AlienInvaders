import sys
import pygame as pg

def check_keydown_events(event, settings, screen, ship):
    if event.key == pg.K_RIGHT: ship.movRight = True
    elif event.key == pg.K_LEFT: ship.movLeft = True
    elif event.key == pg.K_SPACE: ship.shooting_bullets = True
    elif event.key == pg.K_q: sys.exit()

def check_keyup_events(event, ship):
    if event.key == pg.K_RIGHT: ship.movRight = False
    elif event.key == pg.K_LEFT: ship.movLeft = False
    elif event.key == pg.K_SPACE: ship.shooting_bullets = False

#def check_play_button(stats, play_button, mouse_x, mouse_y):
#    if play_button.rect.collidepoint(mouse_x, mouse_y):
#        stats.game_active = True

#def check_events(settings, screen, ship):
    # Watch for keyboard and mouse events.
#    for event in pg.event.get():
#        if event.type == pg.QUIT: sys.exit()
#        elif event.type == pg.MOUSEBUTTONDOWN:
#            mouse_x, mouse_y = pg.mouse.get_pos()
#            check_play_button(stats=stats, play_button=play_button, mouse_x=mouse_x, mouse_y=mouse_y)
#        elif event.type == pg.KEYDOWN: check_keydown_events(event=event, settings=settings, screen=screen,
#                                                            ship=ship, bullets=bullets)
#        elif event.type == pg.KEYUP: check_keyup_events(event=event, ship=ship)

