import numpy as np
import random

EMPTY_SQUARE = '--'
WHITE = 'w'
BLACK = 'b'

KING = 'K'
ROOK = 'R'
KNIGHT = 'N'
BISHOP = 'B'
QUEEN = 'Q'
PAWN = 'P'

KING_VALUE = 900
QUEEN_VALUE = 90
ROOK_VALUE = 50
BISHOP_VALUE = 30
KNIGHT_VALUE = 30
PAWN_VALUE = 10

PROMOTION_PIECES = [ROOK, KNIGHT, BISHOP, QUEEN]
#PROMOTION_PIECES = [QUEEN]

class GameState():

    def __init__(self):

        self.board = np.array([[BLACK + ROOK, BLACK + KNIGHT, BLACK + BISHOP, BLACK + QUEEN, BLACK + KING, BLACK + BISHOP, BLACK + KNIGHT, BLACK + ROOK],
                              [BLACK + PAWN, BLACK + PAWN, BLACK + PAWN, BLACK + PAWN, BLACK + PAWN, BLACK + PAWN, BLACK + PAWN, BLACK + PAWN],
                              [EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE],
                              [EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE],
                              [EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE],
                              [EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE],
                              [WHITE + PAWN, WHITE + PAWN, WHITE + PAWN, WHITE + PAWN, WHITE + PAWN, WHITE + PAWN, WHITE + PAWN, WHITE + PAWN],
                              [WHITE + ROOK, WHITE + KNIGHT, WHITE + BISHOP, WHITE + QUEEN, WHITE + KING, WHITE + BISHOP, WHITE + KNIGHT, WHITE + ROOK]
                              ])


        # Keeps track of the moves that are being made
        self.moveLog = []

        # Indicates who's turn it is
        self.whiteToMove = True

        # Indicates if the game ended in a stalemate
        self.stalemate = False

        # Indicates which king has been checkmated (None, WHITE, BLACK)
        self.checkmateKing = None

        # Position of White King
        self.whiteKing = (7, 4)
        # Shows if the white king moved or not(necessary for castling)
        self.whiteKingMoved = 0

        # Position of White Left Rook
        self.whiteRookLeft = (7, 0)
        # Shows if the left white rook moved or not(necessary for castling)
        self.whiteRookLeftMoved = 0

        # Position of White Right Rook
        self.whiteRookRight = (7, 7)
        # Shows if the right white rook moved or not(necessary for castling)
        self.whiteRookRightMoved = 0

        # Shows if the white king is in check
        self.whiteKingInCheck = False


        # Position of Black King
        self.blackKing = (0, 4)
        # Shows if the black king moved or not(necessary for castling)
        self.blackKingMoved = 0

        # Position of Black Left Rook
        self.blackRookLeft = (0, 0)
        # Shows if the left black rook moved or not(necessary for castling)
        self.blackRookLeftMoved = 0

        # Position of Black Right Rook
        self.blackRookRight = (0, 7)
        # Shows if the right black rook moved or not(necessary for castling)
        self.blackRookRightMoved = 0

        # Shows if the black king is in check
        self.blackKingInCheck = False

    # Selects the move that maximizes the score of the current player and return that move
    # and the asociated score => (bestMove, bestScore)
    def selectBestMove(self, alphaBeta = None):

        validMoves = self.calculateAllValidMoves()

        if len(validMoves) != 0:

            # The color that the current player plays with
            color = WHITE if self.whiteToMove else BLACK

            # White wants to maximize it's score and black wants to minimize it
            f = max if color == WHITE else min

            # Variables that will keep track of the best score and best move
            bestMove = None
            bestScore = -999999 if color == WHITE else 999999

            # A list of moves that generate the same best score
            bestMoves = []

            for move in validMoves:

                # Make the move
                self.makeMove(move)

                # Evaluate the position
                score = self.evaluatePosition()

                # Undo the move
                self.undoMove()

                if f(score, bestScore) == score:
                # Check if this is the best move

                    # If another move existed that generated the same best score
                    # add this move to the best moves list, else reset the best score
                    # best move and best moves.
                    if score == bestScore:

                        bestMoves.append(move)

                    else:

                        bestMoves = [move]
                        bestScore = score
                        bestMove = move

                # Alpha beta pruning
                if alphaBeta is not None and f(alphaBeta, score) == score:
                        break

            # If more than one best move exists return a random one
            if len(bestMoves) > 1:

                return (random.choice(bestMoves), bestScore)

            # Return the best move
            return (bestMove, bestScore)

        # Loss reward
        lossScore = -999999 if self.whiteToMove else 999999

        return (None, lossScore)

    # Minimax for choosing a move
    def miniMax(self, level):

        if level == 1:

            (bestMove, bestScore) = self.selectBestMove()
            return (bestMove, bestScore)

        else:

            # The color that the current player plays with
            color = WHITE if self.whiteToMove else BLACK

            # WHITE => max, BLACK => min
            f = max if self.whiteToMove else min

            # Loss reward
            lossScore = -999999 if self.whiteToMove else 999999

            # The list of valid moves that the current player can make
            validMoves = self.calculateAllValidMoves()

            # If the current player has no valid moves then it has lost
            if len(validMoves) == 0:

                return (None, lossScore)

            # Variables that will keep track of the best score and best move
            bestMove = None
            bestScore = -999999 if color == WHITE else 999999

            # A list of moves that generate the same best score
            bestMoves = []

            for move in validMoves:

                # Make the move
                self.makeMove(move)

                # Ascend further into the tree
                (childMove, childScore) = self.miniMax(level - 1)

                # Undo the move
                self.undoMove()

                # Check if this is the best move
                if f(childScore, bestScore) == childScore:

                    # If another move existed that generated the same best score
                    # add this move to the best moves list, else reset the best score
                    # best move and best moves.
                    if childScore == bestScore:

                        bestMoves.append(move)

                    else:

                        bestMoves = [move]
                        bestScore = childScore
                        bestMove = move

            # If more than one best move exists return a random one
            if len(bestMoves) > 1:

                return (random.choice(bestMoves), bestScore)

            # Return the best move
            return (bestMove, bestScore)

    # Alpha beta prunning for choosing a move
    def alphaBeta(self, level, alphaBeta = None):

        if level == 1:

            (bestMove, bestScore) = self.selectBestMove(alphaBeta=alphaBeta)
            return (bestMove, bestScore)

        else:

            # The color that the current player plays with
            color = WHITE if self.whiteToMove else BLACK

            # WHITE => max, BLACK => min
            f = max if self.whiteToMove else min

            # Loss reward
            lossScore = -999999 if self.whiteToMove else 999999

            # The list of valid moves that the current player can make
            validMoves = self.calculateAllValidMoves()

            # If the current player has no valid moves then it has lost
            if len(validMoves) == 0:
                return (None, lossScore)

            # Variables that will keep track of the best score and best move
            bestMove = None
            bestScore = -999999 if color == WHITE else 999999

            # A list of moves that generate the same best score
            bestMoves = []

            for move in validMoves:

                # Make the move
                self.makeMove(move)

                # Ascend further into the tree
                (childMove, childScore) = self.alphaBeta(level - 1, alphaBeta=bestScore)

                # Undo the move
                self.undoMove()

                # Check if this is the best move
                if f(childScore, bestScore) == childScore:

                    # If another move existed that generated the same best score
                    # add this move to the best moves list, else reset the best score
                    # best move and best moves.
                    if childScore == bestScore:

                        bestMoves.append(move)

                    else:

                        bestMoves = [move]
                        bestScore = childScore
                        bestMove = move

                if alphaBeta is not None and f(alphaBeta, bestScore) == bestScore:
                    break

            # If more than one best move exists return a random one
            if len(bestMoves) > 1:
                return (random.choice(bestMoves), bestScore)

            # Return the best move
            return (bestMove, bestScore)

    # Gradually increase the depth of the search
    def iterativeDeepening(self, maxLevel = 4):

        # WHITE => max, BLACK => min
        f = max if self.whiteToMove else min

        alphaBeta = -999999 if self.whiteToMove else 999999
        bestMove = None

        for level in range(1, maxLevel + 1):

            (bestMoveAtLevel, bestScoreAtLevel) = self.alphaBeta(level=level, alphaBeta=alphaBeta)

            if f(bestScoreAtLevel, alphaBeta) == bestScoreAtLevel:

                alphaBeta = bestScoreAtLevel
                bestMove = bestMoveAtLevel

        return (bestMove, alphaBeta)

    # Evaluate the position
    # Positive score is in favor of white and negative score is in favor of black
    def evaluatePosition(self):

        score = 0

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):

                if self.board[row][col] != EMPTY_SQUARE:
                    score += self.getValueOfPiece(self.board[row][col])

        return score

    # Return the value of a piece
    def getValueOfPiece(self, piece):

        # White will have positive piece value and black will have negative piece value
        multiplier = 1
        if self.getColorOfPiece(piece) == BLACK:

            multiplier = -1

        # Return value of pawn
        if self.getTypeOfPiece(piece) == PAWN:

            return multiplier * PAWN_VALUE

        # Return value of knight
        if self.getTypeOfPiece(piece) == KNIGHT:
            return multiplier * KNIGHT_VALUE

        # Return value of bishop
        if self.getTypeOfPiece(piece) == BISHOP:
            return multiplier * BISHOP_VALUE

        # Return value of rook
        if self.getTypeOfPiece(piece) == ROOK:
            return multiplier * ROOK_VALUE

        # Return value of queen
        if self.getTypeOfPiece(piece) == QUEEN:
            return multiplier * QUEEN_VALUE

        # Return value of king
        if self.getTypeOfPiece(piece) == KING:
            return multiplier * KING_VALUE

    # Calculates all the valid moves of the current player
    def calculateAllValidMoves(self):

        # Color of the current player
        color = WHITE if self.whiteToMove else BLACK

        # List of capure moves
        captureMoves = []
        # Lis of non capture moves
        nonCaptureMoves = []

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):

                if self.getColorOfPiece(self.board[row][col]) == color:

                    #validMoves += (self.getPieceValidMoves(row, col))
                    (captureMovesForPiece, nonCaptureMovesForPiece) = self.getPieceValidMoves(row, col)
                    captureMoves += captureMovesForPiece
                    nonCaptureMoves += nonCaptureMovesForPiece

        return captureMoves + nonCaptureMoves

    # Checks if the current player selected one of his pieces
    def checkSelectedPiece(self, row, col):

        if self.whiteToMove and self.board[row][col][0] == "w":
            return True

        if not self.whiteToMove and self.board[row][col][0] == "b":
            return True

    # Make the corresponding move
    def makeMove(self, move):

        # Check if the moved piece is a King
        if self.getTypeOfPiece(move.movedPiece) == KING:

            if self.getColorOfPiece(move.movedPiece) == WHITE:

                # The white king moved
                self.whiteKingMoved += 1

                # Adjust the position of the white king
                self.whiteKing = (move.endRow, move.endCol)

            else:

                # The black king moved
                self.blackKingMoved += 1

                # Adjust the position of the black king
                self.blackKing = (move.endRow, move.endCol)

        # Check if the moved piece is a Rook
        if self.getTypeOfPiece(move.movedPiece) == ROOK:

            if self.getColorOfPiece(move.movedPiece) == WHITE:

                # A white rook moved
                if self.whiteRookLeft == (move.startRow, move.startCol):

                    # Adjust the number of times the white left rook moved
                    self.whiteRookLeftMoved += 1

                    self.whiteRookLeft = (move.endRow, move.endCol)

                if self.whiteRookRight == (move.startRow, move.startCol):

                    # Adjust the number of times the white right rook moved
                    self.whiteRookRightMoved += 1

                    # Adjust the position of the right white rook
                    self.whiteRookRight = (move.endRow, move.endCol)


            else:

                # A black rook moved
                if self.blackRookLeft == (move.startRow, move.startCol):

                    # Adjust the number of times the white left rook moved
                    self.blackRookLeftMoved += 1

                    self.blackRookLeft = (move.endRow, move.endCol)

                if self.blackRookRight == (move.startRow, move.startCol):

                    # Adjust the number of times the white right rook moved
                    self.blackRookRightMoved += 1

                    # Adjust the position of the right white rook
                    self.blackRookRight = (move.endRow, move.endCol)

        # Move the piece
        self.board[move.endRow][move.endCol] = move.movedPiece
        self.board[move.startRow][move.startCol] = EMPTY_SQUARE

        # Check if the move was an En Passant pawn move
        if move.enPassant == True:
            self.board[move.startRow][move.endCol] = EMPTY_SQUARE

        # Check if the move was a pawn promoting
        if move.pawnPromotion is not None:
            self.board[move.endRow][move.endCol] = move.pawnPromotion

        # Check if the move is a castle long move
        if move.castle == 2:

            # Get color of the king
            kingColor = self.getColorOfPiece(self.board[move.endRow][move.endCol])

            # Move the Rook
            self.board[move.startRow][move.startCol - 4] = EMPTY_SQUARE
            self.board[move.startRow][move.startCol - 1] = kingColor + ROOK

        # Check if the move is a castle short move
        if move.castle == 1:

            # Get color of the king
            kingColor = self.getColorOfPiece(self.board[move.endRow][move.endCol])

            # Move the Rook
            self.board[move.startRow][move.startCol + 3] = EMPTY_SQUARE
            self.board[move.startRow][move.startCol + 1] = kingColor + ROOK

        # Keep track of the moves
        self.moveLog.append((move))

        # Give the move to the other player
        self.whiteToMove = not self.whiteToMove

    # Undo the last move
    def undoMove(self):

        # If there are no prior moves there is nothing to be done
        if len(self.moveLog) == 0:

            return

        # If we undo a move then no king is checkmated
        self.checkmateKing = None

        if len(self.moveLog) != 0:
            # Get last move
            move = self.moveLog.pop()

            # Put pieces back on the board
            self.board[move.startRow][move.startCol] = move.movedPiece

            # Check if the move was a pawn promoting
            if move.pawnPromotion is not None:
                self.board[move.startRow][move.startCol] = self.getColorOfPiece(move.pawnPromotion) + PAWN

            # Check if the move was an En Passant pawn move
            if move.enPassant == True:
                self.board[move.startRow][move.endCol] = move.capturedPiece
                self.board[move.endRow][move.endCol] = EMPTY_SQUARE
            else:
                self.board[move.endRow][move.endCol] = move.capturedPiece

            # Check if the move is a castle long move
            if move.castle == 2:
                
                # Get color of the king
                kingColor = self.getColorOfPiece(self.board[move.startRow][move.startCol])

                # Move the Rook back
                self.board[move.startRow][move.startCol - 4] = kingColor + ROOK
                self.board[move.startRow][move.startCol - 1] = EMPTY_SQUARE

            # Check if the move is a castle short move
            if move.castle == 1:

                # Get color of the king
                kingColor = self.getColorOfPiece(self.board[move.startRow][move.startCol])

                # Move the Rook back
                self.board[move.startRow][move.startCol + 3] = kingColor + ROOK
                self.board[move.startRow][move.startCol + 1] = EMPTY_SQUARE

            # Give control to the other player
            self.whiteToMove = not self.whiteToMove

            # Check if the moved piece was a King
            if self.getTypeOfPiece(move.movedPiece) == KING:

                if self.getColorOfPiece(move.movedPiece) == WHITE:

                    # The white king moved
                    self.whiteKingMoved -= 1

                    # Adjust the position of the white king
                    self.whiteKing = (move.startRow, move.startCol)
                else:

                    # The black king moved
                    self.blackKingMoved -= 1

                    # Adjust the position of the black king
                    self.blackKing = (move.startRow, move.startCol)

        # Check if the moved piece is a Rook
        if self.getTypeOfPiece(move.movedPiece) == ROOK:

            if self.getColorOfPiece(move.movedPiece) == WHITE:

                # A white rook moved
                if self.whiteRookLeft == (move.endRow, move.endCol):

                    # Adjust the number of times the white left rook moved
                    self.whiteRookLeftMoved -= 1

                    self.whiteRookLeft = (move.startRow, move.startCol)

                if self.whiteRookRight == (move.endRow, move.endCol):

                    # Adjust the number of times the white right rook moved
                    self.whiteRookRightMoved -= 1

                    # Adjust the position of the right white rook
                    self.whiteRookRight = (move.startRow, move.startCol)


            else:

                # A black rook moved
                if self.blackRookLeft == (move.endRow, move.endCol):

                    # Adjust the number of times the white left rook moved
                    self.blackRookLeftMoved -= 1

                    self.blackRookLeft = (move.startRow, move.startCol)

                if self.blackRookRight == (move.endRow, move.endCol):

                    # Adjust the number of times the white right rook moved
                    self.blackRookRightMoved -= 1

                    # Adjust the position of the right white rook
                    self.blackRookRight = (move.startRow, move.startCol)


    # Returns the possible moves(including illegal moves that will put the player in check)
    def getPiecePossilbleMoves(self, row, col):

        pieceType = self.board[row][col][1]

        possibleMoves = []

        if pieceType == 'P':
            possibleMoves = self.getPawnMoves(row, col)

        elif pieceType == "R":
            possibleMoves = self.getRookMoves(row, col)

        elif pieceType == "N":
            possibleMoves = self.getKnightMoves(row, col)

        elif pieceType == "B":
            possibleMoves = self.getBishopMoves(row, col)

        elif pieceType == "Q":
            possibleMoves = self.getQueenMoves(row, col)

        elif pieceType == "K":
            possibleMoves = self.getKingMoves(row, col)

        return possibleMoves

    # Returns the possible moves(excluding illegal moves that will put the player in check)
    def getPieceValidMoves(self, row, col):

        # Color of the moved piece
        pieceColor = self.getColorOfPiece(self.board[row][col])

        # Get all the possible moves that a piece can make
        possibleMoves = self.getPiecePossilbleMoves(row, col)

        # List of capture moves
        captureMoves = []
        # List of non capture moves
        nonCaptureMoves = []

        # Eliminate the moves that put the king in check
        for move in possibleMoves:

            # Make the move
            self.makeMove(move)

            # Check if the move left the same colored king in check
            inCheck = self.checkIfInCheck(pieceColor)

            # Undo the move
            self.undoMove()

            if not inCheck:
                #validMoves.append(move)

                if move.capturedPiece != EMPTY_SQUARE:
                    captureMoves.append(move)
                else:
                    nonCaptureMoves.append(move)

        return (captureMoves, nonCaptureMoves)

    # Checks if the piece is being moved on an empty sqaure or if it captures a piece of the opposite color
    # Return 0 if the piece landed on an empty square, 1 if it captured a different color piece and
    # -1 if it captured a similar colored piece
    def checkIfMoveIsPossible(self, move):

        capturedPieceColor = move.capturedPiece[0]
        movedPieceColor = move.movedPiece[0]

        # Check if the piece is on an empty square
        if move.capturedPiece == EMPTY_SQUARE:
            return 0

        # Check if the piece hit a piece of the same color as her
        if capturedPieceColor != movedPieceColor:
            return 1

        return -1

    # Generate all possible moves for a Pawn at (row, col)
    def getPawnMoves(self, row, col):

        # Get the color of the piece
        pieceColor = self.board[row][col][0]

        # Initialize the possible moves list
        possibleMoves = []

        # If the pawn is White
        if pieceColor == WHITE and row - 1 >= 0:

            # Check if the square in front of the pawn is empty
            if self.board[row - 1][col] == EMPTY_SQUARE:

                # Check if the pawn promotes
                if row == 1:
                    for piece in PROMOTION_PIECES:
                        newMove = Move((row, col), (row - 1, col), self.board, pawnPromotion=piece)
                        possibleMoves.append(newMove)
                else:
                    newMove = Move((row, col), (row - 1, col), self.board)
                    possibleMoves.append(newMove)

            # Check if the pawn has not been moved and if the two sqaures in front of it are empty
            if row == 6 and self.board[row - 1][col] == EMPTY_SQUARE and\
                    self.board[row - 2][col] == EMPTY_SQUARE:

                newMove = Move((row, col), (row - 2, col), self.board)
                possibleMoves.append(newMove)

            # Pawn Captures
            if col > 0 and self.board[row - 1][col - 1][0] == BLACK:

                # Check if the pawn promotes
                if row == 1:

                    for piece in PROMOTION_PIECES:

                        newMove = Move((row, col), (row - 1, col - 1), self.board, pawnPromotion=piece)
                        possibleMoves.append(newMove)
                else:

                    newMove = Move((row, col), (row - 1, col - 1), self.board)
                    possibleMoves.append(newMove)

            if col < 7 and self.board[row - 1][col + 1][0] == BLACK:

                # Check if the pawn promotes
                if row == 1:

                    for piece in PROMOTION_PIECES:
                        newMove = Move((row, col), (row - 1, col + 1), self.board, pawnPromotion=piece)
                        possibleMoves.append(newMove)
                else:

                    newMove = Move((row, col), (row - 1, col + 1), self.board)
                    possibleMoves.append(newMove)

            # En Passant
            if row == 3:
                lastMove = self.moveLog[-1]
                if lastMove.movedPiece == 'bP' and lastMove.endRow == 3 and\
                        (lastMove.endCol == col - 1 or lastMove.endCol == col + 1):

                    if lastMove.endCol == col + 1:
                        newMove = Move((row, col), (row - 1, col + 1), self.board, enPassant = True)
                        possibleMoves.append(newMove)

                    if lastMove.endCol == col - 1:
                        newMove = Move((row, col), (row - 1, col - 1), self.board, enPassant = True)
                        possibleMoves.append(newMove)

        # If the pawn is Black
        elif pieceColor == BLACK and row + 1 <= 7:

            # Check if the square in front of the pawn is empty
            if self.board[row + 1][col] == EMPTY_SQUARE:

                # Check if the pawn promotes
                if row == 6:
                    for piece in PROMOTION_PIECES:
                        newMove = Move((row, col), (row + 1, col), self.board, pawnPromotion=piece)
                        possibleMoves.append(newMove)
                else:
                    newMove = Move((row, col), (row + 1, col), self.board)
                    possibleMoves.append(newMove)

            # Check if the pawn has not been moved and if the two sqaures in front of it are empty
            if row == 1 and self.board[row + 1][col] == EMPTY_SQUARE and\
                    self.board[row + 2][col] == EMPTY_SQUARE:

                newMove = Move((row, col), (row + 2, col), self.board)
                possibleMoves.append(newMove)

            # Pawn Captures
            if col > 0 and self.board[row + 1][col - 1][0] == WHITE:

                # Check if the pawn promotes
                if row == 6:
                    for piece in PROMOTION_PIECES:
                        newMove = Move((row, col), (row + 1, col - 1), self.board, pawnPromotion=piece)
                        possibleMoves.append(newMove)
                else:
                    newMove = Move((row, col), (row + 1, col - 1), self.board)
                    possibleMoves.append(newMove)

            if col < 7 and self.board[row + 1][col + 1][0] == WHITE:

                # Check if the pawn promotes
                if row == 6:
                    for piece in PROMOTION_PIECES:
                        newMove = Move((row, col), (row + 1, col + 1), self.board, pawnPromotion=piece)
                        possibleMoves.append(newMove)
                else:
                    newMove = Move((row, col), (row + 1, col + 1), self.board)
                    possibleMoves.append(newMove)

            # En Passant
            if row == 4:
                lastMove = self.moveLog[-1]
                if lastMove.movedPiece == 'wP' and lastMove.endRow == 4 and\
                        (lastMove.endCol == col - 1 or lastMove.endCol == col + 1):

                    if lastMove.endCol == col + 1:
                        newMove = Move((row, col), (row + 1, col + 1), self.board, enPassant = True)
                        possibleMoves.append(newMove)

                    if lastMove.endCol == col - 1:
                        newMove = Move((row, col), (row + 1, col - 1), self.board, enPassant = True)
                        possibleMoves.append(newMove)

        return possibleMoves

    # Generate all possible moves for a Rook at (row, col)
    def getRookMoves(self, row, col):

        # Initialize the possible moves list
        possibleMoves = []

        # Generate possible moves when moving the Rook Up
        r = row - 1
        while r >= 0:

            newMove = Move((row, col), (r, col), self.board)
            isMovePossible = self.checkIfMoveIsPossible(newMove)

            if isMovePossible == -1:
                break
            else:
                possibleMoves.append(newMove)
                if isMovePossible == 1:
                    break

            r -= 1

        # Generate possible moves when moving the Rook Down
        r = row + 1
        while r <= 7:

            newMove = Move((row, col), (r, col), self.board)
            isMovePossible = self.checkIfMoveIsPossible(newMove)

            if isMovePossible == -1:
                break
            else:
                possibleMoves.append(newMove)
                if isMovePossible == 1:
                    break

            r += 1

        # Generate possible moves when moving the Rook Right
        c = col + 1
        while c <= 7:

            newMove = Move((row, col), (row, c), self.board)
            isMovePossible = self.checkIfMoveIsPossible(newMove)

            if isMovePossible == -1:
                break
            else:
                possibleMoves.append(newMove)
                if isMovePossible == 1:
                    break

            c += 1

        # Generate possible moves when moving the Rook Left
        c = col - 1
        while c >= 0:

            newMove = Move((row, col), (row, c), self.board)
            isMovePossible = self.checkIfMoveIsPossible(newMove)

            if isMovePossible == -1:
                break
            else:
                possibleMoves.append(newMove)
                if isMovePossible == 1:
                    break

            c -= 1

        return possibleMoves

    # Generate all possible moves for a Knight at (row, col)
    def getKnightMoves(self, row, col):

        # Initialize the possible moves list
        possibleMoves = []

        # Generate the two leftmost moves of a night
        if col - 2 >= 0:
            if row - 1 >= 0:

                newMove = Move((row, col), (row - 1, col - 2), self.board)
                isMovePossible = self.checkIfMoveIsPossible(newMove)

                if isMovePossible != -1:
                    possibleMoves.append(newMove)

            if row + 1 <= 7:

                newMove = Move((row, col), (row + 1, col - 2), self.board)
                isMovePossible = self.checkIfMoveIsPossible(newMove)

                if isMovePossible != -1:
                    possibleMoves.append(newMove)

        # Generate the two rightmost moves of a night
        if col + 2 <= 7:
            if row - 1 >= 0:

                newMove = Move((row, col), (row - 1, col + 2), self.board)
                isMovePossible = self.checkIfMoveIsPossible(newMove)

                if isMovePossible != -1:
                    possibleMoves.append(newMove)

            if row + 1 <= 7:

                newMove = Move((row, col), (row + 1, col + 2), self.board)
                isMovePossible = self.checkIfMoveIsPossible(newMove)

                if isMovePossible != -1:
                    possibleMoves.append(newMove)

        # Generate the two upmost moves of a night
        if row - 2 >= 0:
            if col - 1 >= 0:

                newMove = Move((row, col), (row - 2, col - 1), self.board)
                isMovePossible = self.checkIfMoveIsPossible(newMove)

                if isMovePossible != -1:
                    possibleMoves.append(newMove)

            if col + 1 <= 7:

                newMove = Move((row, col), (row - 2, col + 1), self.board)
                isMovePossible = self.checkIfMoveIsPossible(newMove)

                if isMovePossible != -1:
                    possibleMoves.append(newMove)

        # Generate the two downmost moves of a night
        if row + 2 <= 7:
            if col - 1 >= 0:

                newMove = Move((row, col), (row + 2, col - 1), self.board)
                isMovePossible = self.checkIfMoveIsPossible(newMove)

                if isMovePossible != -1:
                    possibleMoves.append(newMove)

            if col + 1 <= 7:

                newMove = Move((row, col), (row + 2, col + 1), self.board)
                isMovePossible = self.checkIfMoveIsPossible(newMove)

                if isMovePossible != -1:
                    possibleMoves.append(newMove)

        return possibleMoves

    # Generate all possible moves for a Bishop at (row, col)
    def getBishopMoves(self, row, col):

        # Initialize the possible moves list
        possibleMoves = []

        # Generate possible moves on the Upper Left Diagonal
        (r, c) = (row - 1, col - 1)
        while r >= 0 and c >= 0:

            newMove = Move((row, col), (r, c), self.board)
            isMovePossible = self.checkIfMoveIsPossible(newMove)

            if isMovePossible == -1:
                break
            else:
                possibleMoves.append(newMove)
                if isMovePossible == 1:
                    break

            r -= 1
            c -= 1

        # Generate possible moves on the Upper Right Diagonal
        (r, c) = (row - 1, col + 1)
        while r >= 0 and c <= 7:

            newMove = Move((row, col), (r, c), self.board)
            isMovePossible = self.checkIfMoveIsPossible(newMove)

            if isMovePossible == -1:
                break
            else:
                possibleMoves.append(newMove)
                if isMovePossible == 1:
                    break

            r -= 1
            c += 1

        # Generate possible moves on the Downward Right Diagonal
        (r, c) = (row + 1, col + 1)
        while r <= 7 and c <= 7:

            newMove = Move((row, col), (r, c), self.board)
            isMovePossible = self.checkIfMoveIsPossible(newMove)

            if isMovePossible == -1:
                break
            else:
                possibleMoves.append(newMove)
                if isMovePossible == 1:
                    break

            r += 1
            c += 1

        # Generate possible moves on the Downward Left Diagonal
        (r, c) = (row + 1, col - 1)
        while r <= 7 and c >= 0:

            newMove = Move((row, col), (r, c), self.board)
            isMovePossible = self.checkIfMoveIsPossible(newMove)

            if isMovePossible == -1:
                break
            else:
                possibleMoves.append(newMove)
                if isMovePossible == 1:
                    break

            r += 1
            c -= 1

        return possibleMoves

    # Generate all possible moves for a Queen at (row, col)
    def getQueenMoves(self, row, col):

        return self.getRookMoves(row, col) + self.getBishopMoves(row, col)

    # Generate all possible moves for a King at (row, col)
    def getKingMoves(self, row, col):

        # Initialize the possible moves list
        possibleMoves = []

        upperLeftCorner = (max(0, row - 1), max(0, col - 1))
        lowerRightCorner = (min(row + 1, 7), min(col + 1, 7))

        for r in range(upperLeftCorner[0], lowerRightCorner[0] + 1):
            for c in range(upperLeftCorner[1], lowerRightCorner[1] + 1):

                if (r,c) == (row, col):
                    continue

                newMove = Move((row, col), (r, c), self.board)
                isMovePossible = self.checkIfMoveIsPossible(newMove)

                if isMovePossible != -1:
                    possibleMoves.append(newMove)

        # Castling

        # Get the color of the king
        kingColor = self.getColorOfPiece(self.board[row][col])
        kingInCheck = self.whiteKingInCheck if kingColor == WHITE else self.blackKingInCheck
        hasKingMoved = self.whiteKingMoved if kingColor == WHITE else self.blackKingMoved
        kingRookLeftMoved = self.whiteRookLeftMoved if kingColor == WHITE else self.blackRookLeftMoved
        kingRookRightMoved = self.whiteRookRightMoved if kingColor == WHITE else self.blackRookRightMoved

        if hasKingMoved == 0 and not kingInCheck:

            # Castle long
            if kingRookLeftMoved == 0 and self.board[row][col - 1] == EMPTY_SQUARE and\
                    self.board[row][col - 2] == EMPTY_SQUARE and self.board[row][col - 3] == EMPTY_SQUARE and\
                    self.board[row][col - 4] == kingColor + ROOK:

                newMove = Move((row, col), (row, col - 1), self.board)
                self.makeMove(newMove)
                inCheck1 = self.checkIfInCheck(kingColor)
                self.undoMove()

                newMove = Move((row, col), (row, col - 2), self.board)
                self.makeMove(newMove)
                inCheck2 = self.checkIfInCheck(kingColor)
                self.undoMove()

                # If the king will not pass through a square where he is in check during the castle
                if not inCheck1 and not inCheck2:
                    newMove = Move((row, col), (row, col - 2), self.board, castle=2)
                    possibleMoves.append(newMove)

            # Castle short
            if kingRookRightMoved == 0 and self.board[row][col + 1] == EMPTY_SQUARE and\
                    self.board[row][col + 2] == EMPTY_SQUARE and self.board[row][col + 3] == kingColor + ROOK:

                newMove = Move((row, col), (row, col + 1), self.board)
                self.makeMove(newMove)
                inCheck1 = self.checkIfInCheck(kingColor)
                self.undoMove()

                newMove = Move((row, col), (row, col + 2), self.board)
                self.makeMove(newMove)
                inCheck2 = self.checkIfInCheck(kingColor)
                self.undoMove()

                # If the king will not pass through a square where he is in check during the castle
                if not inCheck1 and not inCheck2:
                    newMove = Move((row, col), (row, col + 2), self.board, castle=1)
                    possibleMoves.append(newMove)



        return possibleMoves

    # Return the color of the piece(piece = (row, col))
    def getColorOfPiece(self, piece):

        return piece[0]

    # Return the type of the piece(piece = (row, col))
    def getTypeOfPiece(self, piece):

        return piece[1]

    # Check if color is in check
    def checkIfInCheck(self, color):
        oppositeColor = WHITE

        if color == WHITE:
            oppositeColor = BLACK

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):

                #Check if at (row, col) exists a piece of the opposite color
                if self.getColorOfPiece(self.board[row][col]) == oppositeColor:

                    # Get all the possible moves of the piece at row and col
                    possibleMoves = self.getPiecePossilbleMoves(row, col)
                    for move in possibleMoves:
                        if self.getTypeOfPiece(move.capturedPiece) == KING:
                            return True

        return False

    # Check if color is in checkmate
    def checkIfCheckmate(self, color):

        # Find all the valid moves that the "color" colored player can make
        validMoves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):

                # Check if at (row, col) exists a piece of the specified color
                if self.getColorOfPiece(self.board[row][col]) == color:

                    # Get all the possible moves of the piece at row and col
                    validMovesPartial = self.getPieceValidMoves(row, col)
                    validMoves += validMovesPartial[0] + validMovesPartial[1]
                    #validMoves += self.getPieceValidMoves(row, col)

                    # If valid moves exists then it's not checkmate
                    if len(validMoves) != 0:
                        return False

        # If the "color" colored player can't make any valid moves then it's checkmate
        if len(validMoves) == 0:

            return True

        print(validMoves[0].movedPiece)
        # Otherwise it's not checkmate
        return False

    def checkIfStalemate(self):

        piecesOnTable = []
        validMoves = []
        color = WHITE if self.whiteToMove else BLACK

        whiteBishopCoord = None
        blackBishopCoord = None

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):

                if self.board[row][col] != EMPTY_SQUARE and len(piecesOnTable) < 3 and\
                        self.getTypeOfPiece(self.board[row][col]) != KING:

                    piecesOnTable.append(self.board[row][col])

                    if self.getTypeOfPiece(self.board[row][col]) == BISHOP:
                        if self.getColorOfPiece(self.board[row][col]) == WHITE:
                            whiteBishopCoord = (row, col)
                        else:
                            blackBishopCoord = (row, col)

                if self.getColorOfPiece(self.board[row][col]) == color:
                    validMovesPartial = self.getPieceValidMoves(row,col)
                    validMoves += validMovesPartial[0] + validMovesPartial[1]
                    #validMoves += self.getPieceValidMoves(row,col)

        # If only the kings remain on the board or the current player has no valid moves then it's stalemate
        if len(piecesOnTable) == 0 or len(validMoves) == 0:
            return True

        # Draw by insufficient material

        # King and Bishop vs King or King and Knight vs King
        if len(piecesOnTable) == 1:
            if self.getTypeOfPiece(piecesOnTable[0]) == KNIGHT or \
                    self.getTypeOfPiece(piecesOnTable[0]) == BISHOP:
                return True

        # King and Bishop vs King and Bishop of the same color
        if len(piecesOnTable) == 2:
            if self.getTypeOfPiece(piecesOnTable[0]) == BISHOP and \
                    self.getTypeOfPiece(piecesOnTable[1]) == BISHOP and \
                    (blackBishopCoord[0] + blackBishopCoord[1]) % 2 == (whiteBishopCoord[0] + whiteBishopCoord[1]) % 2:
                return True

        return False


    def checkIfTheGameEnded(self):

        # Check if the move has put the other player in check
        if self.whiteToMove:

            # If you made a move you are no longer in check
            self.blackKingInCheck = False

            # Check if white is in check
            if self.checkIfInCheck(WHITE):

                self.whiteKingInCheck = True

                # Check if the white king checkmated
                if self.checkIfCheckmate(WHITE):
                    print("Checkmate! Black won the game!")
                    self.checkmateKing = WHITE + KING
                    return

            else:

                self.whiteKingInCheck = False

        else:

            # If you made a move you are no longer in check
            self.whiteKingInCheck = False

            # Check if black is in check
            if self.checkIfInCheck(BLACK):

                self.blackKingInCheck = True

                # Check if the black king checkmated
                if self.checkIfCheckmate(BLACK):
                    print("Checkmate! White won the game!")
                    self.checkmateKing = BLACK + KING
                    return

            else:

                self.blackKingInCheck = False

        # Check if the match ended in stalemate
        if self.checkIfStalemate():
            print("Stalemate!")
            self.stalemate = True
        else:
            self.stalemate = False


