import pygame as p
from Chess import Engine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_DIMENSION = HEIGHT // DIMENSION
MAX_FPS = 15
PIECES_TEXTURES = {}
CAPTURE_TEXTURE = None
CHECK_TEXTURE = None
MOVE_SOUND = None

checkmateKing = None
whiteKingFliped = None
blackKingFliped = None

PLAY_VS_COMPUTER = True

"""
Load the pieces textures into the PIECES_TEXTURES dictionary
"""

def loadSounds():

    global MOVE_SOUND

    MOVE_SOUND = p.mixer.Sound("Sounds/move.wav")

def loadTextures():
    global CAPTURE_TEXTURE
    global CHECK_TEXTURE
    global blackKingFliped
    global whiteKingFliped

    chessPieces = ["bP", "bR", "bN", "bB", "bQ", "bK", "wP", "wR", "wN", "wB", "wQ", "wK"]

    for chessPiece in chessPieces:
        PIECES_TEXTURES[chessPiece] = p.transform.scale(p.image.load("Chess Pieces/" + chessPiece + ".png"), (SQ_DIMENSION, SQ_DIMENSION))
        if chessPiece == "bK":
            blackKingFliped = p.transform.flip(PIECES_TEXTURES[chessPiece], False, True)
        if chessPiece == "wK":
            whiteKingFliped = p.transform.flip(PIECES_TEXTURES[chessPiece], False, True)


    CAPTURE_TEXTURE = p.transform.scale(p.image.load("Chess Pieces/captured.png"), (SQ_DIMENSION, SQ_DIMENSION))
    CHECK_TEXTURE = p.transform.scale(p.image.load("Chess Pieces/check.png"), (SQ_DIMENSION, SQ_DIMENSION))


def main():
    p.init()

    # Load Piece textures
    loadTextures()

    # Load the sound files
    loadSounds()

    drawGameModeOptions()

    # Choose game mode ( Player Vs Computer or Player vs Player)
    if PLAY_VS_COMPUTER:

        playerVsComputer()
    else:

        playOneVsOne()


def playOneVsOne():

    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    # Initialize game state
    gameState = Engine.GameState()
    print(gameState.board)

    running = True

    # The selected piece
    selectedPiece = None

    # Valid moves of the selected piece
    validMoves = []

    # Specifies if the player needs to select the piece that the pawn will be promoted to
    hasToPromote = False

    global checkmateKing
    while running:
        for event in p.event.get():

            if event.type == p.QUIT:
                running = False

            elif hasToPromote:

                drawGameState(screen, gameState, selectedPiece, validMoves)
                drawPromotionOptions(screen, gameState)

                if event.type == p.MOUSEBUTTONDOWN:
                    mousePos = p.mouse.get_pos()

                    row = mousePos[1]
                    col = mousePos[0]

                    piece = selectPromotedPiece(row, col)

                    if piece is not None:

                        color = Engine.BLACK
                        if not gameState.whiteToMove:
                            color = Engine.WHITE

                        hasToPromote = False
                        gameState.board[gameState.moveLog[-1].endRow][gameState.moveLog[-1].endCol] = color + piece
                        gameState.checkIfTheGameEnded()

            # Undo the last move if the U key is pressed
            elif event.type == p.KEYDOWN:
                if event.key == p.K_u:

                    gameState.undoMove()
                    gameState.checkIfTheGameEnded()

                    selectedPiece = None
                    validMoves = []

            # Mouse input handler
            elif event.type == p.MOUSEBUTTONDOWN and gameState.stalemate == False:
                mousePos = p.mouse.get_pos()

                row = mousePos[1] // SQ_DIMENSION
                col = mousePos[0] // SQ_DIMENSION

                if selectedPiece is None:
                    if (gameState.board[row][col] != Engine.EMPTY_SQUARE) and \
                            gameState.checkSelectedPiece(row, col):

                        selectedPiece = (row, col)

                        validMoves = gameState.getPieceValidMoves(selectedPiece[0], selectedPiece[1])
                        validMoves = validMoves[0] + validMoves[1]

                elif selectedPiece == (row, col): #deselect the piece if it is selected twice

                    selectedPiece = None
                    validMoves = []

                else:

                    destinationSquare = (row, col)

                    for validMove in validMoves:
                        if destinationSquare == (validMove.endRow, validMove.endCol):
                            print(validMove.getChessNotation())
                            gameState.makeMove(validMove)

                            selectedPiece = None
                            validMoves = []

                            if validMove.pawnPromotion is not None:

                                color = Engine.BLACK
                                if not gameState.whiteToMove:
                                    color = Engine.WHITE

                                gameState.board[gameState.moveLog[-1].endRow][gameState.moveLog[-1].endCol] = color + Engine.PAWN

                                hasToPromote = True

                            gameState.checkIfTheGameEnded()
                            MOVE_SOUND.play()
                            break

        if not hasToPromote:
            drawGameState(screen, gameState, selectedPiece, validMoves)

        clock.tick(MAX_FPS)
        p.display.flip()

