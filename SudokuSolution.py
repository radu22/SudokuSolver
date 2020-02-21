import main
import pygame
import Settings as stg


def draw(cell):
    x, y = cell.get_xy()
    w, h = cell.get_wh()
    value = cell.get_value()
    pygame.draw.rect(main.screen, cell.cell_color, pygame.Rect(x, y, w, h))
    pygame.draw.rect(main.screen, cell.border_color, pygame.Rect(x, y, w, h), stg.border)
    if value != 0:
        text = main.font.render(str(value), True, cell.value_color)
        main.screen.blit(text,
                         (x + text.get_height() // 2, y + text.get_width() // 2))


def draw_table(table):
    for i in range(9):
        for j in range(9):
            draw(table[i][j])

    main.draw_border()
    pygame.display.flip()
    pygame.time.wait(5)


def mark_invalid(cell, delay):
    """
    Marks the invalid numbers.
    """
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
        pygame.time.wait(delay)

    pygame.time.wait(delay * 2)


def mark_valid(cell, delay):
    """
    Marks the valid numbers.
    Cool effect of displaying all the numbers from 1 to the valid number.
    Cool blinking effect
    """
    x, y = cell.get_xy()
    w, h = cell.get_wh()
    value = cell.get_value()
    for v in range(value - 1):  # displaying all the numbers from 1 to valid number - 1
        pygame.draw.rect(main.screen, stg.colors["white"], pygame.Rect(x, y, w, h))
        pygame.draw.rect(main.screen, cell.border_color, pygame.Rect(x, y, w, h), stg.border)
        text = main.font.render(str(v), True, (0, 0, 0))
        main.screen.blit(text,
                         (x + text.get_height() // 2, y + text.get_width() // 2))
        main.draw_border()
        pygame.display.flip()

        pygame.time.wait(delay)
    for _ in range(2):  # blinking 2 times for the valid number
        pygame.draw.rect(main.screen, cell.cell_color, pygame.Rect(x, y, w, h))
        pygame.draw.rect(main.screen, cell.border_color, pygame.Rect(x, y, w, h), stg.border)
        if value != 0:
            text = main.font.render(str(value), True, (0, 0, 0))
            main.screen.blit(text,
                             (x + text.get_height() // 2, y + text.get_width() // 2))
        main.draw_border()
        pygame.display.flip()
        pygame.time.wait(delay * 10)

        pygame.draw.rect(main.screen, stg.colors["white"], pygame.Rect(x, y, w, h))
        pygame.draw.rect(main.screen, cell.border_color, pygame.Rect(x, y, w, h), stg.border)
        main.draw_border()

        pygame.display.flip()
        pygame.time.wait(delay * 10)


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
        :param row and col of the the current cell
        :returns row and col of the previous cell that got modified
    """
    while True:  # if the previous cell is a cell with a locked value != 0 move back
        if col - 1 >= 0:
            col = col - 1
        else:
            row = row - 1
            col = 8
        if table[row][col].get_locked_value() == 0:
            table[row][col].change_color(stg.colors["red"])
            # mark_invalid(table[row][col])  removed because it made the solution take way too long to finish
            return row, col


def move_forward(table, row, col):
    """
        Moves to the next empty spot
        :param row and col of the the current cell
        :returns row and col of the next cell that needs a valid value
    """
    for i in range(9):
        for j in range(9):
            table[i][j].change_color(stg.colors["white"])

    while True:  # if the next cell is a cell with a locked value != 0 move forward
        if col + 1 < 9:
            col += 1
        else:
            row = row + 1
            col = 0

        if row >= 9 or table[row][col].get_locked_value() == 0:
            if row < 9:
                table[row][col].change_color(stg.colors["green"])
            return row, col


def SudokuSolver(table, delay, stop):
    """
        Is basically a backtracking algorithm going through every empty spot using the move_forward function, placing in the first valid value
        and when it can't find any valid option for a spot it is using move_back function to modify the last value it placed

        :param table = sudoku table
               delay = the time to wait after every step
               stop = stopping button
        :return True   if the solution got to the end
                False  if the solution was stopped
    """
    possible_value = 1
    row = 0
    col = 0
    if table[row][
        col].get_locked_value() != 0:  # if the first value is a locked value it makes sure the program starts with the first empty spot
        row, col = move_forward(table, row, col)

    while 9 > row >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # red X button
                done = True
                quit()
            if event.type == pygame.MOUSEBUTTONUP:    # stop the solution at the current point
                pos_x, pos_y = pygame.mouse.get_pos()
                if stop.is_over((pos_x, pos_y)):
                    stop.change_text("Magic!")
                    return False

        if possible_value != 10:
            if validation(table, row, col, possible_value):
                table[row][col].change_value(possible_value)
                table[row][col].change_color(stg.colors["green"])

                possible_value = 1
                # mark_valid(table[row][col], delay) removed because it made the solution take way too long to finish
                row, col = move_forward(table, row, col)
            else:
                possible_value += 1
        else:
            table[row][col].change_value(0)  # before going back this line makes sure it leaves a empty spot for when it will return
            row, col = move_back(table, row, col)
            possible_value = table[row][col].get_value() + 1  # when going steps back the next value will be greater then the last valid value

        # print(row, col, possible_value)            #debug print
        draw_table(table)
    return True


print("SudokuSolution file loaded")
