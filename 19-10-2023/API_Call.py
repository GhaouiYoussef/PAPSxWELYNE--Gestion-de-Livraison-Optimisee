from flask import Flask, request, jsonify
from Final_algorithm import optimize_delivery_multiple_missions
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/optimize": {"origins": "*"}})  # Allow all origins for the /optimize route
CORS(app)  # Enable CORS for all routes

@app.route('/optimize', methods=['POST'])
def optimize():
    # Get the JSON data from the frontend request
    data_missions = request.get_json()
    # print(f'data_missions: {data_missions[1]} \n')
    mission_tasks = []
    mission_id=[]
    for data in data_missions:
        

        for task in data['tasks']:
            mission_id=data['uid']
            task_id = task['_id']
            task_action = task['action']
            
            # Extracting addresses for pickup and delivery stops
            pickup_stop = task['stops'][0]
            delivery_stop = task['stops'][1]
            
            # Initialize hub information to None
            pickup_hub_name = None
            pickup_hub_city = None
            
            # Check if pickup stop has hub information
            if pickup_stop['hub']:
                pickup_hub_name = pickup_stop['hub']['name']
                pickup_hub_city = pickup_stop['hub']['location']['city']

            
            mission_tasks.append({
                'uid': mission_id,
                'Task ID': task_id,
                'Task Action': task_action,
                'Pickup Address': pickup_stop['address']['address'],
                'Delivery Address': delivery_stop['address']['address'],
                'Pickup Hub Name': pickup_hub_name,
                'Pickup Hub City': pickup_hub_city,
            })

    # Extracting client information from Mission 1
    # client_info_mission = {
    #     'Client Company Name': data['client']['client_company_name'],
    #     'Client Phone Number': data['client']['client_phone_number'],
    #     'Client Email': data['client']['client_contact_email'],
    # }

    # Combine all extracted information for Mission 1
    mission_info = {
        # 'Mission ID': mission_id,
        'Tasks': mission_tasks
        # 'Client Info': client_info_mission,
    }
    # return jsonify(mission_info)
    #     # Run your optimization algorithm using the extracted data for the current mission
    mission_route,data,google_maps_link_list = optimize_delivery_multiple_missions(mission_info)  # Pass the list of stops for this mission
    # )

    # optimized_routes.append(mission_route)

    # # Return the optimization results for all missions as a JSON response
    return jsonify(mission_route,google_maps_link_list,data), 200

if __name__ == '__main__':
    app.run(debug=True)
