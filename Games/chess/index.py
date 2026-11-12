import chess
import chess.pgn
import random
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# pip install python-chess stockfish
try:
    from stockfish import Stockfish  # type: ignore
    stockfish_available = True
except ImportError:
    stockfish_available = False

HAS_STOCKFISH = stockfish_available

PIECES = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚',
}

LIGHT = "#EBECD0"
DARK = "#739552"
SELECT = "#F6F669"
LAST_MOVE = "#BACA2B"
LEGAL_DOT = "#646F40"
CHECK = "#E7746F"

class ChessGame:
    def __init__(self):
        self.board = chess.Board()
        self.player_color = chess.WHITE
        self.selected = None
        self.legal_targets = {}  # square -> move
        self.move_history = []
        self.game_over_flag = False
        self.engine = None
        self.engine_path = r"C:\path\to\stockfish.exe"  # <-- change this

        self._init_engine()

        # --- Window ---
        self.root = tk.Tk()
        self.root.title("Chess vs Engine")
        self.root.resizable(False, False)
        self.root.configure(bg="#312E2B")

        main = tk.Frame(self.root, bg="#312E2B", padx=12, pady=12)
        main.pack()

        # --- Top controls ---
        top = tk.Frame(main, bg="#312E2B")
        top.pack(fill="x", pady=(0, 8))

        tk.Label(top, text="Play as:", bg="#312E2B", fg="white").pack(side="left")
        self.side_var = tk.StringVar(value="White")
        ttk.Combobox(top, textvariable=self.side_var, values=["White", "Black"],
                     width=8, state="readonly").pack(side="left", padx=(4, 12))

        tk.Label(top, text="Difficulty:", bg="#312E2B", fg="white").pack(side="left")
        self.diff_var = tk.StringVar(value="Medium")
        ttk.Combobox(top, textvariable=self.diff_var,
                     values=["Easy", "Medium", "Hard"], width=8,
                     state="readonly").pack(side="left", padx=(4, 12))

        tk.Button(top, text="New Game", command=self.new_game,
                  bg="#81B64C", fg="white", relief="flat", padx=10).pack(side="left")
        tk.Button(top, text="Undo", command=self.undo,
                  bg="#454341", fg="white", relief="flat", padx=10).pack(side="left", padx=(6, 0))
        tk.Button(top, text="Save PGN", command=self.save_game,
                  bg="#454341", fg="white", relief="flat", padx=10).pack(side="left", padx=(6, 0))

        # --- Board ---
        self.squares: dict[int, tk.Button] = {}
        board_frame = tk.Frame(main, bg="black", padx=2, pady=2)
        board_frame.pack()

        for row in range(8):
            for col in range(8):
                sq = chess.square(col, 7 - row)
                btn = tk.Button(board_frame, font=("Segoe UI Symbol", 28),
                                width=2, height=1, relief="flat",
                                command=lambda s=sq: self.on_square_click(s))
                btn.grid(row=row, column=col)
                self.squares[sq] = btn

        # --- Bottom info ---
        self.status = tk.Label(main, text="", bg="#312E2B", fg="white",
                               font=("Segoe UI", 10, "bold"), anchor="w")
        self.status.pack(fill="x", pady=(8, 4))

        bottom = tk.Frame(main, bg="#312E2B")
        bottom.pack(fill="both", expand=True)

        tk.Label(bottom, text="Moves", bg="#312E2B", fg="#B8B8B8",
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.moves_text = tk.Text(bottom, height=6, width=52, bg="#262421",
                                  fg="white", font=("Consolas", 10),
                                  relief="flat", state="disabled")
        self.moves_text.pack(fill="x")

        self.draw_board()
        self.update_status()

        # If player is Black, let engine move first
        if self.player_color == chess.BLACK:
            self.root.after(300, self.ai_move)

    # ---------- Engine ----------
    def _init_engine(self):
        if not HAS_STOCKFISH:
            return
        try:
            self.engine = Stockfish(
                path=self.engine_path,
                parameters={"Threads": 4, "Hash": 512}
            )
            self.engine.set_elo_rating(1400)
        except Exception as e:
            print(f"Stockfish not found ({e}) — using random bot.")
            self.engine = None

    def _engine_depth(self):
        return {"Easy": 8, "Medium": 14, "Hard": 20}.get(self.diff_var.get(), 14)

    def _engine_elo(self):
        return {"Easy": 800, "Medium": 1400, "Hard": 2200}.get(self.diff_var.get(), 1400)

    # ---------- Game flow ----------
    def new_game(self):
        self.board = chess.Board()
        self.player_color = chess.WHITE if self.side_var.get() == "White" else chess.BLACK
        self.selected = None
        self.legal_targets = {}
        self.move_history = []
        self.game_over_flag = False
        if self.engine:
            try:
                self.engine.set_elo_rating(self._engine_elo())
                self.engine.set_depth(self._engine_depth())
            except Exception:
                pass
        self.draw_board()
        self.update_status()
        if self.player_color == chess.BLACK:
            self.root.after(300, self.ai_move)

    def undo(self):
        if self.game_over_flag or len(self.move_history) < 2 and self.player_color == chess.WHITE:
            # allow single undo if engine hasn't moved yet
            if len(self.move_history) == 1 and self.player_color == chess.BLACK:
                pass
            else:
                return
        # Undo engine + player move
        for _ in range(2):
            if self.board.move_stack:
                self.board.pop()
        self.move_history = [m.uci() for m in self.board.move_stack]
        self.selected = None
        self.legal_targets = {}
        self.game_over_flag = False
        self.draw_board()
        self.update_status()

    def on_square_click(self, sq: int):
        if self.game_over_flag:
            return
        if self.board.turn != self.player_color:
            return

        piece = self.board.piece_at(sq)

        # 1. Clicked a legal target -> move there
        if sq in self.legal_targets:
            self.make_player_move(self.legal_targets[sq])
            return

        # 2. Clicked own piece -> select it
        if piece and piece.color == self.player_color:
            self.selected = sq
            self.legal_targets = {
                m.to_square: m
                for m in self.board.legal_moves
                if m.from_square == sq
            }
            self.draw_board()
            return

        # 3. Clicked elsewhere -> deselect
        self.selected = None
        self.legal_targets = {}
        self.draw_board()

    def make_player_move(self, move: chess.Move):
        # Auto-promote to Queen (hold Shift in a real app for choice)
        if move.promotion is None:
            # check if promotion is needed
            promos = [m for m in self.board.legal_moves
                      if m.from_square == move.from_square
                      and m.to_square == move.to_square and m.promotion]
            if promos:
                move = promos[0]  # queen is first

        self.board.push(move)
        self.move_history.append(move.uci())
        self.selected = None
        self.legal_targets = {}
        self.draw_board()
        self.update_status()

        if self.check_game_over():
            return
        self.root.after(250, self.ai_move)

    def ai_move(self):
        if self.game_over_flag or self.board.is_game_over():
            return

        move = None
        if self.engine:
            try:
                self.engine.set_fen_position(self.board.fen())
                uci = self.engine.get_best_move()
                if uci:
                    move = chess.Move.from_uci(uci)
            except Exception:
                move = None

        if move is None or move not in self.board.legal_moves:
            move = random.choice(list(self.board.legal_moves))

        self.board.push(move)
        self.move_history.append(move.uci())
        self.draw_board()
        self.update_status()
        self.check_game_over()

    def check_game_over(self):
        if not self.board.is_game_over():
            return False
        self.game_over_flag = True
        result = self.board.result()
        if self.board.is_checkmate():
            winner = "You win!" if self.board.turn != self.player_color else "Engine wins!"
            msg = f"Checkmate! {winner} ({result})"
        elif self.board.is_stalemate():
            msg = "Draw — Stalemate"
        elif self.board.is_insufficient_material():
            msg = "Draw — Insufficient material"
        elif self.board.is_seventyfive_moves():
            msg = "Draw — 75-move rule"
        elif self.board.is_fivefold_repetition():
            msg = "Draw — Fivefold repetition"
        else:
            msg = f"Game over — {result}"
        self.status.config(text=msg)
        messagebox.showinfo("Game Over", msg)
        return True

    def save_game(self):
        game = chess.pgn.Game.from_board(self.board)
        game.headers["Event"] = "Casual vs Engine"
        game.headers["White"] = "Player" if self.player_color == chess.WHITE else "Engine"
        game.headers["Black"] = "Engine" if self.player_color == chess.WHITE else "Player"
        game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
        game.headers["Result"] = self.board.result() if self.board.is_game_over() else "*"

        filename = f"game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pgn"
        with open(filename, "w") as f:
            f.write(str(game))
        messagebox.showinfo("Saved", f"Saved to {filename}")

    # ---------- Rendering ----------
    def draw_board(self):
        last_move = self.board.peek() if self.board.move_stack else None
        king_sq = None
        if self.board.is_check():
            king_sq = self.board.king(self.board.turn)

        for sq, btn in self.squares.items():
            file, rank = chess.square_file(sq), chess.square_rank(sq)
            is_light = (file + rank) % 2 == 1
            bg = LIGHT if is_light else DARK

            if sq == self.selected:
                bg = SELECT
            elif last_move and sq in (last_move.from_square, last_move.to_square):
                bg = LAST_MOVE
            elif sq == king_sq:
                bg = CHECK

            piece = self.board.piece_at(sq)
            text = PIECES[piece.symbol()] if piece else ""
            if sq in self.legal_targets and not piece:
                text = "•"  # dot for empty legal move
                btn.config(font=("Segoe UI Symbol", 18), fg="#2F2F2F")
            elif sq in self.legal_targets and piece:
                # capture target — keep piece, add ring via bg already
                btn.config(font=("Segoe UI Symbol", 28), fg="black")
            else:
                fg = "white" if piece and piece.color == chess.BLACK else "black"
                btn.config(font=("Segoe UI Symbol", 28), fg=fg)

            btn.config(text=text, bg=bg, activebackground=bg)

    def update_status(self):
        if self.board.is_game_over():
            return
        turn = "Your turn" if self.board.turn == self.player_color else "Engine thinking..."
        check = " — Check!" if self.board.is_check() else ""
        eval_text = ""
        if self.engine and not self.board.is_game_over():
            try:
                self.engine.set_fen_position(self.board.fen())
                ev = self.engine.get_evaluation()
                value = ev.get("value", 0)
                if isinstance(value, str):
                    try:
                        value = int(value)
                    except ValueError:
                        value = 0
                if ev.get("type") == "mate":
                    eval_text = f" | Mate in {value}"
                else:
                    eval_text = f" | Eval: {value/100:+.2f}"
            except Exception:
                pass
        self.status.config(text=f"{turn}{check}{eval_text}")

        # Move list in SAN, 2 columns
        self.moves_text.config(state="normal")
        self.moves_text.delete("1.0", tk.END)
        temp = chess.Board()
        lines: list[str] = []
        for i, m in enumerate(self.board.move_stack):
            san = temp.san(m)
            temp.push(m)
            if i % 2 == 0:
                lines.append(f"{i//2+1}. {san}")
            else:
                lines[-1] += f"  {san}"
        self.moves_text.insert(tk.END, "\n".join(lines))
        self.moves_text.config(state="disabled")

    def start_game(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = ChessGame()
    game.start_game()