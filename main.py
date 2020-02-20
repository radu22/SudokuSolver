import pygame
import Class as cls
import Settings as stg
import SudokuSolution

done = False
pygame.init()
screen = pygame.display.set_mode((stg.xScreen + 400, stg.yScreen + stg.offset + 40))
screen.fill(stg.backgroundColor)
fonts = pygame.font.get_fonts()
font = pygame.font.SysFont(fonts[12], 32)
# pygame.draw.rect(screen, stg.colors["grey"],
#                  pygame.Rect(10, 10, stg.xScreen + stg.offset * 2 - 20, stg.yScreen + stg.offset * 2 - 20))
pygame.draw.rect(screen, stg.colors["grey"],
                 pygame.Rect(10, 10, stg.xScreen + - 20, stg.yScreen - 20))

# font = pygame.font.SysFont("comicsansms", 32)
# print(fonts)


sudoku = [[6, 8, 5, 0, 3, 0, 4, 0, 7],
          [0, 0, 0, 8, 0, 0, 0, 2, 0],
          [0, 1, 0, 4, 0, 0, 5, 0, 0],
          [0, 9, 0, 3, 0, 0, 0, 0, 5],
          [0, 4, 0, 0, 0, 0, 6, 0, 0],
          [5, 0, 8, 0, 0, 4, 0, 3, 0],
          [9, 2, 6, 0, 7, 8, 3, 0, 0],
          [8, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 3, 0, 0, 0, 0, 1, 9]]


# def button(status):
#     if status == "nothing":
#         pygame.draw.rect(screen, stg.colors["button-green"],
#                          pygame.Rect(stg.xScreen + 150, stg.yScreen - 100, 150, 50))
#         text = font.render("Click me!", True, (0, 0, 0))
#         screen.blit(text,
#                     (stg.xScreen + 150 + text.get_height() // 2, stg.yScreen - 100 + text.get_width() // 2))
#
#     elif status == "hover":
#         pygame.draw.rect(screen, stg.colors["button-hover-green"],
#                          pygame.Rect(stg.xScreen + 150, stg.yScreen - 100, 150, 50)),
#     elif status == "clicked":
#         pygame.draw.rect(screen, stg.colors["grey"],
#                          pygame.Rect(stg.xScreen + 150, stg.yScreen - 100, 150, 50)),