def playerVsComputer():

    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    # Initialize game state
    gameState = Engine.GameState()
    print(gameState.board)

    running = True

    # The selected piece
    selectedPiece = None

    # Valid moves of the selected piece
    validMoves = []

    # Specifies if the player needs to select the piece that the pawn will be promoted to
    hasToPromote = False

    # Specifies the color of the player
    player = Engine.WHITE

    global checkmateKing
    while running:
        for event in p.event.get():

            if event.type == p.QUIT:
                running = False

            elif hasToPromote:

                drawGameState(screen, gameState, selectedPiece, validMoves)
                drawPromotionOptions(screen, gameState)

                if event.type == p.MOUSEBUTTONDOWN:
                    mousePos = p.mouse.get_pos()

                    row = mousePos[1]
                    col = mousePos[0]

                    piece = selectPromotedPiece(row, col)

                    if piece is not None:

                        color = Engine.BLACK
                        if not gameState.whiteToMove:
                            color = Engine.WHITE

                        hasToPromote = False
                        gameState.board[gameState.moveLog[-1].endRow][gameState.moveLog[-1].endCol] = color + piece
                        gameState.checkIfTheGameEnded()

            # Check if it's the AI's move
            elif ((not gameState.whiteToMove and player is Engine.WHITE) or \
                    (gameState.whiteToMove and player is Engine.BLACK)) and\
                    (gameState.stalemate == False and gameState.checkmateKing is None):

                # Select the best move for the AI
                #bestMove = gameState.selectBestMove()[0]
                #bestMove = gameState.miniMax(level=3)[0]
                bestMove = gameState.alphaBeta(level=3)[0]
                #bestMove = gameState.iterativeDeepening(maxLevel=3)[0]

                if bestMove is not None:
                    gameState.makeMove((bestMove))


                    # Play the move sound
                    MOVE_SOUND.play()

                # Check if the move ended the game
                gameState.checkIfTheGameEnded()

            # Undo the last move if the U key is pressed
            elif event.type == p.KEYDOWN:
                if event.key == p.K_u:

                    gameState.undoMove()
                    gameState.checkIfTheGameEnded()
                    gameState.undoMove()
                    gameState.checkIfTheGameEnded()

                    selectedPiece = None
                    validMoves = []

            # Mouse input handler
            elif event.type == p.MOUSEBUTTONDOWN and gameState.stalemate == False and gameState.checkmateKing is None:
                mousePos = p.mouse.get_pos()

                row = mousePos[1] // SQ_DIMENSION
                col = mousePos[0] // SQ_DIMENSION

                if selectedPiece is None:
                    if (gameState.board[row][col] != Engine.EMPTY_SQUARE) and \
                            gameState.checkSelectedPiece(row, col):
                        selectedPiece = (row, col)

                        validMoves = gameState.getPieceValidMoves(selectedPiece[0], selectedPiece[1])
                        validMoves = validMoves[0] + validMoves[1]

                elif selectedPiece == (row, col):  # deselect the piece if it is selected twice

                    selectedPiece = None
                    validMoves = []

                else:

                    destinationSquare = (row, col)

                    for validMove in validMoves:
                        if destinationSquare == (validMove.endRow, validMove.endCol):
                            print(validMove.getChessNotation())
                            gameState.makeMove(validMove)

                            selectedPiece = None
                            validMoves = []

                            if validMove.pawnPromotion is not None:

                                color = Engine.BLACK
                                if not gameState.whiteToMove:
                                    color = Engine.WHITE

                                gameState.board[gameState.moveLog[-1].endRow][
                                    gameState.moveLog[-1].endCol] = color + Engine.PAWN

                                hasToPromote = True

                            gameState.checkIfTheGameEnded()
                            MOVE_SOUND.play()
                            print(gameState.evaluatePosition())
                            break

        if not hasToPromote:
            drawGameState(screen, gameState, selectedPiece, validMoves)
        clock.tick(MAX_FPS)
        p.display.flip()

