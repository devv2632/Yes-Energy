import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo

# Load the CSV files
mm_load_df = pd.read_csv('MM_load_fcst_archive.csv')
mw_load_df = pd.read_csv('MW_load_fcst_archive.csv')

# Function to clean and convert date and time to datetime
def convert_datetime(df):
    df['time'] = df['time'].astype(str).str.zfill(4)  # Ensure time is in HHMM format
    df['datetime'] = pd.to_datetime(df['date'].astype(str) + df['time'].str[:2], format='%Y%m%d%H', errors='coerce')
    return df

# Apply the function to both dataframes
mm_load_df = convert_datetime(mm_load_df)
mw_load_df = convert_datetime(mw_load_df)

# Convert the 'revision' column to datetime format if present
if 'revision' in mm_load_df.columns:
    mm_load_df['revision'] = pd.to_datetime(mm_load_df['revision'], format='%d/%m/%Y %H:%M', errors='coerce')
if 'revision' in mw_load_df.columns:
    mw_load_df['revision'] = pd.to_datetime(mw_load_df['revision'], format='%d/%m/%Y %H:%M', errors='coerce')

# Ensure we only use numeric columns for resampling
mm_load_numeric = mm_load_df[['datetime', 'load_fcst']].copy()  # Only numeric columns
mw_load_numeric = mw_load_df[['datetime', 'load_fcst']].copy()  # Only numeric columns

# Resample the data to hourly intervals, filling missing values if necessary
mm_load_df_resampled = mm_load_numeric.set_index('datetime').resample('H').mean().fillna(method='ffill').reset_index()
mw_load_df_resampled = mw_load_numeric.set_index('datetime').resample('H').mean().fillna(method='ffill').reset_index()

# Use scattergl for large datasets
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("MM Load Forecast", "MW Load Forecast"))

# MM Load with scattergl for large datasets
fig.add_trace(go.Scattergl(x=mm_load_df_resampled['datetime'], y=mm_load_df_resampled['load_fcst'], mode='lines', name='MM Load Forecast', line=dict(color='blue')), row=1, col=1)

# MW Load with scattergl for large datasets
fig.add_trace(go.Scattergl(x=mw_load_df_resampled['datetime'], y=mw_load_df_resampled['load_fcst'], mode='lines', name='MW Load Forecast', line=dict(color='orange')), row=2, col=1)

# Update layout to add a range slider and selectors for zooming
fig.update_layout(
    height=700, 
    width=1000, 
    title_text="MM and MW Load Forecasts Over Time", 
    showlegend=True,
    xaxis=dict(rangeselector=dict(buttons=list([
        dict(count=1, label="1d", step="day", stepmode="backward"),
        dict(count=7, label="1w", step="day", stepmode="backward"),
        dict(step="all")
    ])),
    rangeslider=dict(visible=True),
    type="date"
    ),
    xaxis2=dict(rangeselector=dict(buttons=list([
        dict(count=1, label="1d", step="day", stepmode="backward"),
        dict(count=7, label="1w", step="day", stepmode="backward"),
        dict(step="all")
    ])),
    rangeslider=dict(visible=True),
    type="date"
    )
)

# Show plot in browser
pyo.plot(fig)
