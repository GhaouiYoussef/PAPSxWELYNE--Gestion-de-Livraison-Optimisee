from Delivery_op_GM_distance_based import seconds_to_hms,solve_tsp_with_vehicles,split_route,selection,calculate_fitness,create_data_model,crossover,mutation,initialize_population,get_route_distances,generate_google_maps_link



def optimize_delivery_multiple_missions(mission_tasks, GOOGLE_MAPS_API_KEY='AIzaSyAgaRnl5RlSg1bX79_CH3E3xchf_bgA6Gw',
                                         num_vehicles=4, 
                                         max_distance=0.2):#AIzaSyAgaRnl5RlSg1bX79_CH3E3xchf_bgA6Gw
    results = []
    Pickup_locations=[]
    Delivery_locations=[]
    Hub_locations=[]
    google_maps_link_list = []


    for task in mission_tasks:
        Pickup_locations.append(task['Pickup Address'])
        if task['Pickup Hub Name']!=None:
            Hub_locations.append(task['Pickup Hub Name']+','+task['Pickup Hub City'])
        Delivery_locations.append(task['Delivery Address'])
        
    print(f'Pickup_locations: {Pickup_locations} \n')
    print(f'Delivery_locations: {Delivery_locations} \n')
    print(f'Hub_locations: {Hub_locations} \n')
        
    # we are going to make two loops one for pickup and one for delivery
    Pickup_locations=list(set(Pickup_locations))
    Delivery_locations=list(set(Delivery_locations))
    for locations in [Pickup_locations, Delivery_locations]:

        index_to_location = {i: loc for i, loc in enumerate(locations)}

        # Obtenir la matrice des distances entre les emplacements
        distance_matrix = get_route_distances(locations, GOOGLE_MAPS_API_KEY)

        # Créer le modèle de données
        data = create_data_model(locations, num_vehicles)

        # Résoudre le problème du voyageur de commerce (TSP) avec des véhicules
        routes = solve_tsp_with_vehicles(data, distance_matrix, max_distance=max_distance)

        result = ""

        if routes:
            for i, route in enumerate(routes):
                total_distance = sum(distance_matrix[route[j - 1]][route[j]] for j in range(1, len(route)))

                route_names = [index_to_location[loc_idx] for loc_idx in route]
                route_names = [str(item) for item in route_names]

                google_maps_link = generate_google_maps_link(route_names)
                google_maps_link_list.append(google_maps_link)

                result += f"Route optimale pour le véhicule {i + 1}: {' -> '.join(route_names)} \n"
                result += f"Distance totale de la route pour le véhicule {i + 1}: {total_distance:.2f} kilomètres \n\n"
        else:
            result = "Aucune solution trouvée."

        results.append(result)
    # Générer le lien Google Maps
    # google_maps_link = generate_google_maps_link(route_names)
    
    return results,google_maps_link_list
