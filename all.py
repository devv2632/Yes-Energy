import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo

# Function to clean and convert date and time to datetime
def convert_datetime(df):
    df['time'] = df['time'].astype(str).str.zfill(4)  # Ensure time is in HHMM format
    df['datetime'] = pd.to_datetime(df['date'].astype(str) + df['time'].str[:2], format='%Y%m%d%H', errors='coerce')
    return df

# Load and process all CSV files
def load_and_process(file_path, load_col):
    df = pd.read_csv(file_path)
    df = convert_datetime(df)
    return df[['datetime', load_col]].set_index('datetime').resample('H').mean().fillna(method='ffill').reset_index()

# Load actual load data
load_act_resampled = load_and_process('load_act.csv', 'load_act')

# Load forecast data
mm_load_resampled = load_and_process('MM_load_fcst_archive.csv', 'load_fcst')
mw_load_resampled = load_and_process('MW_load_fcst_archive.csv', 'load_fcst')
d_load_resampled = load_and_process('D_load_fcst_archive.csv', 'load_fcst')
j_load_resampled = load_and_process('J_load_fcst_archive.csv', 'load_fcst')

# Create a Plotly figure
fig = go.Figure()

# Add all traces, starting with them visible
fig.add_trace(go.Scattergl(x=load_act_resampled['datetime'], y=load_act_resampled['load_act'],
                           mode='lines', name='Actual Load', line=dict(color='blue'), visible=True))

fig.add_trace(go.Scattergl(x=mm_load_resampled['datetime'], y=mm_load_resampled['load_fcst'],
                           mode='lines', name='MM Load Forecast', line=dict(color='orange'), visible=True))

fig.add_trace(go.Scattergl(x=mw_load_resampled['datetime'], y=mw_load_resampled['load_fcst'],
                           mode='lines', name='MW Load Forecast', line=dict(color='green'), visible=True))

fig.add_trace(go.Scattergl(x=d_load_resampled['datetime'], y=d_load_resampled['load_fcst'],
                           mode='lines', name='D Load Forecast', line=dict(color='red'), visible=True))

fig.add_trace(go.Scattergl(x=j_load_resampled['datetime'], y=j_load_resampled['load_fcst'],
                           mode='lines', name='J Load Forecast', line=dict(color='purple'), visible=True))

# Define buttons to show/hide each dataset
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="down",  # Stack the buttons vertically
            buttons=list([
                dict(
                    args=[{'visible': [True, False, False, False, False]}],
                    label="Show Actual Load",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, True, False, False, False]}],
                    label="Show MM Load Forecast",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, False, True, False, False]}],
                    label="Show MW Load Forecast",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, False, False, True, False]}],
                    label="Show D Load Forecast",
                    method="update"
                ),
                dict(
                    args=[{'visible': [False, False, False, False, True]}],
                    label="Show J Load Forecast",
                    method="update"
                ),
                dict(
                    args=[{'visible': [True, True, True, True, True]}],
                    label="Show All",
                    method="update"
                )
            ]),
            showactive=True,
            x=1.02,  # Move the buttons to the left of the graph
            xanchor="left",
            y=-.4,  # Center the buttons vertically
            yanchor="middle"
        ),
    ]
)

# Update layout to add a range slider, more detailed time units, and zoom options
# Update layout to add a range slider, more detailed time units, and zoom options
fig.update_layout(
    height=700,
    width=1500,
    title_text="Actual Load and Forecasts Over Time",
    showlegend=True,
    xaxis=dict(
        rangeselector=dict(buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(step="all")
        ])),
        rangeslider=dict(visible=True),  # Range slider for zooming
        type="date",
        tickformat="%Y-%m-%d\n%H:%M",  # More detailed time format (Date and time)
        dtick="H1",  # Hourly ticks; adjust based on data granularity
    ),
    yaxis_title="Load (MW)"
)


# Show plot in browser
pyo.plot(fig)
