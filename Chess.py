import time
from Board import Board, PIECES
import os
import keyboard

CYAN = '\033[96m'
RESET = '\033[0m'

class Chess:
    def __init__(self):
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

    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def listenInput(self, key):
        if key == 'w':
            self.changePosition(self.x - 1, self.y)
        elif key == 's':
            self.changePosition(self.x + 1, self.y)
        elif key == 'a':
            self.changePosition(self.x, self.y - 1)
        elif key == 'd':
            self.changePosition(self.x, self.y + 1)
        elif key == 'enter':
            self.validateSelection()
        elif key == 'q':
            self.gameOver = True

    def getPieceColor(self, piece):
        if piece.islower():
            return "black"
        elif piece.isupper():
            return "white"
        return None

    def validateSelection(self):
        piece = self.board.getPieceAt(self.x, self.y)
        if not self.selectedPiece:
            if piece != ' ' and self.getPieceColor(piece) == self.turn:
                self.selectedPiece = (self.x, self.y)
                self.findPossibleMoves(self.x, self.y)
        else:
            if (self.x, self.y) in self.possibleMoves:
                self.movePiece(self.selectedPiece, (self.x, self.y))
                self.selectedPiece = None
                self.possibleMoves.clear()
                self.turn = "black" if self.turn == "white" else "white"

                if self.isStalemate(self.turn):
                    self.render()
                    print("Stalemate! It's a draw.")
                    self.gameOver = True
            else:
                self.selectedPiece = None
                self.possibleMoves.clear()

    def movePiece(self, start, end):
        sx, sy = start
        ex, ey = end
        movingPiece = self.board.getPieceAt(sx, sy)
        targetPiece = self.board.getPieceAt(ex, ey)

        # En Passant Capture
        if movingPiece.lower() == 'p' and (ex, ey) == self.enPassantTarget:
            if self.getPieceColor(movingPiece) == "white":
                captured = self.board.getPieceAt(ex + 1, ey)
                self.capturedBlack.append(captured)
                self.board.board[ex + 1][ey] = ' '
            else:
                captured = self.board.getPieceAt(ex - 1, ey)
                self.capturedWhite.append(captured)
                self.board.board[ex - 1][ey] = ' '

        # Normal capture
        elif targetPiece != ' ':
            if self.getPieceColor(targetPiece) == "white":
                self.capturedBlack.append(targetPiece)
            else:
                self.capturedWhite.append(targetPiece)

        # Update board
        self.board.board[ex][ey] = movingPiece
        self.board.board[sx][sy] = ' '

        # En Passant setup
        if movingPiece.lower() == 'p' and abs(ex - sx) == 2:
            self.enPassantTarget = ((sx + ex) // 2, sy)
        else:
            self.enPassantTarget = None

        self.moveHistory.append(f"{movingPiece}: {chr(65 + sy)}{8 - sx} → {chr(65 + ey)}{8 - ex}")

    def start(self):
        self.render()
        while not self.gameOver:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name.lower()
                self.listenInput(key)
                self.render()
        self.clearScreen()
        print("Game Over! Final board:")
        self.board.printBoard()
    def render(self):
        self.clearScreen()
        self.board.printBoard()
        print(f"Turn: {self.turn}")
        if self.selectedPiece:
            print(f"Selected: {chr(65 + self.selectedPiece[1])}{8 - self.selectedPiece[0]}")
        print(f"Captured by White: {' '.join(PIECES[p] for p in self.capturedWhite) if self.capturedWhite else 'None'}")
        print(f"Captured by Black: {' '.join(PIECES[p] for p in self.capturedBlack) if self.capturedBlack else 'None'}")
        print("Use WASD to move, Enter to select/move, Q to quit.")

        if self.selectedPiece:
            for move in self.possibleMoves:
                mx, my = move
                print(f"{CYAN}{chr(65 + my)}{8 - mx}{RESET}", end=' ')
            print()

    def changePosition(self, newX, newY):
        newX = max(0, min(newX, 7))
        newY = max(0, min(newY, 7))
        self.x = self.board.cursorRow = newX
        self.y = self.board.cursorCol = newY

    def findPossibleMoves(self, x, y):
        self.possibleMoves.clear()
        piece = self.board.getPieceAt(x, y)
        color = self.getPieceColor(piece)

        if piece.lower() == 'p':
            direction = -1 if color == "white" else 1
            startRow = 6 if color == "white" else 1

            nx, ny = x + direction, y
            if 0 <= nx < 8 and self.board.getPieceAt(nx, ny) == ' ':
                self.possibleMoves.append((nx, ny))

                if x == startRow:
                    nx2 = nx + direction
                    if 0 <= nx2 < 8 and self.board.getPieceAt(nx2, ny) == ' ':
                        self.possibleMoves.append((nx2, ny))

            for dy in [-1, 1]:
                cx, cy = x + direction, y + dy
                if 0 <= cx < 8 and 0 <= cy < 8:
                    target = self.board.getPieceAt(cx, cy)
                    if target != ' ' and self.getPieceColor(target) != color:
                        self.possibleMoves.append((cx, cy))

                    # En Passant
                    if self.enPassantTarget == (cx, cy):
                        self.possibleMoves.append((cx, cy))

        elif piece.lower() == 'r':
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                nx, ny = x, y
                while 0 <= nx + dx < 8 and 0 <= ny + dy < 8:
                    nx += dx
                    ny += dy
                    target = self.board.getPieceAt(nx, ny)
                    if target == ' ':
                        self.possibleMoves.append((nx, ny))
                    elif self.getPieceColor(target) != color:
                        self.possibleMoves.append((nx, ny))
                        break
                    else:
                        break

        elif piece.lower() == 'n':
            knight_moves = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2)]
            for dx, dy in knight_moves:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = self.board.getPieceAt(nx, ny)
                    if target == ' ' or self.getPieceColor(target) != color:
                        self.possibleMoves.append((nx, ny))

        elif piece.lower() == 'b':
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in directions:
                nx, ny = x, y
                while 0 <= nx + dx < 8 and 0 <= ny + dy < 8:
                    nx += dx
                    ny += dy
                    target = self.board.getPieceAt(nx, ny)
                    if target == ' ':
                        self.possibleMoves.append((nx, ny))
                    elif self.getPieceColor(target) != color:
                        self.possibleMoves.append((nx, ny))
                        break
                    else:
                        break

        elif piece.lower() == 'q':
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                          (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in directions:
                nx, ny = x, y
                while 0 <= nx + dx < 8 and 0 <= ny + dy < 8:
                    nx += dx
                    ny += dy
                    target = self.board.getPieceAt(nx, ny)
                    if target == ' ':
                        self.possibleMoves.append((nx, ny))
                    elif self.getPieceColor(target) != color:
                        self.possibleMoves.append((nx, ny))
                        break
                    else:
                        break

        elif piece.lower() == 'k':
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                          (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = self.board.getPieceAt(nx, ny)
                    if target == ' ' or self.getPieceColor(target) != color:
                        self.possibleMoves.append((nx, ny))

    def isStalemate(self, color):
        for x in range(8):
            for y in range(8):
                piece = self.board.getPieceAt(x, y)
                if piece != ' ' and self.getPieceColor(piece) == color:
                    self.findPossibleMoves(x, y)
                    if self.possibleMoves:
                        return False
        return True


if __name__ == "__main__":
    chess = Chess()
    chess.start()
