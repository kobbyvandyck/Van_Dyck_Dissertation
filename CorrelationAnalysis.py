import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, zscore
from matplotlib import rcParams
from matplotlib.cm import get_cmap

# Configure matplotlib for colorblind-friendly palettes
rcParams['font.size'] = 14
rcParams['font.family'] = 'Arial'

# Define a colorblind-friendly colormap
colorblind_palette = get_cmap('tab10')

# Load your dataset
# Assuming a CSV file with columns: 'Predicted_pKa', 'Experimental_pKa', 'Residue_Type'
data = pd.read_csv('/Users/papakobinavandyck/Desktop/Corr.csv')

# Function to calculate weighted correlation coefficient
def calculate_weighted_correlation(predicted, experimental, predicted_error, experimental_error):
    weights = 1 / (predicted_error**2 + experimental_error**2)  # Inverse of variance
    mean_pred = np.average(predicted, weights=weights)
    mean_exp = np.average(experimental, weights=weights)

    cov = np.sum(weights * (predicted - mean_pred) * (experimental - mean_exp))
    var_pred = np.sum(weights * (predicted - mean_pred)**2)
    var_exp = np.sum(weights * (experimental - mean_exp)**2)

    correlation = cov / np.sqrt(var_pred * var_exp)
    return correlation

# Remove outliers based on z-score
def remove_outliers(data, column_x, column_y, threshold=3):
    data['Residual'] = data[column_x] - data[column_y]
    data['Z_Score'] = zscore(data['Residual'])
    filtered_data = data[np.abs(data['Z_Score']) <= threshold].drop(columns=['Residual', 'Z_Score'])
    return filtered_data

# Calculate RMSD
def calculate_rmsd(predicted, experimental):
    differences = predicted - experimental
    rmsd = np.sqrt(np.mean(differences**2))
    return rmsd

# Preprocess data (optional outlier removal)
threshold = 3
filtered_data = remove_outliers(data, 'Predicted_pKa', 'Experimental_pKa', threshold)

# Extract data
predicted_pka = filtered_data['Predicted_pKa']
experimental_pka = filtered_data['Experimental_pKa']
residue_type = filtered_data['Residue_Type']
predicted_error = filtered_data['Predicted_Error']  # Assumed column for predicted error
experimental_error = filtered_data['Experimental_Error']  # Assumed column for experimental error

# Calculate weighted correlation coefficient and RMSD
correlation = calculate_weighted_correlation(predicted_pka, experimental_pka, predicted_error, experimental_error)
rmsd = calculate_rmsd(predicted_pka, experimental_pka)

# Calculate residue-specific metrics
residue_metrics = {}
for residue in residue_type.unique():
    subset = filtered_data[filtered_data['Residue_Type'] == residue]
    if not subset.empty:
        res_corr = calculate_weighted_correlation(
            subset['Predicted_pKa'], subset['Experimental_pKa'], 
            subset['Predicted_Error'], subset['Experimental_Error']
        )
        res_rmsd = calculate_rmsd(subset['Predicted_pKa'], subset['Experimental_pKa'])
        residue_metrics[residue] = {'Correlation': res_corr, 'RMSD': res_rmsd}

# Print overall metrics
print(f'Weighted Correlation Coefficient: {correlation:.3f}')
print(f'RMSD: {rmsd:.3f}')

# Print residue-specific metrics
print("\nResidue-Specific Metrics:")
for residue, metrics in residue_metrics.items():
    print(f"{residue}: Correlation = {metrics['Correlation']:.3f}, RMSD = {metrics['RMSD']:.3f}")

# Create scatter plot with color-coded residue types
plt.figure(figsize=(8, 6))

# Assign unique colors for each residue type, ensuring no red or green
safe_colors = ['#377eb8', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf', '#4daf4a', '#999999']
residue_colors = {
    residue: safe_colors[i % len(safe_colors)] for i, residue in enumerate(residue_type.unique())
}

for residue, color in residue_colors.items():
    subset = filtered_data[filtered_data['Residue_Type'] == residue]
    plt.scatter(
        subset['Experimental_pKa'], subset['Predicted_pKa'], 
        label=residue, color=color, alpha=0.7, edgecolor='k', s=70
    )

# Add ideal correlation line
x_min, x_max = min(experimental_pka), max(experimental_pka)
ideal_x = np.linspace(x_min, x_max, 100)
plt.plot(ideal_x, ideal_x, 'k--', label='Ideal Correlation Line')

# Calculate and plot error range for the ideal line
error_margin = np.sqrt(predicted_error.mean()**2 + experimental_error.mean()**2)
plt.plot(ideal_x, ideal_x + error_margin, 'k:', label='Error Range')
plt.plot(ideal_x, ideal_x - error_margin, 'k:', label='_nolegend_')


# Add labels and legend
plt.title('pKa Correlation Analysis')
plt.xlabel('Experimental pKa')
plt.ylabel('Predicted pKa')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Add correlation coefficient and RMSD to the plot
plt.text(
    0.95, 0.05, 
    f"Correlation Coefficient: {correlation:.3f}\nRMSD: {rmsd:.3f}",
    transform=plt.gca().transAxes,
    fontsize=12,
    verticalalignment='bottom',
    horizontalalignment='right',
    bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray')
)

# Save plot with high resolution and transparent background
plt.savefig('pka_correlation_analysis.png', dpi=600, transparent=True, bbox_inches='tight')

# Show plot
plt.show()
