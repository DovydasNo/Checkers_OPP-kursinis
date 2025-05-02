import pygame
from checkers_func.constants import WIDTH, HEIGHT, SQUARE_SIZE
from checkers_func.game import Game

pygame.init()
pygame.font.init()

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers_OOP-kursinis")

def get_coordinates_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    game.reset()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_coordinates_from_mouse(pos)
                game.select(row, col)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()

        game.update()

        winner = game.winner()
        if winner:
            game.announce_winner()
            run = False
    pygame.quit()

main()