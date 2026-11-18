import turtle as t

# Set up the screen
screen = t.Screen()
screen.setup(width=800, height=600)
screen.title("Turtle Graphics - Etch-A-Sketch Pro")
screen.bgcolor("white")

# Create turtle
tim = t.Turtle()
tim.shape("turtle")
tim.color("black")
tim.pensize(3)
tim.speed(0)  # fastest

# State
pen_is_down = True
current_color = "black"
colors = {
    "r": "red",
    "g": "green",
    "b": "blue",
    "y": "gold",
    "p": "purple",
    "k": "black",
    "o": "orange",
}
# Keep track of color keys for display
color_names = {"r": "Red", "g": "Green", "b": "Blue", "y": "Yellow", "p": "Purple", "k": "Black", "o": "Orange"}

# --- Movement ---
def move_forward():
    tim.forward(10)

def move_backward():
    tim.backward(10)

def turn_clockwise():
    tim.right(10)

def turn_anticlockwise():
    tim.left(10)

def move_forward_hold():
    # For smoother hold-to-move, called via onkeypress
    tim.forward(5)

def move_backward_hold():
    tim.backward(5)

# --- Pen Controls ---
def toggle_pen():
    """Space: Lift / put down pen"""
    global pen_is_down
    if pen_is_down:
        tim.penup()
        pen_is_down = False
        screen.title("Turtle Graphics - PEN UP (Space to draw again)")
    else:
        tim.pendown()
        pen_is_down = True
        screen.title("Turtle Graphics - Etch-A-Sketch Pro")

def clear_screen():
    """C: Clear and reset"""
    tim.clear()
    tim.penup()
    tim.home()
    tim.pendown()
    tim.color("black")
    tim.pensize(3)
    global pen_is_down
    pen_is_down = True
    screen.title("Turtle Graphics - Etch-A-Sketch Pro")

# --- Color / Size Controls ---
def set_color(key: str):
    def _inner():
        global current_color
        current_color = colors[key]
        tim.color(colors[key])
        screen.title(f"Turtle Graphics - Color: {color_names[key]}")
    return _inner

def increase_size():
    tim.pensize(tim.pensize() + 1)

def decrease_size():
    if tim.pensize() > 1:
        tim.pensize(tim.pensize() - 1)

def stamp_turtle():
    """X: Stamp a copy of turtle shape"""
    tim.stamp()

# --- Bind Keys ---
screen.listen()
# Movement - W/S tap, also hold to move smoothly
screen.onkey(key="w", fun=move_forward)
screen.onkey(key="s", fun=move_backward)
screen.onkeypress(key="w", fun=move_forward_hold)
screen.onkeypress(key="s", fun=move_backward_hold)
screen.onkeypress(key="d", fun=turn_clockwise)
screen.onkeypress(key="a", fun=turn_anticlockwise)

# Pen
screen.onkey(key="space", fun=toggle_pen)
screen.onkey(key="c", fun=clear_screen)
screen.onkey(key="x", fun=stamp_turtle)

# Colors
for k in colors:
    screen.onkey(key=k, fun=set_color(k))

# Pen size
screen.onkey(key="Up", fun=increase_size)
screen.onkey(key="Down", fun=decrease_size)

# Instructions in console
print("""
=== TURTLE ETCH-A-SKETCH PRO ===
MOVEMENT:
  W / S  - Forward / Backward (tap or hold)
  A / D  - Turn Left / Right (hold)

DRAWING:
  Space  - Pen Up / Down (move without drawing)
  C      - Clear screen + reset
  X      - Stamp turtle shape
  Up / Down Arrow - Thicker / Thinner pen

COLORS:
  R - Red    G - Green  B - Blue
  Y - Yellow P - Purple O - Orange
  K - Black
=================================
""")

screen.mainloop()