# This function creates a menu that allows the player to choose the piece that he wants to promote the pawn to
def selectPromotedPiece(row, col):

    if row >= 3 * SQ_DIMENSION and row <= 5 * SQ_DIMENSION:

        if col < 2 * SQ_DIMENSION:
            return Engine.KNIGHT

        elif col < 4 * SQ_DIMENSION:
            return Engine.BISHOP

        elif col < 6 * SQ_DIMENSION:
            return Engine.ROOK

        elif col < 8 * SQ_DIMENSION:
            return Engine.QUEEN

    return None

# This function draws a menu containing the promtion piece options (Knight, Bishop, Rook, Queen)
def drawPromotionOptions(screen, gameState):

    p.draw.rect(screen, p.Color("papayawhip"),
                p.Rect(0 * SQ_DIMENSION, 3 * SQ_DIMENSION, 8 * SQ_DIMENSION, 2 * SQ_DIMENSION))

    color = Engine.BLACK
    if not gameState.whiteToMove:
        color = Engine.WHITE

    screen.blit(PIECES_TEXTURES[color + Engine.KNIGHT], p.Rect(int(0.5 * SQ_DIMENSION), int(3.5 * SQ_DIMENSION), SQ_DIMENSION, SQ_DIMENSION))
    screen.blit(PIECES_TEXTURES[color + Engine.BISHOP], p.Rect(int(2.5 * SQ_DIMENSION), int(3.5 * SQ_DIMENSION), SQ_DIMENSION, SQ_DIMENSION))
    screen.blit(PIECES_TEXTURES[color + Engine.ROOK], p.Rect(int(4.5 * SQ_DIMENSION), int(3.5 * SQ_DIMENSION), SQ_DIMENSION, SQ_DIMENSION))
    screen.blit(PIECES_TEXTURES[color + Engine.QUEEN], p.Rect(int(6.5 * SQ_DIMENSION), int(3.5 * SQ_DIMENSION), SQ_DIMENSION, SQ_DIMENSION))


# Draw the board and the pieces
def drawGameState(screen, gameState, selectedPiece, validMoves):

    drawBoard(screen, selectedPiece, validMoves, gameState)
    drawPieces(screen, gameState.board, gameState)

