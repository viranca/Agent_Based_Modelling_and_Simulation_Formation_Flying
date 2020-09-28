# =============================================================================
# This file contains the function to do Contract Net Protocol (CNP). 
# =============================================================================

def do_CNP(flight):
    # the do_CNP function takes a flight-agent object
    if not flight.departure_time:
        raise Exception("The object passed to the greedy protocol has no departure time, therefore it seems that it is not a flight.")

#Find all neighbours, and make them targets for bidding.
    if flight.formation_state == 1:
        bidding_targets = flight.find_greedy_candidate()
        
        if bidding_targets != None:
            
#for each agent in bidding target, calculate the potential fuel savings.            
            for agent in bidding_targets:
                formation_savings = flight.calculate_potential_fuelsavings(agent)

#offer the amount of fuel potentially saved fuel as a bid to the best neighbours. (The higher, the better the bid.)
                flight.make_bid(agent, formation_savings)
        
        
        
#check recieved bids
    recieved_bids = flight.recieved_bids

#check if recieved bid is better than offered bid.


#if yes,accept. If no, wait..., reconsider?.                
    

#accept highest bid, make self a manager and target a contractee.

#add/start formation:
    # if len(flight.agents_in_my_formation) > 0:
    #     flight.add_to_formation(formation_target, formation_savings, discard_received_bids=True)
    # else:
    #     flight.start_formation(formation_target, formation_savings, discard_received_bids=True)
    # break       