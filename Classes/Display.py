import pygame
import sys


class Display:
    def __init__(self, screen_x, screen_y) -> None:
        self.width = screen_x
        self.height = screen_y
        self.screen = pygame.display.set_mode(self.width, self.height)


# if __name__ == "__main__":
#     print("Test")
#     pygame.init()

#     size = width, height = 320, 240
#     speed = [1, 1]
#     black = 0, 0, 0

#     screen = pygame.display.set_mode(size)

#     ball = pygame.image.load("./Classes/intro_ball.gif")
#     ballrect = ball.get_rect()

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()

#         ballrect = ballrect.move(speed)
#         if ballrect.left < 0 or ballrect.right > width:
#             speed[0] = -speed[0]
#         if ballrect.top < 0 or ballrect.bottom > height:
#             speed[1] = -speed[1]

#         screen.fill(black)
#         screen.blit(ball, ballrect)
#         pygame.display.flip()
