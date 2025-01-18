import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore
from matplotlib import rcParams
from matplotlib.cm import get_cmap

# Configure matplotlib for colorblind-friendly palettes
rcParams['font.size'] = 14
rcParams['font.family'] = 'Arial'

# Define a colorblind-friendly colormap
colorblind_palette = get_cmap('tab10')  # A widely used colorblind-friendly palette

# Load your dataset
# Assuming a CSV file with columns: 'Delta_Predicted', 'Delta_Experimental', 'Residue_Type'
data = pd.read_csv('/Users/papakobinavandyck/Desktop/delta_data.csv')

# Remove outliers based on z-score
def remove_outliers(data, column_x, column_y, threshold=3):
    data['Residual'] = data[column_x] - data[column_y]
    data['Z_Score'] = zscore(data['Residual'])
    filtered_data = data[np.abs(data['Z_Score']) <= threshold].drop(columns=['Residual', 'Z_Score'])
    return filtered_data

# Calculate RMSD
def calculate_rmsd(delta_predicted, delta_experimental):
    differences = delta_predicted - delta_experimental
    rmsd = np.sqrt(np.mean(differences**2))
    return rmsd

# Preprocess data (optional outlier removal)
threshold = 3
filtered_data = remove_outliers(data, 'Delta_Predicted', 'Delta_Experimental', threshold)

# Extract data
delta_predicted = filtered_data['Delta_Predicted']
delta_experimental = filtered_data['Delta_Experimental']
residue_type = filtered_data['Residue_Type']

# Calculate total RMSD
total_rmsd = calculate_rmsd(delta_predicted, delta_experimental)

# Calculate RMSD for specific residue types
residue_rmsds = {}
for residue in ['ASP', 'LYS', 'GLU']:
    subset = filtered_data[filtered_data['Residue_Type'] == residue]
    if not subset.empty:
        rmsd = calculate_rmsd(subset['Delta_Predicted'], subset['Delta_Experimental'])
        residue_rmsds[residue] = rmsd
    else:
        residue_rmsds[residue] = None

# Print RMSD results
print(f"Total RMSD: {total_rmsd:.3f}")
for residue, rmsd in residue_rmsds.items():
    if rmsd is not None:
        print(f"RMSD for {residue}: {rmsd:.3f}")
    else:
        print(f"RMSD for {residue}: No data available")

# Create scatter plot with color-coded residue types
plt.figure(figsize=(8, 6))

# Assign unique colors for each residue type
residue_colors = {
    residue: colorblind_palette(i) for i, residue in enumerate(residue_type.unique())
}

for residue, color in residue_colors.items():
    subset = filtered_data[filtered_data['Residue_Type'] == residue]
    plt.scatter(
        subset['Delta_Experimental'], subset['Delta_Predicted'], 
        label=residue, color=color, alpha=0.7, edgecolor='k', s=70
    )

# Add ideal correlation line
x_min, x_max = min(delta_experimental), max(delta_experimental)
ideal_x = np.linspace(x_min, x_max, 100)
plt.plot(ideal_x, ideal_x, 'k--', label='Ideal Correlation Line')

# Add lines at 0 for both axes to create quadrants
plt.axhline(0, color='gray', linestyle='-', linewidth=1)  # Horizontal line at y = 0
plt.axvline(0, color='gray', linestyle='-', linewidth=1)  # Vertical line at x = 0

# Add labels and legend
plt.title('Delta pKa Correlation with RMSD (Colorblind-Friendly)')
plt.xlabel('Delta Experimental pKa')
plt.ylabel('Delta Predicted pKa')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Add correlation coefficient and total RMSD to the plot
plt.text(
    0.95, 0.05, 
    f"Total RMSD: {total_rmsd:.3f}\n" +
    "\n".join([f"{res}: {rmsd:.3f}" for res, rmsd in residue_rmsds.items() if rmsd is not None]),
    transform=plt.gca().transAxes,
    fontsize=12,
    verticalalignment='bottom',
    horizontalalignment='right',
    bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray')
)

# Save plot with high resolution and transparent background
plt.savefig('delta_correlation_with_rmsd.png', dpi=600, transparent=True, bbox_inches='tight')

# Show plot
plt.show()
