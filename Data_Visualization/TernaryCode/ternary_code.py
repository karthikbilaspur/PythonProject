import ternary
import matplotlib.pyplot as plt
import numpy as np

# Data
points = np.array([[0.2, 0.3, 0.5], [0.4, 0.4, 0.2], [0.1, 0.7, 0.2], [0.6, 0.2, 0.2], [0.3, 0.5, 0.2]])
values = np.array([10, 20, 30, 40, 50])

# Create the ternary plot
scale = 1
figure, tax = ternary.figure(scale=scale)

# Plot the points
tax.scatter(points, c=values, cmap='viridis', s=100, alpha=0.7, edgecolors='black')

# Set labels and title
tax.set_title("Enhanced Ternary Plot", fontsize=16)
tax.left_axis_label("Left", fontsize=14)
tax.right_axis_label("Right", fontsize=14)
tax.bottom_axis_label("Bottom", fontsize=14)

# Show the grid
tax.gridlines(multiple=0.1, color="blue")

# Add a color bar
plt.colorbar(label='Value', ax=tax.get_axes())

# Show the plot
tax.show()