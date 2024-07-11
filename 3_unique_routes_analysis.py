import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have a DataFrame named 'flights' with columns 'source' and 'destination'
flights = pd.read_csv('/content/drive/MyDrive/passenger_dataset (1).csv')

# Group by 'source' and 'destination' and count the unique combinations
unique_routes = flights.groupby(['source', 'destination']).ngroups

print("Number of unique routes:", unique_routes)

# Visualization: Bar plot of unique routes
route_counts = flights.groupby(['source', 'destination']).size().reset_index(name='counts')
route_counts.sort_values(by='counts', ascending=False, inplace=True)  # Sort by counts for better visualization

plt.figure(figsize=(12, 6))
plt.bar(range(len(route_counts)), route_counts['counts'], color='skyblue')
plt.xlabel('Source-Destination Pairs')
plt.ylabel('Number of Flights')
plt.title('Distribution of Unique Routes')
plt.xticks(range(len(route_counts)), [f"{src} to {dest}" for src, dest in zip(route_counts['source'], route_counts['destination'])], rotation=90)
plt.tight_layout()
plt.show()
