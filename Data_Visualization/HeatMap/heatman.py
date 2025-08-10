import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Data
np.random.seed(0)
data = pd.DataFrame({
    'A': np.random.rand(100),
    'B': np.random.rand(100),
    'C': np.random.rand(100),
    'D': np.random.rand(100),
    'E': np.random.rand(100),
})

# Calculate the correlation matrix
corr_matrix = data.corr()

# Create the heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)

# Set labels and title
plt.title('Correlation Matrix Heatmap')

# Show the plot
plt.show()