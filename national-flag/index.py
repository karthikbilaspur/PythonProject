import turtle
import math
import time

# --- Setup ---
screen = turtle.Screen()
screen.title("Indian National Flag - Waving Animation")
screen.bgcolor("#87CEEB")
screen.setup(900, 600)
screen.tracer(0)  # manual refresh = smooth animation

t = turtle.Turtle()
t.hideturtle()
t.penup()

# --- Colors ---
SAFFRON = "#FF9933"
GREEN = "#138808"
NAVY = "#06038D"
POLE_COLOR = "#6B4226"
GOLD = "#DAA520"

FLAG_X = -250
FLAG_Y_TOP = 180
FLAG_W = 450
FLAG_H = 210
BAND_H = FLAG_H // 3

def draw_pole():
    t.goto(-290, -230)
    t.color(POLE_COLOR)
    t.fillcolor(POLE_COLOR)
    t.begin_fill()
    t.pendown()
    for _ in range(2):
        t.forward(14)
        t.right(90)
        t.forward(430)
        t.right(90)
    t.end_fill()
    t.penup()
    # Golden finial
    t.goto(-283, 205)
    t.dot(22, GOLD)
    t.goto(-283, 220)
    t.dot(10, GOLD)

def draw_ground():
    t.goto(-450, -230)
    t.color("#4CAF50")
    t.fillcolor("#4CAF50")
    t.begin_fill()
    t.pendown()
    t.goto(450, -230)
    t.goto(450, -300)
    t.goto(-450, -300)
    t.goto(-450, -230)
    t.end_fill()
    t.penup()

def draw_cloud(cx: float, cy: float, scale: float = 1.0) -> None:
    t.color("white")
    t.fillcolor("white")
    for dx, dy, r in [(-40, 0, 22), (0, 8, 28), (40, 0, 22)]:
        t.goto(cx + dx * scale, cy + dy * scale)
        t.dot(int(r * 2 * scale), "white")

def wave_y(x: float, time_offset: float) -> float:
    """Sine wave offset - makes flag look like it's waving"""
    return math.sin((x / 60) + time_offset) * 8

def draw_flag(time_offset: float) -> None:
    # Clear only flag area by redrawing 3 wavy bands
    for band, color in enumerate([SAFFRON, "white", GREEN]):
        band_top = FLAG_Y_TOP - band * BAND_H
        band_bottom = band_top - BAND_H

        t.color(color)
        t.fillcolor(color)
        t.begin_fill()
        t.penup()
        t.goto(FLAG_X, band_top + wave_y(FLAG_X, time_offset))
        t.pendown()
        # Top edge (wavy)
        for x in range(FLAG_X, FLAG_X + FLAG_W + 1, 10):
            t.goto(x, band_top + wave_y(x, time_offset))
        # Right edge down
        for y in range(int(band_top), int(band_bottom), -5):
            t.goto(FLAG_X + FLAG_W, y + wave_y(FLAG_X + FLAG_W, time_offset))
        # Bottom edge (wavy, reverse)
        for x in range(FLAG_X + FLAG_W, FLAG_X - 1, -10):
            t.goto(x, band_bottom + wave_y(x, time_offset))
        # Left edge up
        t.goto(FLAG_X, band_top + wave_y(FLAG_X, time_offset))
        t.end_fill()
        t.penup()

def draw_chakra(cx: float, cy: float, radius: float, rotation: float) -> None:
    # Center of flag
    # Add wave offset so chakra moves with flag
    cy += wave_y(cx, rotation * 0.3)

    t.color(NAVY)
    t.pensize(2)
    # Outer circle
    t.goto(cx, cy - radius)
    t.pendown()
    t.circle(radius)
    t.penup()

    # Center hub
    t.goto(cx, cy)
    t.dot(7, NAVY)

    # 24 spokes - rotating
    t.pensize(1)
    for i in range(24):
        angle = rotation + i * (360 / 24)
        t.goto(cx, cy)
        t.setheading(90 + angle)
        t.pendown()
        t.forward(radius)
        t.penup()

# --- Main animation loop ---
frame = 0
while True:
    t.clear()
    draw_ground()
    draw_cloud(-280, 240, 0.8)
    draw_cloud(220, 250, 1.1)
    draw_cloud(80, 220, 0.7)
    draw_pole()

    time_offset = frame * 0.15
    draw_flag(time_offset)

    # Chakra in middle of flag
    chakra_x = FLAG_X + FLAG_W // 2
    chakra_y = FLAG_Y_TOP - BAND_H - BAND_H // 2
    draw_chakra(chakra_x, chakra_y, 28, frame * 1.2)

    # Title
    t.goto(0, -265)
    t.color("white")
    t.write("Proud to be Indian  •  Jai Hind",
            align="center", font=("Arial", 16, "bold"))

    screen.update()
    time.sleep(0.03)
    frame += 1