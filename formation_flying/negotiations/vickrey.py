'''
# =============================================================================
# This file contains the function to do a Vickrey auction. 
# =============================================================================
'''

def do_Vickrey(flight):
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
            possible_savings_sorted.sort(reverse=True) #sorts savings from highest to lowest
            if len(possible_savings_sorted) > flight.model.true_value_av_amount: #true_value_av_amount is the index for the possible savings used
                flight.savings_threshold = flight.model.max_bid_contractor*sum(possible_savings_sorted[:(flight.model.true_value_av_amount+1)])/len(possible_savings_sorted[:(flight.model.true_value_av_amount+1)]) 
            else: 
                flight.savings_threshold = flight.model.max_bid_contractor*sum(possible_savings_sorted)/len(possible_savings_sorted) #if there are too little targets, the average gets used. 
            if flight.savings_threshold < (0.30*max(possible_savings)): #If the savings threshold is lower than 30% of the max savings, it gets replaced with this value
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
                if savings[j]:
                    if flight.alliance == True and targets[j].alliance == True: 
                        flight.savings_threshold = 0 #savings to keep set to zero when both alliance members
                    
                    bid = savings[j] - flight.savings_threshold
                    
                    if bid != None and bid > 0: 
                        targets[j].received_bids.append(bid)
                        targets[j].bids_agents.append(flight)
                        flight.bids_placed_to.append(targets[j])

#------------------------------------------------------------------------------
#THIS IS THE IF PART THAT THE AUCTIONEERS (managers) FOLLOW
#------------------------------------------------------------------------------
    
    elif flight.manager == 1: 
        if flight.awaiting_bid > 2: #This means that every thirdth step, the managers look at the received bids, done due to activation
            if len(flight.received_bids) != 0: #if bids are placed, the highest is saved in a list, as well as the agent that placed it
                formation_target = flight.bids_agents[flight.received_bids.index(max(flight.received_bids))] #highest bid is chosen for formation
                formation_savings = flight.calculate_potential_fuelsavings(formation_target)
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
            flight.awaiting_bid = 0
        flight.awaiting_bid += 1
