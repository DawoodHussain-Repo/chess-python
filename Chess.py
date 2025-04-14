import time
from Board import Board, PIECES
import os
import keyboard
import random
import copy

CYAN = '\033[96m'
RESET = '\033[0m'
RED = '\033[91m'

PIECE_VALUES = {
    'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -100,
    'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100,
    ' ': 0
}

PAWN_TABLE = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

KNIGHT_TABLE = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

BISHOP_TABLE = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5,  5,  5,  5,  5,-10],
    [-10,  0,  5,  0,  0,  5,  0,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

ROOK_TABLE = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [0,  0,  0,  5,  5,  0,  0,  0]
]

QUEEN_TABLE = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,  0,  5,  5,  5,  5,  0, -5],
    [0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

KING_TABLE = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20, 20,  0,  0,  0,  0, 20, 20],
    [20, 30, 10,  0,  0, 10, 30, 20]
]

def flip_table(table):
    return table[::-1]

class Chess:
    def __init__(self, play_as="white", difficulty=3):
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
        self.play_as = play_as  # "white" or "black"
        self.ai_difficulty = difficulty  # AI search depth
        self.waiting_for_ai = False
        
        # Start with AI move if playing as black
        if self.play_as == "black":
            self.waiting_for_ai = True

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
                self.possibleMoves = [move for move in self.possibleMoves if not self.moveIntoCheck(self.selectedPiece, move)]
        else:
            if (self.x, self.y) in self.possibleMoves:
                self.movePiece(self.selectedPiece, (self.x, self.y))
                self.selectedPiece = None
                self.possibleMoves.clear()
                
                self.turn = "black" if self.turn == "white" else "white"
                
                self.check = self.isInCheck(self.turn)
                
                if self.isCheckmate(self.turn):
                    self.checkmate = True
                    self.render()
                    winner = "White" if self.turn == "black" else "Black"
                    print(f"Checkmate! {winner} wins!")
                    self.gameOver = True
                elif self.isStalemate(self.turn):
                    self.render()
                    print("Stalemate! It's a draw.")
                    self.gameOver = True
                
                if self.turn != self.play_as and not self.gameOver:
                    self.waiting_for_ai = True
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
                self.capturedWhite.append(targetPiece)
            else:
                self.capturedBlack.append(targetPiece)

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
            # Check if it's AI's turn
            if self.waiting_for_ai:
                self.render()
                print("AI is thinking...")
                self.makeAIMove()
                self.waiting_for_ai = False
                self.render()
                if self.gameOver:
                    break
            
            # Human player's turn
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name.lower()
                self.listenInput(key)
                self.render()
        
        self.clearScreen()
        print("Game Over! Final board:")
        self.board.printBoard()
        print("\nMove History:")
        for i, move in enumerate(self.moveHistory):
            print(f"{i+1}. {move}")

    def render(self):
        self.clearScreen()
        self.board.printBoard()
        print(f"Turn: {self.turn.capitalize()} {'(AI)' if self.turn != self.play_as else '(You)'}")
        
        if self.check:
            print(f"{RED}CHECK!{RESET}")
            
        if self.selectedPiece:
            print(f"Selected: {chr(65 + self.selectedPiece[1])}{8 - self.selectedPiece[0]}")
        
        print(f"Captured by White: {' '.join(PIECES[p] for p in self.capturedWhite) if self.capturedWhite else 'None'}")
        print(f"Captured by Black: {' '.join(PIECES[p] for p in self.capturedBlack) if self.capturedBlack else 'None'}")
        
        print("Use WASD to move, Enter to select/move, Q to quit.")

        if self.moveHistory:
            print(f"Last move: {self.moveHistory[-1]}")

        if self.selectedPiece:
            print("Possible moves:", end=' ')
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
        if self.isInCheck(color):
            return False
            
        for x in range(8):
            for y in range(8):
                piece = self.board.getPieceAt(x, y)
                if piece != ' ' and self.getPieceColor(piece) == color:
                    self.findPossibleMoves(x, y)
                    legal_moves = [move for move in self.possibleMoves if not self.moveIntoCheck((x, y), move)]
                    if legal_moves:
                        return False
        return True

    def isInCheck(self, color):
        # Find king position
        king = 'K' if color == "white" else 'k'
        king_pos = None
        for i in range(8):
            for j in range(8):
                if self.board.getPieceAt(i, j) == king:
                    king_pos = (i, j)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False  
        
        opponent_color = "black" if color == "white" else "white"
        for i in range(8):
            for j in range(8):
                piece = self.board.getPieceAt(i, j)
                if piece != ' ' and self.getPieceColor(piece) == opponent_color:
                    self.findPossibleMoves(i, j)
                    if king_pos in self.possibleMoves:
                        return True
        
        return False

    def isCheckmate(self, color):
        if not self.isInCheck(color):
            return False
        
        for x in range(8):
            for y in range(8):
                piece = self.board.getPieceAt(x, y)
                if piece != ' ' and self.getPieceColor(piece) == color:
                    self.findPossibleMoves(x, y)
                    for move in self.possibleMoves:
                        if not self.moveIntoCheck((x, y), move):
                            return False  
        
        return True
    def moveIntoCheck(self, start, end):
        """Test if a move would put the player's king in check"""
        # Make a copy of the board to simulate the move
        temp_board = copy.deepcopy(self.board.board)
        
        # Get the moving piece's color
        sx, sy = start
        piece = self.board.getPieceAt(sx, sy)
        color = self.getPieceColor(piece)
        
        # Simulate the move
        ex, ey = end
        temp_board[ex][ey] = temp_board[sx][sy]
        temp_board[sx][sy] = ' '
        
        # Find the king's position after the move
        king = 'K' if color == "white" else 'k'
        king_pos = None
        for i in range(8):
            for j in range(8):
                if temp_board[i][j] == king:
                    king_pos = (i, j)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False  # No king found (shouldn't happen)
        
        # Check if any opponent piece can attack the king
        opponent_color = "black" if color == "white" else "white"
        for i in range(8):
            for j in range(8):
                piece = temp_board[i][j]
                if piece != ' ' and self.getPieceColor(piece) == opponent_color:
                    # Calculate opponent piece's possible moves using the temporary board
                    moves = self.calculateMoves(temp_board, i, j)
                    if king_pos in moves:
                        return True  # King would be in check
        
        return False  # King would not be in check
        
    def calculateMoves(self, board, x, y):
        """Calculate possible moves for a piece without modifying the game state"""
        moves = []
        piece = board[x][y]
        color = self.getPieceColor(piece)

        if piece.lower() == 'p':
            direction = -1 if color == "white" else 1
            startRow = 6 if color == "white" else 1

            nx, ny = x + direction, y
            if 0 <= nx < 8 and board[nx][ny] == ' ':
                moves.append((nx, ny))

                if x == startRow:
                    nx2 = nx + direction
                    if 0 <= nx2 < 8 and board[nx2][ny] == ' ':
                        moves.append((nx2, ny))

            for dy in [-1, 1]:
                cx, cy = x + direction, y + dy
                if 0 <= cx < 8 and 0 <= cy < 8:
                    target = board[cx][cy]
                    if target != ' ' and self.getPieceColor(target) != color:
                        moves.append((cx, cy))
                    
                    # Note: En passant is not checked here for simplicity

        elif piece.lower() == 'r':
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                nx, ny = x, y
                while 0 <= nx + dx < 8 and 0 <= ny + dy < 8:
                    nx += dx
                    ny += dy
                    target = board[nx][ny]
                    if target == ' ':
                        moves.append((nx, ny))
                    elif self.getPieceColor(target) != color:
                        moves.append((nx, ny))
                        break
                    else:
                        break

        elif piece.lower() == 'n':
            knight_moves = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2)]
            for dx, dy in knight_moves:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = board[nx][ny]
                    if target == ' ' or self.getPieceColor(target) != color:
                        moves.append((nx, ny))

        elif piece.lower() == 'b':
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in directions:
                nx, ny = x, y
                while 0 <= nx + dx < 8 and 0 <= ny + dy < 8:
                    nx += dx
                    ny += dy
                    target = board[nx][ny]
                    if target == ' ':
                        moves.append((nx, ny))
                    elif self.getPieceColor(target) != color:
                        moves.append((nx, ny))
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
                    target = board[nx][ny]
                    if target == ' ':
                        moves.append((nx, ny))
                    elif self.getPieceColor(target) != color:
                        moves.append((nx, ny))
                        break
                    else:
                        break

        elif piece.lower() == 'k':
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                        (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = board[nx][ny]
                    if target == ' ' or self.getPieceColor(target) != color:
                        moves.append((nx, ny))

        return moves
    
    def evaluateBoard(self, board):
        """Evaluate the board position from white's perspective"""
        score = 0
        
        # Material value
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece != ' ':
                    # Base material value
                    score += PIECE_VALUES[piece]
                    
                    # Position value
                    if piece.lower() == 'p':
                        if piece.isupper():  # White pawn
                            score += PAWN_TABLE[i][j] * 0.1
                        else:  # Black pawn
                            score -= flip_table(PAWN_TABLE)[i][j] * 0.1
                    elif piece.lower() == 'n':
                        if piece.isupper():  # White knight
                            score += KNIGHT_TABLE[i][j] * 0.1
                        else:  # Black knight
                            score -= flip_table(KNIGHT_TABLE)[i][j] * 0.1
                    elif piece.lower() == 'b':
                        if piece.isupper():  # White bishop
                            score += BISHOP_TABLE[i][j] * 0.1
                        else:  # Black bishop
                            score -= flip_table(BISHOP_TABLE)[i][j] * 0.1
                    elif piece.lower() == 'r':
                        if piece.isupper():  # White rook
                            score += ROOK_TABLE[i][j] * 0.1
                        else:  # Black rook
                            score -= flip_table(ROOK_TABLE)[i][j] * 0.1
                    elif piece.lower() == 'q':
                        if piece.isupper():  # White queen
                            score += QUEEN_TABLE[i][j] * 0.1
                        else:  # Black queen
                            score -= flip_table(QUEEN_TABLE)[i][j] * 0.1
                    elif piece.lower() == 'k':
                        if piece.isupper():  # White king
                            score += KING_TABLE[i][j] * 0.1
                        else:  # Black king
                            score -= flip_table(KING_TABLE)[i][j] * 0.1
        
        return score
        
    def alphaBeta(self, board, depth, alpha, beta, is_maximizing):
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0:
            return self.evaluateBoard(board)
        
        if is_maximizing:  # White's turn (maximizing)
            max_eval = float('-inf')
            for i in range(8):
                for j in range(8):
                    piece = board[i][j]
                    if piece != ' ' and piece.isupper():  # White piece
                        moves = self.calculateMoves(board, i, j)
                        for move in moves:
                            # Make temporary move
                            ex, ey = move
                            temp_board = copy.deepcopy(board)
                            temp_board[ex][ey] = temp_board[i][j]
                            temp_board[i][j] = ' '
                            
                            # Recursive evaluation
                            eval = self.alphaBeta(temp_board, depth - 1, alpha, beta, False)
                            max_eval = max(max_eval, eval)
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break  # Beta cutoff
                        if beta <= alpha:
                            break
                if beta <= alpha:
                    break
            return max_eval
        else:  # Black's turn (minimizing)
            min_eval = float('inf')
            for i in range(8):
                for j in range(8):
                    piece = board[i][j]
                    if piece != ' ' and piece.islower():  # Black piece
                        moves = self.calculateMoves(board, i, j)
                        for move in moves:
                            # Make temporary move
                            ex, ey = move
                            temp_board = copy.deepcopy(board)
                            temp_board[ex][ey] = temp_board[i][j]
                            temp_board = copy.deepcopy(board)
                            temp_board[ex][ey] = temp_board[i][j]
                            temp_board[i][j] = ' '
                            
                            # Recursive evaluation
                            eval = self.alphaBeta(temp_board, depth - 1, alpha, beta, True)
                            min_eval = min(min_eval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                break  # Alpha cutoff
                        if beta <= alpha:
                            break
                if beta <= alpha:
                    break
            return min_eval
    
    def makeAIMove(self):
        """Use alpha-beta pruning to find the best move for the AI"""
        start_time = time.time()
        best_score = float('-inf') if self.turn == "white" else float('inf')
        best_move = None
        best_piece = None
        
        # For each piece of the current color
        for i in range(8):
            for j in range(8):
                piece = self.board.getPieceAt(i, j)
                if piece != ' ' and self.getPieceColor(piece) == self.turn:
                    # Find all possible moves for this piece
                    self.findPossibleMoves(i, j)
                    # Filter out moves that would leave/put the king in check
                    legal_moves = [move for move in self.possibleMoves if not self.moveIntoCheck((i, j), move)]
                    
                    for move in legal_moves:
                        # Create a temporary board to simulate the move
                        temp_board = copy.deepcopy(self.board.board)
                        ex, ey = move
                        temp_board[ex][ey] = temp_board[i][j]
                        temp_board[i][j] = ' '
                        
                        # Evaluate the move using alpha-beta pruning
                        if self.turn == "white":
                            score = self.alphaBeta(temp_board, self.ai_difficulty - 1, float('-inf'), float('inf'), False)
                            if score > best_score:
                                best_score = score
                                best_move = move
                                best_piece = (i, j)
                        else:
                            score = self.alphaBeta(temp_board, self.ai_difficulty - 1, float('-inf'), float('inf'), True)
                            if score < best_score:
                                best_score = score
                                best_move = move
                                best_piece = (i, j)
        
        # Execute the best move found
        if best_move and best_piece:
            # Set cursor to the selected piece
            self.x = self.board.cursorRow = best_piece[0]
            self.y = self.board.cursorCol = best_piece[1]
            self.render()
            time.sleep(0.5)  # Pause briefly to show the piece selection
            
            # Set cursor to the destination
            self.x = self.board.cursorRow = best_move[0]
            self.y = self.board.cursorCol = best_move[1]
            
            # Execute the move
            self.selectedPiece = best_piece
            self.findPossibleMoves(best_piece[0], best_piece[1])
            self.movePiece(best_piece, best_move)
            self.selectedPiece = None
            self.possibleMoves.clear()
            
            # Switch turns
            self.turn = "black" if self.turn == "white" else "white"
            
            # Check for check and checkmate
            self.check = self.isInCheck(self.turn)
            
            if self.isCheckmate(self.turn):
                self.checkmate = True
                self.render()
                winner = "White" if self.turn == "black" else "Black"
                print(f"Checkmate! {winner} wins!")
                self.gameOver = True
            elif self.isStalemate(self.turn):
                self.render()
                print("Stalemate! It's a draw.")
                self.gameOver = True
        else:
            print("AI couldn't find a valid move. Game ends in draw.")
            self.gameOver = True
        
        # Print AI thinking time
        end_time = time.time()
        print(f"AI move calculated in {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    # Ask player to choose a color
    print("Welcome to Chess with AI opponent!")
    while True:
        color = input("Do you want to play as white or black? (w/b): ").lower()
        if color in ['w', 'white']:
            play_as = "white"
            break
        elif color in ['b', 'black']:
            play_as = "black"
            break
        else:
            print("Invalid choice. Please enter 'w' or 'b'.")
    
    # Ask for difficulty level
    while True:
        try:
            difficulty = int(input("Choose AI difficulty (1-4, higher is stronger but slower): "))
            if 1 <= difficulty <= 4:
                break
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Start the game
    chess = Chess(play_as=play_as, difficulty=difficulty)
    chess.start()