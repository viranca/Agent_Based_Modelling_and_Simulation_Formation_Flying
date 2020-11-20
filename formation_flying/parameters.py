'''
# =============================================================================
# In this file one can change the parameters as stated by the exercises. 
# Clarifications of the of the model parameters can be found in the assignment.
#
# Airport and canvas parameters:
# 	n_origin_airports = 20 [-]. Number of randomly generated origin airports.
# 	n_destination_airports = 20 [-]. Number of randomly generated destination airports.
# 	width = 750 [km]. Width of the canvas.
# 	height = 750 [km]. Height of the canvas.
# 	Boundaries of randomly generated airports:
# 	origin_airport_x: [0.01, 0.3]. 
# 	origin_airport_y: [0.01, 0.3].
# 	destination_airport_x: [0.7, 0.99].
# 	destination_airport_y: [0.7, 0.99].
#
# Flight parameters:
# 	n_flights = 50 [-]. Number of aircraft/flights.
# 	departure_window = 3 [s]. 
# 	speed = 0.3 [km/s]. Speed of the aircraft.
# 	communication_range = 200 [km]. Range 
# 	fuel_reduction = 0.75 [-]. When flying in formation, you use 75% of your original fuel consumption.
# 	negotiation_method = 0 [-]. Set which negotiation method to use 
#           (0: greedy algorithm, 1: CNP, 2: English, 3: Vickrey, 4: Japanese).
#
# Simulation parameters:
# 	n_iterations = 1 [-]. Number of simulation runs, used in the batch runner.

# =============================================================================
'''

from .metrics import *


# This can be infinite, as the model should stop on its own when all agents have arrived at their destination.
max_steps = 4000
# Multiple iterations are used when running the batchrunner.py:
n_iterations = 100

model_params = {
    "n_flights": 50,
    "n_origin_airports": 20,
    "n_destination_airports": 20,
    "communication_range": 200, #[km]
    "width": 750, # [km]
    "height": 750, # [km]
    "speed": 0.3, #[km / second]
    "fuel_reduction": 0.75, 
    "negotiation_method": 4,
    "auction_step": 5, #The stepsize that is added to a bid inside the auctions
    "auction_start": 0.5,
    "joining_method": 2,
    "bidding_threshold": 0.9, #the percentage of the max value, that a manager wants at least (used in CNP)
    "departure_window": 3, 
    "area_range": 25, #[km]
    "n_manager": 40, #[%]
    "origin_airport_x": [0.01, 0.3], 
    "origin_airport_y": [0.01, 0.3],
    "destination_airport_x": [0.7, 0.99], 
    "destination_airport_y": [0.7, 0.99],
    "max_bid_contractor": 0.5,
    "min_bid_auctioneer": 0.5,
    "true_value_av_amount_per": 2,
}

# To run model with a variable parameter:
# example: variable_params = {"communication_range": [0, 100, 500]}
variable_params = {"communication_range": [200]}

'''
# =============================================================================
# Additional parameters are added here, to be tracked by the Datacollector and metrics.py
# =============================================================================
'''

model_reporter_parameters={"Total Fuel Used": compute_total_fuel_used, 
                           "steps": compute_model_steps, 
                           "new formations": new_formation_counter, 
                           "added to formations": add_to_formation_counter, 
                           "Total planned Fuel": compute_planned_fuel,
                           "Total saved potential saved fuel": fuel_savings_closed_deals, 
                           "Real saved fuel": real_fuel_saved,
                           "Deal values": total_deal_value,
                           "Total Arrival Time": compute_total_arrival_time,
                           "Arrival Times": flight_arrivals,
                           "Av Savings Alliance": average_alliance_fuel,
                           "Av Savings non-Alliance": average_nonalliance_fuel,
                           "Av Savings Managers": average_manager_fuel,
                           "Av Savings Contractors": average_contractor_fuel}

# In order to collect values like "deal-value", they should be specified on all agents.
agent_reporter_parameters={"Deal value": "deal_value"} 