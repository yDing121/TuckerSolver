import pygame
import sympy

pygame.init()

class InputBox:
    def __init__(self, x, y, w, h, text='', text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, text_color)
        self.active = False
        self.text_color = text_color

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = (0, 255, 0) if self.active else (200, 200, 200)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = (200, 200, 200)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.text_color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def main():
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    intro_boxes = [InputBox(300, 150, 140, 32, text='3'),  # Default rows
                   InputBox(300, 200, 140, 32, text='4')]  # Default columns

    done = False
    dimensions_set = False
    input_boxes = []

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if not dimensions_set:
                for box in intro_boxes:
                    box.handle_event(event)
            else:
                for row in input_boxes:
                    for box in row:
                        box.handle_event(event)

        if not dimensions_set:
            if all(not box.active for box in intro_boxes) and intro_boxes[0].text and intro_boxes[1].text:
                # Initialize matrix input grids once dimensions are set
                rows, cols = int(intro_boxes[0].text), int(intro_boxes[1].text)
                input_boxes = [
                    [InputBox(100 + j * 60, 100 + i * 40, 50, 30) for j in range(cols)]
                    for i in range(rows)
                ]
                dimensions_set = True
                screen = pygame.display.set_mode((max(800, 100 + cols * 60), max(600, 100 + rows * 40)))

        screen.fill((30, 30, 30))
        if not dimensions_set:
            for box in intro_boxes:
                box.draw(screen)
        else:
            for row in input_boxes:
                for box in row:
                    box.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    # Converting inputs to sympy matrix
    if dimensions_set:
        matrix_data = [
            [sympy.sympify(box.text) for box in row] for row in input_boxes
        ]
        return sympy.Matrix(matrix_data)

if __name__ == '__main__':
    matrix = main()
    if matrix:
        print("The matrix you entered is:")
        sympy.pprint(matrix)
    pygame.quit()