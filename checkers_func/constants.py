import pygame

ROWS, COLS = 8, 8
SQUARE_SIZE = 100

WIDTH = COLS * SQUARE_SIZE
HEIGHT = ROWS * SQUARE_SIZE

PADDING = 15
OUTLINE = 2

BLACK_SQUARES = (153, 71, 65)
WHITE_SQUARES = (243, 224, 221)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

DIRECTIONS = {
    "white": [(-1, -1), (-1, 1)],
    "black": [(1, -1), (1, 1)],
}

CROWN = pygame.transform.scale(pygame.image.load('checkers_func/resources/crown.png'), (50, 50))


def make_my_text_pretty(func):
    def wrapper(*args, **kwargs):
        print("\n°º¤ø,__,ø¤º°`°º¤ø,__,ø¤°º¤ø,__,ø¤º°`°º¤ø,\n\n")
        result = func(*args, **kwargs)
        print("\n\n°º¤ø,__,ø¤º°`°º¤ø,__,ø¤°º¤ø,__,ø¤º°`°º¤ø,\n")
        return result
    return wrapper