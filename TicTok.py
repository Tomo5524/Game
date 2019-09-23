
# Invent Your Own Computer Games with Python,
import random

def ShowBoard(board):
    print(board[1] + '|' + board[2] + '|' + board[3])
    print('-+-+-')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-')

    print(board[7] + '|' + board[8] + '|' + board[9])

# Letting the Player Choose X or O
def pickLetter():

    letter = ''
    while letter != "X" and letter != "O":
        letter = input("O or X: ").upper()

    if letter == "O":
        return ["O","X"]
    else:
        return ["X", "O"]

# deciding who goes first
def whoGoesFirst():

    return True if random.randint(1,2) == 1 else False

# Placing a Mark on the Board
def makeMove(letter, move,bo):
    bo[move] = letter

# Letting the Player Enter a Move

def getPlayerMove(board):
    # return index at which player wants to place the letter
    move = ''
    while move not in "1,2,3,4,5,6,7,8,9".split(',') or not isEmpty(int(move),board):
        # it will be true the first time for sure as move is just ''
        move = input('What is your next move? (1-9): ')

    return int(move) # convert it to int as input is str

# Checking Whether the Player Won

def win(le,board):


    return ((board[7] == le and board[8] == le and board[9] == le) or  # Across the top
            (board[4] == le and board[5] == le and board[6] == le) or  # Across the middle
            (board[1] == le and board[2] == le and board[3] == le) or  # Across the bottom
            (board[7] == le and board[4] == le and board[1] == le) or  # Down the left side
            (board[8] == le and board[5] == le and board[2] == le) or  # Down the middle
            (board[9] == le and board[6] == le and board[3] == le) or  # Down the right side
            (board[7] == le and board[5] == le and board[3] == le) or  # Diagonal
            (board[9] == le and board[5] == le and board[1] == le))  # Diagonal

def chooseRandomMoveFromList(movelist,board): # need to create movelist
    possibleMoves = []
    # movelist  = [1,3,7,9]
    # movelist  = [2,4,6,8]
    for i in movelist:
        if isEmpty(i,board):
            possibleMoves.append(i)

    if possibleMoves:
        return random.choice(possibleMoves)

    else:
        return None


def getBoardCopy(board):
    new_board = []
    #new_board = TicTacToe() # create new_empty list by calling class
    #new_board = t.board, this will mess up cuz it is constantly updated
    for i in board:
        new_board.append(i)

    return new_board


# check if player can make a valid move

def isEmpty(move,board):
    return board[move] == " "


def getComputerMove(cpLetter,board):

    """
    1, See if there’s a move the computer can make that will win the game.
        If there is, take that move. Otherwise, go to step 2.
    2, See if there’s a move the player can make that will cause the computer to lose the game.
        If there is, the computer should move there to block the player. Otherwise, go to step 3.
    3, Check if any of the corners (spaces 1, 3, 7, or 9) are free.
        If no corner space is free, go to step 4.
    4, Check if the center is free.
        If so, move there. If it isn’t, go to step 5.
    5, Move on any of the sides (spaces 2, 4, 6, or 8).
        There are no more steps, because the side spaces are the only spaces left if the execution has reached this step.
    """

    if cpLetter == "X":
        player_letter = "O"
    else:
        player_letter = "X"

    # check if cp wins
    # problem is self.board gets updated constantly
    # by creating dummy, updating can be prevented
    for i in range(1,10):
        board_copy = getBoardCopy(board)
        if isEmpty(i,board):
            makeMove(cpLetter,i,board_copy)
            if win(cpLetter,board_copy):
                return i

    # check if player_letter wins
    for i in range(1,10):
        board_copy = getBoardCopy(board)
        if isEmpty(i,board):
            makeMove(player_letter,i,board_copy)
            if win(player_letter,board_copy):
                return i

    # step 3 check corner
    move = chooseRandomMoveFromList([1,3,7,9],board)
    if move:
        return move

    # step 4 take the center, if it is free.
    if isEmpty(5):
        return 5

    # step5
    return chooseRandomMoveFromList([2,4,6,8])

def isBoardFull(board):

    for i in range(1,10):
        if isEmpty(i,board):
            # if empty found, board is not full
            return False

    return True

def main():
    print("Welcome to Tic-Tac-Toe!")
    run = True
    #whoGoesFirstround():
    #you, cp = pickLetter() # only pick once
    while run:
        main_board = [" " for i in range(10)]
        player_letter, cp_letter = pickLetter()
        gameIsPlaying = True
        turn = whoGoesFirst()
        if turn: print("Player goes first")
        else: print("The computer will go first.")
        while gameIsPlaying:

            if turn:
                # player goes first
                move = getPlayerMove(main_board)
                makeMove(player_letter,move,main_board)
                if win(player_letter,main_board):
                    print('Hooray! You have won the game!')
                    gameIsPlaying = False

                else:
                    if isBoardFull(main_board):
                        print('the game is a tie')
                        break
                    else:
                        # change turn
                        turn = False

            else:
                # computer's turn
                move = getComputerMove(cp_letter,main_board)
                makeMove(cp_letter,move,main_board)
                if win(cp_letter,main_board):
                    print('You got defeated.')
                    gameIsPlaying = False

                else:
                    if isBoardFull(main_board):
                        print('the game is a tie')
                        ShowBoard(main_board)
                        break
                    else:
                        turn = True

                ShowBoard(main_board)

        ask = input("wanna play again? if so, type yes: ")
        if ask != 'yes':
            run = False
            print('thank you for playing')


# t = TicTacToe()
# t.ShowBoard()
main()




