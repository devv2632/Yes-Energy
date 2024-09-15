import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = 'load_act.csv'
data = pd.read_csv(file_path)

# Convert date and time to datetime format
data['datetime'] = pd.to_datetime(data['date'].astype(str) + data['time'].astype(str).str.zfill(4), format='%Y%m%d%H%M')

# Plot the load_act over time
plt.figure(figsize=(10, 6))
plt.plot(data['datetime'], data['load_act'], label='Load Activity')
plt.title('Load Activity Over Time')
plt.xlabel('Datetime')
plt.ylabel('Load Activity')
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.show()
