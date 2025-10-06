import turtle as t

# Set up the screen
screen = t.Screen()
screen.setup(width=800, height=600)  # Set the screen size

# Create a turtle object
tim = t.Turtle()
tim.speed(0)  # Fastest speed

def move_forward():
    """Move the turtle forward by 10 units"""
    tim.forward(10)

def move_backward():
    """Move the turtle backward by 10 units"""
    tim.backward(10)

def turn_clockwise():
    """Turn the turtle clockwise by 10 degrees"""
    tim.right(10)

def turn_anticlockwise():
    """Turn the turtle anticlockwise by 10 degrees"""
    tim.left(10)

def clear_screen():
    """Clear the screen and reset the turtle's position"""
    tim.clear()
    tim.penup()
    tim.home()
    tim.pendown()

# Bind keys to functions
screen.listen()
screen.onkey(key="w", fun=move_forward)
screen.onkey(key="s", fun=move_backward)
screen.onkeypress(key="d", fun=turn_clockwise)
screen.onkeypress(key="a", fun=turn_anticlockwise)
screen.onkey(key="c", fun=clear_screen)

# Add a title to the screen
screen.title("Turtle Graphics")

# Keep the window open
screen.mainloop()