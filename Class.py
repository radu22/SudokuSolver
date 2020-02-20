import pygame
import Settings as stg


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False

    def change_color(self, color):
        self.color = color

    def change_text(self, text):
        self.text = text


class Cell:
    width = 60
    height = 60
    value = 0
    locked_value = 0
    border = 1
    border_color = stg.colors["grey"]
    cell_color = stg.colors["white"]
    value_color = stg.colors["blue2"]
    block = 0
    focus = False
    state = False

    def __init__(self, x, y, locked_value, block):
        self.x = x
        self.y = y
        self.locked_value = locked_value
        if locked_value != 0:
            self.value_color = (0, 0, 0)
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

    def change_value_color(self, state):
        if state:
            self.value_color = stg.colors["blue2"]
        else:
            self.value_color = stg.colors["red2"]

    def change_locked_value(self, x):
        self.locked_value = x

    def get_locked_value(self):
        return self.locked_value

    def print_values(self):
        print("value: ", self.value, " locked: ", self.locked_value)

    def get_color(self):
        return self.cell_color

    def get_value_color(self):
        return self.value_color

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

    def change_state_false(self):
        self.state = False

    def change_state_true(self):
        self.state = True

    def change_focus_state(self):
        self.focus = not self.focus

    def default(self):
        self.cell_color = stg.colors["white"]
        self.state = False
        self.focus = False


print("Salut")
