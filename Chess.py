from Board import Board
from MoveLogic import getPieceColor, findPossibleMoves, movePiece
from GameLogic import isInCheck, isCheckmate, isStalemate, moveIntoCheck
from Ai import makeAiMove
from Interface import start

class Chess:
    def __init__(self, playAs="white", difficulty=3):
        self.board = Board()
        self.turn = "white"
        self.selectedPiece = None
        self.x = self.board.cursorRow
        self.y = self.board.cursorCol
        self.moveHistory = []
        self.gameOver = False
        self.capturedWhite = []
        self.capturedBlack = []
        self.possibleMoves = []
        self.enPassantTarget = None
        self.check = False
        self.checkmate = False
        self.playAs = playAs
        self.aiDifficulty = difficulty
        self.waitingForAi = False
        
        if self.playAs == "black":
            self.waitingForAi = True

    def getPieceColor(self, piece):
        return getPieceColor(piece)

    def findPossibleMoves(self, x, y):
        return findPossibleMoves(self.board, x, y, self.enPassantTarget)

    def movePiece(self, start, end):
        return movePiece(self.board, start, end, self.enPassantTarget, self.capturedWhite, self.capturedBlack, self.moveHistory)

    def isInCheck(self, color):
        return isInCheck(self.board, color)

    def isCheckmate(self, color):
        return isCheckmate(self.board, color, self.enPassantTarget)

    def isStalemate(self, color):
        return isStalemate(self.board, color, self.enPassantTarget)

    def moveIntoCheck(self, start, end):
        return moveIntoCheck(self.board, start, end)

    def makeAiMove(self):
        makeAiMove(self)

if __name__ == "__main__":
    print("Welcome to Chess with AI opponent!")
    while True:
        color = input("Do you want to play as white or yellow? (w/y): ").lower()
        if color in ['w', 'white']:
            playAs = "white"
            break
        elif color in ['y', 'yellow']:
            playAs = "black"
            break
        else:
            print("Invalid choice. Please enter 'w' or 'y'.")
    
    while True:
        try:
            difficulty = int(input("Choose AI difficulty (1-4, higher is stronger but slower): "))
            if 1 <= difficulty <= 4:
                break
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")
    
    chess = Chess(playAs=playAs, difficulty=difficulty)
    start(chess)