import random
import sys
WIDTH = 8
HEIGHT = 8

def drawBoard(board):

    # Print the board passed to this function. Return None.
    print('  12345678')
    print(' +--------+')
    for y in range(HEIGHT):
       print('%s|' % (y+1), end='')
       for x in range(WIDTH):
           print(board[x][y], end='')
       print('|%s' % (y+1))
    print(' +--------+')
    print('  12345678')

def getNewBoard():
    return [[" " for _ in range(HEIGHT)] for i in range(WIDTH)]

def isOnBoard(row,col,board):
    # make sure current cell is not out of boundary
    if row >= 0 and row < len(board) and col >= 0 and col < len(board[0]):
        return True
    return False

def isValidMove(board,tile,row,col):

    # return False if current cell is invalid
    # return a list of cells Player would get if they moved to current row and col

    if board[row][col] != " " or not isOnBoard(row,col,board):
        return False

    cp_tile = "O" if tile == "X" else "X"

    canFlip = []
    #visited = set() # returns a list of all the opponent’s tiles
                     # that would be flipped by this move.

    neighbours = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, 1), (1, -1), (-1, -1), (1, 1)]
    for neighbour in neighbours:
        #r,c = row,col
        r = row + neighbour[0]
        c = col + neighbour[1]

        while isOnBoard(r,c,board) and board[r][c] == cp_tile:
            # for a move to be valid, it must be both on the board and
            # next to one of the other player’s tiles so there are tiles to flip
            # as long as current cell is cp's, keep moving
            r += neighbour[0]
            c += neighbour[1]

            #visited.add([r,c])

            if isOnBoard(r,c,board) and board[r][c] == tile:
                # go back to where it came from and and add visited cells
                while True:
                    r -= neighbour[0]
                    c -= neighbour[1]
                    if r == row and c == col:
                        break # goes back to line 43 as original cell (row,col) is empty
                                # so line 48 will become false
                    canFlip.append([r,c])

    if not canFlip:
        return False

    return canFlip


def getValidMoves(board,tile):
    # return a list of [r,c] lists of valid moves
    validMoves = []
    for row in range(WIDTH):
        for col in range(HEIGHT):
            if isValidMove(board,tile,row,col): # non empty list becomes true
                validMoves.append([row,col])
    return validMoves

def getBoardWithValidMoves(board, tile):
    # return a copy board with a hint
    board_copy = getBoardCopy(board)
    for r,c in getValidMoves(board_copy,tile):
        board_copy[r][c] = "."

    return board_copy

def getScore(board):
    # create dictionary that holds each score
    dic = {}
    dic["X"],dic["O"] = 0,0
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if board[i][j] == "X":
                dic["X"] += 1

            if board[i][j] == "O":
                dic["O"] += 1

    return dic

def getTile():
    # return player's tile
    tile = ''
    while tile != "O" and tile != "X":
        tile = input("Choose your tile, X or O: ").upper()

    cp = "O" if tile == "X" else "X"
    return [tile,cp]


def whoGoesFirst():
    # if true, player goes first
    return random.randint(1,2) == 1

def makeMove(board,tile,row,col):
    # if current cell is valid, place player's tile along with flipping enemy's tile
    #flip = isValidMove(board,tile,row,col)
    if isValidMove(board,tile,row,col):
        #board[row][col] = tile
        flip = isValidMove(board, tile, row, col)  # false cuz row and col placed in line 120 so it is not empty thus false
        board[row][col] = tile
        for x,y in flip:
            board[x][y] = tile
        return board

    return False

def getBoardCopy(board):
    # Make a duplicate of the board list and return it.
    new_board = getNewBoard()
    for row in range(WIDTH):
        for col in range(HEIGHT):
            new_board[row][col] = board[row][col]

    return new_board

def isOnCorner(row,col):
    # Return True if current cell is in one of the four corners.
    #return (row == 0 or row == WIDTH - 1) and (col == 0 or col == HEIGHT - 1)
    return [row,col] == [0,0] or [row,col] == [0,7] or [row,col] == [7,0] or [row,col] == [7,7]

def getPlayerMove(board,tile):
    # player enter moves
    # return the move as [x,y]
    choices = [i for i in '1 2 3 4 5 6 7 8'.split()]
    while True:
        move = input('Enter 2 digits as your moves, "quit" to end the game, or "hints" to to get hints: ').lower()
        if move == 'quit' or move == 'hints':
            return move
        #playerMove = []
        if len(move) == 2 and move[0] in choices and move[1] in choices:
            row = int(move[0]) -1
            col = int(move[1]) -1

            if isValidMove(board,tile,row,col):
                return [row,col]

            else:
                print('That is not a valid move. Enter the column (1-8) and then the row(1 - 8).')

        else:
            print('That is not a valid move. Enter the column (1-8) and then the row(1 - 8).')

        peek = input("wanna peek at board? si y no?: ")
        if peek == "si":
            drawBoard(board)

def getComputerMove(board,tile):
    # return a list of best moves
    possibleMoves = getValidMoves(board,tile)
    random.shuffle(possibleMoves)
    # Corner moves are a good idea in Reversegam
    # because once a tile has been placed on a corner, it can never be flipped over.
    for r,c in possibleMoves:
        if isOnCorner(r,c):
            return [r,c]

    # place tile at the cell that gets the most points
    cpMove = []
    bestScore = float("-inf")
    for r, c in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy,tile,r,c)
        score = getScore(boardCopy)[tile] # get value of cp tile
        if bestScore < score:
            cpMove = [r,c]
            bestScore = score
    return cpMove

def printScore(board,tile):

    score = getScore(board)
    cp = "O" if tile == "X" else "X"
    print("Player's score: ", score[tile])
    print("Cp's score: ", score[cp])



def main():
    hints = False
    turn = whoGoesFirst()
    if turn:
        print("player goes first")
    else:
        print("Cp goes first")

    tile,cp = getTile()
    board = getNewBoard()
    board[(len(board) // 2) - 1][(len(board) // 2) - 1] = "X"  # 3,3
    board[(len(board) // 2) - 1][len(board) // 2] = "O"
    board[len(board) // 2][(len(board) // 2) - 1] = "O"
    board[(len(board) // 2)][(len(board) // 2)] = "X"

    run = True
    while run:
        # check whether either side can make a move by getting a list of valid moves.
        # If both of these lists are empty,
        # then neither player can make a move.
        playerValidMoves = getValidMoves(board,tile)
        cpValidMoves = getValidMoves(board,cp)
        if not playerValidMoves and cpValidMoves:
            return board # no room to place

        elif turn: # player goes first
            if playerValidMoves:
                if hints:
                    #print(getBoardWithValidMoves(board,tile)) # just print 2d array
                    temp = getBoardWithValidMoves(board, tile)
                    drawBoard(temp)
                    hints = False

                else:
                    move = getPlayerMove(board,tile)
                    if move == 'quit':
                        print('Thank you for playing')
                        run = False
                        sys.exit()
                    elif move == 'hints':
                        hints = True

                    else:
                        makeMove(board,tile,move[0],move[1])
                        turn = False
                        drawBoard(board)

        else:
            if cpValidMoves:
                move = getComputerMove(board,cp) # does not get valid moves
                makeMove(board,cp,move[0],move[1])
                ask = input("would you like to see cp's move? yes or no: ").lower()
                if ask == "yes":
                    drawBoard(board)

            turn = True

main()




