from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import random

class TicTacToe:
    def __init__(self):
        self.board = [" "] * 9
        self.score = {"X": 0, "O": 0, "Tie": 0}
        self.game_mode = "ai"

    def print_board(self):
        return f"""
        <pre>
        {self.board[0]} | {self.board[1]} | {self.board[2]}
        --+---+--
        {self.board[3]} | {self.board[4]} | {self.board[5]}
        --+---+--
        {self.board[6]} | {self.board[7]} | {self.board[8]}
        </pre>
        Score: X - {self.score["X"]}, O - {self.score["O"]}, Tie - {self.score["Tie"]}
        """

    def check_win(self):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != " ":
                return self.board[condition[0]]
        if " " not in self.board:
            return "Tie"
        return False

    def ai_move(self):
        possible_moves = [i for i, x in enumerate(self.board) if x == " "]
        move = None

        # Try to win
        for i in possible_moves:
            board_copy = self.board[:]
            board_copy[i] = "O"
            if self.check_win_board(board_copy) == "O":
                move = i
                break

        # Block player from winning
        if move is None:
            for i in possible_moves:
                board_copy = self.board[:]
                board_copy[i] = "X"
                if self.check_win_board(board_copy) == "X":
                    move = i
                    break

        # Move to center
        if move is None and 4 in possible_moves:
            move = 4

        # Random move
        if move is None:
            move = random.choice(possible_moves)

        return move

    def check_win_board(self, board):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for condition in win_conditions:
            if board[condition[0]] == board[condition[1]] == board[condition[2]] != " ":
                return board[condition[0]]
        if " " not in board:
            return "Tie"
        return False

    def reset_game(self):
        self.board = [" "] * 9
        self.score = {"X": 0, "O": 0, "Tie": 0}

class RequestHandler(BaseHTTPRequestHandler):
    game = TicTacToe()

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
            <html>
            <body>
            <h1>Tic Tac Toe</h1>
            """ + self.game.print_board().encode() + b"""
            <form action="/move" method="post">
            <input type="text" name="move" placeholder="Enter move (1-9)">
            <input type="submit" value="Make move">
            </form>
            <form action="/reset" method="post">
            <input type="submit" value="Reset game">
            </form>
            <form action="/mode" method="post">
            <select name="mode">
            <option value="ai">Play against AI</option>
            <option value="human">Play against human</option>
            </select>
            <input type="submit" value="Change game mode">
            </form>
            </body>
            </html>
            """)
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not found")

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/move":
            content_length = int(self.headers["Content-Length"])
            post_body = self.rfile.read(content_length)
            move = urllib.parse.parse_qs(post_body.decode())["move"][0]
            try:
                move = int(move) - 1
                if self.game.board[move] != " ":
                    self.send_response(400)
                    self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write(b"Invalid move")
                else:
                    self.game.board[move] = "X"
                    result = self.game.check_win()
                    if result:
                        if result == "Tie":
                            self.game.score["Tie"] += 1
                        else:
                            self.game.score[result] += 1
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        if result == "Tie":
                            self.wfile.write(b"It's a tie!")
                        else:
                            self.wfile.write(f"{result} wins!".encode())
                        self.wfile.write(b"""
                        <form action="/reset" method="post">
                        <input type="submit" value="Play again">
                        </form>
                        """)
                    else:
                        if self.game.game_mode == "ai":
                            ai_move_index = self.game.ai_move()
                            self.game.board[ai_move_index] = "O"
                            result = self.game.check_win()
                            if result:
                                if result == "Tie":
                                    self.game.score["Tie"] += 1
                                else:
                                    self.game.score[result] += 1
                                self.send_response(200)
                                self.send_header("Content-type", "text/html")
                                self.end_headers()
                                if result == "Tie":
                                    self.wfile.write(b"It's a tie!")
                                else:
                                    self.wfile.write(f"{result} wins!".encode())
                                self.wfile.write(b"""
                                <form action="/reset" method="post">
                                <input type="submit" value="Play again">
                                </form>
                                """)
                            else:
                                self.send_response(200)
                                self.send_header("Content-type", "text/html")
                                self.end_headers()
                                self.wfile.write(b"""
                                <html>
                                <body>
                                <h1>Tic Tac Toe</h1>
                                """ + self.game.print_board().encode() + b"""
                                <form action="/move" method="post">
                                <input type="text" name="move" placeholder="Enter move (1-9)">
                                <input type="submit" value="Make move">
                                </form>
                                <form action="/reset" method="post">
                                <input type="submit" value="Reset game">
                                </form>
                                <form action="/mode" method="post">
                                <select name="mode">
                                <option value="ai">Play against AI</option>
                                <option value="human">Play against human</option>
                                </select>
                                <input type="submit" value="Change game mode">
                                </form>
                                </body>
                                </html>
                                """)
                        else:
                            self.send_response(200)
                            self.send_header("Content-type", "text/html")
                            self.end_headers()
                            self.wfile.write(b"""
                            <html>
                            <body>
                            <h1>Tic Tac Toe</h1>
                            """ + self.game.print_board().encode() + b"""
                            <form action="/move2" method="post">
                            <input type="text" name="move" placeholder="Enter move (1-9)">
                            <input type="submit" value="Make move">
                            </form>
                            <form action="/reset" method="post">
                            <input type="submit" value="Reset game">
                            </form>
                            <form action="/mode" method="post">
                            <select name="mode">
                            <option value="ai">Play against AI</option>
                            <option value="human">Play against human</option>
                            </select>
                            <input type="submit" value="Change game mode">
                            </form>
                            </body>
                            </html>
                            """)
            except (ValueError, IndexError):
                self.send_response(400)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Invalid move")
        elif parsed_path.path == "/reset":
            self.game.reset_game()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
            <html>
            <body>
            <h1>Tic Tac Toe</h1>
            """ + self.game.print_board().encode() + b"""
            <form action="/move" method="post">
            <input type="text" name="move" placeholder="Enter move (1-9)">
            <input type="submit" value="Make move">
            </form>
            <form action="/reset" method="post">
            <input type="submit" value="Reset game">
            </form>
            <form action="/mode" method="post">
            <select name="mode">
            <option value="ai">Play against AI</option>
            <option value="human">Play against human</option>
            </select>
            <input type="submit" value="Change game mode">
            </form>
            </body>
            </html>
            """)
        elif parsed_path.path == "/mode":
            content_length = int(self.headers["Content-Length"])
            post_body = self.rfile.read(content_length)
            mode = urllib.parse.parse_qs(post_body.decode())["mode"][0]
            self.game.game_mode = mode
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
            <html>
            <body>
            <h1>Tic Tac Toe</h1>
            """ + self.game.print_board().encode() + b"""
            <form action="/move" method="post">
            <input type="text" name="move" placeholder="Enter move (1-9)">
            <input type="submit" value="Make move">
            </form>
            <form action="/reset" method="post">
            <input type="submit" value="Reset game">
            </form>
            <form action="/mode" method="post">
            <select name="mode">
            <option value="ai">Play against AI</option>
            <option value="human">Play against human</option>
            </select>
            <input type="submit" value="Change game mode">
            </form>
            </body>
            </html>
            """)
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not found")

def run_server():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server running at http://localhost:8000")
    httpd.serve_forever()

run_server()