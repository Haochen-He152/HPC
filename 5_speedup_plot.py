import pandas as pd
import matplotlib.pyplot as plt

# Load data from your Task_5 folder
df = pd.read_csv('Task_5/speedup.csv')

plt.figure(figsize=(10, 6))

# Plot Measured Speed-up
plt.plot(df['cores'], df['speedup'], marker='o', linestyle='-', color='b', label='Measured Speed-up')

# Plot Ideal Speed-up (y = x)
plt.plot(df['cores'], df['cores'], linestyle='--', color='r', label='Ideal (Linear) Speed-up')

plt.title('Task 5: Speed-up vs. CPU Cores (Static Scheduling)')
plt.xlabel('Number of CPU Cores')
plt.ylabel('Speed-up')
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend()

# Save to Task_5 folder
plt.savefig('Task_5/speedup_plot.png')
print("Plot saved to Task_5/speedup_plot.png")