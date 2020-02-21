import pygame
import Class as cls
import Settings as stg
import SudokuSolution
import inputs as inp
from random import choice, randrange

done = False
pygame.init()
screen = pygame.display.set_mode(
    (stg.xScreen + 400, stg.yScreen + stg.offset + 40))  # xScreen & yScreen represent the Sudoku playable area
screen.fill(stg.backgroundColor)
fonts = pygame.font.get_fonts()  # get all available the fonts
font = pygame.font.SysFont(fonts[12], 32)
pygame.draw.rect(screen, stg.colors["grey"],
                 pygame.Rect(stg.offset / 2, stg.offset / 2, stg.xScreen + stg.offset,
                             stg.yScreen + stg.offset))  # Draws the rectangle behind the playable area


# font = pygame.font.SysFont("comicsansms", 32)
# print(fonts)


def create_cells(cell_list, sudoku):
    """ The cell_list is a list of objects of class Cell
        sudoku param is a list of all available games in inputs.py file
        :return sudoku game chose
    """
    k = randrange(len(sudoku))
    for i in range(9):
        a = []
        for j in range(9):
            a.append(
                cls.Cell(60 * j + stg.offset, 60 * i + stg.offset, sudoku[k][i][j], (i // 3 + j // 3) + (i // 3) * 2))
        cell_list.append(a)
    return k

def new_sudoku(cells, sudoku):
    """Changes the current sudoku game"""
    for i in range(9):
        for j in range(9):
            cells[i][j].default()

    for i in range(9):
        for j in range(9):
            cells[i][j].change_locked_value(sudoku[i][j])


def draw_border():
    """Draws all the grids between cells and the outer borders"""
    for i in range(4):
        pygame.draw.line(screen, stg.colors["black"], (stg.offset + i * stg.xBlock, stg.offset),
                         (stg.offset + i * stg.xBlock, stg.yScreen + stg.offset),
                         stg.border + 1)
        pygame.draw.line(screen, stg.colors["black"], (stg.offset, i * stg.xBlock + stg.offset),
                         (stg.xScreen + stg.offset, i * stg.xBlock + stg.offset),
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
        pygame.draw.rect(screen, cell.border_color, pygame.Rect(x, y, w, h),
                         stg.border)  # Draws the cells with locked values
        text = font.render(str(locked_value), True, (0, 0, 0))
        screen.blit(text,
                    (x + text.get_height() // 2, y + text.get_width() // 2))
    else:
        if value != 0:

            pygame.draw.rect(screen, cell.cell_color, pygame.Rect(x, y, w, h))
            pygame.draw.rect(screen, cell.border_color, pygame.Rect(x, y, w, h),
                             stg.border)  # Draws the cells which have a user given value
            text = font.render(str(value), True, cell.get_value_color())
            screen.blit(text,
                        (x + text.get_height() // 2, y + text.get_width() // 2))
        else:
            pygame.draw.rect(screen, cell.cell_color, pygame.Rect(x, y, w, h))
            pygame.draw.rect(screen, cell.border_color, pygame.Rect(x, y, w, h), stg.border)  # Draws the empty cells


def draw_table(cell_list):
    for i in range(9):
        for j in range(9):
            draw_cell(cell_list[i][j])
    draw_border()


def write_value(cell, value, status):
    x, y = cell.get_xy()
    if status:
        text = font.render(str(value), True, cell.get_value_color())
        screen.blit(text,
                    (x + text.get_height() // 2, y + text.get_width() // 2))
    else:
        text = font.render(str(value), True, cell.get_value_color())
        screen.blit(text,
                    (x + text.get_height() // 2, y + text.get_width() // 2))


def mark_clicked(cell):
    """ Marks the clicked cell and the family cells

        family cells == cells that are from the same row/col or
                         cells that are from the same block or
                         cells that have the same value
    """
    x, y = cell.get_xy()
    for i in range(9):
        for j in range(9):
            cells[i][j].change_state_false()
            x1, y1 = cells[i][j].get_xy()
            if x1 == x or y1 == y or cells[i][j].get_block() == cell.get_block() or (
                    cells[i][j].get_value() == cell.get_value() and cell.get_value() != 0):
                cells[i][j].change_color(stg.colors["family"])
                cells[i][j].change_state_true()

    cell.change_color(stg.colors["selected"])


def clicked(cell, solved):
    """
    Tracks the clicked cells.
    Useful for many cells selected without any input given.
    Keeps the selected and clicked items functionality going
    :parameter solved makes sure that no input can be given if the sudoku is solved
    """
    mark_clicked(cell)
    draw_table(cells)
    pygame.display.flip()
    input_status = False
    if not solved:
        if cell.get_locked_value() == 0:
            cell.change_focus_state()
            while cell.focus:
                for ev in pygame.event.get():
                    if event.type == pygame.QUIT:  # Red X button
                        done = True
                        quit()
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        pos_x, pos_y = pygame.mouse.get_pos()
                        if stg.offset < pos_x < stg.xScreen + stg.offset and stg.offset < pos_y < stg.yScreen + stg.offset:  # if the click is in the playable area
                            cell.change_focus_state()
                            clicked(
                                cells[(pos_y - stg.offset) // cls.Cell.width][(pos_x - stg.offset) // cls.Cell.height],
                                solved_status)
                        else:
                            reset_colors(cells)  # deselect everything
                            draw_table(cells)
                            pygame.display.flip()
                            cell.change_focus_state()
                            return None

                    if ev.type == pygame.KEYDOWN:
                        number = numbers(ev.key)  # Gives only the 1....9 numbers, any other input is replaced with 0
                        if number == "#":
                            number = "0"
                        if input_validation(cell, int(number)):  # Validates or invalidates the input given
                            input_status = True
                        else:
                            input_status = False
                        cell.change_value(int(number))
                        cell.change_value_color(input_status)  # red or blue color for the input
                        mark_clicked(cell)

                    draw_table(cells)
                    pygame.display.flip()


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


def reset_colors(cells):
    for i in range(9):
        for j in range(9):
            cells[i][j].deselect()


def redraw(cells):
    """ Redraw the table to default colors and without any input"""
    for i in range(9):
        for j in range(9):
            cells[i][j].set_default_colors()
            cells[i][j].change_value(cells[i][j].get_locked_value())
    draw_table(cells)
    pygame.display.flip()


def input_validation(cell, value):
    """
        This function makes sure that the game rules are not broken.
        Checks if a possible value already exists in the current col or row
        Also checks if the possible value already exists in the current block
    """
    x, y = cell.get_xy()
    row = int(y / 60)
    col = int(x / 60)

    for i in range(9):
        if i != col:
            if cells[row][i].get_value() == value:  # searches the current row to find if the values is already there
                return False
        if i != row:
            if cells[i][col].get_value() == value:  # searches the current col to find if the values is already there
                return False

    block_first_row = 3 * int(row / 3)
    block_first_col = 3 * int(col / 3)

    for i in range(3):
        for j in range(3):
            if (block_first_row + i != row) or (
                    block_first_col + j != col):  # searches the current box to find if the values is already there
                if cells[block_first_row + i][block_first_col + j].get_value() == value:
                    return False

    return True


def display_text():
    """ Displays all the text in the window """
    text_container = cls.Button(stg.colors["grey"], stg.xScreen + 100, 40, 270, 300, "")
    text_container.draw(screen, 1)

    title_font = pygame.font.SysFont("comicsansms", 26)
    title_text = title_font.render("Welcome to Sudoku!", True, (0, 0, 0))
    screen.blit(title_text,
                ((stg.xScreen + 100) + (270 / 2 - title_text.get_width() / 2),
                 40 + (60 / 2 - title_text.get_height() / 2)))

    desc_font = pygame.font.SysFont("comicsansms", 22)
    desc_text = desc_font.render("red means bad", True, stg.colors["red2"])
    screen.blit(desc_text,
                ((stg.xScreen + 100) + 10,
                 40 + (200 / 2 - desc_text.get_height() / 2)))

    desc_text2 = desc_font.render("blue means good", True, stg.colors["blue2"])
    screen.blit(desc_text2,
                ((stg.xScreen + 100) + 10,
                 40 + (280 / 2 - desc_text2.get_height() / 2)))

    desc_text3 = desc_font.render("Pls don't break it", True, (0, 0, 0))
    screen.blit(desc_text3,
                ((stg.xScreen + 100) + 10,
                 40 + (500 / 2 - desc_text3.get_height() / 2)))


if __name__ == "__main__":
    cells = []
    current_sudoku = create_cells(cells, inp.sudoku)
    draw_table(cells)
    button = cls.Button(stg.colors["button-green"], stg.xScreen + 150, stg.yScreen - 100, 170, 50, "Magic!")
    new_game = cls.Button(stg.colors["white"], stg.xScreen + 175, stg.yScreen - 30, 120, 30, "New Game",
                          stg.colors["button-blue"], 30)
    button.draw(screen, 1)
    new_game.draw(screen)
    display_text()
    solved_status = False
    while not done:     # Somehow infinite loop to keep the make the game playable
        x_mouse, y_mouse = pygame.mouse.get_pos()

        # ###################### hover over buttons ##########################
        if button.is_over((x_mouse, y_mouse)):
            button.change_color(stg.colors["button-hover-green"])
            button.draw(screen)
        else:
            button.change_color(stg.colors["button-green"])
            button.draw(screen)
        if new_game.is_over((x_mouse, y_mouse)):
            new_game.change_text_color(stg.colors["button-hover-blue"])
            new_game.draw(screen)
        else:
            new_game.change_text_color(stg.colors["button-blue"])
            new_game.draw(screen)

        # ##################### getting all the events and answering them ############################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # close the window
                done = True
                quit()
            if event.type == pygame.MOUSEBUTTONUP:  # mouse click
                pos_x, pos_y = pygame.mouse.get_pos()
                if stg.offset < pos_x < stg.xScreen + stg.offset and stg.offset < pos_y < stg.yScreen + stg.offset:  # mouse click over a cell
                    clicked(cells[(pos_y - stg.offset) // cls.Cell.width][(pos_x - stg.offset) // cls.Cell.height],
                            solved_status)
                else:                                   # mouse click over blank area
                    reset_colors(cells)
                    pygame.display.flip()

                if button.is_over((pos_x, pos_y)):     # mouse click over "Magic!" button
                    button.change_text("Stop")
                    button.draw(screen, 1)
                    redraw(cells)
                    solved_status = SudokuSolution.SudokuSolver(cells, 0, button)  # Solve the Sudoku
                if new_game.is_over((pos_x, pos_y)):  # mouse click over "New Game" button
                    x = choice(inp.sudoku)
                    while x == current_sudoku:   # get a random sudoku from sudoku list
                        x = choice(inp.sudoku)
                    new_sudoku(cells, x)
                    current_sudoku = x
                    draw_table(cells)

        draw_table(cells)
        pygame.display.flip()
        stg.clock.tick(120)   # FPS
