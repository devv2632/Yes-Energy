import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo

# Load the actual load CSV file
load_act_df = pd.read_csv('load_act.csv')

# Function to clean and convert date and time to datetime (reused from previous code)
def convert_datetime(df):
    df['time'] = df['time'].astype(str).str.zfill(4)  # Ensure time is in HHMM format
    df['datetime'] = pd.to_datetime(df['date'].astype(str) + df['time'].str[:2], format='%Y%m%d%H', errors='coerce')
    return df

# Apply the function to the actual load dataframe
load_act_df = convert_datetime(load_act_df)
print(load_act_df.columns)
# Ensure we only use numeric columns for resampling
load_act_numeric = load_act_df[['datetime', 'load_act']].copy()  # Assuming 'actual_load' is the column for actual load

# Resample the actual load data to hourly intervals, filling missing values if necessary
load_act_resampled = load_act_numeric.set_index('datetime').resample('H').mean().fillna(method='ffill').reset_index()
# Check the columns of the actual load dataframe


# Create a Plotly figure for the actual load data
fig = go.Figure()

# Actual Load with scattergl for large datasets
fig.add_trace(go.Scattergl(x=load_act_resampled['datetime'], y=load_act_resampled['load_act'], mode='lines', name='Actual Load', line=dict(color='blue')))

# Update layout to add a range slider and selectors for zooming
fig.update_layout(
    height=500, 
    width=1000, 
    title_text="Actual Load Over Time", 
    showlegend=True,
    xaxis=dict(rangeselector=dict(buttons=list([
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
