import matplotlib.pyplot as plt
import numpy as np

# Data
labels = ['Start', 'A', 'B', 'C', 'D', 'End']
values = [0, 10, -5, 7, -3, 9]

# Calculate the cumulative sum
cumulative = np.cumsum(values)

# Create the waterfall chart
fig, ax = plt.subplots(figsize=(10, 6))
for i in range(len(values) - 1):
    if values[i + 1] > 0:
        ax.bar(labels[i + 1], values[i + 1], bottom=cumulative[i], color='green')
    else:
        ax.bar(labels[i + 1], values[i + 1], bottom=cumulative[i], color='red')

# Set labels and title
ax.set_xlabel('Category')
ax.set_ylabel('Value')
ax.set_title('Waterfall Chart')

# Show the plot
plt.show()