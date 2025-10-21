# -*- coding: utf-8 -*-
"""
Instagram Data Analysis
-----------------------
Analyze social media performance using data from Google Sheets:
- Clean and structure engagement data
- Perform statistical tests (Mann–Whitney U)
- Visualize post performance and audience insights
"""

# === 1️⃣ Imports ===
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu, shapiro
import numpy as np

# === 2️⃣ Load Data ===
# Read from Google Sheets or local CSV
# df = pd.read_csv("data/instagram_data.csv")
# (In Colab use gspread authentication)
print(df.shape)
print(df.columns)

# === 3️⃣ Data Cleaning ===
df.rename(columns={
    '分類編碼': 'Label',
    'Description (English)': 'Des_eng',
    'Avg_eng': 'Engagement_Rate'
}, inplace=True)

df_clean = df[df['Post type'] != 'IG image'].drop(
    columns=['Post ID', 'Account ID', 'Account username', 'Account name', 'Data comment'],
    errors='ignore'
)

# === 4️⃣ Statistical Analysis Function ===
def analyze_group_diff(df, group_col, value_col):
    """Compare engagement metrics between groups (non-parametric test)."""
    def remove_outliers(g):
        Q1, Q3 = g[value_col].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        return g[(g[value_col] >= Q1 - 1.5*IQR) & (g[value_col] <= Q3 + 1.5*IQR)]

    df_no_outliers = df.groupby(group_col, group_keys=False).apply(remove_outliers)
    print(f"Original n={len(df)}, after removing outliers={len(df_no_outliers)}")

    # Test
    groups = df_no_outliers[group_col].unique()
    if len(groups) == 2:
        g1 = df_no_outliers[df_no_outliers[group_col] == groups[0]][value_col]
        g2 = df_no_outliers[df_no_outliers[group_col] == groups[1]][value_col]
        stat, p = mannwhitneyu(g1, g2, alternative='two-sided')
        print(f"U={stat:.2f}, p={p:.4f}")
    return df_no_outliers

# Example:
analyze_group_diff(df_clean, "Post type", "Engagement_Rate")

# === 5️⃣ Visualization Example ===
sns.boxplot(data=df_clean, x='Post type', y='Engagement_Rate')
plt.title("Engagement Rate by Post Type")
plt.show()
