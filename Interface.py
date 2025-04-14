import os
import keyboard
from Constants import CONST_YELLOW, CONST_RED, CONST_RESET
from Board import CONST_PIECES

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def listenInput(chess, key):
    if key == 'w':
        changePosition(chess, chess.x - 1, chess.y)
    elif key == 's':
        changePosition(chess, chess.x + 1, chess.y)
    elif key == 'a':
        changePosition(chess, chess.x, chess.y - 1)
    elif key == 'd':
        changePosition(chess, chess.x, chess.y + 1)
    elif key == 'enter':
        validateSelection(chess)
    elif key == 'q':
        chess.gameOver = True

def changePosition(chess, newX, newY):
    newX = max(0, min(newX, 7))
    newY = max(0, min(newY, 7))
    chess.x = chess.board.cursorRow = newX
    chess.y = chess.board.cursorCol = newY

def validateSelection(chess):
    piece = chess.board.getPieceAt(chess.x, chess.y)
    if not chess.selectedPiece:
        if piece != ' ' and chess.getPieceColor(piece) == chess.turn:
            chess.selectedPiece = (chess.x, chess.y)
            chess.possibleMoves = chess.findPossibleMoves(chess.x, chess.y)
            chess.possibleMoves = [move for move in chess.possibleMoves if not chess.moveIntoCheck(chess.selectedPiece, move)]
    else:
        if (chess.x, chess.y) in chess.possibleMoves:
            chess.enPassantTarget = chess.movePiece(chess.selectedPiece, (chess.x, chess.y))
            chess.selectedPiece = None
            chess.possibleMoves.clear()
            
            chess.turn = "black" if chess.turn == "white" else "white"
            
            chess.check = chess.isInCheck(chess.turn)
            
            if chess.isCheckmate(chess.turn):
                chess.checkmate = True
                render(chess)
                winner = "White" if chess.turn == "black" else "Black"
                print(f"Checkmate! {winner} wins!")
                chess.gameOver = True
            elif chess.isStalemate(chess.turn):
                render(chess)
                print("Stalemate! It's a draw.")
                chess.gameOver = True
            
            if chess.turn != chess.playAs and not chess.gameOver:
                chess.waitingForAi = True
        else:
            chess.selectedPiece = None
            chess.possibleMoves.clear()

def render(chess):
    clearScreen()
    chess.board.printBoard()
    print(f"Turn: {chess.turn.capitalize()} {'(AI)' if chess.turn != chess.playAs else '(You)'}")
    
    if chess.check:
        print(f"{CONST_RED}CHECK!{CONST_RESET}")
        
    if chess.selectedPiece:
        print(f"Selected: {chr(65 + chess.selectedPiece[1])}{8 - chess.selectedPiece[0]}")
    
    print(f"Captured by White: {' '.join(CONST_PIECES[p] for p in chess.capturedWhite) if chess.capturedWhite else 'None'}")
    print(f"Captured by Yellow: {' '.join(CONST_PIECES[p] for p in chess.capturedBlack) if chess.capturedBlack else 'None'}")
    
    print("Use WASD to move, Enter to select/move, Q to quit.")

    if chess.moveHistory:
        print(f"Last move: {chess.moveHistory[-1]}")

    if chess.selectedPiece:
        print("Possible moves:", end=' ')
        for move in chess.possibleMoves:
            mx, my = move
            print(f"{CONST_YELLOW}{chr(65 + my)}{8 - mx}{CONST_RESET}", end=' ')
        print()

def start(chess):
    render(chess)
    while not chess.gameOver:
        if chess.waitingForAi:
            render(chess)
            print("AI is thinking...")
            chess.makeAiMove()
            chess.waitingForAi = False
            render(chess)
            if chess.gameOver:
                break
        
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name.lower()
            listenInput(chess, key)
            render(chess)
    
    clearScreen()
    print("Game Over! Final board:")
    chess.board.printBoard()
    print("\nMove History:")
    for i, move in enumerate(chess.moveHistory):
        print(f"{i+1}. {move}")
    print("Press Q to quit")
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name.lower() == 'q':
            break    