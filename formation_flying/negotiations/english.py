'''
# =============================================================================
# This file contains the function to do an English auction. 
# =============================================================================
'''
from ..metrics import *

def do_English(flight):
    if not flight.departure_time:
        raise Exception("The object passed to the greedy protocol has no departure time, therefore it seems that it is not a flight.")
    
#------------------------------------------------------------------------------
#THIS IS THE IF PART THAT THE CONTRACTORS FOLLOW
#------------------------------------------------------------------------------
    
    if flight.contractor == 1 and flight.formation == False:  #contractors only go in if not in formation
            
#------ Find the possible savings for all available auctioneers
        formation_targets = flight.find_greedy_candidate()
        possible_savings = []
        if len(formation_targets) != 0:
            for agent in formation_targets:
                possible_savings.append(flight.calculate_potential_fuelsavings(agent))
            
           #Calculate the savings threshold, which is the minimum savings an contractor will keep for itself.
            possible_savings_sorted = possible_savings
            possible_savings_sorted.sort(reverse=True)  #sorts savings from highest to lowest
            if len(possible_savings_sorted) > flight.model.true_value_av_amount: #true_value_av_amount is the index for the possible savings used
                flight.savings_threshold = flight.model.max_bid_contractor*sum(possible_savings_sorted[:(flight.model.true_value_av_amount+1)])/len(possible_savings_sorted[:(flight.model.true_value_av_amount+1)]) 
            else: 
                flight.savings_threshold = flight.model.max_bid_contractor*sum(possible_savings_sorted)/len(possible_savings_sorted) #if there are too little targets, the average gets used. 
            if flight.savings_threshold < (0.30*max(possible_savings)):  #If the savings threshold is lower than 30% of the max savings, it gets replaced with this value
                flight.savings_threshold = 0.30*max(possible_savings)
            if flight.savings_threshold < 0: #minimum savings to keep must be positive
                flight.savings_threshold = 0
            #A bid will be placed to the best three targets
            if len(formation_targets) <= 3: 
                targets = formation_targets
                savings = possible_savings
            elif len(formation_targets) > 3: 
                targets = [] #this will become a list with the targets in whose auctions the contractor will participate
                savings = [] #these are the savings that belong to those targeted auctioneers
                for i in range(3): 
                    target = formation_targets[possible_savings.index(max(possible_savings))]
                    saving = max(possible_savings)
                    del formation_targets[possible_savings.index(max(possible_savings))]
                    del possible_savings[possible_savings.index(max(possible_savings))]
                    if target != 0 and saving > 0:
                        targets.append(target)
                        savings.append(saving)
                    target = 0

#---------- A bid will be placed to all three targets -------------------------                    
            for j in range(len(targets)): 
                if savings[j] > 0:
                    if flight.alliance == True and targets[j].alliance == True: 
                        flight.savings_threshold = 0 #savings to keep set to zero when both alliance members
                    
                    flight.bid_threshold = savings[j] - flight.savings_threshold #bid threshold is the max bid to place in this auction
               
                    if len(targets[j].received_bids) == 0: #Checks if there are bids placed in the current step
                        if len(targets[j].high_bid) == 0: #Checks if this is the start of this auction round
                            bid = targets[j].bid_threshold #if it is the start, bid starting value
                        else: 
                            if (targets[j].high_bid[-1] + flight.model.auction_step) <= flight.bid_threshold: #check if new bid is below max bid
                                if targets[j].high_bid[-1] == flight.prev_bid_placed: #if highest bid is your last bid, repeat bid
                                    bid = targets[j].high_bid[-1]
                                else: 
                                    bid = targets[j].high_bid[-1] + flight.model.auction_step #if not, bid slightly higher
                            else: 
                                bid = None
                    else: 
                        #if the highest bid + the step is smaller than the agents maximum allowed bid, then a new bid is placed
                        if (max(targets[j].received_bids) + flight.model.auction_step) <= flight.bid_threshold:
                            bid = max(targets[j].received_bids) + flight.model.auction_step
                        else: 
                            bid = None       
                    if bid != None: 
                        if (savings[j] - bid) >= 0 and bid > 0: #you cant bid more than is saved and a bid must be positive
                            targets[j].received_bids.append(bid)
                            targets[j].bids_agents.append(flight)
                            flight.bids_placed_to.append(targets[j])
                            flight.prev_bid_placed = bid

#------------------------------------------------------------------------------
#THIS IS THE IF PART THAT THE AUCTIONEERS (managers) FOLLOW
#------------------------------------------------------------------------------
    
    elif flight.manager == 1: 
        flight.bid_threshold = 0 #For auctioneers the bid threshold is the minimum bid they want to receive, so auction starting point, which is calculated below
        formation_targets = flight.find_neighbors("a", flight.communication_range, "not formation") #All neighbor contractors in a list
        flight.best_target, possible_savings_man = flight.find_highest_fuelsaving(formation_targets)   
        if flight.best_target != None: 
            #This minimum bidvalue is the min of what this agent wants to receive as bid, same procedure as for contractors
            possible_savings_sorted_man = possible_savings_man
            possible_savings_sorted_man.sort(reverse=True) 
            if len(possible_savings_sorted_man) > flight.model.true_value_av_amount:
                flight.bid_threshold = flight.model.min_bid_auctioneer * possible_savings_sorted_man[flight.model.true_value_av_amount]
            else: 
                flight.bid_threshold = flight.model.min_bid_auctioneer * possible_savings_sorted_man[-1]
            if flight.bid_threshold < 0.3 * possible_savings_sorted_man[0]:
                flight.bid_threshold = 0.3 * possible_savings_sorted_man[0]
         
            if len(flight.received_bids) != 0: #if bids are placed, the highest is saved in a list, as well as the agent that placed it
                highest_bid = max(flight.received_bids)
                flight.high_bid.append(highest_bid)
                flight.high_agent.append(flight.bids_agents[flight.received_bids.index(highest_bid)])
            if len(flight.high_bid) >=1:
                if flight.prev_lst_len == len(flight.high_bid): #if the highest bid is the same for 2 times in a row
                    formation_target = flight.high_agent[-1]
                    formation_savings = flight.high_bid[-1]
                    if len(flight.agents_in_my_formation) > 0 and len(formation_target.agents_in_my_formation) == 0:
                        flight.add_to_formation(formation_target, formation_savings, discard_received_bids=True)
                    elif len(flight.agents_in_my_formation) > 0 and len(formation_target.agents_in_my_formation) > 0:
                        a=1
                    elif len(flight.agents_in_my_formation) == 0 and len(formation_target.agents_in_my_formation) > 0:
                        a=1
                    elif len(flight.agents_in_my_formation) == 0 and len(formation_target.agents_in_my_formation) == 0:
                        flight.start_formation(formation_target, formation_savings, discard_received_bids=True)
                    flight.high_bid = []
                flight.prev_lst_len = len(flight.high_bid)
            flight.received_bids = []
            flight.bids_agents = []
            flight.best_target = 0   

