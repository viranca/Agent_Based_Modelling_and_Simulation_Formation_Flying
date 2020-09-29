# =============================================================================
# This file contains the function to do Contract Net Protocol (CNP). 
# =============================================================================
from ..metrics import *

def do_CNP(flight):

    if not flight.departure_time:
        raise Exception("The object passed to the greedy protocol has no departure time, therefore it seems that it is not a flight.")
    loop = False
    if flight.manager == 1: 
        formation_targets = flight.find_greedy_candidate()
        flight.best_target, possible_savings = find_highest_fuelsaving(formation_targets)    
        target = flight.best_target
        loop = True
                
    if flight.formation_state == 0 and flight.auctioneer == 0:
        #Find the best target for the current flight
        formation_targets = flight.find_greedy_candidate()
        flight.best_target, possible_savings = find_highest_fuelsaving(formation_targets)    
        target = flight.best_target
        #Update the best target of the target for the current flight
        target_formation_targets = target.find_greedy_candidate()
        target.best_target = find_highest_fuelsaving(target_formation_targets)[0]
        loop = True
        
    #if the best target of the best target of our flight is our flight, then this means we have a match 
    if loop == True:       
        if target.best_target.unique_id == flight.unique_id:        
            formation_target = target
            formation_savings = max(possible_savings)
            if len(flight.agents_in_my_formation) > 0 and len(target.agents_in_my_formation) == 0:
                flight.add_to_formation(formation_target, formation_savings, discard_received_bids=True)
            elif len(flight.agents_in_my_formation) > 0 and len(target.agents_in_my_formation) > 0:
                a=1
            elif len(flight.agents_in_my_formation) == 0 and len(target.agents_in_my_formation) > 0:
                a=1
            else:
                flight.start_formation(formation_target, formation_savings, discard_received_bids=True)


  