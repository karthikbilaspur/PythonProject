import matplotlib.pyplot as plt
import numpy as np

# Data
np.random.seed(0)
x = np.random.randn(10)
y = np.random.randn(10)
sizes = np.random.uniform(10, 500, 10)  
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# Create the figure and axis
fig, ax = plt.subplots(figsize=(8, 8))

# Create the bubble chart
for i, (x_val, y_val, size, label) in enumerate(zip(x, y, sizes, labels)):
    ax.scatter(x_val, y_val, s=size, alpha=0.5, label=label)

# Set labels and title
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_title('Bubble Chart Example')

# Legend
plt.legend()

# Show the plot
plt.show()