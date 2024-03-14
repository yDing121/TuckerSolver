import pygame
import sys
import numpy as np
import Solver


class Display:
    class Button:
        def __init__(self, w, h) -> None:
            self.button_w = w
            self.button_h = h
    
    def __init__(self, screen_x, screen_y, n, m) -> None:
        self.width = screen_x
        self.height = screen_y
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tucker Helper")

        self.BUTTON_WIDTH = 20
        self.BUTTON_HEIGHT = 20

        self.solver = Solver.Solver(n, m)

        self.n = n
        self.m = m

    # TODO Fix the buttons and clicking
    # Function to draw buttons
    def draw_buttons(self, buttons):
        for button in buttons:
            pygame.draw.rect(self.screen, button['color'], button['rect'])

    # Function to create buttons
    def create_buttons(self):
        buttons = []
        for row in range(self.m + 1):
            for col in range(self.n + 1):
                rect = pygame.Rect(col * self.BUTTON_WIDTH, row * self.BUTTON_HEIGHT, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
                button = {'rect': rect, 'color': (30, 30, 30), 'clicked': False}
                buttons.append(button)
        return buttons

    def print_tucker(self):
        print(self.solver)


if __name__ == "__main__":
    disp = Display(500, 500, 2,3)
    
