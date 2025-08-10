import matplotlib.pyplot as plt
import numpy as np

# Data
labels = ['A', 'B', 'C', 'D']
men_values = [10, 15, 7, 12]
women_values = [8, 12, 10, 9]

# Create the figure and axis
x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 6))

# Create the bar chart
rects1 = ax.bar(x - width/2, men_values, width, label='Men')
rects2 = ax.bar(x + width/2, women_values, width, label='Women')

# Set labels and title
ax.set_xlabel('Group')
ax.set_ylabel('Value')
ax.set_title('Grouped Bar Chart')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

# Show the plot
plt.show()