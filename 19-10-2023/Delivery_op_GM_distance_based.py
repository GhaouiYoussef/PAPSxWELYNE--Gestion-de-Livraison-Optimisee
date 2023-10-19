import random
import requests
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

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

def create_data_model(locations, num_vehicles=2):
    data = {}
    data['locations'] = locations
    data['num_vehicles'] = num_vehicles
    data['depot'] = 0  # Starting location (index of the Firm location in the locations list)
    return data


def initialize_population(num_routes, num_locations):
    population = []
    for _ in range(num_routes):
        route = list(range(1, num_locations))  # Exclude the starting location (Firm)
        random.shuffle(route)
        population.append(route)
    return population



def calculate_fitness(route, distance_matrix):
    # print(f'route unside calculate_fitness: {route[0]}\n')
    total_distance = distance_matrix[0][route[0]]
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]
    total_distance += distance_matrix[route[-1]][0]  # Return to the Firm
    return total_distance

def selection(population, distance_matrix, num_selected):
    selected_routes = random.sample(population, num_selected)
    return sorted(selected_routes, key=lambda x: calculate_fitness(x, distance_matrix))[:2]

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
    child2 = parent2[:crossover_point] + [gene for gene in parent1 if gene not in parent2[:crossover_point]]
    return child1, child2

def mutation(route):
    mutation_point1, mutation_point2 = random.sample(range(len(route)), 2)
    route[mutation_point1], route[mutation_point2] = route[mutation_point2], route[mutation_point1]
    return route

def genetic_algorithm(distance_matrix, num_routes, num_generations):
    num_locations = len(distance_matrix)
    population = initialize_population(num_routes, num_locations)

    for generation in range(num_generations):
        new_population = []
        for _ in range(num_routes // 2):
            parent1, parent2 = selection(population, distance_matrix, 2)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutation(child1)
            child2 = mutation(child2)
            new_population.extend([child1, child2])
        population = new_population

    best_route = min(population, key=lambda x: calculate_fitness(x, distance_matrix))
    return [0] + best_route + [0]  # Include the starting location (Firm)

 
def solve_tsp_with_vehicles(data, distance_matrix, max_distance=1):
    max_distance = max_distance * 1000  # Convert max_distance to meters
    depot_index = 0

    # Create a routing index manager with the number of locations, number of vehicles, and depot (starting location) index
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), data['num_vehicles'], depot_index)

    # Create a routing model
    routing = pywrapcp.RoutingModel(manager)

    # Define a distance callback function that calculates the distance between two locations
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Set the cost evaluator for all vehicles
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Configure search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search_parameters.time_limit.seconds = 1

    # Solve the TSP with the configured parameters
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        routes = []
        vehicle_id = data['num_vehicles'] - 1
        index = routing.Start(vehicle_id)
        route = []
        
        # Extract the routes for each vehicle
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            index = solution.Value(routing.NextVar(index))
        
        # Modify the routes to start and end with the depot index
        routes = [[0] + route + [0] for route in routes]    
        routes.append(route)

        # Calculate the total distance for each route
        total_distances = [
            sum(distance_matrix[route[j - 1]][route[j]] for j in range(1, len(route)))
            for route in routes
        ]

        # Find the best route and check if its distance exceeds max_distance
        best_route_idx = total_distances.index(min(total_distances))
        best_route_distance = total_distances[best_route_idx]

        if best_route_distance > max_distance or data['num_vehicles'] >= 2:
            # Split the best route into multiple routes if needed
            best_route = routes[best_route_idx]
            new_routes = split_route(best_route, distance_matrix, max_distance)
            if new_routes:
                routes.pop(best_route_idx)
                routes.extend(new_routes)

        return routes

    return None

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




