import copy
from Constants import (
    CONST_PIECE_VALUES, CONST_PAWN_TABLE, CONST_KNIGHT_TABLE,
    CONST_BISHOP_TABLE, CONST_ROOK_TABLE, CONST_QUEEN_TABLE, CONST_KING_TABLE
)
from MoveLogic import calculateMoves, getPieceColor, findPossibleMoves
from GameLogic import isCheckmate
from Interface import render

def flipTable(table):
    return table[::-1]

def evaluateBoard(board):
    score = 0
    
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece != ' ':
                score += CONST_PIECE_VALUES[piece]
                
                if piece.lower() == 'p':
                    if piece.isupper():
                        score += CONST_PAWN_TABLE[i][j] * 0.1
                    else:
                        score -= flipTable(CONST_PAWN_TABLE)[i][j] * 0.1
                elif piece.lower() == 'n':
                    if piece.isupper():
                        score += CONST_KNIGHT_TABLE[i][j] * 0.1
                    else:
                        score -= flipTable(CONST_KNIGHT_TABLE)[i][j] * 0.1
                elif piece.lower() == 'b':
                    if piece.isupper():
                        score += CONST_BISHOP_TABLE[i][j] * 0.1
                    else:
                        score -= flipTable(CONST_BISHOP_TABLE)[i][j] * 0.1
                elif piece.lower() == 'r':
                    if piece.isupper():
                        score += CONST_ROOK_TABLE[i][j] * 0.1
                    else:
                        score -= flipTable(CONST_ROOK_TABLE)[i][j] * 0.1
                elif piece.lower() == 'q':
                    if piece.isupper():
                        score += CONST_QUEEN_TABLE[i][j] * 0.1
                    else:
                        score -= flipTable(CONST_QUEEN_TABLE)[i][j] * 0.1
                elif piece.lower() == 'k':
                    if piece.isupper():
                        score += CONST_KING_TABLE[i][j] * 0.1
                    else:
                        score -= flipTable(CONST_KING_TABLE)[i][j] * 0.1
    
    return score

def alphaBeta(board, depth, alpha, beta, isMaximizing, chess):
    opponent_color = "black" if isMaximizing else "white"
    if isCheckmate(chess.board, opponent_color, chess.enPassantTarget):
        return float('inf') if isMaximizing else float('-inf')
    
    if depth == 0:
        return evaluateBoard(board)
    
    if isMaximizing:
        maxEval = float('-inf')
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece != ' ' and piece.isupper():
                    moves = calculateMoves(board, i, j)
                    for move in moves:
                        ex, ey = move
                        if board[ex][ey] != 'k': 
                            tempBoard = copy.deepcopy(board)
                            tempBoard[ex][ey] = tempBoard[i][j]
                            tempBoard[i][j] = ' '
                            
                            eval = alphaBeta(tempBoard, depth - 1, alpha, beta, False, chess)
                            maxEval = max(maxEval, eval)
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float('inf')
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece != ' ' and piece.islower():
                    moves = calculateMoves(board, i, j)
                    for move in moves:
                        ex, ey = move
                        if board[ex][ey] != 'K': 
                            tempBoard = copy.deepcopy(board)
                            tempBoard[ex][ey] = tempBoard[i][j]
                            tempBoard[i][j] = ' '
                            
                            eval = alphaBeta(tempBoard, depth - 1, alpha, beta, True, chess)
                            minEval = min(minEval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                break
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        return minEval

def makeAiMove(chess):
    bestScore = float('-inf') if chess.turn == "white" else float('inf')
    bestMove = None
    bestPiece = None
    opponent_king = 'k' if chess.turn == "white" else 'K'
    
    for i in range(8):
        for j in range(8):
            piece = chess.board.getPieceAt(i, j)
            if piece != ' ' and getPieceColor(piece) == chess.turn:
                moves = findPossibleMoves(chess.board, i, j, chess.enPassantTarget)
                legalMoves = [move for move in moves if not chess.moveIntoCheck((i, j), move)]
                
                for move in legalMoves:
                    ex, ey = move
                    if chess.board.getPieceAt(ex, ey) != opponent_king:
                        tempBoard = copy.deepcopy(chess.board.board)
                        tempBoard[ex][ey] = tempBoard[i][j]
                        tempBoard[i][j] = ' '
                        
                        score = alphaBeta(tempBoard, chess.aiDifficulty - 1, float('-inf'), float('inf'), chess.turn != "white", chess)
                        if chess.turn == "white" and score > bestScore:
                            bestScore = score
                            bestMove = move
                            bestPiece = (i, j)
                        elif chess.turn == "black" and score < bestScore:
                            bestScore = score
                            bestMove = move
                            bestPiece = (i, j)
    
    if bestMove and bestPiece:
        chess.x = chess.board.cursorRow = bestPiece[0]
        chess.y = chess.board.cursorCol = bestPiece[1]
        render(chess)
        
        chess.x = chess.board.cursorRow = bestMove[0]
        chess.y = chess.board.cursorCol = bestMove[1]
        
        chess.selectedPiece = bestPiece
        moves = findPossibleMoves(chess.board, bestPiece[0], bestPiece[1], chess.enPassantTarget)
        chess.possibleMoves = moves
        chess.enPassantTarget = chess.movePiece(bestPiece, bestMove)
        chess.selectedPiece = None
        chess.possibleMoves.clear()
        
        chess.turn = "black" if chess.turn == "white" else "white"
        
        chess.check = chess.isInCheck(chess.turn)
        
        if chess.isCheckmate(chess.turn):
            chess.checkmate = True
            render(chess)
            winner = "White" if chess.turn == "black" else "Yellow"
            print(f"Checkmate! {winner} wins!")
            chess.gameOver = True
        elif chess.isStalemate(chess.turn):
            render(chess)
            print("Stalemate! It's a draw.")
            chess.gameOver = True
    else:
        print("AI couldn't find a valid move. Game ends in draw.")
        chess.gameOver = True