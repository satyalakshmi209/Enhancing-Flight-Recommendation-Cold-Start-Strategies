import pandas as pd
import matplotlib.pyplot as plt

def route_partition(data, route):
    """Filters data based on the route."""
    return data[data['route'] == route]

def extract_distribution(data, features):
    """Extracts distribution of features from the data."""
    distribution = {}
    for feature in features:
        distribution[feature] = data[feature].value_counts(normalize=True).to_dict()
    return distribution

def get_weight(data, features, overall_feature_distribution):
    """Calculates weights based on the features."""
    weights = {}
    for feature in features:
        weights[feature] = 1 / len(features)  # Equal weight for each feature
    return weights

def get_optimal_route(data):
    """Determines the optimal route based on the data."""
    return data['route'].mode()[0]

def normalize_distribution(distribution):
    """Normalizes the distribution."""
    total_orders = sum(sum(subdict.values()) for subdict in distribution.values())
    normalized_distribution = {key: {subkey: value / total_orders for subkey, value in nested_dict.items()} for key, nested_dict in distribution.items()}
    return normalized_distribution

def calculate_overall_feature_distribution(data):
    """Calculates overall feature distribution across all routes."""
    overall_feature_distribution = {}
    total_passengers = len(data)

    # Calculate distribution for each feature
    for feature in ['source', 'destination', 'passenger_id']:
        feature_counts = data[feature].value_counts(normalize=True)
        overall_feature_distribution[feature] = feature_counts.to_dict()

    return overall_feature_distribution

def combine_models(model1, model2, weight1, weight2):
    """Combines the two models linearly based on the weights."""
    combined_model = {}
    for key in model1.keys():
        combined_model[key] = {subkey: weight1 * model1[key].get(subkey, 0) + weight2 * model2[key].get(subkey, 0) for subkey in set(model1[key]) | set(model2[key])}
    return combined_model

def user_model_transfer(data, recommended_route, overall_feature_distribution):
    """Performs user model transfer for the recommended route."""
    partitioned_data = route_partition(data, recommended_route)

    if partitioned_data.empty:
        print("No data found for the recommended route:", recommended_route)
        return None

    features = ['source', 'destination', 'passenger_id']  # Example features, adjust as needed
    D = {}
    W = {}

    for route, route_data in partitioned_data.groupby('route'):
        D[route] = extract_distribution(route_data, features)
        W[route] = get_weight(route_data, features, overall_feature_distribution)

    optimal_route = get_optimal_route(partitioned_data)

    D0_rb = {key: {subkey: value / overall_feature_distribution.get(key, {}).get(subkey, 1) for subkey, value in nested_dict.items()} for key, nested_dict in D[optimal_route].items()}

    Dmix = normalize_distribution(D[recommended_route])  # Initializing with user's direct model

    weight_recommended = len(partitioned_data) / len(data)
    weight_optimal = 1 - weight_recommended
    combined_model = combine_models(Dmix, D0_rb, weight_recommended, weight_optimal)

    return combined_model

def get_top_recommendations(data, recommended_route, passenger_id):
    """Gets top recommendations for a given route and passenger."""
    overall_feature_distribution = calculate_overall_feature_distribution(data)

    enhanced_user_model = user_model_transfer(data, recommended_route, overall_feature_distribution)

    if enhanced_user_model:
        data['combined_weight'] = data.apply(lambda row: sum(enhanced_user_model[feature].get(row[feature], 0) for feature in ['source', 'destination', 'passenger_id']), axis=1)

        data = data.drop_duplicates(subset='passenger_id', keep='first')

        top_recommendations = data[data['route'] == recommended_route].sort_values(by='combined_weight', ascending=False).head(10)

        print("Top 10 Recommended Flight Details:")
        print(top_recommendations[['airline', 'passenger_id', 'flight', 'source', 'destination', 'class', 'price']])

    else:
        return None
# Example usage:
data = pd.read_csv('/content/drive/MyDrive/passenger_dataset (1).csv')  # Replace with your data path
recommended_route = input("Enter recommended route: ")
passenger_id = input("Enter passenger ID: ")
get_top_recommendations(data, recommended_route, passenger_id)
