import pygame
import Class as cls
import Settings as stg
import SudokuSolution

done = False
pygame.init()
screen = pygame.display.set_mode((stg.xScreen+400, stg.yScreen+10))
screen.fill(stg.backgroundColor)
fonts = pygame.font.get_fonts()
font = pygame.font.SysFont(fonts[12], 32)
# font = pygame.font.SysFont("comicsansms", 32)
# print(fonts)


sudoku = [[0, 7, 3, 0, 0, 0, 8, 0, 0],
          [0, 0, 0, 7, 0, 0, 0, 4, 0],
          [0, 5, 0, 4, 0, 9, 0, 0, 6],
          [0, 0, 5, 0, 0, 2, 0, 0, 9],
          [7, 0, 0, 9, 0, 0, 1, 0, 0],
          [2, 1, 0, 0, 0, 0, 5, 0, 8],
          [0, 0, 0, 2, 0, 7, 0, 1, 3],
          [3, 0, 0, 0, 9, 5, 6, 8, 0],
          [0, 0, 7, 8, 0, 0, 0, 0, 0]]


def create_cells(cell_list):
    for i in range(9):
        a = []
        for j in range(9):
            a.append(cls.Cell(stg.offset + 60 * j, stg.offset + 60 * i, sudoku[i][j], (i // 3 + j // 3) + (i // 3) * 2))
        cell_list.append(a)


def draw_border():
    for i in range(4):
        pygame.draw.line(screen, stg.colors["black"], (i * stg.xBlock, 0), (i * stg.xBlock, stg.yScreen),
                         stg.border + 1)
        pygame.draw.line(screen, stg.colors["black"], (0, i * stg.xBlock + stg.offset), (stg.xScreen, i * stg.xBlock),
                         stg.border + 1)


def draw_cell(cell):
    x, y = cell.get_xy()
    w, h = cell.get_wh()
    locked_value = cell.get_locked_value()
    value = cell.get_value()

    x_mouse, y_mouse = pygame.mouse.get_pos()
    if not cell.state:
        if (x < x_mouse < x + 60) and (y < y_mouse < y + 60):
            cell.change_color(stg.colors["blue"])
        else:
            cell.change_color(stg.colors["white"])

    if locked_value != 0:
        pygame.draw.rect(screen, cell.cell_color, pygame.Rect(x, y, w, h))
        pygame.draw.rect(screen, cell.border_color, pygame.Rect(x, y, w, h), stg.border)
        text = font.render(str(locked_value), True, (0, 0, 0))
        screen.blit(text,
                    (x + text.get_height() // 2, y + text.get_width() // 2))
    else:
        if value != 0:

            pygame.draw.rect(screen, cell.cell_color, pygame.Rect(x, y, w, h))
            pygame.draw.rect(screen, cell.border_color, pygame.Rect(x, y, w, h), stg.border)
            text = font.render(str(value), True, (0, 0, 0))
            screen.blit(text,
                        (x + text.get_height() // 2, y + text.get_width() // 2))
        else:
            pygame.draw.rect(screen, cell.cell_color, pygame.Rect(x, y, w, h))
            pygame.draw.rect(screen, cell.border_color, pygame.Rect(x, y, w, h), stg.border)


def draw_table(cell_list):
    for i in range(9):
        for j in range(9):
            draw_cell(cell_list[i][j])
    draw_border()

def write_value(cell, value):
    x, y = cell.get_xy()
    cell.change_value(value)
    text = font.render(str(value), True, (0, 0, 0))
    screen.blit(text,
                (x + text.get_height() // 2, y + text.get_width() // 2))


def clicked(cell, solved):
    x, y = cell.get_xy()

    if not cell.state or cell.get_color() == stg.colors["clicked"]:
        for i in range(9):
            for j in range(9):
                cells[i][j].change_state_false()
                x1, y1 = cells[i][j].get_xy()
                if x1 == x or y1 == y or cells[i][j].get_block() == cell.get_block() or (
                        cells[i][j].get_value() == cell.get_value() and cell.get_value() != 0):
                    cells[i][j].change_color(stg.colors["clicked"])
                    cells[i][j].change_state()

        cell.change_color(stg.colors["selected"])
    draw_table(cells)
    pygame.display.flip()
    if not solved:
        if cell.get_locked_value() == 0:
            cell.change_state()
            while not cell.state:
                for ev in pygame.event.get():
                    if ev.type == pygame.KEYDOWN:
                        number = numbers(ev.key)
                        if number == "#":
                            number = "0"
                        cell.change_value(int(number))
                        # cell.change_locked_value(int(number))
                        write_value(cell, cell.get_value())
                        cell.change_state()


def numbers(argument):
    switcher = {
        pygame.K_1: "1",
        pygame.K_2: "2",
        pygame.K_3: "3",
        pygame.K_4: "4",
        pygame.K_5: "5",
        pygame.K_6: "6",
        pygame.K_7: "7",
        pygame.K_8: "8",
        pygame.K_9: "9",
    }
    return switcher.get(argument, "#")


def redraw(cells):
    for i in range(9):
        for j in range(9):
            cells[i][j].change_value(cells[i][j].get_locked_value())
    draw_table(cells)
    pygame.display.flip()


if __name__ == "__main__":
    cells = []
    create_cells(cells)
    draw_table(cells)
    solved_status = False
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONUP:
                pos_x, pos_y = pygame.mouse.get_pos()
                clicked(cells[pos_y // cls.Cell.width][pos_x // cls.Cell.height], solved_status)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SLASH:
                    redraw(cells)
                    SudokuSolution.SudokuSolver(cells)
                    solved_status = True

        draw_table(cells)
        pygame.display.flip()
        stg.clock.tick(120)
