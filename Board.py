import keyboard
import os
import time

PEACH = '\033[93m'
RESET = '\033[0m'
CYAN = '\033[96m'
PIECES = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟',
    ' ': '□'
}

class Board:
    def __init__(self):
        self.rows = 8
        self.cols = 8
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
    
    def printBoard(self):
        os.system('cls' if os.name == 'nt' else 'clear')  
        print(f"  {'-' * 27}")
        for i in range(self.rows):
            print(f"{8 - i} ", end='')
            print(f"| ", end='')
            for j in range(self.cols):
                cell = self.board[i][j]
                symbol = PIECES[cell]
               
                if i == self.cursorRow and j == self.cursorCol:
                    print(f"{CYAN}{symbol:2}\033[0m ", end='') 
                elif cell == ' ' and (i + j) % 2 == 0:
                    print(f"{PEACH}{symbol:2}{RESET} ", end='')
                elif cell == ' ':
                    print(f"{RESET}{symbol:2}{RESET} ", end='')
                elif cell.islower():
                    print(f"{PEACH}{symbol:2}{RESET} ", end='')
                else:
                    print(f"{symbol:2} ", end='')
            print(f"|")
        print(f"  {'-' * 27}")
        print("    A  B  C  D  E  F  G  H")
        print(f"Cursor at: {chr(65 + self.cursorCol)}{8 - self.cursorRow}")
    def getPiece(self):
        return self.board[self.cursorRow][self.cursorCol]
    def getPieceAt(self,x,y):
        return self.board[x][y]
