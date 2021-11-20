#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import curses
from mainMenu import MainMenu
from window import Window
# from chars import Chars


def start(window):
    # chars = Chars(window)
    # chars.run()
    mainMenu = MainMenu(window)
    mainMenu.run()


def main(stdscr):
    window = Window(stdscr)
    start(window)


if __name__ == "__main__":
    curses.wrapper(main)
