import pygame

offset = 20
xCell = 60
yCell = 60
xBlock = 3 * xCell
yBlock = 3 * yCell
xScreen = 3 * xBlock
yScreen = 3 * yBlock
border = 1
spacing = 1
colors = {
    "black": (20, 26, 54),
    "white": (245, 244, 242),
    "grey": (201, 201, 201),
    "grey2": (166, 169, 186),
    "red": (229, 115, 115),
    "red2": (245, 22, 22),
    "green": (203, 247, 176),
    "blue": (121, 212, 247),
    "blue2": (3, 72, 168),
    "family": (226, 231, 237),
    "selected": (187, 222, 251),
    "button-green": (76, 175, 80),
    "button-hover-green": (84, 196, 89),
    "button-blue":(61, 192, 212),
    "button-hover-blue": (69, 215, 237)
}

backgroundColor = colors["white"]
clock = pygame.time.Clock()

print("Settings file loaded")