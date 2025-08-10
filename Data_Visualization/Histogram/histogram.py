import matplotlib.pyplot as plt
import numpy as np

# Data
np.random.seed(0)
scores = np.random.normal(75, 10, 100)

# Create the histogram
plt.figure(figsize=(8, 6))
plt.hist(scores, bins=10, alpha=0.7, color='blue', edgecolor='black')

# Set labels and title
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.title('Distribution of Exam Scores')

# Add a vertical line for the mean score
mean_score = np.mean(scores)
plt.axvline(mean_score, color='red', linestyle='dashed', linewidth=2, label=f'Mean Score: {mean_score:.2f}')

# Add a legend
plt.legend()

# Show the plot
plt.show()