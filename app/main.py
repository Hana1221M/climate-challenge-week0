import streamlit as st
import pandas as pd
import plotly.express as px
import os
from utils import load_data, filter_data, COUNTRIES

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="African Climate Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def get_data():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    return load_data(data_path)

df = get_data()

# ============================================
# SIDEBAR
# ============================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Africa_%28orthographic_projection%29.svg/240px-Africa_%28orthographic_projection%29.svg.png", width=120)
st.sidebar.title("🌍 Dashboard Controls")

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=COUNTRIES,
    default=COUNTRIES
)

year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=2015,
    max_value=2026,
    value=(2015, 2026)
)

variable = st.sidebar.selectbox(
    "Select Climate Variable",
    options={
        'T2M': 'Mean Temperature (°C)',
        'T2M_MAX': 'Max Temperature (°C)',
        'T2M_MIN': 'Min Temperature (°C)',
        'PRECTOTCORR': 'Precipitation (mm/day)',
        'RH2M': 'Relative Humidity (%)',
        'WS2M': 'Wind Speed (m/s)',
    }.keys(),
    format_func=lambda x: {
        'T2M': 'Mean Temperature (°C)',
        'T2M_MAX': 'Max Temperature (°C)',
        'T2M_MIN': 'Min Temperature (°C)',
        'PRECTOTCORR': 'Precipitation (mm/day)',
        'RH2M': 'Relative Humidity (%)',
        'WS2M': 'Wind Speed (m/s)',
    }[x]
)

# ============================================
# FILTER DATA
# ============================================
filtered = filter_data(df, selected_countries, year_range)

# ============================================
# HEADER
# ============================================
st.title("🌍 African Climate Trend Dashboard")
st.markdown("**10 Academy KAIM9 — Week 0 | Hana Mesfin**")
st.markdown("---")

# ============================================
# KPI CARDS
# ============================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Countries Selected", len(selected_countries))
col2.metric("Years Covered", f"{year_range[0]} - {year_range[1]}")
col3.metric("Total Records", f"{len(filtered):,}")
col4.metric("Avg Temperature", f"{filtered['T2M'].mean():.1f}°C")

st.markdown("---")

# ============================================
# CHART 1: Temperature Trend Line Chart
# ============================================
st.subheader(f"📈 Monthly {variable} Trend by Country")

monthly = filtered.groupby(['Country', 'YEAR', 'Month'])[variable].mean().reset_index()
monthly['Date'] = pd.to_datetime(monthly[['YEAR', 'Month']].assign(DAY=1))

fig1 = px.line(
    monthly,
    x='Date',
    y=variable,
    color='Country',
    title=f"Monthly Average {variable} ({year_range[0]}–{year_range[1]})",
    labels={variable: variable, 'Date': 'Date'},
    template='plotly_white'
)
fig1.update_layout(height=400, legend_title="Country")
st.plotly_chart(fig1, use_container_width=True)

# ============================================
# CHART 2: Precipitation Boxplot
# ============================================
st.subheader("🌧️ Precipitation Distribution by Country")

fig2 = px.box(
    filtered,
    x='Country',
    y='PRECTOTCORR',
    color='Country',
    title="Precipitation Distribution (mm/day)",
    labels={'PRECTOTCORR': 'Precipitation (mm/day)'},
    template='plotly_white'
)
fig2.update_layout(height=400, showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

# ============================================
# CHART 3: Vulnerability Summary Table
# ============================================
st.subheader("🌡️ Climate Vulnerability Summary")

summary = filtered.groupby('Country').agg(
    Mean_Temp=('T2M', 'mean'),
    Max_Temp=('T2M_MAX', 'max'),
    Mean_Rain=('PRECTOTCORR', 'mean'),
    Dry_Days=('PRECTOTCORR', lambda x: (x < 1).sum()),
    Heat_Days=('T2M_MAX', lambda x: (x > 35).sum())
).round(2).reset_index()

summary.columns = ['Country', 'Mean Temp (°C)', 'Max Temp (°C)', 
                   'Mean Rain (mm)', 'Dry Days', 'Heat Days (>35°C)']

st.dataframe(summary, use_container_width=True)

# ============================================
# CHART 4: Bar Chart Comparison
# ============================================
st.subheader(f"📊 {variable} Comparison by Country")

bar_data = filtered.groupby('Country')[variable].mean().reset_index()
fig3 = px.bar(
    bar_data,
    x='Country',
    y=variable,
    color='Country',
    title=f"Average {variable} by Country",
    template='plotly_white'
)
fig3.update_layout(height=350, showlegend=False)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.caption("Data source: NASA POWER | 10 Academy KAIM9 Week 0 | Hana Mesfin")