
import pandas as pd
import numpy as np

# Define functions

# Algorithm 1: User Model Construction
def model_construction(orders, features):
    D = {}
    for index, order in orders.iterrows():
        for f in features:
            if f not in D:
                D[f] = {}
            tf = order[f]
            D[f][tf] = D[f].get(tf, 0) + 1

    W = {}
    for f in features:
        if f in D:  # Check if the feature is present in the dictionary
            W[f] = np.log(len(D[f])) - sum(D[f].values()) / len(D[f])

    return D, W

# Algorithm 2: Flight Ticket Recommendation
def ticket_recommendation(orders, features, candidates, popular_flights, passenger_id):
    D, W = model_construction(orders, features)
    R = []
    for index, ticket in candidates.iterrows():
        Gt = 0
        for f in features:
            tf = ticket[f]
            if f in D and tf in D[f]:
                Gt += D[f][tf] / sum(D[f].values()) * W[f]
        R.append((ticket, Gt))
    R.sort(key=lambda x: x[1], reverse=True)
    recommended_tickets = [ticket[0] for ticket in R]
    if not recommended_tickets:
        return None, False  # No personalized recommendations available
    return recommended_tickets[:5], True  # Return top 5 recommended tickets

# Load dataset from CSV file
csv_path = input("Enter the path to the CSV file: ")
try:
    passenger_df = pd.read_csv(csv_path)
except FileNotFoundError:
    print("Error: File not found. Please provide a valid CSV file path.")
    exit(1)
except Exception as e:
    print("Error:", e)
    exit(1)

# Ensure required attributes are present
required_attributes = ['airline', 'passenger_id', 'source', 'destination', 'class', 'price']
missing_attributes = [attr for attr in required_attributes if attr not in passenger_df.columns]
if missing_attributes:
    print("Error: The dataset is missing the following attributes:", missing_attributes)
    exit(1)

# Get passenger ID for recommendations
passenger_id = input("Enter passenger ID for recommendations: ")
if not passenger_id.isdigit():
    print("Error: Please enter a valid passenger ID (a positive integer).")
    exit(1)
passenger_id = int(passenger_id)

# Get route for recommendations
source = input("Enter source for recommendations: ").strip().capitalize()
destination = input("Enter destination for recommendations: ").strip().capitalize()
route = f"{source} to {destination}"

# Filter dataset for the given passenger ID's travel history on the specified route
passenger_history_route = passenger_df[(passenger_df['passenger_id'] == passenger_id) &
                                       (passenger_df['source'] == source) &
                                       (passenger_df['destination'] == destination)]

# Filter dataset for the given route
route_data = passenger_df[(passenger_df['source'] == source) & (passenger_df['destination'] == destination)]

# Define features and candidate ticket list
features = ['airline', 'class', 'price']  # Considering Airline, Class, and Price as features
candidates = route_data.drop_duplicates(subset=['airline'])  # Using the unique Airlines for the given route as candidate tickets

# Check if the passenger has traveled on the same route before
if passenger_history_route.empty:
    print(f"The passenger with ID {passenger_id} hasn't traveled on the route {route} previously.")
    print("No personalized recommendations available.")
else:
    # Get popular flights
    popular_flights = route_data['airline'].value_counts().index.tolist()

    # Get recommendations
    recommended_tickets, user_travelled = ticket_recommendation(passenger_history_route, features, candidates, popular_flights, passenger_id)

    # Print recommendations
    if user_travelled and recommended_tickets:
        print(f"Top 5 Recommended Tickets for Passenger ID {passenger_id} on Route {route}:")
        for ticket in recommended_tickets:
            print("Airline:", ticket['airline'])
            print("Class:", ticket['class'])
            print("Flight:",ticket['flight'])
            print("Price:", ticket['price'])
            print()  # Add a line break between tickets
    elif not user_travelled:
        print(f"The passenger with ID {passenger_id} hasn't traveled on the route {route} previously.")
        print("No personalized recommendations available.")
