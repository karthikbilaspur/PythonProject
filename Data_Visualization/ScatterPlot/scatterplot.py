import matplotlib.pyplot as plt
import numpy as np

# Data
np.random.seed(0)
x = np.random.rand(100)
y = np.random.rand(100)

# Create the scatter plot
plt.figure(figsize=(8, 8))
plt.scatter(x, y, s=100, c=y, cmap='plasma', alpha=0.7, edgecolors='black', marker='*')

# Set labels and title
plt.xlabel('X Axis', fontsize=14)
plt.ylabel('Y Axis', fontsize=14)
plt.title('Enhanced Scatter Plot', fontsize=16)

# Add annotations
for i in range(10):
    plt.annotate(f'({x[i]:.2f}, {y[i]:.2f})', (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Add a color bar
plt.colorbar(label='Y Value')

# Show the plot
plt.tight_layout()
plt.show()