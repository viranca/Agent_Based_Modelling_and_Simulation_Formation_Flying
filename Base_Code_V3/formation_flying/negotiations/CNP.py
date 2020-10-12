# =============================================================================
# This file contains the function to do Contract Net Protocol (CNP). 
# =============================================================================
from ..metrics import *

def do_CNP(flight):
    if not flight.departure_time:
        raise Exception("The object passed to the greedy protocol has no departure time, therefore it seems that it is not a flight.")
    
    if flight.auctioneer == 1 and flight.formation == False:             
        #Find the best target for the current flight
        formation_targets = flight.find_greedy_candidate()
        flight.best_target, possible_savings_auc = flight.find_highest_fuelsaving(formation_targets)
        if flight.best_target != None: 
            possible_savings_auc.sort(reverse=True)
            savings = possible_savings_auc[flight.auc_man_steps] #Gives the highest combined savings
            bid = flight.bid_multiplicity * 0.5 * savings #Gives a certain percentage of saving to manager, start with 50%
            savings_auc = savings - bid
            
            
            if flight.auc_man_steps < (len(possible_savings_auc)-2):
                #if with the current bid, the savings of the auctioneer are lower than when giving 50% to the an othere manager
                #then the auctioneer will bid to the next manager
                if savings_auc < (0.5*(possible_savings_auc[flight.auc_man_steps+1])):
                    flight.auc_man_steps +=1
                    flight.bid_multiplicity = 0
                    savings = possible_savings_auc[flight.auc_man_steps]
                    bid = flight.bid_multiplicity * 0.5 * savings

            #If an auctioneer goes a certain amount of steps bidding to the same manager without getting into formation, 
            #the bid is increased by 10 %, with a limit of 50% increase
            if flight.bids_placed_to.count(flight.best_target) > 6: 
                flight.bids_placed_to = []
                flight.bid_multiplicity *= 1.1
            if flight.bid_multiplicity > 1.5:
                flight.bid_multiplicity = 1.5
                
            bid = flight.bid_multiplicity * 0.5 * max(possible_savings_auc)
            flight.best_target.received_bids.append(bid)
            flight.best_target.bids_agents.append(flight)
            flight.bids_placed_to.append(flight.best_target)
    
    elif flight.manager == 1: 
        if flight.awaiting_bid > 2: #This means that every thirdth step, the managers look at the received bids, done due to activation
            bid_treshold = 0
            formation_targets = flight.find_neighbors("a", flight.communication_range)
            flight.best_target, possible_savings_man = flight.find_highest_fuelsaving(formation_targets)   
            if flight.best_target != None: 
                bid_treshold = 0.5* flight.model.bidding_threshold * max(possible_savings_man)
                if len(flight.received_bids) != 0:
                    if max(flight.received_bids) >= bid_treshold: 
                        formation_target = flight.bids_agents[flight.received_bids.index(max(flight.received_bids))]
                        formation_savings = max(flight.received_bids)
                        if len(flight.agents_in_my_formation) > 0 and len(formation_target.agents_in_my_formation) == 0:
                            flight.add_to_formation(formation_target, formation_savings, discard_received_bids=True)
                        elif len(flight.agents_in_my_formation) > 0 and len(formation_target.agents_in_my_formation) > 0:
                            a=1
                        elif len(flight.agents_in_my_formation) == 0 and len(formation_target.agents_in_my_formation) > 0:
                            a=1
                        elif len(flight.agents_in_my_formation) == 0 and len(formation_target.agents_in_my_formation) == 0:
                            flight.start_formation(formation_target, formation_savings, discard_received_bids=True)
        
                flight.received_bids = []
                flight.bids_agents = []
                flight.best_target = 0   
                flight.awaiting_bid = 0
        flight.awaiting_bid += 1
