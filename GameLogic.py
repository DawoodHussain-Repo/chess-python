import copy
from MoveLogic import getPieceColor, calculateMoves, findPossibleMoves

def isInCheck(board, color):
    king = 'K' if color == "white" else 'k'
    kingPos = None
    for i in range(8):
        for j in range(8):
            if board.getPieceAt(i, j) == king:
                kingPos = (i, j)
                break
        if kingPos:
            break
    
    if not kingPos:
        return False
    
    opponentColor = "black" if color == "white" else "white"
    for i in range(8):
        for j in range(8):
            piece = board.getPieceAt(i, j)
            if piece != ' ' and getPieceColor(piece) == opponentColor:
                moves = findPossibleMoves(board, i, j)
                if kingPos in moves:
                    return True
    
    return False

def isCheckmate(board, color, enPassantTarget):
    if not isInCheck(board, color):
        return False
    
    for x in range(8):
        for y in range(8):
            piece = board.getPieceAt(x, y)
            if piece != ' ' and getPieceColor(piece) == color:
                moves = findPossibleMoves(board, x, y, enPassantTarget)
                for move in moves:
                    if not moveIntoCheck(board, (x, y), move):
                        return False
    
    return True

def isStalemate(board, color, enPassantTarget):
    if isInCheck(board, color):
        return False
        
    for x in range(8):
        for y in range(8):
            piece = board.getPieceAt(x, y)
            if piece != ' ' and getPieceColor(piece) == color:
                moves = findPossibleMoves(board, x, y, enPassantTarget)
                legalMoves = [move for move in moves if not moveIntoCheck(board, (x, y), move)]
                if legalMoves:
                    return False
    return True

def moveIntoCheck(board, start, end):
    tempBoard = copy.deepcopy(board.board)
    
    sx, sy = start
    piece = board.getPieceAt(sx, sy)
    color = getPieceColor(piece)
    
    ex, ey = end
    target = board.getPieceAt(ex, ey)
    opponent_king = 'k' if color == "white" else 'K'
    if target == opponent_king:
        return True  # Prevent move that captures the king
    
    tempBoard[ex][ey] = tempBoard[sx][sy]
    tempBoard[sx][sy] = ' '
    
    king = 'K' if color == "white" else 'k'
    kingPos = None
    for i in range(8):
        for j in range(8):
            if tempBoard[i][j] == king:
                kingPos = (i, j)
                break
        if kingPos:
            break
    
    if not kingPos:
        return False
    
    opponentColor = "black" if color == "white" else "white"
    for i in range(8):
        for j in range(8):
            piece = tempBoard[i][j]
            if piece != ' ' and getPieceColor(piece) == opponentColor:
                moves = calculateMoves(tempBoard, i, j)
                if kingPos in moves:
                    return True
    
    return False