from math import inf
from random import randint, shuffle, random
from time import sleep


class Coordinate:
    def __init__(self, coordinates, size=3):
        self.size = size
        (self.x, self.y) = map(int, coordinates.split(" "))

    def not_in_range(self):
        if self.y > self.size or self.x > self.size:
            return True
        else:
            return False

    def x(self):
        pass
    def y(self):
        pass

class SeqCoordinate:
    def __init__(self, number, size=3):
        self.size = size
        (self.x, self.y) = (number-1)//3, (number-1)%3

    def not_in_range(self):
        if self.y > self.size or self.x > self.size:
            return True
        else:
            return False

    def x(self):
        pass
    def y(self):
        pass


# 13  23  33
# 12  22  32
# 11  21  31
class TicTacToeBoard:
    def __init__(self, board="", size=3):
        self.size = size
        self.board = [[" " for _ in range(size)] for _ in range(size)]
        if len(board) == 0:
            board = "                                            "

        if len(board) >= size ** 2:
            for i in range(size):
                for j in range(size):
                    self.board[i][j] = board[i * size + j]

        x_count = board.count('X')
        o_count = board.count('O')
        if x_count == o_count:
            self.next_turn = "X"
        else:
            self.next_turn = "O"

    def __str__(self):
        answer = "-" * (3 * self.size) + "\n"
        for i in range(self.size):
            answer += "| "
            for j in range(self.size):
                answer += self.board[i][j] + " "
            if i != self.size:
                answer += "|\n"
        answer += "-" * (3 * self.size)
        return answer

    def game_on(self):  # snake_case
        if not self.empty_spots():
            return False
        return True

    def place(self, i, j, piece):
        if not self.board[i][j] in "XO":
            self.board[i][j] = piece
            return True
        else:
            return False

    def reset(self, i, j):
        self.board[i][j] = " "

    def empty_spots(self):
        return [(x, y) for x in range(self.size) for y in range(self.size) if self.board[x][y] == " "]
    def draw(self):
        if self.empty_spots() == 0 and not self.win("X") and not self.win("O"):
            return True
        else:
            return False
    def win(self, piece):
        mark = piece
        for i in range(self.size):
            # check rows
            row_length = 0
            column_length = 0
            for j in range(self.size):
                if self.board[i][j] == mark:
                    row_length += 1
                if self.board[j][i] == mark:
                    column_length += 1

            if row_length == self.size or column_length == self.size:
                return True

        # check diag
        diag1 = diag2 = True
        for i in range(self.size):
            if self.board[i][i] != mark:
                diag1 = False
            if self.board[i][self.size - 1 - i] != mark:
                diag2 = False

        return diag1 or diag2

    def random_place(self, piece):
        empty_spot = self.empty_spots()
        (i, j) = empty_spot[randint(0, len(empty_spot)) - 1]
        self.place(i, j, piece)


class Player:
    def __init__(self, piece):

        self.piece = piece
        self.other_piece = "X" if self.piece == "O" else "O"

    @staticmethod
    def create(level, piece):
        if level == "easy":
            return EasyPlayer(piece)
        if level == "medium":
            return MediumPlayer(piece)
        if level == "user":
            return HumanPlayer(piece)
        if level == "hard":
            return HardPlayer(piece)


class HumanPlayer(Player):
    def move(self, board):
        while True:
            input_str = input("Enter the coordinates:")

            try:
                coordinate = Coordinate(input_str, board.size)
            except ValueError:
                print("You should enter numbers")
                continue

            if coordinate.not_in_range():
                print("Coordinates should be from 1 to " + str(board.size) + "!")
            elif board.place(board.size - coordinate.y, coordinate.x - 1, self.piece):
                return
            else:
                print("This cell is occupied! Choose another one!")


class EasyPlayer(Player):
    def move(self, board):
        print('Making move level "easy"')
        sleep(1)
        board.random_place(self.piece)


class MediumPlayer(Player):
    def move(self, board):
        print('Making move level "medium"')
        sleep(1)
        empty_spots = board.empty_spots()
        shuffle(empty_spots)
        for (i, j) in empty_spots:
            board.place(i, j, self.piece)
            if board.win(self.piece):
                return
            else:
                board.reset(i, j)

        for (i, j) in empty_spots:
            board.place(i, j, self.other_piece)
            if board.win(self.other_piece):
                board.reset(i, j)
                board.place(i, j, self.piece)
                return
            else:
                board.reset(i, j)

        board.random_place(self.piece)


class HardPlayer(Player):
    def move(self, board):
        if not board.win("X") and not board.win("O"):
            print('Making move level "hard"')
            sleep(0.5)
            if len(board.empty_spots()) == 9:
                board.random_place(self.piece)
                return
            (i,j, score) = self.minimax(board, True)
            board.place(i,j,self.piece)
        return
    # (i,j,score)
    def minimax(self, board, max):
        answer = (-1, -1, -inf if max else inf)
        empty_spots = board.empty_spots()
        if not board.game_on() or board.win(self.piece) or board.win(self.other_piece):
            return (-1, -1, self.utility_score(board))

        for (i, j) in empty_spots:
            board.place(i, j, self.piece if max else self.other_piece)
            score = self.minimax(board, not max)
            if max and score[2] > answer[2] :
                answer = (i, j, score[2])
            if not max and score[2] < answer[2]:
                answer = (i, j, score[2])

            if score[2] == answer[2] and random()>0.5:
                answer = (i, j, score[2])

            board.reset(i,j)
        return answer

    def utility_score(self, board):
        empty_spots = board.empty_spots()
        score = len(empty_spots) + 1
        if board.win(self.piece):
            return score
        if board.win(self.other_piece):
            return -score

        return 0