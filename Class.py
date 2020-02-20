import pygame
import Settings as stg


class Cell:
    width = 60
    height = 60
    value = 0
    locked_value = 0
    border = 1
    border_color = stg.colors["grey"]
    cell_color = stg.colors["white"]
    block = 0
    state = False

    def __init__(self, x, y, locked_value, block):
        self.x = x + stg.offset
        self.y = y + stg.offset
        self.locked_value = locked_value
        self.value = locked_value
        self.block = block
        self.state = False

    def get_xy(self):
        return self.x, self.y

    def get_wh(self):
        return self.width, self.height

    def get_value(self):
        return self.value

    def get_block(self):
        return self.block

    def change_value(self, x):
        self.value = x

    def change_locked_value(self, x):
        self.locked_value = x

    def get_locked_value(self):
        return self.locked_value

    def print_values(self):
        print("value: ", self.value, " locked: ", self.locked_value)

    def get_color(self):
        return self.cell_color

    def change_color(self, color):
        self.cell_color = color

    # def clicked(self):
    #     pygame.draw.rect(screen, self.green, pygame.Rect(self.x, self.y, self.width, self.height))
    #     self.state = True
    #     while self.state:
    #         pygame.draw.rect(screen, self.green, pygame.Rect(self.x, self.y, self.width, self.height))
    #         for event in pygame.event.get():
    #             if event.type == pygame.KEYDOWN:
    #                 number = numbers(event.key)
    #                 if number == "#":
    #                     number = "0"
    #                 self.value = int(number)
    #                 self.locked_value = self.value
    #                 cells[self.y // Cell.width][self.x // Cell.height].write_number(number)
    #                 self.state = False

    def state(self):
        return self.state

    def change_state_false(self):
        self.state = False

    def change_state(self):
        self.state = not self.state


print("Salut")
