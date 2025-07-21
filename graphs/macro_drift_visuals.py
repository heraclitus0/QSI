"""
Drift Volatility and Demand Decoupling Visualization — Rupture Detector
Author: Pulikanti Sashi Bharadwaj
Purpose: High-clarity professional visuals for policy period vs day-type drift distributions.
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('datasets/hyderabad_saffron_rice_supply_may_june.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Policy window (May 10–30 based on Telangana bulk ration policy)
df['Policy_Period'] = df['Date'].between('2025-05-10', '2025-05-30')

# Drift Calculation (absolute forecast error)
df['Drift'] = (df['Forecast'] - df['Actual']).abs()

# Day Type Classification
df['Day_Type'] = df['Date'].dt.dayofweek.apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')

# ✅ Boxplot — Drift Distribution (Policy vs Non-Policy)
plt.figure(figsize=(6,4))
df.boxplot(column='Drift', by='Policy_Period', grid=False, patch_artist=True,
           boxprops=dict(facecolor='skyblue', color='black'),
           medianprops=dict(color='black'))
plt.title('Drift Distribution: Policy vs Non-Policy Period')
plt.suptitle('')
plt.ylabel('Drift (kg)')
plt.xticks([1, 2], ['Non-Policy', 'Policy'])
plt.tight_layout()
plt.savefig('graphs/boxplot_policy_vs_nonpolicy.png')

# ✅ Boxplot — Drift Distribution (Weekday vs Weekend)
plt.figure(figsize=(6,4))
df.boxplot(column='Drift', by='Day_Type', grid=False, patch_artist=True,
           boxprops=dict(facecolor='lightgreen', color='black'),
           medianprops=dict(color='black'))
plt.title('Drift Distribution by Day Type')
plt.suptitle('')
plt.ylabel('Drift (kg)')
plt.tight_layout()
plt.savefig('graphs/boxplot_weekday_vs_weekend.png')

print("✅ Boxplots saved under /graphs for report-ready use.")
