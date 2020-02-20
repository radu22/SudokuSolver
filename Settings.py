import pygame
offset = 10
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
    "white": (255, 255, 255),
    "grey": (201, 201, 201),
    "grey2":(166, 169, 186),
    "red": (229,115,115),
    "green": (203, 247, 176),
    "blue": (121, 212, 247),
    "clicked": (226, 231, 237),
    "selected": (187, 222, 251)
}

backgroundColor = colors["white"]
clock = pygame.time.Clock()
# 237, 29, 14