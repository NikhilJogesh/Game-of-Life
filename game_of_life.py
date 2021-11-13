import pygame
import numpy

pygame.init()
WIN_WIDTH = 640
WIN_HEIGTH = 720
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGTH))
pygame.display.set_caption("Game of Life")
CLOCK = pygame.time.Clock()
FPS = 144

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ROW = 80
COLUMN = 80
LINE_THICKNESS = 1

GAME_STATES = ["Editing", "Simulating"]

FONT_30 = pygame.font.SysFont("Roboto", size=30)
FONT_25 = pygame.font.SysFont("Roboto", size=25)

class Button:
    padding = 10
    outline = 2

    def __init__(self, surface, font, text, colour1, colour2, x=None, y=None):
        self.hovered = False
        self.surface = surface
        self.font = font
        self.colour1 = colour1
        self.colour2 = colour2

        self.text = self.font.render(text, 1, colour1)
        if x == None:
        	self.x = (self.surface.get_width() - self.text.get_width())/2
        else:
        	self.x = x
        if y == None:
        	self.y = (self.surface.get_height() - self.text.get_height())/2
        else:
        	self.y = y
        self.width = self.text.get_width()
        self.height = self.text.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.hovered_text = self.font.render(text, 1 , colour2)
        self.hovered_x = self.x - self.padding/2
        self.hovered_y = self.y - self.padding/2
        self.hovered_width = self.text.get_width() + self.padding
        self.hovered_height = self.text.get_height() + self.padding
        self.hovered_rect = pygame.Rect(self.hovered_x, self.hovered_y, self.hovered_width, self.hovered_height)

    def render(self):
        if self.hovered:
            pygame.draw.rect(self.surface, self.colour1, self.hovered_rect)
            self.surface.blit(self.hovered_text, (self.hovered_x + (self.hovered_width - self.hovered_text.get_width())/2, self.hovered_y + (self.hovered_height - self.hovered_text.get_height())/2 ))
        else:
        	pygame.draw.rect(self.surface, self.colour1, self.hovered_rect)
        	pygame.draw.rect(self.surface, self.colour2, (self.hovered_x + self.outline, self.hovered_y + self.outline, self.hovered_width - self.outline*2, self.hovered_height - self.outline*2))
        	self.surface.blit(self.text, (self.x + (self.width - self.text.get_width())/2, self.y + (self.height - self.text.get_height())/2 ))


def create_grids(start_x, start_y, width, height, columns, rows, line_width):
    grids = []
    cell_width = (width - line_width * (columns-1))/ columns
    cell_height = (height - line_width * (rows-1))/ rows

    x = start_x
    y = start_y
    for _ in range(columns - 1):
        x += cell_width
        grids.append(pygame.Rect(x, y, line_width, height))
        x += line_width

    x = start_x
    y = start_y
    for _ in range(rows - 1):
        y += cell_height
        grids.append(pygame.Rect(x, y, width, line_width))
        y += line_width

    return grids


def create_graphic_cells(cells, start_x, start_y, width, height, gap):
    graphic_cells = []
    y = start_y
    for row in cells:
        graphic_cells_row = []
        #print(start_x)
        x = start_x
        for _ in row:
            #print(x)
            graphic_cells_row.append(pygame.Rect(x, y, width, height))
            x += gap + width
            
        graphic_cells.append(graphic_cells_row)
        y += gap + height

    return graphic_cells

def cell_size(target, number):
    for i in range(number): 
        if (target + i) % number == 0:
            return target + i
        elif (target - i) % number == 0:
            return target - i

print(f"Answer: {cell_size(798, 80)}")

GRID_X = 0
GRID_Y = WIN_HEIGTH - WIN_WIDTH
GRID_WIDTH = WIN_WIDTH
GRID_HEIGHT = WIN_HEIGTH - (WIN_HEIGTH - WIN_WIDTH)
grid = create_grids(GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT, COLUMN, ROW, LINE_THICKNESS)
#grid = []

CELLS_START_X = GRID_X
CELLS_START_Y = GRID_Y
CELL_WIDTH =  (WIN_WIDTH - LINE_THICKNESS * (COLUMN - 1))/COLUMN
CELL_HEIGHT = ((WIN_HEIGTH - (WIN_HEIGTH - WIN_WIDTH)) - LINE_THICKNESS * (ROW - 1))/ ROW
cells = numpy.zeros((COLUMN, ROW), dtype=int)
graphic_cells = create_graphic_cells(cells, CELLS_START_X, CELLS_START_Y, CELL_WIDTH, CELL_HEIGHT, LINE_THICKNESS)

def render_editor(win, grid, cells, graphic_cells, buttons):
    win.fill(WHITE)
    for cell in grid:
        pygame.draw.rect(win, BLACK, cell)

    for i, row in enumerate(cells):
        for j, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(win, BLACK, graphic_cells[i][j])
            else:
                pygame.draw.rect(win, WHITE, graphic_cells[i][j])

    pygame.draw.rect(win, BLACK, (0, 0, WIN_WIDTH, WIN_HEIGTH - WIN_WIDTH))
    pygame.draw.rect(win, WHITE, (0, WIN_HEIGTH - WIN_WIDTH - 10, WIN_WIDTH, 10))
    for button in buttons:
        button.render()
    pygame.display.update()

