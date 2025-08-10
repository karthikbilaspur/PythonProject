import numpy as np
import matplotlib.pyplot as plt

# Data
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# Create the figure and axis
fig = plt.figure(figsize=(12, 6))

# Create the 3D surface plot
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(X, Y, Z, cmap='viridis')
ax1.set_title('3D Surface Plot')

# Create the contour plot
ax2 = fig.add_subplot(122)
ax2.contourf(X, Y, Z, levels=20)
ax2.contour(X, Y, Z, levels=20, colors='black')
ax2.set_title('Contour Plot')

# Show the plot
plt.show()