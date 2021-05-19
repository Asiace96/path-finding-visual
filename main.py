import pygame as pg
from consts import Colors
from gui import Button, MainMenu
import os


def main():
    # ---------------------------------------- Pygame general settings ---------------------------------------- #
    pg.init()

    WIDTH = 800
    SIZE = (WIDTH, WIDTH)
    screen = pg.display.set_mode(SIZE)
    main_icon = pg.image.load(os.path.join('assets', 'main_icon.png'))
    icon = pg.image.load(os.path.join('assets', 'icon.png'))
    pg.display.set_icon(icon)
    pg.display.set_caption('Path Finding Algorithm Visualizer')
    font = pg.font.Font(os.path.join('assets', 'Ubuntu-Bold.ttf'), 22)
    title_font = pg.font.Font(os.path.join('assets', 'Ubuntu-Bold.ttf'), 50)

    # ---------------------------------------- Main-Menu settings ---------------------------------------- #
    buttons = []
    buttons.append(Button(50, 70, 260, 50, Colors.LIGHT_GREEN, font, 'Controls'))
    buttons.append(Button(50, WIDTH-200, 260, 50, Colors.LIGHT_GREEN, font, 'Breadth First Search'))
    buttons.append(Button(500, WIDTH-200, 260, 50, Colors.LIGHT_GREEN, font, 'Depth First Search'))
    buttons.append(Button(50, WIDTH-100, 260, 50, Colors.LIGHT_GREEN, font, 'A* Search'))
    buttons.append(Button(500, WIDTH-100, 260, 50, Colors.LIGHT_GREEN, font, 'Greedy Best First Search'))
    menu = MainMenu(screen, main_icon, title_font, font, buttons)

    menu.loop()
    


if __name__ == '__main__':
    main()
