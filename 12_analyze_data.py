import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 设置专业的绘图主题（类似你截图中的风格）
sns.set_theme(style="darkgrid")

# 1. 加载数据
csv_file = 'Task_12/all_results.csv'
print(f"Loading data from {csv_file}...")

df = pd.read_csv(csv_file, skipinitialspace=True, skiprows=1)

# 转换数据类型
cols_to_convert = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
df[cols_to_convert] = df[cols_to_convert].astype(float)

print(f"Successfully loaded data for {len(df)} buildings.\n")
print("=" * 50)

# ==========================================
# 图 A & B: 平均温度的分布 (Mean Temperatures)
# ==========================================
avg_mean_temp = df['mean_temp'].mean()
print(f"b) Average mean temperature of all buildings: {avg_mean_temp:.2f} °C")

plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='mean_temp', bins=40, kde=True, color='#E68193') # 类似你截图的粉色
plt.axvline(avg_mean_temp, color='blue', linestyle='--', linewidth=2, label=f'Overall Average: {avg_mean_temp:.2f}°C')
plt.axvline(18, color='red', linestyle='-.', label='18°C Threshold')
plt.axvline(15, color='orange', linestyle='-.', label='15°C Threshold')
plt.title('Distribution of Mean Temperatures (All Buildings)', fontsize=14)
plt.xlabel('Mean Temperature (°C)', fontsize=12)
plt.ylabel('Number of Buildings', fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig('Task_12/plot_ab_mean_temp.png', dpi=300)
plt.close()

# ==========================================
# 图 C: 温度标准差的分布 (Standard Deviation)
# ==========================================
avg_std_temp = df['std_temp'].mean()
print(f"c) Average temperature standard deviation: {avg_std_temp:.2f} °C")

plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='std_temp', bins=40, kde=True, color='#8E8CD8') # 紫色系
plt.axvline(avg_std_temp, color='red', linestyle='--', linewidth=2, label=f'Average Std Dev: {avg_std_temp:.2f}°C')
plt.title('Distribution of Temperature Standard Deviation', fontsize=14)
plt.xlabel('Standard Deviation of Temperature (°C)', fontsize=12)
plt.ylabel('Number of Buildings', fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig('Task_12/plot_c_std_temp.png', dpi=300)
plt.close()

# ==========================================
# 图 D: 室内面积高于 18°C 的比例分布
# ==========================================
num_above_18 = len(df[df['pct_above_18'] >= 50.0])
print(f"d) Buildings with at least 50% area above 18°C: {num_above_18} buildings")

plt.figure(figsize=(10, 6))
# 画直方图
ax = sns.histplot(data=df, x='pct_above_18', bins=20, color='#45B39D', edgecolor='black')
# 标出 50% 面积的阈值线
plt.axvline(50, color='red', linestyle='--', linewidth=2, label='50% Area Threshold')
# 在图上添加文本框说明满足条件的建筑数量
plt.text(52, ax.get_ylim()[1]*0.9, f"{num_above_18} Buildings\nmeet this criteria", 
         fontsize=12, color='darkred', bbox=dict(facecolor='white', alpha=0.8))

plt.title('Percentage of Building Area Above 18°C', fontsize=14)
plt.xlabel('Area Percentage (%)', fontsize=12)
plt.ylabel('Number of Buildings', fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig('Task_12/plot_d_above_18.png', dpi=300)
plt.close()

# ==========================================
# 图 E: 室内面积低于 15°C 的比例分布
# ==========================================
num_below_15 = len(df[df['pct_below_15'] >= 50.0])
print(f"e) Buildings with at least 50% area below 15°C: {num_below_15} buildings")

plt.figure(figsize=(10, 6))
ax = sns.histplot(data=df, x='pct_below_15', bins=20, color='#5DADE2', edgecolor='black')
plt.axvline(50, color='red', linestyle='--', linewidth=2, label='50% Area Threshold')
plt.text(52, ax.get_ylim()[1]*0.9, f"{num_below_15} Buildings\nfall in this range", 
         fontsize=12, color='darkred', bbox=dict(facecolor='white', alpha=0.8))

plt.title('Percentage of Building Area Below 15°C (Cold Buildings)', fontsize=14)
plt.xlabel('Area Percentage (%)', fontsize=12)
plt.ylabel('Number of Buildings', fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig('Task_12/plot_e_below_15.png', dpi=300)
plt.close()

print("=" * 50)
print("All plots generated successfully! Check the Task_12/ directory.")