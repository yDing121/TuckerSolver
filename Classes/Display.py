import pygame
import sys
from Classes import TableauGetter
from Classes import Solver


class MatrixDisplay:
    def __init__(self, solver: Solver, cell_size=80, margin=5, bg_color=(255, 255, 255), text_color=(0, 0, 0)):
        """ Initialize the matrix display parameters. """
        self.solver = solver
        self.matrix = solver.arr.copy()
        self.rows, self.cols = self.matrix.shape
        self.cell_size = cell_size
        self.margin = margin
        self.bg_color = bg_color
        self.text_color = text_color
        self.start_x = cell_size * 1.5
        self.start_y = cell_size * 1.5

        # self.solver.create_from_sympy(self.matrix)

        # Set up Pygame display
        pygame.init()
        self.font = pygame.font.Font(None, 36)
        width = self.start_x + self.cols * (cell_size + margin) + self.start_x + 4 * cell_size
        height = max(self.start_y + self.rows * (cell_size + margin) + self.start_y, 6 * cell_size)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Matrix Display")

        # Update the entire display
        self.draw_matrix()

    def draw_matrix(self, highlight_row=-1, highlight_col=-1):
        """ Draw the entire matrix on the screen. """
        self.screen.fill(self.bg_color)
        for row in range(self.rows):
            for col in range(self.cols):
                value = str(self.matrix[row, col])

                rect = pygame.Rect(
                    self.start_x + col * (self.cell_size + self.margin) + self.margin,
                    self.start_y + row * (self.cell_size + self.margin) + self.margin,
                    self.cell_size,
                    self.cell_size
                )

                # Highlight cell green
                if col == highlight_col and row == highlight_row:
                    pygame.draw.rect(self.screen, (119, 237, 140), rect)
                else:
                    pygame.draw.rect(self.screen, (200, 200, 200), rect)

                text_surface = self.font.render(value, True, self.text_color)
                text_rect = text_surface.get_rect(center=rect.center)
                self.screen.blit(text_surface, text_rect)

        # Bounding box
        vline_cell_cols = [0, self.cols - 1, self.cols]
        hline_cell_rows = [0, self.rows - 1, self.rows]

        for xloc in vline_cell_cols:
            xcoord = self.start_x + xloc * (self.cell_size + self.margin) + self.margin//2
            pygame.draw.line(self.screen,
                             (0, 0, 0),
                             (xcoord, self.start_y),
                             (xcoord, self.start_y + self.rows * (self.cell_size + self.margin) + self.margin),
                             width=4)

        for yloc in hline_cell_rows:
            ycoord = self.start_y + yloc * (self.cell_size + self.margin) + self.margin//2
            pygame.draw.line(self.screen,
                             (0, 0, 0),
                             (self.start_x, ycoord),
                             (self.start_x + self.cols * (self.cell_size + self.margin) + self.margin, ycoord),
                             width=4)

        # Pivot box
        rect = pygame.Rect(self.start_x + (self.cols - 1 + 3) * (self.cell_size + self.margin),
                           self.start_y + self.margin,
                           self.cell_size * 2,
                           self.cell_size)
        pygame.draw.rect(self.screen, (121, 163, 232), rect)
        text_surface = self.font.render("Pivot", True, self.text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

        # Delete row
        rect = pygame.Rect(self.start_x + (self.cols - 1 + 3) * (self.cell_size + self.margin),
                           self.start_y + (1) * (self.cell_size + self.margin) + self.margin,
                           self.cell_size * 2,
                           self.cell_size)
        pygame.draw.rect(self.screen, (232, 121, 225), rect)
        text_surface = self.font.render("Del Row", True, self.text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

        # Delete column
        rect = pygame.Rect(self.start_x + (self.cols - 1 + 3) * (self.cell_size + self.margin),
                           self.start_y + (2) * (self.cell_size + self.margin) + self.margin,
                           self.cell_size * 2,
                           self.cell_size)
        pygame.draw.rect(self.screen, (232, 121, 225), rect)
        text_surface = self.font.render("Del Col", True, self.text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def run(self):
        """ Main event loop. """
        running = True
        coord = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if coord:
                        print(f"=={coord}==")
                        ret = self.handle_click(event.pos, coord[0], coord[1])
                    else:
                        ret = self.handle_click(event.pos)

                    if ret is not None:
                        coord = ret
                        print(f"New coordinates:\t{coord}\t detected.")
            pygame.display.update()

        pygame.quit()
        sys.exit()

    def handle_click(self, position, lastcell_row=None, lastcell_col=None):
        """ Handle cell click to toggle the value. """
        x, y = position
        col = int((x - self.start_x) // (self.cell_size + self.margin))
        row = int((y - self.start_y) // (self.cell_size + self.margin))
        print(f"({row}, {col})")

        if self.cols + 2 <= col <= self.cols + 3:
            if row == 0:
                print("pivot")
                del self.solver
                self.solver = Solver.Solver()
                self.solver.create_from_sympy(self.matrix)
                self.solver.pivot(lastcell_row, lastcell_col)
                self.matrix = self.solver.arr.copy()
                self.draw_matrix()

                # print(self.solver.pivot(lastcell_row, lastcell_col))
                # self.matrix = self.solver.pivot2(lastcell_row, lastcell_col)
                print(self.matrix)
            elif row == 1:
                print("del row")
            elif row == 2:
                print("del col")
            else:
                print("what")
            # self.matrix = self.solver.arr
            self.draw_matrix()
            return None

        if 0 <= col < self.cols and 0 <= row < self.rows:
            # # Check if the click is within bounds
            # # Example operation: toggling between 0 and 1 for demonstration
            # new_value = 1 if self.matrix[row, col] == 0 else 0
            # self.matrix[row, col] = new_value
            self.draw_matrix(row, col)
            return tuple((row, col))


# Example usage
if __name__ == "__main__":
    # # Create a 4x4 symbolic matrix
    # example_matrix = sympy.Matrix([[1/2, 0, 0, 0],
    #                                [0, 0, 0, 0],
    #                                [0, 0, 1, 0],
    #                                [0, 0, 0, 0]])
    # app = MatrixDisplay(example_matrix)

    # fraction_matrix = sympy.Matrix([
    #     [sympy.Rational(1, 3), sympy.Rational(2, 3)],
    #     [sympy.Rational(1, 4), sympy.Rational(3, 4)],
    #     [sympy.Rational(1, 5), sympy.Rational(2, 5)]
    # ])
    # app = MatrixDisplay(fraction_matrix)

    solver = Solver.Solver(-1, -1)
    solver.create_from_sympy(TableauGetter.main().copy())

    app = MatrixDisplay(solver, cell_size=70)  # Larger cell size to accommodate fraction strings

    app.run()
