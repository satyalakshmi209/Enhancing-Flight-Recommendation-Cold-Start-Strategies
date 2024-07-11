import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define functions for Algorithm 4
# (Function definitions here)

# Load flight data
flights = pd.read_csv('/content/drive/MyDrive/passenger_dataset (1).csv')

# Display unique routes
print("Unique Routes:")
for route in flights['route'].unique():
    print(route)

# Visualize the distribution of route prices
plt.figure(figsize=(10, 6))
flights.groupby(['source', 'destination'])['price'].plot(kind='hist', alpha=0.5, legend=True)
plt.title('Distribution of Route Prices')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Display route prices
print("\nRoute Prices:")
print(flights.groupby(['source', 'destination'])['price'].agg([('Lowest Price', 'min'), ('Highest Price', 'max')]))

# Display unique airlines
print("\nUnique Airlines:")
for airline in flights['airline'].unique():
    print(airline)

# Visualize the distribution of airlines
plt.figure(figsize=(10, 6))
flights['airline'].value_counts().plot(kind='bar', color='skyblue')
plt.title('Distribution of Airlines')
plt.xlabel('Airline')
plt.ylabel('Frequency')
plt.grid(axis='y')
plt.show()

# Display unique flights
print("\nUnique Flights:")
print(flights['flight'].unique())

# Display prices for the given route
print("\nPrices:")
print(flights.groupby('flight')['price'].unique())

# Display flight times for the given route
print("\nFlight Times:")
# Assuming flight_duration is provided in the dataset
print(flights.groupby('flight')['flight_duration'].mean())
