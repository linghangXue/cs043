import random
class TicTacToe:
    def __init__(self, board):
        self.board = board
    def drawBoard(self, board):
        boardpage = '''<form style="line-height:5px"><pre>         |    |<br>
         ''' + board[7] + ''' | ''' + board[8] + ''' | ''' + board[9] + '''<br>
         |    |<br>
        -----------------<br>
         |    |<br>
         ''' + board[4] + ''' | ''' + board[5] + ''' | ''' + board[6] + '''<br>
         |    |<br>
        -----------------<br>
         |    |<br>
         ''' + board[1] + ''' | ''' + board[2] + ''' | ''' + board[3] + '''<br>
         |    |</pre><br>
         <input type="submit" value="Make Move"></form>
        '''
        return boardpage

    def whoGoesFirst(self):
        if random.randint(0, 1) == 0:
            return 'X'
        else:
            return 'O'

    def makeMove(self, board, letter, move):
        board[int(move)] = letter
        return board

    def isWinner(self, bo, le):

        return ((bo[1] == le and bo[2] == le and bo[3] == le) or
                (bo[4] == le and bo[5] == le and bo[6] == le) or
                (bo[7] == le and bo[8] == le and bo[9] == le) or
                (bo[1] == le and bo[4] == le and bo[7] == le) or
                (bo[2] == le and bo[5] == le and bo[8] == le) or
                (bo[3] == le and bo[6] == le and bo[9] == le) or
                (bo[1] == le and bo[5] == le and bo[9] == le) or
                (bo[3] == le and bo[5] == le and bo[7] == le))


    def isFull(self, board):
        boardIsFull = True
        for i in range(1, 10):
            if (board[i] != 'X') and (board[i] != 'O'):
                boardIsFull = False
        return boardIsFull
