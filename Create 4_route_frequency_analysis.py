import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have a DataFrame named 'flights' with columns 'source_city' and 'destination_city'
# Replace '/content/Indian Airlines.csv' with the actual file path if needed
flights = pd.read_csv('/content/drive/MyDrive/passenger_dataset (1).csv')

# Concatenate 'source_city' and 'destination_city' columns to create route names
flights['Route'] = flights['source'] + ' to ' + flights['destination']

# Get unique route names along with their frequencies
route_counts = flights['Route'].value_counts()

# Print the names of unique routes along with their frequencies
for route, count in route_counts.items():
    print(f"{route}: {count}")
