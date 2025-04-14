from Constants import CONST_WHITE, CONST_YELLOW, CONST_RESET

CONST_PIECES = {
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚',
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    ' ': ' '
}

class Board:
    def __init__(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self.cursorRow = 0
        self.cursorCol = 0

    def getPieceAt(self, row, col):
        return self.board[row][col]

    def printBoard(self):
        print("  A B C D E F G H")
        for i in range(8):
            print(f"{8-i} ", end='')
            for j in range(8):
                piece = self.board[i][j]
                color = CONST_WHITE if piece.isupper() else CONST_YELLOW if piece.islower() else ''
                piece_display = CONST_PIECES[piece]
                if i == self.cursorRow and j == self.cursorCol:
                    print(f"{color}[{piece_display}]{CONST_RESET}", end='')
                else:
                    print(f"{color} {piece_display} {CONST_RESET}", end='')
            print(f" {8-i}")
        print("  A B C D E F G H")