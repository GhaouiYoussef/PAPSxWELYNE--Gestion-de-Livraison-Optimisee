import numpy as np


def find_closest_unvisited_location(distance_matrix, current_location, visited, fixed_order_constraint,      pick_hub_index,      max_consecutive_pickups ,locations_abstract):# pick_hub_index=[2,4] e.g.
    n = len(distance_matrix)
    order_constraint=fixed_order_constraint.copy()
    # print('len(distance_matrix): ',len(distance_matrix))
    min_distance = float('inf')
    closest_location = None

    nb_hubs = len(pick_hub_index)
    # print('Pick_hub_index: ',pick_hub_index )
    unlocked_locations=[]
    num_pickups = (n- nb_hubs)//2
    # print('num_pickups: ',num_pickups)
    p_cons=0
    #let's make sure we havent break the max_consecutive_pickups allowed 
    list_cons_pick=[i for i in range((n-nb_hubs)//2 )]
    # print('list_cons_pick: ',list_cons_pick)





#entry check
    # for i in range(n):
    # print('i: ',i)
    # print('visited: ',visited)  
    #     print('current_location: ',current_location)
    #     print(f' order_const_before_ change : {locations_abstract[current_location]} && {locations_abstract[i]} : {order_constraint[current_location][i]}' )


#-------------------------------------------------------------------------------------------
    # print('first visited: ',visited)
    for i,loc in enumerate(visited):
        if loc < (n-nb_hubs)//2 :
            list_cons_pick.remove(loc)
            # print('list_cons_pick: ',list_cons_pick)
            p_cons+=1
            # print('p_cons: ',p_cons)
            if (p_cons==max_consecutive_pickups) :
                if  ((i+1==len(visited)) or (visited[i+1] < (n-nb_hubs)//2)):
                    order_constraint[:, list_cons_pick ] = 1# we lock thepickups outside the consutive ones , since they will be locked by the other constraint
                    # print('We locked the pickups outside the consutive ones')
                else:
                    p_cons=0
                    list_cons_pick=[ i for i in range((n-nb_hubs)//2 )]


    #-------------------------------------------------------------------------------------------------------------
    for location in visited:
        # print('location: in visted loop ',location)

        if ((location < num_pickups) and (location not in pick_hub_index)):
            unlocked_locations.append(location   +num_pickups)

        elif ((location < num_pickups) and(location in pick_hub_index)): #((location < n//2) pour optimiser

            unlocked_hub_index=pick_hub_index.index(location) # return 0 for .index(2) if pick_hub=[2,4]


            unlocked_locations.append(n - nb_hubs + unlocked_hub_index )# we unlock the hub instead of the delivery
        elif ((location >= n - nb_hubs)):
            unlocked_delivery_from_hub_index= location - 2*num_pickups 
            pickup_correspondant=pick_hub_index[unlocked_delivery_from_hub_index]

            unlocked_locations.append( pickup_correspondant +num_pickups)

    # print('visited: ',visited)
    order_constraint[:, unlocked_locations ] = 0
    # print('unlocked_locations: ',unlocked_locations)
    # print('order_constraint: ',order_constraint)
    

    # current_location=visited[-1]
    

    for i in range(n):
        # print('i: ',i)
        # print('visited: ',visited)  
        # print('current_location: ',current_location)
        # print(f' order_const : {locations_abstract[current_location]} && {locations_abstract[i]} : {order_constraint[current_location][i]}' )
        if  (i  in visited or order_constraint[current_location][i] == 1):
            # print('entered if')
            # print(distance_matrix[current_location][i])
            continue  # Skip locations that violate the condition
        else:
            # print('entered else')
            distance = distance_matrix[current_location][i]
            # print(f'distance entre {current_location} and {i} : {distance}')
            if distance < min_distance:
                min_distance = distance
                closest_location = i
    # print('order_constraint: ',order_constraint )
    # print('closest_location: ',closest_location)

    # If no location is found, consider unvisited locations without order constraints
    # if closest_location is None:
    #     for i in range(n):
    #         if i not in visited:
    #             distance = distance_matrix[current_location][i]
    #             if distance < min_distance:
    #                 min_distance = distance
    #                 closest_location = i

    return closest_location


def tsp(matrix, start_location,order_constraint,        pick_hub_index,        max_consecutive_pickups,locations_abstract):
    # print('locations_abstract: ',locations_abstract)
    n = len(matrix)
    visited = [start_location]
    
    Fixed_order_constraint=order_constraint.copy()
    while len(visited) < n:
        current_location = visited[-1]
        # print(f'order_constraint: for {current_location} ',Fixed_order_constraint)
        
        # print('visited in TSP : ',visited)
        closest_location = find_closest_unvisited_location(matrix, current_location, visited,Fixed_order_constraint,      pick_hub_index,      max_consecutive_pickups  ,locations_abstract)

        if closest_location is not None:
            visited.append(closest_location)
            current_location = closest_location
        else:
            break

    return visited

    
# def create_order_constraint(pickup_locations, delivery_locations):
def create_order_constraint(pickup_locations,delivery_locations,hub_locations):
    num_pickups = len(pickup_locations)
    num_deliveries = len(delivery_locations)
    num_hubs = len(hub_locations)

    #  Create an ordered list of locations (P1, P2, ,..., Pn, D1, D2, ..., Dn)
    # locations = pickup_locations+delivery_locations
    locations = pickup_locations+delivery_locations+hub_locations

    # Initialize an order_constraint matrix with the left half as 1 and the right half as 0
    order_constraint = np.zeros((len(locations), len(locations)), dtype=int)
    order_constraint[:, num_pickups :] = 1

    return order_constraint,locations



# l = ['p0', 'd0', 'p1', 'd1', 'p2', 'd2', 'p3', 'd3', 'p4', 'd4', 'p5', 'd5', 'p6', 'd6', 'p7', 'd7', 'p8', 'd8', 'p9', 'd9']
# input=[l[i] for i in range(0, len(l), 2)], [l[i] for i in range(1, len(l), 2)],['e2','e4']

# print(create_order_constraint(input[0],input[1],input[2],[2,4]))