class Move():

    rankToRow = {"1" : 7, "2" : 6, "3" : 5, "4" : 4,
                 "5" : 3, "6" : 2, "7" : 1, "8" : 0}

    rowToRank = {v : k for k, v in rankToRow.items()}

    fileToCol = {"a" : 0, "b" : 1, "c" : 2, "d" : 3,
                 "e" : 4, "f" : 5, "g" : 6, "h" : 7}

    colToFile = {v : k for k, v in fileToCol.items()}

    # castle = 0 => no castle, castle = 1 => castle short, castle = 2 => castle long
    def __init__(self, startSquare, endSquare, board, enPassant = False, castle = 0, pawnPromotion = None):

        self.startRow = startSquare[0]
        self.startCol = startSquare[1]

        self.endRow = endSquare[0]
        self.endCol = endSquare[1]

        self.movedPiece = board[self.startRow][self.startCol]

        # Specifies if the pawn has been promoted and the piece that the pawn got promoted to
        self.pawnPromotion = self.movedPiece[0] + pawnPromotion if pawnPromotion is not None else pawnPromotion

        # Specifies if this is a castle move
        self.castle = castle

        # Sets the captured piece depending if it's an en passant move or not
        self.enPassant = enPassant

        if enPassant == False:
            self.capturedPiece = board[self.endRow][self.endCol]
        else:
            self.capturedPiece = board[self.startRow][self.endCol]

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colToFile[col] + self.rowToRank[row]