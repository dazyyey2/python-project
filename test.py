import matplotlib.pyplot as plt
import numpy as np

# Example data
categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 56, 78, 33]

# Create the figure and axis
fig, ax = plt.subplots(figsize=(8, 5))

# Bar colors (optional gradient-style palette)
colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(values)))

# Create bars
bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=0.8)

# Add title and labels
ax.set_title('Category Performance', fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel('Category', fontsize=12)
ax.set_ylabel('Value', fontsize=12)

# Clean up the look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle='--', alpha=0.6)

# Add value labels on top of bars
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval}', 
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# Tight layout for better spacing
plt.tight_layout()
plt.show()