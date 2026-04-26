import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ============================================
# STEP 1: Load All Countries
# ============================================
base = r"C:\Users\User\OneDrive\Desktop\java fx\climate-challenge-week0\data"
countries = ['ethiopia', 'kenya', 'sudan', 'tanzania', 'nigeria']
dfs = []

for country in countries:
    df = pd.read_csv(f"{base}\\{country}.csv")
    df['Country'] = country.capitalize()
    df.replace(-999, np.nan, inplace=True)
    df['Date'] = pd.to_datetime(df['YEAR'] * 1000 + df['DOY'], format='%Y%j')
    df['Month'] = df['Date'].dt.month
    df.ffill(inplace=True)
    dfs.append(df)

all_df = pd.concat(dfs, ignore_index=True)
print("=== ALL COUNTRIES LOADED ===")
print(all_df['Country'].value_counts())

# ============================================
# STEP 2: Temperature Trend Comparison
# ============================================
monthly_temp = all_df.groupby(['Country', 'YEAR', 'Month'])['T2M'].mean().reset_index()
monthly_temp['Date'] = pd.to_datetime(monthly_temp[['YEAR', 'Month']].assign(DAY=1))

plt.figure(figsize=(14, 6))
for country in all_df['Country'].unique():
    data = monthly_temp[monthly_temp['Country'] == country]
    plt.plot(data['Date'], data['T2M'], label=country, linewidth=1.5)

plt.title('Monthly Average Temperature - All Countries (2015-2026)')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.tight_layout()
plt.savefig(f"{base}\\temperature_comparison.png")
print("Temperature comparison plot saved!")

# ============================================
# STEP 3: Temperature Summary Table
# ============================================
temp_summary = all_df.groupby('Country')['T2M'].agg(['mean', 'median', 'std']).round(2)
temp_summary.columns = ['Mean T2M', 'Median T2M', 'Std T2M']
print("\n=== TEMPERATURE SUMMARY ===")
print(temp_summary)

# ============================================
# STEP 4: Precipitation Boxplot
# ============================================
plt.figure(figsize=(12, 6))
sns.boxplot(data=all_df, x='Country', y='PRECTOTCORR', palette='Set2')
plt.title('Precipitation Distribution by Country')
plt.xlabel('Country')
plt.ylabel('Precipitation (mm/day)')
plt.tight_layout()
plt.savefig(f"{base}\\precipitation_boxplot.png")
print("Precipitation boxplot saved!")

# ============================================
# STEP 5: Precipitation Summary Table
# ============================================
rain_summary = all_df.groupby('Country')['PRECTOTCORR'].agg(['mean', 'median', 'std']).round(2)
rain_summary.columns = ['Mean Rain', 'Median Rain', 'Std Rain']
print("\n=== PRECIPITATION SUMMARY ===")
print(rain_summary)

# ============================================
# STEP 6: Extreme Heat Days (T2M_MAX > 35°C)
# ============================================
heat_days = all_df[all_df['T2M_MAX'] > 35].groupby(['Country', 'YEAR']).size().reset_index(name='Heat Days')
heat_avg = heat_days.groupby('Country')['Heat Days'].mean().round(1)

plt.figure(figsize=(10, 5))
heat_avg.plot(kind='bar', color='tomato', edgecolor='black')
plt.title('Average Extreme Heat Days per Year (T2M_MAX > 35°C)')
plt.xlabel('Country')
plt.ylabel('Days per Year')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{base}\\extreme_heat_days.png")
print("Extreme heat days plot saved!")

# ============================================
# STEP 7: Consecutive Dry Days
# ============================================
def count_dry_days(group):
    return (group['PRECTOTCORR'] < 1).sum()

dry_days = all_df.groupby(['Country', 'YEAR']).apply(count_dry_days).reset_index(name='Dry Days')
dry_avg = dry_days.groupby('Country')['Dry Days'].mean().round(1)

plt.figure(figsize=(10, 5))
dry_avg.plot(kind='bar', color='steelblue', edgecolor='black')
plt.title('Average Consecutive Dry Days per Year (PRECTOTCORR < 1mm)')
plt.xlabel('Country')
plt.ylabel('Days per Year')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{base}\\dry_days.png")
print("Dry days plot saved!")

# ============================================
# STEP 8: Statistical Test (ANOVA)
# ============================================
groups = [group['T2M'].values for name, group in all_df.groupby('Country')]
f_stat, p_value = stats.f_oneway(*groups)
print(f"\n=== ANOVA TEST ===")
print(f"F-statistic: {f_stat:.2f}")
print(f"P-value: {p_value:.6f}")
if p_value < 0.05:
    print("Result: Significant difference in temperatures across countries!")

# ============================================
# STEP 9: Vulnerability Ranking
# ============================================
vulnerability = pd.DataFrame({
    'Mean Temp (°C)': temp_summary['Mean T2M'],
    'Temp Std': temp_summary['Std T2M'],
    'Mean Rain (mm)': rain_summary['Mean Rain'],
    'Rain Std': rain_summary['Std Rain'],
    'Heat Days/Year': heat_avg,
    'Dry Days/Year': dry_avg
}).round(2)

print("\n=== VULNERABILITY RANKING TABLE ===")
print(vulnerability.sort_values('Heat Days/Year', ascending=False))

print("\n=== ALL DONE! ===")