'''
# =============================================================================
# Data functions are saved here (instead of Model.py) for a better overview. 
# These functions can be called upon by the DataCollector. 
# You can add more advanced metric here!
# =============================================================================
'''
def compute_total_fuel_used(model):
    return model.total_fuel_consumption

def compute_planned_fuel(model):
    return model.total_planned_fuel

def fuel_savings_closed_deals(model):
    return model.fuel_savings_closed_deals

def real_fuel_saved(model):
    return model.total_planned_fuel - model.total_fuel_consumption

def total_deal_value(model):
    deal_values = [agent.deal_value for agent in model.schedule.agents]
    return sum(deal_values)

def compute_total_flight_time(model):
    return model.total_flight_time

def compute_model_steps(model):
    return model.schedule.steps

def new_formation_counter(model):
    return model.new_formation_counter

def add_to_formation_counter(model):
    return model.add_to_formation_counter

def give_id_list(list_of_agents):
    id_list = []
    for agent in list_of_agents: 
        id_list.append(agent.unique_id)
    return id_list

#finds the highest fuel savings 
def find_highest_fuelsaving(list_of_agents):
    if list_of_agents != None:
            #Makes a list of the possible savings of all formation_targets 
            possible_savings = []
            for agent in list_of_agents:
                possible_savings.append(agent.calculate_potential_fuelsavings(agent))
            #The best target is assignt to the agent with the highest possible savings, the value for best target is this agent
            if len(possible_savings) != 0:
                target = list_of_agents[possible_savings.index(max(possible_savings))]
    return target, possible_savings