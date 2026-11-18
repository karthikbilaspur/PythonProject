
import tkinter as tk
from random import randint, choice
import time

class LudoGame:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("Ludo Game - Full Version")
        self.root.geometry("720x820")
        self.root.resizable(False, False)

        self.colors = ["red", "green", "yellow", "blue"]
        self.names = ["Red", "Green", "Yellow", "Blue"]
        # Start index on 52-cell track
        self.start_idx = [0, 13, 26, 39]
        self.safe = [0, 8, 13, 21, 26, 34, 39, 47]
        self.mode = tk.StringVar(value="vs_cpu")  # vs_cpu, 2p, 4p
        self.num_players = 2
        self.current_player = 0
        self.dice_value = 0
        self.can_move = False
        self.movable = []  # list of token indices for current player that can move
        self.animating = False

        # positions[player][token] : -1 base, 0-51 main track offset, 52-57 home col, 58 finished
        self.positions = [[-1]*4 for _ in range(4)]
        self.tokens: list[list[int]] = [[-1]*4 for _ in range(4)]

        # --- Top bar: mode select ---
        top = tk.Frame(root)
        top.pack(pady=8)
        tk.Label(top, text="Mode:", font=("Arial", 11, "bold")).pack(side="left")
        tk.Radiobutton(top, text="You vs Computer", variable=self.mode, value="vs_cpu", command=self.change_mode).pack(side="left", padx=6)
        tk.Radiobutton(top, text="2 Players", variable=self.mode, value="2p", command=self.change_mode).pack(side="left", padx=6)
        tk.Radiobutton(top, text="4 Players", variable=self.mode, value="4p", command=self.change_mode).pack(side="left", padx=6)

        self.canvas = tk.Canvas(root, width=600, height=600, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.path = self.build_path()
        self.create_board()
        self.create_all_tokens()

        controls = tk.Frame(root)
        controls.pack(pady=8)
        self.roll_btn = tk.Button(controls, text="🎲 Roll Dice", command=self.roll_dice, font=("Arial", 13, "bold"), bg="#222", fg="white", padx=18, pady=6)
        self.roll_btn.pack(side="left", padx=8)
        self.reset_btn = tk.Button(controls, text="Reset", command=self.reset_game, font=("Arial", 11), padx=12)
        self.reset_btn.pack(side="left", padx=8)
        self.hint_btn = tk.Button(controls, text="Auto / Hint", command=self.auto_move, font=("Arial", 11), padx=12)
        self.hint_btn.pack(side="left", padx=8)

        self.turn_label = tk.Label(root, text="", font=("Arial", 13, "bold"))
        self.turn_label.pack()
        self.dice_label = tk.Label(root, text="🎲  -", font=("Arial", 22, "bold"))
        self.dice_label.pack()
        self.msg_label = tk.Label(root, text="Red starts. Roll a 6 to leave base!", font=("Arial", 11), fg="#333", wraplength=650)
        self.msg_label.pack(pady=2)
        self.score_label = tk.Label(root, text="", font=("Arial", 10), fg="#555")
        self.score_label.pack()

        self.update_labels()
        self.update_score()

    # ---------- Board ----------
    def build_path(self):
        coords = [
            (6,13),(6,12),(6,11),(6,10),(6,9),
            (5,8),(4,8),(3,8),(2,8),(1,8),(0,8),
            (0,7),(0,6),
            (1,6),(2,6),(3,6),(4,6),(5,6),
            (6,5),(6,4),(6,3),(6,2),(6,1),(6,0),
            (7,0),(8,0),
            (8,1),(8,2),(8,3),(8,4),(8,5),
            (9,6),(10,6),(11,6),(12,6),(13,6),(14,6),
            (14,7),(14,8),
            (13,8),(12,8),(11,8),(10,8),(9,8),
            (8,9),(8,10),(8,11),(8,12),(8,13),(8,14),
            (7,14),(6,14),
        ]
        return [(c*40, r*40) for c, r in coords]

    def create_board(self):
        # Bases: Red TL, Green TR, Yellow BR, Blue BL
        bases = [(0,0,"red"), (9,0,"green"), (9,9,"yellow"), (0,9,"blue")]
        for bx, by, col in bases:
            self.canvas.create_rectangle(bx*40, by*40, (bx+6)*40, (by+6)*40, fill=col, outline="black", width=2)
            self.canvas.create_rectangle((bx+1)*40, (by+1)*40, (bx+5)*40, (by+5)*40, fill="white")
            self.canvas.create_text((bx+3)*40, (by+0.4)*40, text=col.upper(), font=("Arial", 9, "bold"), fill="white")
        # Center
        self.canvas.create_rectangle(6*40, 6*40, 9*40, 9*40, fill="gold", outline="black", width=2)
        self.canvas.create_text(7.5*40, 7.5*40, text="HOME", font=("Arial", 11, "bold"))
        # Path
        for i, (x, y) in enumerate(self.path):
            fill = "#ffd166" if i in self.safe else "white"
            self.canvas.create_rectangle(x, y, x+40, y+40, fill=fill, outline="#999")
            if i in self.safe:
                self.canvas.create_text(x+20, y+20, text="★", font=("Arial", 10), fill="#888")
        # Home columns colors
        home_cols = [
            ([(6,14),(6,13),(6,12),(6,11),(6,10),(6,9)], "red"),
            ([(1,8),(2,8),(3,8),(4,8),(5,8),(6,8)], "green"),
            ([(13,8),(12,8),(11,8),(10,8),(9,8),(8,8)], "yellow"),
            ([(8,1),(8,2),(8,3),(8,4),(8,5),(8,6)], "blue"),
        ]
        for cells, col in home_cols:
            for c, r in cells:
                self.canvas.create_rectangle(c*40, r*40, (c+1)*40, (r+1)*40, fill=col, outline="black", stipple="gray25")

    def base_positions_for(self, player: int):
        # 4 spots inside base
        bases_origin = [(0,0),(9,0),(9,9),(0,9)] # red, green, yellow, blue
        bx, by = bases_origin[player]
        offsets = [(2,2),(4,2),(2,4),(4,4)]
        return [((bx+ox)*40+10, (by+oy)*40+10) for ox, oy in offsets]  # top-left of 20px token box? we use center calc below
        # Actually return centers
    def base_center(self, player: int, token_idx: int) -> tuple[int, int]:
        bases_origin = [(0,0),(9,0),(9,9),(0,9)]
        bx, by = bases_origin[player]
        offsets = [(2,2),(4,2),(2,4),(4,4)]
        ox, oy = offsets[token_idx]
        return ((bx+ox)*40+20, (by+oy)*40+20)

    def home_cell(self, player: int, pos: int) -> tuple[int, int]:
        # pos 52-57
        home_paths = {
            0: [(6,14),(6,13),(6,12),(6,11),(6,10),(6,9)],
            1: [(1,8),(2,8),(3,8),(4,8),(5,8),(6,8)],
            2: [(13,8),(12,8),(11,8),(10,8),(9,8),(8,8)],
            3: [(8,1),(8,2),(8,3),(8,4),(8,5),(8,6)],
        }
        c, r = home_paths[player][pos-52]
        return (c*40+20, r*40+20)

    def get_xy(self, player: int, token_idx: int) -> tuple[int, int]:
        pos = self.positions[player][token_idx]
        if pos == -1:
            return self.base_center(player, token_idx)
        if pos >= 58:
            return (300, 300)
        if pos >= 52:
            return self.home_cell(player, pos)
        idx = (self.start_idx[player] + pos) % 52
        x, y = self.path[idx]
        return (x+20, y+20)

    def create_all_tokens(self):
        for p in range(4):
            for t in range(4):
                cx, cy = self.get_xy(p, t)
                oid = self.canvas.create_oval(cx-13, cy-13, cx+13, cy+13, fill=self.colors[p], outline="black", width=2, tags=f"token_{p}_{t}")
                # white dot in middle for visibility
                self.canvas.create_oval(cx-4, cy-4, cx+4, cy+4, fill="white", outline="", tags=f"token_{p}_{t}")
                self.tokens[p][t] = oid

    def refresh_token(self, p: int, t: int) -> None:
        cx, cy = self.get_xy(p, t)
        # offset stacking: count tokens on same board cell
        pos = self.positions[p][t]
        if pos != -1 and pos < 58:
            # simpler: collect all tokens with the same absolute board position
            stack: list[tuple[int, int]] = []
            for pp in range(4):
                for tt in range(4):
                    if pp==p and tt==t:
                        continue
                    if self.same_cell(p, t, pp, tt):
                        stack.append((pp, tt))
            if stack:
                # offset by index in stack
                idx = len(stack)  # rough
                cx += (idx % 2)*10 - 5
                cy += (idx // 2)*10 - 5
        self.canvas.coords(self.tokens[p][t], cx-13, cy-13, cx+13, cy+13)
        # move white dot too - find items with tag
        items = self.canvas.find_withtag(f"token_{p}_{t}")
        # items[0] is outer, items[1] is dot
        if len(items) >= 2:
            self.canvas.coords(items[1], cx-4, cy-4, cx+4, cy+4)

    def same_cell(self, p1: int, t1: int, p2: int, t2: int) -> bool:
        pos1 = self.positions[p1][t1]
        pos2 = self.positions[p2][t2]
        if pos1 == -1 or pos2 == -1 or pos1 >= 52 or pos2 >= 52:
            return pos1 == pos2 and pos1 != -1 and p1==p2  # home col same player only
        a = (self.start_idx[p1] + pos1) % 52
        b = (self.start_idx[p2] + pos2) % 52
        return a == b

    def refresh_all(self):
        for p in range(4):
            for t in range(4):
                self.refresh_token(p, t)

    # ---------- Game flow ----------
    def change_mode(self):
        m = self.mode.get()
        if m == "vs_cpu":
            self.num_players = 2
        elif m == "2p":
            self.num_players = 2
        else:
            self.num_players = 4
        self.reset_game()
        if m == "vs_cpu":
            self.msg_label.config(text="You are Red. Computer is Green. Roll a 6 to start!")
        elif m == "2p":
            self.msg_label.config(text="2 Players: Red vs Green. Red starts.")
        else:
            self.msg_label.config(text="4 Players: Red starts.")

    def is_cpu_turn(self):
        return self.mode.get() == "vs_cpu" and self.current_player == 1

    def update_labels(self):
        name = self.names[self.current_player]
        if self.is_cpu_turn():
            name += " (Computer)"
        self.turn_label.config(text=f"{name}'s Turn  •  {self.colors[self.current_player].capitalize()}", fg=self.colors[self.current_player])
        self.root.title(f"Ludo - {name}'s Turn")

    def update_score(self):
        parts: list[str] = []
        for p in range(self.num_players):
            finished = sum(1 for v in self.positions[p] if v == 58)
            on_board = sum(1 for v in self.positions[p] if v >= 0)
            parts.append(f"{self.names[p]}: {finished}/4 home • {on_board} out")
        self.score_label.config(text="  |  ".join(parts))

    def get_movable(self, player: int, roll: int) -> list[int]:
        res: list[int] = []
        for t in range(4):
            pos = self.positions[player][t]
            if pos == -1:
                if roll == 6:
                    res.append(t)
            elif pos + roll <= 58:
                res.append(t)
        return res

    def roll_dice(self):
        if self.animating or self.can_move:
            return
        if self.is_cpu_turn():
            return
        self.do_roll()

    def do_roll(self):
        self.animating = True
        self.roll_btn.config(state="disabled")
        self.animate_dice(0)

    def animate_dice(self, step: int):
        if step < 8:
            self.dice_label.config(text=f"🎲 {randint(1,6)}")
            self.root.after(70, lambda: self.animate_dice(step+1))
        else:
            roll = randint(1, 6)
            self.dice_value = roll
            self.dice_label.config(text=f"🎲 {roll}")
            self.animating = False
            self.after_roll(roll)

    def after_roll(self, roll: int):
        p = self.current_player
        movable = self.get_movable(p, roll)
        self.movable = movable
        if not movable:
            self.msg_label.config(text=f"{self.names[p]} rolled {roll} - no move possible.")
            self.root.after(900, self.end_turn)
            return
        if len(movable) == 1:
            # Auto move if only one choice, but still show it briefly
            self.msg_label.config(text=f"{self.names[p]} rolled {roll} - moving token {movable[0]+1}")
            self.can_move = False
            self.root.after(500, lambda: self.move_token(p, movable[0], roll))
            return
        # Multiple choices - player must click
        self.can_move = True
        self.highlight_movable()
        if self.is_cpu_turn():
            self.root.after(700, self.cpu_choose)
        else:
            self.msg_label.config(text=f"{self.names[p]} rolled {roll} - CLICK one of the glowing tokens to move it!")
            self.roll_btn.config(state="disabled")

    def highlight_movable(self):
        for t in self.movable:
            oid = self.tokens[self.current_player][t]
            self.canvas.itemconfig(oid, outline="gold", width=4)
            # pulse: bring to front
            self.canvas.tag_raise(oid)

    def clear_highlight(self):
        for p in range(4):
            for t in range(4):
                self.canvas.itemconfig(self.tokens[p][t], outline="black", width=2)
        self.can_move = False
        self.movable = []

    def on_canvas_click(self, event: tk.Event) -> None:
        if not self.can_move or self.animating:
            return
        # Find closest token
        clicked = self.canvas.find_closest(event.x, event.y)
        if not clicked:
            return
        tags = self.canvas.gettags(clicked[0])
        for tag in tags:
            if tag.startswith("token_"):
                _, p_str, t_str = tag.split("_")
                p, t = int(p_str), int(t_str)
                if p == self.current_player and t in self.movable:
                    self.move_token(p, t, self.dice_value)
                elif p == self.current_player:
                    self.msg_label.config(text=f"That token can't move with {self.dice_value}. Pick a glowing one!")
                return

    def cpu_choose(self):
        # Simple CPU: prefer capture > finish > leave base > move furthest
        p = self.current_player
        roll = self.dice_value
        best = self.movable[0]
        best_score = -999
        for t in self.movable:
            pos = self.positions[p][t]
            score = 0
            if pos == -1:
                score = 50
            elif pos + roll == 58:
                score = 100
            elif pos + roll < 52:
                target = (self.start_idx[p] + pos + roll) % 52
                # capture?
                for op in range(self.num_players):
                    if op == p: continue
                    for ot in range(4):
                        opos = self.positions[op][ot]
                        if 0 <= opos < 52:
                            oidx = (self.start_idx[op] + opos) % 52
                            if oidx == target and target not in self.safe:
                                score += 80
                score += pos  # prefer advanced tokens
            else:
                score = 60 + pos
            if score > best_score:
                best_score = score
                best = t
        self.msg_label.config(text=f"Computer rolled {roll} - moving token {best+1}")
        self.move_token(p, best, roll)

    def auto_move(self):
        # Hint / auto for human: pick best move
        if self.can_move and not self.is_cpu_turn():
            self.cpu_choose()
        elif not self.can_move and not self.animating:
            self.msg_label.config(text="Roll the dice first!")

    def move_token(self, p: int, t: int, roll: int) -> None:
        self.clear_highlight()
        old = self.positions[p][t]
        if old == -1:
            self.positions[p][t] = 0
            self.msg_label.config(text=f"{self.names[p]}'s token {t+1} leaves base! 🎉")
        else:
            self.positions[p][t] = old + roll
            if self.positions[p][t] == 58:
                self.msg_label.config(text=f"{self.names[p]}'s token {t+1} reached HOME! 🏠")
        self.refresh_token(p, t)
        self.update_score()

        # Capture check
        captured = None
        new_pos = self.positions[p][t]
        if 0 <= new_pos < 52:
            board_idx = (self.start_idx[p] + new_pos) % 52
            if board_idx not in self.safe:
                for op in range(self.num_players):
                    if op == p: continue
                    for ot in range(4):
                        opos = self.positions[op][ot]
                        if 0 <= opos < 52:
                            oidx = (self.start_idx[op] + opos) % 52
                            if oidx == board_idx:
                                self.positions[op][ot] = -1
                                self.refresh_token(op, ot)
                                captured = (op, ot)
                                self.msg_label.config(text=f"{self.names[p]} captured {self.names[op]}'s token {ot+1}! 💥")
                                break
                    if captured:
                        break
        self.update_score()

        # Win check: all 4 home
        if all(v == 58 for v in self.positions[p]):
            self.game_over(p)
            return

        # Extra turn on 6
        if roll == 6:
            self.msg_label.config(text=self.msg_label.cget("text") + "  • Rolled 6 - roll again!")
            self.end_turn(extra=True)
        else:
            self.end_turn(extra=False)

    def end_turn(self, extra: bool = False) -> None:
        if not extra:
            self.current_player = (self.current_player + 1) % self.num_players
        self.update_labels()
        self.update_score()
        self.roll_btn.config(state="normal")
        if self.is_cpu_turn():
            self.roll_btn.config(state="disabled")
            self.msg_label.config(text="Computer's turn...")
            self.root.after(900, self.do_roll)
        else:
            if extra:
                self.msg_label.config(text=self.msg_label.cget("text") + " Roll again!")
            else:
                # keep message if capture etc, else generic
                pass

    def game_over(self, player: int) -> None:
        self.msg_label.config(text=f"🏆 {self.names[player]} WINS! All 4 tokens home!")
        self.turn_label.config(text=f"{self.names[player]} Wins!")
        self.roll_btn.config(state="disabled")
        self.can_move = False

    def reset_game(self):
        self.current_player = 0
        self.positions = [[-1]*4 for _ in range(4)]
        self.dice_value = 0
        self.can_move = False
        self.movable = []
        self.animating = False
        self.clear_highlight()
        self.refresh_all()
        self.dice_label.config(text="🎲  -")
        self.roll_btn.config(state="normal")
        self.update_labels()
        self.update_score()
        self.msg_label.config(text="New game! Red starts. Roll a 6 to leave base.")

if __name__ == "__main__":
    root = tk.Tk()
    game = LudoGame(root)
    root.mainloop()
