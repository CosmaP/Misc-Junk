#!/usr/bin/env python

# Rules
# Dead from starvation.
# Continue living.
# Dead from overcrowding.
# Alive from reproduction.

import math
import numpy
import PySimpleGUI as sg

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

def PlayGame(PlayingField):
    #PlayingField.draw_text(text="(0,0)", location=(0,0))
    #PlayingField.draw_text(text="(50,50)", location=(50,50))
    #PlayingField.draw_line((0,0),(50,50))
    for x in my_range(0, 1, 0.1):
        print(x)
        PlayingField.draw_line(((math.sin(x) * 10),(math.cos(x) * 10)),
                               ((math.sin(x) * 10),(math.cos(x) * 10)))
    sg.popup('Game Over')

def Main(X,Y):

    title="Game Of Life"
    WindowMargin=(10, 10)
    WindowSize=(X, Y)
    PlayingField = sg.Graph(WindowSize, (0,0),(200,200),background_color="white")

    sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [  [PlayingField],
                [sg.Button('Ok'), sg.Button('Cancel')] ]

    # Create the Window
    window = sg.Window(title, layout, margins=WindowMargin)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        
        if event == 'Ok' : # Start the Game
            PlayGame(PlayingField)


if (__name__ == "__main__"):
    Main(X=400, Y=400)
    #window.close()