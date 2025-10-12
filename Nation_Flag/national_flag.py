import turtle

def draw_rectangle(turtle, x, y, width, height, color):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.color(color)
    turtle.begin_fill()
    for _ in range(2):
        turtle.forward(width)
        turtle.right(90)
        turtle.forward(height)
        turtle.right(90)
    turtle.end_fill()

def draw_circle(turtle, x, y, radius, color):
    turtle.penup()
    turtle.goto(x, y - radius)
    turtle.pendown()
    turtle.color(color)
    turtle.begin_fill()
    turtle.circle(radius)
    turtle.end_fill()

def draw_spokes(turtle, x, y, radius, num_spokes, color):
    turtle.penup()
    turtle.goto(x, y)
    turtle.setheading(90)
    turtle.color(color)
    turtle.pensize(2)
    for _ in range(num_spokes):
        turtle.pendown()
        turtle.forward(radius)
        turtle.backward(radius)
        turtle.right(360 / num_spokes)

def main():
    # Create the turtle screen
    screen = turtle.Screen()
    screen.title("Indian National Flag Animation")
    screen.bgcolor("white")

    # Set up the turtle object
    flag_turtle = turtle.Turtle()
    flag_turtle.speed(2)

    # Draw the Indian National Flag
    draw_rectangle(flag_turtle, -200, 150, 400, 50, "#FF9933")  # Orange band
    draw_rectangle(flag_turtle, -200, 100, 400, 50, "white")  # White band
    draw_rectangle(flag_turtle, -200, 50, 400, 50, "#138808")  # Green band

    # Draw the Ashoka Chakra
    draw_circle(flag_turtle, 0, 75, 30, "navy")  # Blue circle
    draw_spokes(flag_turtle, 0, 75, 30, 24, "#FF9933")  # 24 spokes

    # Hide the turtle cursor
    flag_turtle.hideturtle()

    # Close the turtle graphics window on click
    turtle.exitonclick()

if __name__ == "__main__":
    main()