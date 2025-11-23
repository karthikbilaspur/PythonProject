import turtle
import random

# Set up the screen
screen = turtle.Screen()
screen.title("Turtle Race")
screen.bgcolor("lightgreen")

# Create turtles
turtle1 = turtle.Turtle()
turtle1.shape("turtle")
turtle1.color("red")
turtle1.penup()
turtle1.goto(-200, 100)

turtle2 = turtle.Turtle()
turtle2.shape("turtle")
turtle2.color("blue")
turtle2.penup()
turtle2.goto(-200, 50)

# Betting system
bet = screen.textinput("Make your bet", "Which turtle will win? (red/blue)")

# Game loop
while True:
    turtle1.forward(random.randint(1, 10))
    turtle2.forward(random.randint(1, 10))

    if turtle1.xcor() > 200:
        winner = "red"
        break
    elif turtle2.xcor() > 200:
        winner = "blue"
        break

# Display winner
if winner == bet:
    screen.textinput("Result", "You won!")
else:
    screen.textinput("Result", f"The {winner} turtle won!")

turtle.done()