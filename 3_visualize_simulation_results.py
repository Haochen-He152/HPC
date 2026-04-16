import pandas as pd
import matplotlib.pyplot as plt
import os

# Define input and output path
input_file = 'Task_2/output_results.csv'
output_folder = 'Task_3'

# Create Task_3 directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the simulation results
if not os.path.exists(input_file):
    print(f"Error: I can't find {input_file}. I need to run Task 2 first.")
    exit()

# Load data using pandas
df = pd.read_csv(input_file, skipinitialspace=True)

building_ids = df['building_id'].astype(str)

# Create a figure with multiple subplots for analysis
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Statistical Analysis of 20 Building Simulations', fontsize=16)

# --- Top Row ---

# Top-left: A simple bar chart showing the mean temperature for each building
axes[0, 0].bar(building_ids, df['mean_temp'], color='skyblue', edgecolor='black')
axes[0, 0].set_title('Mean Temperature per Building')
axes[0, 0].set_ylabel('Mean Temperature (°C)')
axes[0, 0].tick_params(axis='x', rotation=45) 

# Top-right: Scatter plot to see if hotter buildings have more temperature variation
axes[0, 1].scatter(df['mean_temp'], df['std_temp'], color='green')
axes[0, 1].set_title('Mean Temp vs Temperature Variation (Std Dev)')
axes[0, 1].set_xlabel('Mean Temp (°C)')
axes[0, 1].set_ylabel('Std Dev')

# --- Bottom Row ---

# Bottom-left: Checking which buildings are too cold (below 15°C)
axes[1, 0].bar(building_ids, df['pct_below_15'], color='salmon', edgecolor='black')
axes[1, 0].set_title('Percentage of Area Below 15°C')
axes[1, 0].set_ylabel('Percentage (%)')
axes[1, 0].tick_params(axis='x', rotation=45)

# Bottom-right: Checking which buildings have good heating coverage (above 18°C)
axes[1, 1].bar(building_ids, df['pct_above_18'], color='gold', edgecolor='black')
axes[1, 1].set_title('Percentage of Area Above 18°C')
axes[1, 1].set_ylabel('Percentage (%)')
axes[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Finally, saving plot and closing the figure to free up memory
save_path = os.path.join(output_folder, 'simulation_summary_analysis.png')
plt.savefig(save_path, dpi=300)
plt.close(fig)

print(f"Task 3 completed! I saved the chart as: {save_path}")