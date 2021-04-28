import pygame
from Back_End import *
from time import sleep
from sys import exit
import math

pygame.init()
screen = pygame.display.set_mode((900, 900))
end_screen = pygame.display.set_mode((900, 900))
blank_list = []


class Piece(pygame.sprite.Sprite):
    def __init__(self, Path, Piece, Board):
        super().__init__()
        self.path = pygame.image.load(Path)
        self.Piece = Piece
        self.board = Board

    def update(self):
        for l1, i in enumerate(self.board):
            for l2, j in enumerate(i):
                if j == self.Piece:
                    screen.blit(self.path, (l2 * 300 + 5, l1 * 300 + 5 * l1))


screen.fill('white')
black = (0, 0, 0)
test_board = TicTacToeBoard("                                                   ")
# Make the sprites
X = Piece('X.png', "X", test_board.board)
O = Piece('O.png', "O", test_board.board)
blank_square = Piece('blank.png', ' ', test_board.board)
# Make the sprite Groups
board = pygame.sprite.Group(X, O, blank_square)
blank = pygame.sprite.Group(blank_square)
pygame.display.flip()
game_font = pygame.font.Font(None, 40)
p = 0
# level = input("Input your level:\n").lower()
level = "hard"
# piece = input("Input your Piece(Enter X or O):\n").upper()
piece = "X"
player = (Player.create("user", piece), Player.create(level, "O" if piece == "X" else "X"))
player_play = False


def end_game():
    if test_board.win(piece):
        text_surface = game_font.render('You Lose', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(450, 450))
    elif not test_board.empty_spots():
        text_surface = game_font.render('Draw', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(450, 450))
    else:
        text_surface = game_font.render('You Win', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(450, 450))
    screen.blit(text_surface, text_rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos, int(math.ceil(pos[0] / 300)), int(math.ceil(pos[1] / 100)))
            if test_board.place(int(math.floor(pos[1] / 300)), int(math.floor(pos[0] / 300)), piece):
                player[1].move(test_board)
    p = (p + 1) % 2
    board.update()
    if test_board.empty_spots() == [] or test_board.win("X") or test_board.win("O"):
        screen.fill((0, 0, 0))
        end_game()
        pygame.display.flip()
        sleep(10)
        pygame.quit()
        exit()
    pygame.draw.line(screen, black, (300, 10), (300, 890), width=5)
    pygame.draw.line(screen, black, (600, 10), (600, 890), width=4)
    pygame.draw.line(screen, black, (10, 300), (950, 300), width=5)
    pygame.draw.line(screen, black, (10, 600), (950, 600), width=4)
    pygame.display.flip()
    print(test_board.empty_spots())