def editor():
    global game_state

    buttons = [
    Button(WIN, FONT_30, "Start", WHITE, BLACK, x=None, y=0.035*WIN_HEIGTH),
    Button(WIN, FONT_25, "Clear", WHITE, BLACK, x=0.8*WIN_WIDTH, y=0.035*WIN_HEIGTH)
    ]
    while game_state == GAME_STATES[0]:
        CLOCK.tick(FPS)
        #print(CLOCK.get_fps())
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pressed()
            if event.type  == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                #print(mouse_pos)
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):
                        button.hovered = True
                    else:
                        button.hovered = False

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = event.pos
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if button is buttons[0]:
                            game_state = GAME_STATES[1]
                        elif button is buttons[1]:
                            cells[:] = numpy.zeros((COLUMN, ROW), dtype=int)

            if mouse[0]:
                mouse_pos = pygame.mouse.get_pos()
                for i, graphic_cell_row in enumerate(graphic_cells):
                    for j, graphic_cell in enumerate(graphic_cell_row):
                        if graphic_cell.collidepoint(mouse_pos):
                            if cells[i][j] == 0: cells[i][j] = 1

            elif mouse[2]:
                mouse_pos = pygame.mouse.get_pos()
                for i, graphic_cell_row in enumerate(graphic_cells):
                    for j, graphic_cell in enumerate(graphic_cell_row):
                        if graphic_cell.collidepoint(mouse_pos):
                            if cells[i][j] == 1: cells[i][j] = 0


        render_editor(WIN, grid, cells, graphic_cells, buttons)

def new_dead(cells):
    dead = []
    for i, row in enumerate(cells):
        if i == 0 or i == len(cells) - 1:
            continue
        for j, cell in enumerate(row):
            if j == 0 or j == len(row) - 1:
                continue
            if cell == 1:
                neighbours = [
                    cells[i-1][j-1], 
                    cells[i-1][j],
                    cells[i-1][j+1],
                    cells[i][j-1],
                    cells[i][j+1],
                    cells[i+1][j-1],
                    cells[i+1][j],
                    cells[i+1][j+1]]
                if neighbours.count(1) > 3:
                    dead.append([i, j])

                elif neighbours.count(1) < 2:
                    dead.append([i, j])

    return dead

def new_born(cells):
    born = []
    for i, row in enumerate(cells):
        if i == 0 or i == len(cells) - 1:
            continue
        for j, cell in enumerate(row):
            if j == 0 or j == len(row) - 1:
                continue
            if cell == 0:
                neighbours = [
                    cells[i-1][j-1], 
                    cells[i-1][j],
                    cells[i-1][j+1],
                    cells[i][j-1],
                    cells[i][j+1],
                    cells[i+1][j-1],
                    cells[i+1][j],
                    cells[i+1][j+1]
                ]
                if neighbours.count(1) == 3:
                    born.append([i, j])

    return born

def remove_cells(cells, dead_cells):
    for dead_cell in dead_cells:
        cells[dead_cell[0]][dead_cell[1]] = 0

def add_cells(cells, new_born_cells):
    for new_born_cell in new_born_cells:
        cells[new_born_cell[0]][new_born_cell[1]] = 1

def render_simulator(win, cells, graphic_cells, buttons):
    win.fill(WHITE)
    for cell in grid:
        pygame.draw.rect(win, BLACK, cell)

    for i, row in enumerate(cells):
        for j, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(win, BLACK, graphic_cells[i][j])
            else:
                pygame.draw.rect(win, WHITE, graphic_cells[i][j])

    pygame.draw.rect(win, BLACK, (0, 0, WIN_WIDTH, WIN_HEIGTH - WIN_WIDTH))
    pygame.draw.rect(win, WHITE, (0, WIN_HEIGTH - WIN_WIDTH - 10, WIN_WIDTH, 10))
    for button in buttons:
        button.render()
    pygame.display.update()

def simulator():
    global game_state

    buttons = [
        Button(WIN, FONT_30, "Stop", WHITE, BLACK, x=None, y=0.035*WIN_HEIGTH)
    ]
    while game_state == GAME_STATES[1]:
        CLOCK.tick(60)
        #print(f"FPS: {int(CLOCK.get_fps())}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                #print(mouse_pos)
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):
                        button.hovered = True
                    else:
                        button.hovered = False

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = event.pos
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):
                        if button is buttons[0]:
                            game_state = GAME_STATES[0]
        
        new_dead_cells = new_dead(cells)
        new_born_cells = new_born(cells)
        remove_cells(cells, new_dead_cells)
        add_cells(cells, new_born_cells)

        render_simulator(WIN, cells, graphic_cells, buttons)

def main():
    global game_state
    game_state = GAME_STATES[0]
    while True:
        if game_state == GAME_STATES[0]:
            editor()
        elif game_state == GAME_STATES[1]:
            simulator()

if __name__ == "__main__":
    main()
