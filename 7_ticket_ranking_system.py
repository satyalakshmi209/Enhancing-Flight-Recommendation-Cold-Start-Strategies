import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def getSearchResult(source, destination, dataset):
    # Simulated function to generate search results for a given source and destination
    # In a real application, this function would query a database or API based on the provided source and destination
    # Here, we'll simulate by filtering the dataset based on source and destination
    filtered_data = dataset[(dataset['source'] == source) & (dataset['destination'] == destination)]
    if filtered_data.empty:
        return np.array([])
    else:
        # Simulate search results based on price from filtered data
        return np.array(filtered_data['price'])

def rank_tickets(O, F, C, alpha, lambda_val, dataset):
    # Initialize latent factors Wu and Mti
    Wu = 1e-10  # Initialize to a small value to avoid division by zero
    Mti = 1e-10  # Initialize to a small value to avoid division by zero

    # Iterate over historical routes
    for o in O:
        source, destination = o.split('-')
        Co = getSearchResult(source, destination, dataset)
        for to in Co:
            if to != 0 and Wu != 0 and Mti != 0:  # Avoid division by zero errors
                # Update latent factors Wu and Mti
                Wu = Wu + alpha * (np.log(to) / Wu - lambda_val * Wu)
                Mti = Mti + alpha * (np.log(to) / Mti - lambda_val * Mti)

    R = []
    # Calculate Rt for each ticket in C
    for t in C:
        if t != 0 and Wu != 0 and Mti != 0:  # Avoid division by zero errors
            # Calculate Rt based on the latent factors
            Rt = Wu * t + Mti * t
            R.append(Rt)

    R.sort()
    return R

# Load user dataset
dataset = pd.read_csv('/content/drive/MyDrive/passenger_dataset (1).csv')  # Assuming the dataset is in CSV format

# Accept user input for historical routes
O = input("Enter historical routes separated by commas: ").split(',')

# Accept user input for ticket features
F_input = input("Enter ticket features separated by commas: ")
F = [x.strip() for x in F_input.split(',') if x.strip()]  # Filter out empty strings and remove leading/trailing whitespace

# Generate a placeholder for the search result list
C = dataset['price'].values.tolist()  # Using actual prices from the dataset as the search result list

alpha = float(input("Enter learning rate (alpha): "))
lambda_val = float(input("Enter regularization parameter (lambda): "))

# Rank tickets
ranked_tickets = rank_tickets(O, F, C, alpha, lambda_val, dataset)
print("\nRanked Tickets:", ranked_tickets)
