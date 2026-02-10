"""
Project: Interactive Extraction Dashboard - Green Solvents Comparison
Publication Reference: "Extraction of Aloesin from Aloe vera Rind Using Alternative Green Solvents" (Biology 2021)
Description: 
    This dashboard generates a 3x3 matrix of interactive 3D response surfaces.
    Rows: Solvent Systems (Ethanol, Propylene Glycol, Glycerol)
    Columns: Process Slices (Fixed Solvent, Fixed Temp, Fixed Time)
Author: Mikel (PhD & Data Scientist)
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os
import streamlit as st

# 1. DATA LOADING & PRE-PROCESSING
GITHUB_RAW_URL = "https://raw.githubusercontent.com/mikel-ao/aloe-extraction-optimization/refs/heads/main/ccd_aloe.csv"

@st.cache_data
def load_data(url):
    """
    Fetch data directly from the GitHub repository.
    Uses @st.cache_data to prevent redundant downloads and improve performance.
    """
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        st.error(f"Critical Error: Unable to retrieve data from GitHub. {e}")
        st.stop()

# Load the dataset
df = load_data(GITHUB_RAW_URL)

# Coding Variables (CCRD Standard)
df['t_cod'] = (df['time'] - 110) / 60
df['T_cod'] = (df['temp'] - 60) / 20
df['S_cod'] = (df['solvent'] - 50) / 30

# 2. MODEL DEFINITION
# Using the Article-Validated Reduced Cubic Formula for consistency
formula = (
    'target ~ t_cod + T_cod + S_cod + '
    'I(t_cod**2) + I(T_cod**2) + '
    't_cod:T_cod + t_cod:S_cod + '
    'I(t_cod**2):S_cod + t_cod:I(T_cod**2) + '
    'I(t_cod**2):I(T_cod**2)'
)

solvents = {'et_w': 'Ethanol-Water', 'pg_w': 'Propylene Glycol-Water', 'gly_w': 'Glycerol-Water'}
models = {}

for key in solvents.keys():
    # Dynamic formula injection for each solvent system
    current_f = formula.replace('target', key)
    models[key] = smf.ols(formula=current_f, data=df).fit()

# 3. DASHBOARD CONFIGURATION (3x3 Subplots)
fig = make_subplots(
    rows=3, cols=3,
    specs=[[{'type': 'surface'}]*3]*3,
    subplot_titles=(
        "Et-W: Time vs Temp", "Et-W: Time vs Solv", "Et-W: Temp vs Solv",
        "PG-W: Time vs Temp", "PG-W: Time vs Solv", "PG-W: Temp vs Solv",
        "Gly-W: Time vs Temp", "Gly-W: Time vs Solv", "Gly-W: Temp vs Solv"
    ),
    vertical_spacing=0.05,
    horizontal_spacing=0.05
)

# Ranges for grids
t_range = np.linspace(df['time'].min(), df['time'].max(), 30)
T_range = np.linspace(df['temp'].min(), df['temp'].max(), 30)
S_range = np.linspace(df['solvent'].min(), df['solvent'].max(), 30)

# Helper function to generate surface data
def get_surface(model, x_range, y_range, fixed_val, fixed_type):
    X, Y = np.meshgrid(x_range, y_range)
    pdf = pd.DataFrame({'time': 110, 'temp': 60, 'solvent': 50}, index=range(len(X.ravel())))
    
    if fixed_type == 'solvent':
        pdf['temp'], pdf['time'], pdf['solvent'] = X.ravel(), Y.ravel(), fixed_val
    elif fixed_type == 'temp':
        pdf['solvent'], pdf['time'], pdf['temp'] = X.ravel(), Y.ravel(), fixed_val
    elif fixed_type == 'time':
        pdf['temp'], pdf['solvent'], pdf['time'] = X.ravel(), Y.ravel(), fixed_val
        
    pdf['t_cod'] = (pdf['time'] - 110) / 60
    pdf['T_cod'] = (pdf['temp'] - 60) / 21
    pdf['S_cod'] = (pdf['solvent'] - 50) / 30
    Z = model.predict(pdf).values.reshape(X.shape)
    return X, Y, Z

# 4. PLOTTING LOOP
for i, (s_key, s_name) in enumerate(solvents.items()):
    row = i + 1
    # Column 1: Time vs Temp (Solvent fixed at 50%)
    X, Y, Z = get_surface(models[s_key], T_range, t_range, 50, 'solvent')
    fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', showscale=False), row=row, col=1)
    
    # Column 2: Time vs Solvent (Temp fixed at 60C)
    X, Y, Z = get_surface(models[s_key], S_range, t_range, 60, 'temp')
    fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='Plasma', showscale=False), row=row, col=2)
    
    # Column 3: Temp vs Solvent (Time fixed at 110 min)
    X, Y, Z = get_surface(models[s_key], T_range, S_range, 110, 'time')
    fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale='Cividis', showscale=False), row=row, col=3)

# 5. LAYOUT AND STYLE
fig.update_layout(
    title_text="<b>Extraction Optimization Dashboard</b><br>Comparative Analysis of 3 Solvent Systems (Article-Validated Reduced Cubic Model)",
    height=1200, 
    width=1400,
    template="plotly_dark",
    showlegend=False
)

# 6. AXIS LABELING (Fixed axis naming logic)
# Row 1: Ethanol | Row 2: PG | Row 3: Glycerol
# Col 1: Time vs Temp | Col 2: Time vs Solv | Col 3: Temp vs Solv
for row in range(1, 4):
    # Column 1
    fig.update_scenes(row=row, col=1, xaxis_title='Temp (°C)', yaxis_title='Time (min)', zaxis_title='Yield')
    # Column 2
    fig.update_scenes(row=row, col=2, xaxis_title='Solvent (%)', yaxis_title='Time (min)', zaxis_title='Yield')
    # Column 3
    fig.update_scenes(row=row, col=3, xaxis_title='Temp (°C)', yaxis_title='Solvent (%)', zaxis_title='Yield')

fig.show()