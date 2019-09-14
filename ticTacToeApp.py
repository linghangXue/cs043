import wsgiref.simple_server
import urllib.parse
import sqlite3
import http.cookies
from ticTacToe import TicTacToe

connection = sqlite3.connect('users.db')
try:
    connection.execute('CREATE TABLE users (username, password)')
    connection.commit()
except:
    pass
cursor = connection.cursor()

theBoard = ['',
            '<input type="radio" name="playerMove"  value="1">',
            '<input type="radio" name="playerMove"  value="2">',
            '<input type="radio" name="playerMove"  value="3">',
            '<input type="radio" name="playerMove"  value="4">',
            '<input type="radio" name="playerMove"  value="5">',
            '<input type="radio" name="playerMove"  value="6">',
            '<input type="radio" name="playerMove"  value="7">',
            '<input type="radio" name="playerMove"  value="8">',
            '<input type="radio" name="playerMove"  value="9">']
game = TicTacToe(theBoard)
game.turn = 'new'
turnMap = {0: "X", 1: "O"}
login_page = '''<!DOCTYPE html>
                       <html>
                       <head></head>
                       <body>
                       <h1>{}</h1>
                       <form action = "/login">
                           Username <input type="text" name="username"><br>
                           Password <input type="password" name="password"><br>
                           <input type="submit" value = 'login'>
                       </form>
                       <br>
                       <a href="/">Home Page</a>
                       </body></html>'''


