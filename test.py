import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================
# STEP 1: Load & Clean Data
# ============================================
df = pd.read_csv(r"C:\Users\User\OneDrive\Desktop\java fx\climate-challenge-week0\data\ethiopia.csv")

df['Country'] = 'Ethiopia'
df.replace(-999, np.nan, inplace=True)
df['Date'] = pd.to_datetime(df['YEAR'] * 1000 + df['DOY'], format='%Y%j')
df['Month'] = df['Date'].dt.month

print("Shape:", df.shape)
print("\nMissing Values:")
print(df.isna().sum())

# Remove duplicates
dups = df.duplicated().sum()
print(f"\nDuplicate rows: {dups}")
df.drop_duplicates(inplace=True)

# ============================================
# STEP 2: Outlier Detection
# ============================================
cols = ['T2M', 'T2M_MAX', 'T2M_MIN', 'PRECTOTCORR', 'RH2M', 'WS2M', 'WS2M_MAX']
for col in cols:
    z = (df[col] - df[col].mean()) / df[col].std()
    outliers = (z.abs() > 3).sum()
    print(f"Outliers in {col}: {outliers}")

# Forward fill missing values
df[cols] = df[cols].ffill()

# Export cleaned data
df.to_csv(r"C:\Users\User\OneDrive\Desktop\java fx\climate-challenge-week0\data\ethiopia_clean.csv", index=False)
print("\n=== Cleaned data saved! ===")

# ============================================
# STEP 3: Time Series Plot
# ============================================
monthly = df.groupby(['YEAR', 'Month'])['T2M'].mean().reset_index()
monthly['Date'] = pd.to_datetime(monthly[['YEAR', 'Month']].assign(DAY=1))

plt.figure(figsize=(14, 5))
plt.plot(monthly['Date'], monthly['T2M'], color='tomato', linewidth=1.5)
plt.title('Monthly Average Temperature - Ethiopia (2015-2026)')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.tight_layout()
plt.savefig(r"C:\Users\User\OneDrive\Desktop\java fx\climate-challenge-week0\data\temperature_trend.png")
print("Temperature plot saved!")

# ============================================
# STEP 4: Precipitation Bar Chart
# ============================================
monthly_rain = df.groupby('Month')['PRECTOTCORR'].sum().reset_index()

plt.figure(figsize=(10, 5))
plt.bar(monthly_rain['Month'], monthly_rain['PRECTOTCORR'], color='steelblue')
plt.title('Monthly Total Precipitation - Ethiopia')
plt.xlabel('Month')
plt.ylabel('Precipitation (mm)')
plt.tight_layout()
plt.savefig(r"C:\Users\User\OneDrive\Desktop\java fx\climate-challenge-week0\data\precipitation_bar.png")
print("Precipitation plot saved!")

# ============================================
# STEP 5: Correlation Heatmap
# ============================================
plt.figure(figsize=(10, 8))
sns.heatmap(df[cols].corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap - Ethiopia Climate Variables')
plt.tight_layout()
plt.savefig(r"C:\Users\User\OneDrive\Desktop\java fx\climate-challenge-week0\data\correlation_heatmap.png")
print("Heatmap saved!")

print("\n=== ALL DONE! ===")