def create_cells(cell_list):
    for i in range(9):
        a = []
        for j in range(9):
            a.append(cls.Cell(60 * j + stg.offset, 60 * i + stg.offset, sudoku[i][j], (i // 3 + j // 3) + (i // 3) * 2))
        cell_list.append(a)


def draw_border():
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
        pygame.draw.rect(screen, cell.border_color, pygame.Rect(x, y, w, h), stg.border)
        text = font.render(str(locked_value), True, (0, 0, 0))
        screen.blit(text,
                    (x + text.get_height() // 2, y + text.get_width() // 2))
    else:
        if value != 0:

            pygame.draw.rect(screen, cell.cell_color, pygame.Rect(x, y, w, h))
            pygame.draw.rect(screen, cell.border_color, pygame.Rect(x, y, w, h), stg.border)
            text = font.render(str(value), True, cell.get_value_color())
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


def write_value(cell, value, status):
    x, y = cell.get_xy()
    # cell.change_value(value)
    if status:
        text = font.render(str(value), True, cell.get_value_color())
        screen.blit(text,
                    (x + text.get_height() // 2, y + text.get_width() // 2))
    else:
        text = font.render(str(value), True, cell.get_value_color())
        screen.blit(text,
                    (x + text.get_height() // 2, y + text.get_width() // 2))


def mark_clicked(cell):
    x, y = cell.get_xy()
    print(x, y)
    # if cell.family_focus or cell.get_color() == stg.colors["family"]:
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
    mark_clicked(cell)
    draw_table(cells)
    pygame.display.flip()
    input_status = False
    if not solved:
        if cell.get_locked_value() == 0:
            cell.change_focus_state()
            while cell.focus:
                # cell.change_state()
                for ev in pygame.event.get():
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        pos_x, pos_y = pygame.mouse.get_pos()
                        print(pos_x,pos_y)
                        if stg.offset < pos_x < stg.xScreen + stg.offset and stg.offset < pos_y < stg.yScreen + stg.offset:
                            cell.change_focus_state()
                            clicked(cells[pos_y // (cls.Cell.width + stg.offset)][pos_x // (cls.Cell.height + stg.offset)], solved_status)
                        else:
                            reset_colors(cells)
                            draw_table(cells)
                            pygame.display.flip()
                            cell.change_focus_state()
                            return None

                    if ev.type == pygame.KEYDOWN:
                        number = numbers(ev.key)
                        if number == "#":
                            number = "0"
                        if input_validation(cell, int(number)):
                            input_status = True
                        else:
                            input_status = False
                        cell.change_value(int(number))
                        cell.change_value_color(input_status)
                        # cell.change_locked_value(int(number))
                        # write_value(cell, cell.get_value(), input_status)
                        mark_clicked(cell)
                        draw_table(cells)
                        pygame.display.flip()

                # cell.change_state()


# def clicked(cell, solved):
#     mark_clicked(cell)
#     draw_table(cells)
#     pygame.display.flip()
#     input_status = False
#     if not solved:
#         if cell.get_locked_value() == 0:
#             cell.change_state()
#             while not cell.state:
#                 # cell.change_state()
#                 for ev in pygame.event.get():
#                     if ev.type == pygame.MOUSEBUTTONDOWN:
#                         pos_x, pos_y = pygame.mouse.get_pos()
#                         if 10 < pos_x < stg.xScreen and 10 < pos_y < stg.yScreen:
#                             clicked(cells[pos_y // cls.Cell.width][pos_x // cls.Cell.height], solved_status)
#
#                     if ev.type == pygame.KEYDOWN:
#                         number = numbers(ev.key)
#                         if number == "#":
#                             number = "0"
#                         if input_validation(cell, int(number)):
#                             input_status = True
#                         else:
#                             input_status = False
#                         cell.change_value(int(number))
#                         cell.change_value_color(input_status)
#                         # cell.change_locked_value(int(number))
#                         write_value(cell, cell.get_value(), input_status)
#                         cell.change_state()


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
            cells[i][j].default()


def redraw(cells):
    for i in range(9):
        for j in range(9):
            cells[i][j].change_value(cells[i][j].get_locked_value())
    draw_table(cells)
    pygame.display.flip()


def input_validation(cell, value):
    """
        This function makes sure that the game rules are not broken.
        Checks if a possible value already exists in the current col or row
        Also checks if the possible value already exists in the curent block
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

    blockFirstRow = 3 * int(row / 3)
    blockFirstCol = 3 * int(col / 3)

    for i in range(3):
        for j in range(3):
            if (blockFirstRow + i != row) or (
                    blockFirstCol + j != col):  # searches the current box to find if the values is already there
                if cells[blockFirstRow + i][blockFirstCol + j].get_value() == value:
                    return False

    return True


def display_text():
    text_container = cls.Button(stg.colors["grey"], stg.xScreen + 100, 40, 270, 300, "")
    text_container.draw(screen, 1)

    title_font = pygame.font.SysFont("comicsansms", 26)
    title_text = title_font.render("Welcome to Sudoku!", True, (0, 0, 0))
    screen.blit(title_text,
                ((stg.xScreen + 100) + (270 / 2 - title_text.get_width() / 2),
                 40 + (60 / 2 - title_text.get_height() / 2)))

    desc_font = pygame.font.SysFont("comicsansms", 22)
    desc_text = desc_font.render("red means bad", True, (0, 0, 0))
    screen.blit(desc_text,
                ((stg.xScreen + 100) + 10,
                 40 + (200 / 2 - desc_text.get_height() / 2)))

    desc_text2 = desc_font.render("blue means good", True, (0, 0, 0))
    screen.blit(desc_text2,
                ((stg.xScreen + 100) + 10,
                 40 + (280 / 2 - desc_text2.get_height() / 2)))

    desc_text3 = desc_font.render("Pls don't break it", True, (0, 0, 0))
    screen.blit(desc_text3,
                ((stg.xScreen + 100) + 10,
                 40 + (500 / 2 - desc_text3.get_height() / 2)))


if __name__ == "__main__":
    cells = []
    create_cells(cells)
    draw_table(cells)
    button = cls.Button(stg.colors["button-green"], stg.xScreen + 150, stg.yScreen - 100, 170, 50, "Magic!")
    button.draw(screen, 1)
    display_text()
    solved_status = False
    while not done:
        x_mouse, y_mouse = pygame.mouse.get_pos()
        if button.is_over((x_mouse, y_mouse)):
            button.change_color(stg.colors["button-hover-green"])
            button.draw(screen)
        else:
            button.change_color(stg.colors["button-green"])
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONUP:
                pos_x, pos_y = pygame.mouse.get_pos()
                if stg.offset < pos_x < stg.xScreen + stg.offset and stg.offset < pos_y < stg.yScreen + stg.offset:
                    clicked(cells[pos_y // (cls.Cell.width + stg.offset)][pos_x // (cls.Cell.height + stg.offset)], solved_status)
                else:
                    reset_colors(cells)
                    pygame.display.flip()

                if button.is_over((pos_x, pos_y)):
                    button.change_text("Hackerman")
                    button.draw(screen, 1)
                    redraw(cells)
                    SudokuSolution.SudokuSolver(cells, 0)
                    solved_status = True

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SLASH:
            #         redraw(cells)
            #         SudokuSolution.SudokuSolver(cells, 0)
            #         solved_status = True

        draw_table(cells)
        pygame.display.flip()
        stg.clock.tick(120)
