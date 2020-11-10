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
            
#------ Find the best targets for the current flight and the maximum bidvalue
        formation_targets = flight.find_greedy_candidate()
        possible_savings = []
        if len(formation_targets) != 0:
            for agent in formation_targets:
                possible_savings.append(flight.calculate_potential_fuelsavings(agent))
            
            #For contractors in the vickrey auction, the bid_threshold is the savings that they want to keep. So the worth of the savings is the total savings minus this threshold
            possible_savings_sorted = possible_savings
            possible_savings_sorted.sort(reverse=True) 
            if len(possible_savings_sorted) > flight.model.true_value_av_amount:
                flight.bid_threshold = flight.model.max_bid_contractor*sum(possible_savings_sorted[:(flight.model.true_value_av_amount+1)])/len(possible_savings_sorted[:(flight.model.true_value_av_amount+1)]) 
            else: 
                flight.bid_threshold = flight.model.max_bid_contractor*sum(possible_savings_sorted)/len(possible_savings_sorted) 
            if flight.bid_threshold < (0.25*max(possible_savings)): 
                flight.bid_threshold = 0.25*max(possible_savings)
            if flight.bid_threshold < 0: 
                flight.bid_threshold = 0
            #A bid will be placed to the best three targets
            if len(formation_targets) <= 3: 
                targets = formation_targets
                savings = possible_savings
            elif len(formation_targets) > 3: 
                targets = []
                savings = []
                for i in range(3): 
                    target = formation_targets[possible_savings.index(max(possible_savings))]
                    saving = max(possible_savings)
                    del formation_targets[possible_savings.index(max(possible_savings))]
                    del possible_savings[possible_savings.index(max(possible_savings))]
                    if target != 0:
                        targets.append(target)
                        savings.append(saving)
                    target = 0

#---------- A bid will be placed to all three targets -------------------------                    
            for j in range(len(targets)): 
                if savings[j]:
                    if flight.alliance == True and targets[j].alliance == True:
                        flight.bid_threshold = 0 #if both in alliance, the contractor is willing to bid everything
                    
                    bid = savings[j] - flight.bid_threshold
                    
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
                formation_target = flight.bids_agents[flight.received_bids.index(max(flight.received_bids))]
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
