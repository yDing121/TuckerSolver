import pygame
import pygame.freetype
import sympy


class InputBox:
    def __init__(self, x, y, width, height, initial_text='', text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (200, 200, 200)
        self.text = initial_text
        self.font = pygame.freetype.SysFont(None, 24)
        self.text_color = text_color
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = (0, 255, 0) if self.active else (200, 200, 200)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = (200, 200, 200)
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        self.update()

    def update(self):
        # Prevent overflowing text
        width = max(50, self.font.get_rect(self.text).width + 10)
        self.rect.w = width

    def draw(self, screen):
        # Render the text.
        self.font.render_to(screen, (self.rect.x+5, self.rect.y+10), self.text, self.text_color)
        # Draw the box
        pygame.draw.rect(screen, self.color, self.rect, 2)


def assign_matrix(screen, rows, cols):
    box_w = 60
    box_h = 40
    input_boxes = [[InputBox(150 + j * (box_w + 15), 100 + i * (box_h + 15), box_w, box_h, '') for j in range(cols)] for i in range(rows)]

    done = False
    while not done and rows and cols:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            for row in input_boxes:
                for box in row:
                    box.handle_event(event)

        screen.fill((30, 30, 30))
        for row in input_boxes:
            for box in row:
                box.draw(screen)

        pygame.display.flip()
    matrix_data = [[sympy.sympify(box.text) if box.text else sympy.S.Zero for box in row] for row in input_boxes]
    return sympy.Matrix(matrix_data)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    # Set dimensions
    rows_box = InputBox(300, 150, 50, 40, '3')
    cols_box = InputBox(300, 200, 50, 40, '4')

    rows = cols = None
    waiting_for_dims = True
    while waiting_for_dims:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                rows_box.handle_event(event)
                cols_box.handle_event(event)
                if not rows_box.active and not cols_box.active:
                    waiting_for_dims = False
                    rows = int(rows_box.text)
                    cols = int(cols_box.text)
                    break

        screen.fill((150, 150, 150))
        rows_box.draw(screen)
        cols_box.draw(screen)
        pygame.display.flip()

    result_matrix = assign_matrix(screen, rows, cols)
    if result_matrix is not None:
        print("Matrix entered:")
        sympy.pprint(result_matrix)

    pygame.quit()

    return result_matrix


if __name__ == '__main__':
    print(main())
