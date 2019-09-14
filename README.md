## Project: Tic-Tac-Toe

### Introduce
In this project you will modify the code that you worked on in the previous CS course to do three things:

Allows two players to play against each other.
Utilizes object oriented programming, making a Tic-Tac-Toe class with functions.
Adds other improvements to make the program more user friendly.

### Requirements
#### a) Rules
Tic-tac-toe , noughts and crosses (British English), or Xs and Os is a paper-and-pencil game for two players, X and O, who take turns marking the spaces in a 3×3 grid. The player who succeeds in placing three of their marks in a horizontal, vertical, or diagonal row wins the game.
#### b) how to play
1. Draw the board. First, you have to draw the board, which is made up of a 3 x 3 grid of squares. This means it has three rows of three squares. 
2. Have the first player go first. Though traditionally, the first player goes with "X", you can allow the first player to decide whether he wants to go with "X"s or "O"s. These symbols will be placed on the table, in the attempt to have three of them in a row. 
3. Have the second player go second. After the first player goes, then the second player should put down his symbol, which will be different from the symbol of the first player. The second player can either try to block the first player from creating a row of three, or focus on creating his or her own row of three. Ideally, the player can do both.
4. Keep alternating moves until one of the players has drawn a row of three symbols or until no one can win. The first player to draw three of his or her symbols in a row, whether it is horizontal, vertical, or diagonal, has won tic-tac-toe. However, if both players are playing with optimal strategy, then there's a good chance that no one will win because you will have blocked all of each other's opportunities to create a row of three.

### Design
1. Classes: I will create a class called TicTacToe that contains some attributes and methods.
    1. Attributes： board
    2. Methods：drawBoard, whoGoesFirst, playAgain, makeMove,isWinner,isFull
2. Objects: Every match will create a TicTacToe-based object.
3. Form: I will use the web app , allowing two players to take turns playing chess on the page through browser.

### WebApp

- env: python3
- run command: python ticTacToeApp.py
- open browser:  http://localhost:8000