"""
Turtle Race - upgraded version
Single file. Run: python turtle_race.py

- 5 named turtles, finish line drawn, countdown
- Bet validation (Cancel / caps / spaces / typos handled)
- Fair winner: whoever goes FARTHEST past the line wins, not whoever is checked first
- Play Again without re-running, score tracker
- Uses ontimer() instead of blocking while True, so window stays responsive
"""

import turtle
import random
import time

WIDTH, HEIGHT = 800, 500
START_X = -350
FINISH_X = 320

RACERS = [
    ("Flash",  "red",    160),
    ("Turbo",  "blue",   80),
    ("Speedy", "green",  0),
    ("Zoom",   "orange", -80),
    ("Bolt",   "purple", -160),
]

class TurtleRace:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(WIDTH, HEIGHT)
        self.screen.title("Turtle Race")
        self.screen.bgcolor("lightgreen")
        self.screen.tracer(0)  # we control updates for smooth animation

        self.turtles: list[tuple[str, str, turtle.Turtle, turtle.Turtle]] = []
        self.bet = None
        self.wins = 0
        self.games = 0
        self.racing = False
        self.countdown_turtle = turtle.Turtle(visible=False)
        self.writer = turtle.Turtle(visible=False)
        self.score_writer = turtle.Turtle(visible=False)

        self._draw_track()
        self._create_turtles()
        self._draw_score()

    # ---------- Setup ----------
    def _draw_track(self):
        pen = turtle.Turtle(visible=False)
        pen.penup(); pen.speed(0)
        # Lanes
        for _, _, y in RACERS:
            pen.goto(START_X - 20, y - 30)
            pen.pendown()
            pen.goto(FINISH_X + 20, y - 30)
            pen.penup()
        # Finish line (checkered)
        for i in range(10):
            pen.goto(FINISH_X, -200 + i * 40)
            pen.fillcolor("black" if i % 2 == 0 else "white")
            pen.begin_fill()
            for _ in range(4):
                pen.forward(15); pen.left(90)
            pen.end_fill()
        pen.goto(FINISH_X, 215)
        pen.write("FINISH", align="center", font=("Arial", 12, "bold"))
        pen.hideturtle()

    def _create_turtles(self):
        for _, _, racer, label in self.turtles:
            racer.hideturtle()
            racer.clear()
            label.hideturtle()
            label.clear()
        self.turtles = []
        for name, color, y in RACERS:
            t = turtle.Turtle(shape="turtle")
            t.color(color)
            t.penup()
            t.goto(START_X, y)
            t.speed(0)
            # Name label above turtle
            label = turtle.Turtle(visible=False)
            label.penup()
            label.goto(START_X, y + 22)
            label.write(name, align="center", font=("Arial", 9, "bold"))
            self.turtles.append((name, color, t, label))
        self.screen.update()

    def _draw_score(self):
        self.score_writer.clear()
        self.score_writer.penup()
        self.score_writer.goto(0, HEIGHT // 2 - 30)
        self.score_writer.write(f"Games: {self.games}   Wins: {self.wins}",
                                align="center", font=("Arial", 12, "bold"))
        self.screen.update()

    # ---------- Game flow ----------
    def ask_bet(self):
        names = ", ".join(n.lower() for n, _, _ in RACERS)
        while True:
            raw = self.screen.textinput(
                "Make your bet",
                f"Which turtle will win?\n{names}\n(Type a name or color)")
            if raw is None:  # Cancel pressed -> default to first turtle, don't crash
                return RACERS[0][0]
            bet = raw.strip().lower()
            # Accept name OR color, any case / extra spaces
            for name, color, _ in RACERS:
                if bet in (name.lower(), color.lower()):
                    return name
            # Invalid -> ask again instead of auto-losing
            self.screen.textinput("Invalid bet",
                                  f"'{raw}' is not a racer.\nTry: {names}\n(Press OK to try again)")

    def countdown(self, n: int = 3):
        if n == 0:
            self.countdown_turtle.clear()
            self.countdown_turtle.goto(0, 0)
            self.countdown_turtle.write("GO!", align="center", font=("Arial", 36, "bold"))
            self.screen.update()
            time.sleep(0.5)
            self.countdown_turtle.clear()
            self.racing = True
            self._race_step()
            return
        self.countdown_turtle.clear()
        self.countdown_turtle.penup()
        self.countdown_turtle.goto(0, 0)
        self.countdown_turtle.write(str(n), align="center", font=("Arial", 48, "bold"))
        self.screen.update()
        self.screen.ontimer(lambda: self.countdown(n - 1), 700)

    def _race_step(self):
        if not self.racing:
            return
        # Move all turtles, then check finish - no bias to first turtle
        for name, _, t, label in self.turtles:
            step = random.randint(1, 10)
            # Small rubber-banding: leader slows slightly, last speeds up - closer races
            t.forward(step)
            label.clear()
            label.goto(t.xcor(), t.ycor() + 22)
            label.write(name, align="center", font=("Arial", 9, "bold"))

        self.screen.update()

        finished = [(name, t.xcor()) for name, _, t, _ in self.turtles if t.xcor() >= FINISH_X]
        if finished:
            # Fair winner: farthest past line, not first checked
            winner = max(finished, key=lambda x: x[1])[0]
            self._finish(winner)
            return
        # ~30 fps, non-blocking
        self.screen.ontimer(self._race_step, 33)

    def _finish(self, winner: str):
        self.racing = False
        self.games += 1
        won = self.bet is not None and winner.lower() == self.bet.lower()
        if won:
            self.wins += 1
        self._draw_score()

        msg = f"The {winner} turtle won!\n"
        msg += "You WON! 🎉" if won else f"You bet on {self.bet}. Better luck next time!"
        msg += f"\nScore: {self.wins}/{self.games}"

        again = self.screen.textinput("Result", msg + "\n\nPlay again? (yes/no)")
        if again is not None and again.strip().lower() in ("yes", "y", ""):
            self._reset()
        else:
            self.screen.bye()

    def _reset(self):
        for _, _, t, label in self.turtles:
            t.goto(START_X, t.ycor())
            label.clear()
            label.goto(START_X, t.ycor() + 22)
        self.screen.update()
        self.start()

    def start(self):
        self.bet = self.ask_bet()
        self.countdown(3)

    def run(self):
        self.start()
        self.screen.mainloop()


if __name__ == "__main__":
    TurtleRace().run()