# Draw the actual board
def drawBoard(screen, selectedPiece, validMoves, gameState):

    # Get references to the moveLog and the board
    moveLog = gameState.moveLog
    board = gameState.board

    # Define colors
    white = p.Color("white")
    black = p.Color("gray")
    highlight = (44, 140, 40)
    previousMoveHighlight = p.Color("green")

    # Get the last move if it exists
    lastMove = None
    if len(moveLog) != 0:
        lastMove = moveLog[-1]

    # Draw the board
    for row in range(DIMENSION):
        for col in range(DIMENSION):

            # Highlight the previous move
            if lastMove is not None:
                if (row, col) == (lastMove.startRow, lastMove.startCol) or\
                        (row, col) == (lastMove.endRow, lastMove.endCol):
                    p.draw.rect(screen, previousMoveHighlight,
                                p.Rect(col * SQ_DIMENSION, row * SQ_DIMENSION, SQ_DIMENSION, SQ_DIMENSION))
                    continue

            # Highlight the selected piece
            if (row, col) == selectedPiece:
                p.draw.rect(screen, highlight,
                            p.Rect(col * SQ_DIMENSION, row * SQ_DIMENSION, SQ_DIMENSION, SQ_DIMENSION))
                continue

            # Draw the black squares
            if (row + col) % 2 == 1:
                p.draw.rect(screen, black,
                            p.Rect(col * SQ_DIMENSION, row * SQ_DIMENSION, SQ_DIMENSION, SQ_DIMENSION))
            else:
                # Draw the white squares
                p.draw.rect(screen, white,
                            p.Rect(col * SQ_DIMENSION, row * SQ_DIMENSION, SQ_DIMENSION, SQ_DIMENSION))

    # Highlight possible moves and captures
    for move in validMoves:

        if board[move.endRow][move.endCol] != Engine.EMPTY_SQUARE:

            screen.blit(CAPTURE_TEXTURE,
                        p.Rect(move.endCol * SQ_DIMENSION, move.endRow * SQ_DIMENSION, SQ_DIMENSION, SQ_DIMENSION))

        elif move.enPassant == True:

            p.draw.circle(screen,
                          p.Color("blue"),
                          (int((move.endCol + 0.5) * SQ_DIMENSION), int((move.endRow + 0.5) * SQ_DIMENSION)),
                          SQ_DIMENSION // 8)

            screen.blit(CAPTURE_TEXTURE,
                        p.Rect(move.endCol * SQ_DIMENSION, move.startRow * SQ_DIMENSION, SQ_DIMENSION, SQ_DIMENSION))

        else:

            p.draw.circle(screen,
                          p.Color("blue"),
                          (int((move.endCol + 0.5) * SQ_DIMENSION), int((move.endRow + 0.5) * SQ_DIMENSION)),
                          SQ_DIMENSION // 8)

    # Highlight the check if it exists
    if gameState.whiteKingInCheck:
        screen.blit(CHECK_TEXTURE,
                    p.Rect(gameState.whiteKing[1] * SQ_DIMENSION, gameState.whiteKing[0] * SQ_DIMENSION, SQ_DIMENSION, SQ_DIMENSION))

    if gameState.blackKingInCheck:
        screen.blit(CHECK_TEXTURE,
                    p.Rect(gameState.blackKing[1] * SQ_DIMENSION, gameState.blackKing[0] * SQ_DIMENSION, SQ_DIMENSION, SQ_DIMENSION))


# Draw the pieces from the current gamestate
def drawPieces(screen,  board, gamestate):

    for row in range(DIMENSION):
        for col in range(DIMENSION):

            piece = board[row][col]

            if gamestate.checkmateKing is not None and gamestate.checkmateKing == piece:
                if gamestate.getColorOfPiece(gamestate.checkmateKing) == Engine.WHITE:
                    screen.blit(whiteKingFliped,
                                p.Rect(col * SQ_DIMENSION, row * SQ_DIMENSION, SQ_DIMENSION, SQ_DIMENSION))
                else:
                    screen.blit(blackKingFliped,
                                p.Rect(col * SQ_DIMENSION, row * SQ_DIMENSION, SQ_DIMENSION, SQ_DIMENSION))
                continue

            if piece != Engine.EMPTY_SQUARE:
                screen.blit(PIECES_TEXTURES[piece], p.Rect(col * SQ_DIMENSION, row * SQ_DIMENSION, SQ_DIMENSION, SQ_DIMENSION))

def drawGameModeOptions():

    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    # Initialize game state
    gameState = Engine.GameState()
    print(gameState.board)

    running = True
    while(running):

        for event in p.event.get():

            if event.type == p.QUIT:
                running = False

            if event.type == p.MOUSEBUTTONDOWN:
                mousePos = p.mouse.get_pos()

                row = mousePos[1]
                col = mousePos[0]

                selectGameModeOption(row, col)
                running = False

        drawBoard(screen, selectedPiece=None, validMoves=[], gameState=gameState)

        p.font.init()
        myfont = p.font.SysFont('calibri', 90)

        vsPlayer = myfont.render('VS Player', True, (0, 0, 0))
        vsPlayer = p.transform.rotate(vsPlayer, -90)

        screen.blit(vsPlayer, (int(1.5 * SQ_DIMENSION), int(1.5 * SQ_DIMENSION)))

        vsComputer = myfont.render('VS Computer', True, (0, 0, 0))
        vsComputer = p.transform.rotate(vsComputer, -90)

        screen.blit(vsComputer, (int(5.5 * SQ_DIMENSION), int(0.25 * SQ_DIMENSION)))

        clock.tick(MAX_FPS)
        p.display.flip()

def selectGameModeOption(row, col):

    global PLAY_VS_COMPUTER

    if col < 4 * SQ_DIMENSION:

        PLAY_VS_COMPUTER = False
        return

    PLAY_VS_COMPUTER = True

if __name__ == "__main__":
    main()