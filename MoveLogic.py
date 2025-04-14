from Board import Board

def getPieceColor(piece):
    if piece.islower():
        return "black"
    elif piece.isupper():
        return "white"
    return None

def findPossibleMoves(board, x, y, enPassantTarget=None):
    possibleMoves = []
    piece = board.getPieceAt(x, y)
    color = getPieceColor(piece)

    if piece.lower() == 'p':
        direction = -1 if color == "white" else 1
        startRow = 6 if color == "white" else 1

        nx, ny = x + direction, y
        if 0 <= nx < 8 and board.getPieceAt(nx, ny) == ' ':
            possibleMoves.append((nx, ny))

            if x == startRow:
                nx2 = nx + direction
                if 0 <= nx2 < 8 and board.getPieceAt(nx2, ny) == ' ':
                    possibleMoves.append((nx2, ny))

        for dy in [-1, 1]:
            cx, cy = x + direction, y + dy
            if 0 <= cx < 8 and 0 <= cy < 8:
                target = board.getPieceAt(cx, cy)
                if target != ' ' and getPieceColor(target) != color:
                    possibleMoves.append((cx, cy))

                if enPassantTarget == (cx, cy):
                    possibleMoves.append((cx, cy))

    elif piece.lower() == 'r':
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x, y
            while 0 <= nx + dx < 8 and 0 <= ny + dy < 8:
                nx += dx
                ny += dy
                target = board.getPieceAt(nx, ny)
                if target == ' ':
                    possibleMoves.append((nx, ny))
                elif getPieceColor(target) != color:
                    possibleMoves.append((nx, ny))
                    break
                else:
                    break

    elif piece.lower() == 'n':
        knightMoves = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2)]
        for dx, dy in knightMoves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board.getPieceAt(nx, ny)
                if target == ' ' or getPieceColor(target) != color:
                    possibleMoves.append((nx, ny))

    elif piece.lower() == 'b':
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            nx, ny = x, y
            while 0 <= nx + dx < 8 and 0 <= ny + dy < 8:
                nx += dx
                ny += dy
                target = board.getPieceAt(nx, ny)
                if target == ' ':
                    possibleMoves.append((nx, ny))
                elif getPieceColor(target) != color:
                    possibleMoves.append((nx, ny))
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
                target = board.getPieceAt(nx, ny)
                if target == ' ':
                    possibleMoves.append((nx, ny))
                elif getPieceColor(target) != color:
                    possibleMoves.append((nx, ny))
                    break
                else:
                    break

    elif piece.lower() == 'k':
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board.getPieceAt(nx, ny)
                if target == ' ' or getPieceColor(target) != color:
                    possibleMoves.append((nx, ny))

    return possibleMoves

def calculateMoves(board, x, y):
    moves = []
    piece = board[x][y]
    color = getPieceColor(piece)

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
                target = board[nx][ny]
                if target != ' ' and getPieceColor(target) != color:
                    moves.append((cx, cy))

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
                elif getPieceColor(target) != color:
                    moves.append((nx, ny))
                    break
                else:
                    break

    elif piece.lower() == 'n':
        knightMoves = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2)]
        for dx, dy in knightMoves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[nx][ny]
                if target == ' ' or getPieceColor(target) != color:
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
                elif getPieceColor(target) != color:
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
                elif getPieceColor(target) != color:
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
                if target == ' ' or getPieceColor(target) != color:
                    moves.append((nx, ny))

    return moves

def movePiece(board, start, end, enPassantTarget, capturedWhite, capturedBlack, moveHistory):
    sx, sy = start
    ex, ey = end
    movingPiece = board.getPieceAt(sx, sy)
    targetPiece = board.getPieceAt(ex, ey)

    if movingPiece.lower() == 'p' and (ex, ey) == enPassantTarget:
        if getPieceColor(movingPiece) == "white":
            captured = board.getPieceAt(ex + 1, ey)
            capturedBlack.append(captured)
            board.board[ex + 1][ey] = ' '
        else:
            captured = board.getPieceAt(ex - 1, ey)
            capturedWhite.append(captured)
            board.board[ex - 1][ey] = ' '

    elif targetPiece != ' ':
        if getPieceColor(targetPiece) == "white":
            capturedWhite.append(targetPiece)
        else:
            capturedBlack.append(targetPiece)

    board.board[ex][ey] = movingPiece
    board.board[sx][sy] = ' '

    newEnPassantTarget = None
    if movingPiece.lower() == 'p' and abs(ex - sx) == 2:
        newEnPassantTarget = ((sx + ex) // 2, sy)

    moveHistory.append(f"{movingPiece}: {chr(65 + sy)}{8 - sx} → {chr(65 + ey)}{8 - ex}")

    return newEnPassantTarget