import pygame
import sys
from sympy import Matrix, symbols

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_TOP_MARGIN = 50
GRID_LEFT_MARGIN = 200
CELL_SIZE = 50
FONT_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_COLOR = (200, 200, 200)


# # Function to create grid
# def create_grid(rows, cols):
#     grid = []
#     for i in range(rows):
#         row = []
#         for j in range(cols):
#             row.append(0)
#         grid.append(row)
#     return grid

def create_grid(rows, cols):
    symbols_list = symbols(','.join(['x{}_{}'.format(i, j) for i in range(rows) for j in range(cols)]))
    grid = Matrix(rows, cols, symbols_list)
    return grid


# Function to draw grid
def draw_grid(screen, grid):
    # Draw outer box
    lines = [0, len(grid), len(grid)+1]
    for i in lines:
        # Horizontal
        pygame.draw.line(screen, BLACK, (GRID_LEFT_MARGIN, GRID_TOP_MARGIN + i * CELL_SIZE),
                         (GRID_LEFT_MARGIN + (grid.shape[1] + 1) * CELL_SIZE, GRID_TOP_MARGIN + i * CELL_SIZE), 2)
        # Vertical
        pygame.draw.line(screen, BLACK, (GRID_LEFT_MARGIN + i * CELL_SIZE, GRID_TOP_MARGIN),
                         (GRID_LEFT_MARGIN + i * CELL_SIZE, GRID_TOP_MARGIN + (grid.shape[0] + 1)* CELL_SIZE), 2)

    # Draw numbers in cells
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            font = pygame.font.SysFont(None, FONT_SIZE)
            text = font.render(str(cell), True, BLACK)
            screen.blit(text, (
            GRID_LEFT_MARGIN + j * CELL_SIZE + CELL_SIZE // 4, GRID_TOP_MARGIN + i * CELL_SIZE + CELL_SIZE // 4))


# Function to detect click and return grid index
def detect_click(pos):
    x, y = pos
    grid_x = (x - GRID_LEFT_MARGIN) // CELL_SIZE
    grid_y = (y - GRID_TOP_MARGIN) // CELL_SIZE
    return grid_y, grid_x


# Function to create text input box
class TextInputBox:
    def __init__(self, screen, x, y, width, height, font, prompt=''):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.prompt = prompt
        self.text = ''
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def update(self):
        text_surface = self.font.render(self.text, True, BLACK)
        width = max(200, text_surface.get_width() + 10)
        self.rect.w = width

    def draw(self):
        pygame.draw.rect(self.screen, WHITE, self.rect, 2)
        self.screen.blit(self.font.render(self.prompt + self.text, True, BLACK), (self.rect.x + 5, self.rect.y + 5))


# Function to change the value of a cell
def change_cell_value(grid, row, col, new_value):
    grid[row][col] = new_value


# Main function
def main():
    # Initialize screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Grid Input")

    # Variables
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))
    grid = create_grid(rows, cols)
    font = pygame.font.SysFont(None, FONT_SIZE)

    # Text input box for new cell value
    input_box = TextInputBox(screen, GRID_LEFT_MARGIN, SCREEN_HEIGHT - 50, 200, 30, font, 'New Value: ')

    # Main loop
    while True:
        screen.fill(GRID_COLOR)
        draw_grid(screen, grid)

        # Draw input box
        input_box.update()
        input_box.draw()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    clicked_pos = pygame.mouse.get_pos()
                    grid_y, grid_x = detect_click(clicked_pos)
                    print("Clicked on cell:", grid_y, grid_x)
                    input_box.active = True
            input_box.handle_event(event)

        # Update the value of the clicked cell
        if not input_box.active and input_box.text.strip():
            try:
                new_value = int(input_box.text)
                change_cell_value(grid, grid_y, grid_x, new_value)
            except ValueError or IndexError:
                print("Error encountered, check input")
            input_box.text = ''

        pygame.display.update()


if __name__ == "__main__":
    main()
