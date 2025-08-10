import matplotlib.pyplot as plt

# Data
brands = ['Apple', 'Samsung', 'Huawei', 'Xiaomi', 'Others']
sales = [25, 30, 20, 15, 10]

# Create the pie chart
plt.figure(figsize=(8, 8))
plt.pie(sales, labels=brands, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})

# Set title
plt.title('Mobile Phone Sales Market Share', fontsize=16)

# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')

# Show the plot
plt.tight_layout()
plt.show()