# =============================================================================
# This file contains the function to do Contract Net Protocol (CNP). 
# Version V2 Alliance in there
# =============================================================================
from ..metrics import *

def do_CNP(flight):
    if not flight.departure_time:
        raise Exception("The object passed to the greedy protocol has no departure time, therefore it seems that it is not a flight.")
    
    if flight.auctioneer == 1 and flight.formation == False:             
        #Find the best target for the current flight
        formation_targets = flight.find_greedy_candidate()
        possible_savings = flight.find_highest_fuelsaving(formation_targets)[1]
        
        if flight.auc_man_steps >= (len(possible_savings)-1):
            flight.auc_man_steps = 0    
        
        if len(possible_savings) != 0: 
            for i in range(len(possible_savings)):
                #If you are an alliance member, but the target is not, you bid 50% of the savings. If both are alliance, you bid 100%
                if formation_targets[i].alliance == False and flight.alliance == True: 
                    possible_savings[i] *= 0.5
                #if you are not an alliance member, you start bidding 50% of the savings
                elif flight.alliance == False: 
                    possible_savings[i] *= 0.5
                    
            possible_savings_sorted = possible_savings
            possible_savings_sorted.sort(reverse=True)
            
                     
            savings = possible_savings_sorted[flight.auc_man_steps] #Gives the highest combined savings
            flight.best_target = formation_targets[possible_savings.index(savings)]
            
            if flight.alliance == False: 
                bid = flight.bid_multiplicity * savings
                savings_auc = savings - bid
            elif flight.alliance == True: 
                bid = savings
                savings_auc = bid
            
            

                #if with the current bid, the savings of the auctioneer are lower than when giving 50% to the an othere manager
                #then the auctioneer will bid to the next manager
            if flight.auc_man_steps < (len(possible_savings_sorted)-1):
                if savings_auc < (possible_savings_sorted[flight.auc_man_steps+1]):
                    flight.auc_man_steps +=1
                    flight.bid_multiplicity = 1

            #If an auctioneer goes a certain amount of steps bidding to the same manager without getting into formation, 
            #the bid is increased by 10 %, with a limit of 50% increase
            if flight.bids_placed_to.count(flight.best_target) > 6: 
                flight.bids_placed_to = []
                flight.bid_multiplicity *= 1.1
            if flight.bid_multiplicity > 1.5:
                flight.bid_multiplicity = 1.5
            
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
