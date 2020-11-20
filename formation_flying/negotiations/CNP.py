# =============================================================================
# This file contains the function to do Contract Net Protocol (CNP). 
# Version V2 Alliance in there
# =============================================================================
from ..metrics import *

def do_CNP(flight):
    if not flight.departure_time:
        raise Exception("The object passed to the greedy protocol has no departure time, therefore it seems that it is not a flight.")

#------------------------------------------------------------------------------
#THIS IS THE IF PART THAT THE CONTRACTORS FOLLOW
#------------------------------------------------------------------------------
    
    if flight.contractor == 1 and flight.formation == False: #All contractors go into this loop, if they are not part of a formation       
        formation_targets = flight.find_greedy_candidate()
        possible_savings = flight.find_highest_fuelsaving(formation_targets)[1] #These are the savings for all targets
        
        if flight.auc_man_steps >= (len(possible_savings)-1):
            flight.auc_man_steps = 0   #This is a variable needed to start at the max saving target, and go to the next one if it does not work out 
        
        if len(possible_savings) != 0: 
            for i in range(len(possible_savings)):
                #If you are an alliance member, but the target is not, you bid 50% of the savings. If both are alliance, you bid 100%
                if formation_targets[i].alliance == False and flight.alliance == True: 
                    possible_savings[i] *= 0.5
                #if you are not an alliance member, you start bidding 50% of the savings
                elif flight.alliance == False: 
                    possible_savings[i] *= 0.5
                    
            possible_savings_sorted = possible_savings[:]
            possible_savings_sorted.sort(reverse=True) #Savings are sorted, max savings in front of list
            
                     
            savings = possible_savings_sorted[flight.auc_man_steps] #Gives the savings of the current target
            flight.best_target = formation_targets[possible_savings.index(savings)] #Gives the agent that belongs to these savings
            
            if flight.alliance == False: 
                bid = flight.bid_multiplicity * savings
                savings_auc = savings - bid
            elif flight.alliance == True: 
                bid = savings
                savings_auc = bid
            
            if savings_auc < bid:
                bid = 0.9*savings
            

                #if with the current bid, the savings of the contractor are lower than when giving 50% to the an othere manager
                #then the contractor will bid to the next manager. This only happens when the bid is increased enough
            if flight.auc_man_steps < (len(possible_savings_sorted)-1):
                if savings_auc < (possible_savings_sorted[flight.auc_man_steps+1]):
                    flight.auc_man_steps +=1
                    flight.bid_multiplicity = 1

            #If an contractor goes a certain amount of steps bidding to the same manager without getting into formation, 
            #the bid is increased by 10 %, with a limit of 50% increase
            if flight.bids_placed_to.count(flight.best_target) > 6: 
                flight.bids_placed_to = []
                flight.bid_multiplicity *= 1.1
            if flight.bid_multiplicity > 1.5:
                flight.bid_multiplicity = 1.5
          
            flight.best_target.received_bids.append(bid)
            flight.best_target.bids_agents.append(flight)
            flight.bids_placed_to.append(flight.best_target)

#------------------------------------------------------------------------------
#THIS IS THE IF PART THAT THE MANAGERS FOLLOW
#------------------------------------------------------------------------------

    elif flight.manager == 1: #All managers go into this function
        if flight.awaiting_bid > 2: #This means that every thirth step, the managers look at the received bids
            bid_treshold = 0
            formation_targets = flight.find_neighbors("a", flight.communication_range, "not formation") #Gives all contractors in neighborhood
            flight.best_target, possible_savings_man = flight.find_highest_fuelsaving(formation_targets)  #Best target, and savings belonging to all contractors from previous line 
            if flight.best_target != None: 
                bid_treshold = 0.40* max(possible_savings_man) #Minimum bid a manager wants
                if len(flight.received_bids) != 0: #Checks if bids are received
                    if max(flight.received_bids) >= bid_treshold and max(flight.received_bids) > 0: #Checks if highest bid is larger than minimum accepteble bid for manager
                        formation_target = flight.bids_agents[flight.received_bids.index(max(flight.received_bids))]
                        formation_savings = max(flight.received_bids)
                        if formation_target not in flight.agents_in_my_formation:
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
