from Main_functions  import seconds_to_hms  ,split_route,get_route_distances    ,generate_google_maps_link  ,calculate_total_distance   ,choose_starting_point

from Tsp_modified import tsp , create_order_constraint



def optimize_delivery_multiple_missions(mission_tasks, GOOGLE_MAPS_API_KEY='AIzaSyAgaRnl5RlSg1bX79_CH3E3xchf_bgA6Gw',):#AIzaSyAgaRnl5RlSg1bX79_CH3E3xchf_bgA6Gw

    results = []
    Pickup_locations=[]
    Pick_hub_index=[]
    Delivery_locations=[]
    Hub_locations=[]
    google_maps_link_list = []


    for task in mission_tasks:
        Pickup_locations.append(task['Pickup Address'])
        if task['Pickup Hub Name']!=None:
            Pick_hub_index.append(len(Pickup_locations)-1) # index of the pickup location that has a hub
            # print(f'Pick_hub_index: {Pick_hub_index} \n')

            Hub_locations.append(task['Pickup Hub Name']+','+task['Pickup Hub City'])
        Delivery_locations.append(task['Delivery Address'])
        
    print(f'Pickup_locations: {Pickup_locations} \n')
    print(f'Delivery_locations: {Delivery_locations} \n')
    print(f'Hub_locations: {Hub_locations} \n')


    #-------------------------------------------------------------------------------------------------------------
    # Pickup_locations=list(set(Pickup_locations))
    # Delivery_locations=list(set(Delivery_locations))
    # for locations in [Pickup_locations, Delivery_locations]:
    # we are going to make two loops one for pickup and one for delivery
    #-------------------------------------------------------------------------------------------------------------



    # Créer une contrainte d'ordre pour les emplacements de ramassage et de livraison

    order_constraint,locations = create_order_constraint(Pickup_locations,Delivery_locations,Hub_locations)

    index_to_location = {i: loc for i, loc in enumerate(locations)}
    # print(f'index_to_location {index_to_location} \n')
    # Obtenir la matrice des distances entre les emplacements
    distance_matrix = get_route_distances(locations, GOOGLE_MAPS_API_KEY)
    # print( f'distance_matrix {distance_matrix }\n ' )

    
    # A visual explination -------------------------------------------------------------------------------------------------------------
    locations_abstract = [f"p{i}" for i in range(   (len(Pickup_locations)+len(Delivery_locations)) //2)] + [f"d{i}" for i in range((len(Pickup_locations)+len(Delivery_locations))//2)]
    for i, index in enumerate(Pick_hub_index):
        locations_abstract.append(f"e{index}")  
    #-------------------------------------------------------------------------------------------------------------

    # Résoudre le problème du voyageur de commerce (TSP) avec des véhicules
    start_location= choose_starting_point(distance_matrix[:len(Pickup_locations)])

    routes = tsp(distance_matrix,start_location,order_constraint,      Pick_hub_index,3 ,locations_abstract)#default value  
    # print(f'route: {routes} \n')

    '''
    # no optimzation solution
    routes=[0,10,1,11,2,12,3,13,4,14,5,15,6,16,7,17,8,18,9,19]
    print(f'NON OPTIMIZED   route: {routes} \n')
    '''
    
    result = ""
    if routes:
        total_distance= calculate_total_distance(distance_matrix, routes)
        

        print(f'locations_abstract: {locations_abstract} \n')





        route_names = [locations_abstract[loc_idx] for loc_idx in routes]
        print(f'route_names: {route_names} \n')

        #-------------------------------------------------------------------------------------------------------------
        #set the corresponding locations to the routes
        route_names = [index_to_location[loc_idx] for loc_idx in routes]
        print(f'route_names: {route_names} \n')

        # route_names = [str(item) for item in route_names]
        # locations_abstract = [f"p{i // 2}" if i % 2 == 0 else f"d{i // 2}" for i in range(len(locations))]



        #gey the google maps link for the route
        google_maps_link = generate_google_maps_link(route_names)
        google_maps_link_list.append(google_maps_link)

        result += f"Optimal route : {' --> '.join(route_names)} <br>"
        result += f"Total distance : {total_distance:.2f} kilometers <br> <br>"

    else:
        result = "No solution found."

    results.append(result)
        
    return results,google_maps_link_list
