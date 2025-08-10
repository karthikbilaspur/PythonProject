import numpy as np
import matplotlib.pyplot as plt

# Data
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# Scatter plot data
scatter_x = np.random.uniform(-10, 10, 50)
scatter_y = np.random.uniform(-10, 10, 50)

# Create the figure and axis
plt.figure(figsize=(8, 8))

# Create the contour plot
plt.contourf(X, Y, Z, levels=20)
plt.contour(X, Y, Z, levels=20, colors='black')

# Add scatter plot
plt.scatter(scatter_x, scatter_y, color='red')

# Set labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Contour Plot with Scatter Plot')

# Show the plot
plt.show()