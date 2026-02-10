import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Aloe Extraction Optimizer", layout="wide")

st.title("🧪 Aloe Vera Bioactive Extraction Optimizer")
st.markdown("""
This app predicts the **Aloesin yield** based on the Reduced Cubic models published in *Biology 2021*.
Adjust the parameters in the sidebar to explore the response surfaces.
""")

# --- DATA LOADING ---
# Replace the URL below with your actual GitHub Raw URL
GITHUB_RAW_URL = "https://raw.githubusercontent.com/mikel-ao/aloe-extraction-optimization/refs/heads/main/ccd_aloe.csv"

@st.cache_data # This keeps the app fast by storing the data in memory
def load_data(url):
    try:
        df = pd.read_csv(url)
        # Pre-coding for the statistical model
        df['t_cod'] = (df['time'] - 110) / 60
        df['T_cod'] = (df['temp'] - 60) / 20
        df['S_cod'] = (df['solvent'] - 50) / 30
        return df
    except Exception as e:
        st.error(f"Error loading data from GitHub: {e}")
        st.stop()

df = load_data(GITHUB_RAW_URL)

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Control Panel")
solvent_choice = st.sidebar.selectbox(
    "Select Solvent System",
    options=['et_w', 'pg_w', 'gly_w'],
    format_func=lambda x: {'et_w': 'Ethanol', 'pg_w': 'Propylene Glycol', 'gly_w': 'Glycerol'}[x]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Visualization Slices")
fixed_factor = st.sidebar.radio("Keep constant:", ['Solvent (%)', 'Temperature (°C)', 'Time (min)'])

# Dynamic sliders based on dataset limits
val_time = st.sidebar.slider("Time (min)", int(df.time.min()), int(df.time.max()), 110)
val_temp = st.sidebar.slider("Temperature (°C)", int(df.temp.min()), int(df.temp.max()), 60)
val_solv = st.sidebar.slider("Solvent Concentration (%)", int(df.solvent.min()), int(df.solvent.max()), 50)

# --- MODELING ---
formula = (
    f'{solvent_choice} ~ t_cod + T_cod + S_cod + '
    'I(t_cod**2) + I(T_cod**2) + '
    't_cod:T_cod + t_cod:S_cod + '
    'I(t_cod**2):S_cod + t_cod:I(T_cod**2) + '
    'I(t_cod**2):I(T_cod**2)'
)
model = smf.ols(formula=formula, data=df).fit()

# --- SURFACE GENERATION ---
def get_plot_data(fixed_mode):
    res = 40 # Grid resolution
    if fixed_mode == 'Solvent (%)':
        x_range = np.linspace(df.temp.min(), df.temp.max(), res)
        y_range = np.linspace(df.time.min(), df.time.max(), res)
        X, Y = np.meshgrid(x_range, y_range)
        pdf = pd.DataFrame({'temp': X.ravel(), 'time': Y.ravel(), 'solvent': val_solv})
        xt, yt = 'Temperature (°C)', 'Time (min)'
    elif fixed_mode == 'Temperature (°C)':
        x_range = np.linspace(df.solvent.min(), df.solvent.max(), res)
        y_range = np.linspace(df.time.min(), df.time.max(), res)
        X, Y = np.meshgrid(x_range, y_range)
        pdf = pd.DataFrame({'solvent': X.ravel(), 'time': Y.ravel(), 'temp': val_temp})
        xt, yt = 'Solvent (%)', 'Time (min)'
    else: # Time fixed
        x_range = np.linspace(df.temp.min(), df.temp.max(), res)
        y_range = np.linspace(df.solvent.min(), df.solvent.max(), res)
        X, Y = np.meshgrid(x_range, y_range)
        pdf = pd.DataFrame({'temp': X.ravel(), 'solvent': Y.ravel(), 'time': val_time})
        xt, yt = 'Temperature (°C)', 'Solvent (%)'

    # Coding for prediction
    pdf['t_cod'] = (pdf['time'] - 110) / 60
    pdf['T_cod'] = (pdf['temp'] - 60) / 20  # Fixed to match load_data scaling (20, not 21)
    pdf['S_cod'] = (pdf['solvent'] - 50) / 30
    Z = model.predict(pdf).values.reshape(X.shape)
    return X, Y, Z, xt, yt

X, Y, Z, xlabel, ylabel = get_plot_data(fixed_factor)

# --- VISUALIZATION ---
col1, col2 = st.columns([3, 1])

with col1:
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Plasma')])
    fig.update_layout(
        title=f"Predictive Surface for {solvent_choice.upper()}",
        scene=dict(xaxis_title=xlabel, yaxis_title=ylabel, zaxis_title="Yield (mg/L)"),
        width=800, height=600, template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric("Model R² (Adj)", f"{model.rsquared_adj:.3f}")
    st.metric("Max Yield in View", f"{Z.max():.2f} mg/L")
    st.info(f"Currently viewing the interaction between **{xlabel}** and **{ylabel}**.")


st.success("Analysis based on Article-Validated Reduced Cubic Model.")

# --- FEATURE IMPORTANCE ---
st.markdown("---")
st.subheader(f"🎯 Factor Impact Analysis: {solvent_choice.upper()}")

# Extract coefficients (excluding the Intercept)
# We use absolute values to show magnitude of impact
coefs = model.params.drop('Intercept')
coef_df = pd.DataFrame({
    'Feature': coefs.index,
    'Importance': coefs.values,
    'AbsImportance': np.abs(coefs.values)
}).sort_values(by='AbsImportance', ascending=True)

# Map coded names to human-readable names
name_map = {
    't_cod': 'Time', 'T_cod': 'Temperature', 'S_cod': 'Solvent %',
    'I(t_cod ** 2)': 'Time²', 'I(T_cod ** 2)': 'Temp²',
    't_cod:T_cod': 'Time:Temp', 't_cod:S_cod': 'Time:Solvent',
    'I(t_cod ** 2):S_cod': 'Time²:Solvent', 't_cod:I(T_cod ** 2)': 'Time:Temp²',
    'I(t_cod ** 2):I(T_cod ** 2)': 'Time²:Temp²'
}
coef_df['Feature'] = coef_df['Feature'].map(name_map)

fig_imp = go.Figure(go.Bar(
    x=coef_df['Importance'],
    y=coef_df['Feature'],
    orientation='h',
    marker=dict(color=coef_df['Importance'], colorscale='Viridis')
))

fig_imp.update_layout(
    title="Model Coefficients (Coded Units)",
    xaxis_title="Coefficient Magnitude (Impact)",
    yaxis_title="Process Factors & Interactions",
    height=400,
    template="plotly_dark"
)

st.plotly_chart(fig_imp, use_container_width=True)

st.info("""
**Interpretation:** Larger bars (positive or negative) indicate a stronger influence on Aloesin yield. 
Since variables are coded, we can directly compare the weight of each factor and its interactions.
""")
