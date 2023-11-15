import random
import requests
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

def calculate_total_distance(distance_matrix, route):
    total_distance = 0.0
    for i in range(1, len(route)):
        from_location = route[i - 1]
        to_location = route[i]
        distance = distance_matrix[from_location][to_location]
        total_distance += distance
    return total_distance
    
def get_route_distances(locations, api_key):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    num_locations = len(locations)
    distances = [[0] * num_locations for _ in range(num_locations)]  # Initialize the distances matrix

    for i in range(num_locations):
        for j in range(i + 1, num_locations):
            params = {
                'key': api_key,
                'origins': locations[i],
                'destinations': locations[j],
                'mode': 'driving',
            }
            response = requests.get(url, params=params)
            data = response.json()

            if 'rows' in data and len(data['rows']) > 0 and 'elements' in data['rows'][0] and 'distance' in data['rows'][0]['elements'][0]:
                distance = data['rows'][0]['elements'][0]['distance']['value'] / 1000
                distances[i][j] = distance
                distances[j][i] = distance  # Distance matrix is symmetric

    return distances

def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours}h {minutes}m {seconds}s"

def choose_starting_point(distance_matrix):
    num_locations = len(distance_matrix)
    
    # Create a list of all location indices
    location_indices = list(range(num_locations))

    # Calculate the sum of distances to the top three closest locations for each location
    sum_distances = [sum(sorted(distance_matrix[i])) for i in location_indices]#[:3]
    
    # Find the location with the minimum sum of distances
    best_starting_point = location_indices[sum_distances.index(min(sum_distances))]
    
    return best_starting_point

def split_route(route, distance_matrix, max_distance=1):
    sub_routes = []
    sub_route = [0]
    distance_sum = 0

    for i in range(1, len(route)):
        distance_sum += distance_matrix[route[i - 1]][route[i]]
        if distance_sum > max_distance:
            if len(sub_route) > 1:  # Avoid sub-routes with only the starting location
                sub_routes.append(sub_route)
            sub_route = [0]
            distance_sum = 0

        sub_route.append(route[i])

    sub_routes.append(sub_route)
    return sub_routes

def generate_google_maps_link(locations):
    base_url = "https://www.google.com/maps/dir/"
    
    # Convert each location to a format suitable for the URL
    formatted_locations = [location.replace(' ', '+') for location in locations]
    
    # Combine the formatted locations to create the complete URL
    full_url = base_url + '/'.join(formatted_locations)
    
    return full_url




