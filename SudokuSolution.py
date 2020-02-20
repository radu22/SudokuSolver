import main
import Class
import pygame
import Settings as stg


def draw(cell):
    x, y = cell.get_xy()
    w, h = cell.get_wh()
    value = cell.get_value()
    pygame.draw.rect(main.screen, cell.cell_color, pygame.Rect(x, y, w, h))
    pygame.draw.rect(main.screen, cell.border_color, pygame.Rect(x, y, w, h), stg.border)
    if value != 0:
        text = main.font.render(str(value), True, (0, 0, 0))
        main.screen.blit(text,
                         (x + text.get_height() // 2, y + text.get_width() // 2))


def draw_table(table):
    for i in range(9):
        for j in range(9):
            draw(table[i][j])

    main.draw_border()
    pygame.display.flip()
    pygame.time.wait(5)


def mark_invalid(cell):
    x, y = cell.get_xy()
    w, h = cell.get_wh()
    value = cell.get_value()
    for v in range(value, 9):
        pygame.draw.rect(main.screen, stg.colors["red"], pygame.Rect(x, y, w, h))
        pygame.draw.rect(main.screen, cell.border_color, pygame.Rect(x, y, w, h), stg.border)
        text = main.font.render(str(v), True, (0, 0, 0))
        main.screen.blit(text,
                         (x + text.get_height() // 2, y + text.get_width() // 2))

        main.draw_border()
        pygame.display.flip()
        pygame.time.wait(30)

    pygame.time.wait(100
                     )
def mark_valid(cell):
    x, y = cell.get_xy()
    w, h = cell.get_wh()
    value = cell.get_value()
    for v in range(value - 1):
        pygame.draw.rect(main.screen, stg.colors["white"], pygame.Rect(x, y, w, h))
        pygame.draw.rect(main.screen, cell.border_color, pygame.Rect(x, y, w, h), stg.border)
        text = main.font.render(str(v), True, (0, 0, 0))
        main.screen.blit(text,
                         (x + text.get_height() // 2, y + text.get_width() // 2))
        main.draw_border()
        pygame.display.flip()

        pygame.time.wait(30)
    for _ in range(2):
        pygame.draw.rect(main.screen, cell.cell_color, pygame.Rect(x, y, w, h))
        pygame.draw.rect(main.screen, cell.border_color, pygame.Rect(x, y, w, h), stg.border)
        if value != 0:
            text = main.font.render(str(value), True, (0, 0, 0))
            main.screen.blit(text,
                             (x + text.get_height() // 2, y + text.get_width() // 2))
        main.draw_border()
        pygame.display.flip()
        pygame.time.wait(200)

        pygame.draw.rect(main.screen, stg.colors["white"], pygame.Rect(x, y, w, h))
        pygame.draw.rect(main.screen, cell.border_color, pygame.Rect(x, y, w, h), stg.border)
        main.draw_border()

        pygame.display.flip()
        pygame.time.wait(200)


def validation(table, row, col, value):
    """
        This function makes sure that the game rules are not broken.
        Checks if a possible value already exists in the current col or row
        Also checks if the possible value already exists in the curent block
    """

    for i in range(9):
        if i != col:
            if table[row][i].get_value() == value:  # searches the current row to find if the values is already there
                return False
        if i != row:
            if table[i][col].get_value() == value:  # searches the current col to find if the values is already there
                return False

    blockFirstRow = 3 * int(row / 3)
    blockFirstCol = 3 * int(col / 3)

    for i in range(3):
        for j in range(3):
            if (blockFirstRow + i != row) or (
                    blockFirstCol + j != col):  # searches the current box to find if the values is already there
                if table[blockFirstRow + i][blockFirstCol + j].get_value() == value:
                    return False

    return True


def move_back(table, row, col):
    """
        Moves to the last spot modified
    """
    while True:
        if col - 1 >= 0:
            col = col - 1
        else:
            row = row - 1
            col = 8
        if table[row][col].get_locked_value() == 0:
            table[row][col].change_color(stg.colors["red"])
          # mark_invalid(table[row][col])
            return row, col


def move_forward(table, row, col):
    """
        Moves to the next empty spot
    """
    for i in range(9):
        for j in range(9):
            table[i][j].change_color(stg.colors["white"])

    while True:
        if col + 1 < 9:
            col += 1
        else:
            row = row + 1
            col = 0

        if row >= 9 or table[row][col].get_locked_value() == 0:
            if row < 9:
                table[row][col].change_color(stg.colors["green"])
            return row, col


def SudokuSolver(table):
    """
        Is basically a backtracking algorithm going through every empty spot using the move_forward function, placing in the first valid value
        and when it can't find any valid option for a spot it is using move_back function to modify the last value it placed
    """

    current_time = main.pygame.time.get_ticks()
    possible_value = 1
    row = 0
    col = 0
    if table[row][
        col].get_locked_value() != 0:  # if the first value is a locked value it makes sure the program starts with the first empty spot
        row, col = move_forward(table, row, col)

    while 9 > row >= 0:
        # table[row][col].change_color(stg.colors["white"])
        if possible_value != 10:
            if validation(table, row, col, possible_value):
                table[row][col].change_value(possible_value)
                table[row][col].change_color(stg.colors["green"])

                # draw(table[row][col])

                # pygame.time.wait(50)
                # print('Am pus',table[row][col])     #debug print

                possible_value = 1
                mark_valid(table[row][col])
                row, col = move_forward(table, row, col)
            else:
                # print(possible_value, "nevalid")   #debug print

                possible_value += 1
        else:
            table[row][col].change_value(
                0)  # before going back this line makes sure it leaves a empty spot for when it will return
            row, col = move_back(table, row, col)
            possible_value = table[row][
                                 col].get_value() + 1  # when going steps back the next value will be greater then the last valid value

        # print(row, col, possible_value)            #debug print
        draw_table(table)

# print(np.matrix(table))


# def test_validare(row, col):
#     """
#         This function is used for showing all the valid values that can be placed into an empty spot
#     """
#     for i in range(1, 10):
#         if validation(row, col, i):
#             print(i, 'valid')
#         else:
#             print(i, 'invalid')
#
# # test_validare(0,0)
