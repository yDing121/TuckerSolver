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
        grid_surface = pygame.Surface(self.width, self.height)
        self.solver = Solver.Solver(n, m)
    
    def print_tucker(self):
        print(self.A)
    
    
        

if __name__ == "__main__":
    disp = Display(500, 500)
    