def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]
    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    un = params['username'][0] if 'username' in params else None
    pw = params['password'][0] if 'password' in params else None

    if path == '/register' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ?', [un]).fetchall()
        if user:
            start_response('200 OK', headers)
            page = '''<!DOCTYPE html>
                                      <html>
                                      <head></head>
                                      <body>
                                          Sorry, username "{}" is taken, Try Again
                                          <br>
                                          
                                          <a href="/">Home</a>
                                      </body></html>'''.format(un)
            return [page.encode()]
        else:
            connection.execute('INSERT INTO users VALUES (?,?)', (un, pw))
            connection.commit()
            start_response('200 OK', headers)
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            page = '''<!DOCTYPE html>
                                      <html>
                                      <head></head>
                                      <body>
                                          Congratulations, username {} been successfully registered
                                          <br>
                                          <a href="/play">Let's go to Tic-Tac-Toe</a>
                                      </body></html>'''.format(un)
            return [page.encode()]

    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)
            page = '''<!DOCTYPE html>
                            <html>
                            <head></head>
                            <body>
                                User {} successfully logged in.
                                <br>
                                <a href="/play">Let's go to Tic-Tac-Toe</a>
                            </body></html>'''.format(un)
            return [page.encode()]
        else:
            start_response('200 OK', headers)
            return [login_page.format("You have input wrong username or password, Try Again.").encode()]

    elif path == '/logout':
        headers.append(('Set-Cookie', 'session=0; expires=Thu, 01 Jan 1970 00:00:00 GMT'))
        start_response('200 OK', headers)
        return [login_page.format("Wanna Play Again? Login First!").encode()]

    elif path == '/play':
        start_response('200 OK', headers)

        if 'HTTP_COOKIE' not in environ:
            return [login_page.format("Wanna Play? Login First!").encode()]

        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        if 'session' not in cookies:
            return [login_page.format("Wanna Play? Login First!").encode()]

        [un, pw] = cookies['session'].value.split(':')
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()

        if user:
            page = str('<!DOCTYPE html><html><head><title>Tic-Tac-Toe</title></head><body style="text-align:center;">' +
                       '<h2>Tic-Tac-Toe</h2>')

            theBoard = ['', '<input type="radio" name="playerMove" value="1">',
                        '<input type="radio" name="playerMove" value="2">',
                        '<input type="radio" name="playerMove" value="3">',
                        '<input type="radio" name="playerMove" value="4">',
                        '<input type="radio" name="playerMove" value="5">',
                        '<input type="radio" name="playerMove" value="6">',
                        '<input type="radio" name="playerMove" value="7">',
                        '<input type="radio" name="playerMove" value="8">',
                        '<input type="radio" name="playerMove" value="9">']

            if game.turn == 'new':
                game.turn = game.whoGoesFirst()

            if game.turn == 'X':
                if 'playerMove' not in params:
                    page += '<br>It is X\'s turn<br>'
                    page += TicTacToe.drawBoard(game, game.board)
                    return [page.encode()]
                else:
                    page += '<br>It is O\'s turn<br>'
                    playerMove = params['playerMove'][0]
                    game.board = game.makeMove(game.board, 'X', playerMove)
                    page += game.drawBoard(game.board)
                    game.turn = 'O'
                    if game.isWinner(game.board, 'X'):
                        page = '''<!DOCTYPE html><html><head><title>TTT Game</title></head>
                                  <body style="text-align:center;">                        
                                  <h2>Tic-Tac-Toe</h2><br>                                 
                                  Player X wins!<br>                                   
                                  <a href="/play">Play again</a><br>                       
                                  <a href="/logout">Log out</a>'''
                        game.board = theBoard
                        game.turn = 'new game'
                        return [page.encode()]
                    elif game.isFull(game.board):
                        page = '''<!DOCTYPE html><html><head><title>TTT Game</title></head>
                                  <body style="text-align:center;">                        
                                  <h2>Tic-Tac-Toe</h2><br>                                 
                                  The game is a tie.<br>                                   
                                  <a href="/play">Play again</a><br>                       
                                  <a href="/logout">Log out</a>'''
                        game.board = theBoard
                        game.turn = 'new'
                        return [page.encode()]
                    else:
                        return [page.encode()]

            elif game.turn == 'O':
                if 'playerMove' not in params:
                    page += '<br>It is O\'s turn<br>'
                    page += TicTacToe.drawBoard(game, game.board)
                    return [page.encode()]
                else:
                    page += '<br>It is X\'s turn<br>'
                    playerMove = params['playerMove'][0]
                    game.board = game.makeMove(game.board, 'O', playerMove)
                    page += game.drawBoard(game.board)
                    game.turn = 'X'
                    if game.isWinner(game.board, 'O'):
                        page = '''<!DOCTYPE html><html><head><title>TTT Game</title></head>
                                  <body style="text-align:center;">                        
                                  <h2>Tic-Tac-Toe</h2><br>                                 
                                  Player O wins!<br>                                   
                                  <a href="/play">Play again</a><br>                       
                                  <a href="/logout">Log out</a>'''
                        game.board = theBoard
                        game.turn = 'new game'
                        return [page.encode()]
                    elif game.isFull(game.board):
                        page = '''<!DOCTYPE html><html><head><title>TTT Game</title></head>
                                  <body style="text-align:center;">                        
                                  <h2>Tic-Tac-Toe</h2><br>                                 
                                  The game is a tie.<br>                                   
                                  <a href="/play">Play again</a><br>                       
                                  <a href="/logout">Log out</a>'''
                        game.board = theBoard
                        game.turn = 'new'
                        return [page.encode()]
                    else:
                        return [page.encode()]
        else:
            return [login_page.format("Wanna Play Game? Login First!").encode()]

    elif path == '/':
        start_response('200 OK', headers)
        page = '''<!DOCTYPE html>
                <html>
                <head></head>
                <body>
                <form action = "/login">
                    Username <input type="text" name="username"><br>
                    Password <input type="password" name="password"><br>
                    <input type="submit" value = 'login'>
                </form>
                <form action = "/register">
                    Username <input type="text" name="username"><br>
                    Password <input type="password" name="password"><br>
                    <input type="submit" value = 'register'>
                </form>
                </body></html>'''
        return [page.encode()]

    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()
