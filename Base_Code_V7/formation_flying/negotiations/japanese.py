'''
# =============================================================================
# This file contains the function to do a Japanese auction. 
# =============================================================================
'''
from ..metrics import *

def do_Japanese(flight):
    if not flight.departure_time:
        raise Exception("The object passed to the greedy protocol has no departure time, therefore it seems that it is not a flight.")
    
#------------------------------------------------------------------------------
#THIS IS THE IF PART THAT THE CONTRACTORS FOLLOW
#------------------------------------------------------------------------------
    
    if flight.contractor == 1 and flight.formation == False: #contractors only go in if not in formation
            
#------ Find the best targets for the current flight and the maximum bidvalue
        formation_targets = flight.find_greedy_candidate()
        possible_savings = []
        if len(formation_targets) != 0:
            for agent in formation_targets:
                possible_savings.append(flight.calculate_potential_fuelsavings(agent))
            
            #For contractors in the japanese auction, the bid_threshold is the savings that they want to keep. So if they dont keep this savings when in an auction, they leave
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

#---------- Contractor will participate in all three auctions -----------------                    
            for j in range(len(targets)): 
                if savings[j] > 0:
                    if flight.alliance == True and targets[j].alliance == True:
                        flight.bid_threshold = 0
                        
                    max_bid = (savings[j] - flight.bid_threshold)
                    if max_bid < 0: 
                        max_bid = 0
                        
                    if len(targets[j].agents_left) == 0: #You can join the auction as long as no agents have left it
                        if targets[j] not in flight.agents_joined: #checks if you are not already part of this auction
                            targets[j].agents_joined.append(flight) #add to participantslist of the tartget
                            flight.agents_joined.append(targets[j]) #add target to own list of auctions agent is part of
                            
                    if targets[j] in flight.agents_joined:         
                        if targets[j].auction_value > max_bid:
                            targets[j].agents_left.append(flight) #add to list of agents that left the auction
                            del flight.agents_joined[flight.agents_joined.index(targets[j])] #delete target from own participants list
                            del targets[j].agents_joined[targets[j].agents_joined.index(flight)] #delete self from targets participants list
                    print(flight.unique_id, give_id_list(flight.agents_joined), give_id_list(targets[j].agents_joined), give_id_list(targets[j].agents_left))

#------------------------------------------------------------------------------
#THIS IS THE IF PART THAT THE AUCTIONEERS (managers) FOLLOW
#------------------------------------------------------------------------------
    
    elif flight.manager == 1: 
        loop = False
       #if flight.awaiting_bid > 2: #This means that every thirdth step, the managers look at the received bids, done due to activation
        flight.bid_threshold = 0 #For auctioneers the bid threshold is the minimum bid they want to receive, so auction starting point, which is calculated below
        formation_targets = flight.find_neighbors("a", flight.communication_range, "not formation") #All neighbor contractors in a list
        flight.best_target, possible_savings_man = flight.find_highest_fuelsaving(formation_targets)   
        if flight.best_target != None: 
            if max(possible_savings_man) > 0: #no negative saving taken 
                #This minimum bidvalue is the min of what this agent wants to receive as bid
                possible_savings_sorted_man = possible_savings_man
                possible_savings_sorted_man.sort(reverse=True) 
                if len(possible_savings_sorted_man) > flight.model.true_value_av_amount:
                    flight.bid_threshold = flight.model.min_bid_auctioneer*possible_savings_sorted_man[flight.model.true_value_av_amount]
                else: 
                    flight.bid_threshold = flight.model.min_bid_auctioneer*possible_savings_sorted_man[-1]
                if flight.bid_threshold < 0: 
                    flight.bid_threshold = 0
                
                if flight.auction_value == 0: #if the value is zero, the auction has not start so the start value is the minimum threshold
                    flight.auction_value = flight.bid_threshold 
                
                for agent in flight.agents_joined: 
                    if agent.formation == True: 
                        del flight.agents_joined[flight.agents_joined.index(agent)]
                
                flight.auction_value = flight.auction_value + flight.model.auction_step #Every step the bid is increase by 1 step-value
                if len(flight.agents_joined) == 1: #There is only one agent left in the auction, so that will become the target
                    formation_target = flight.agents_joined[0]
                    formation_savings = flight.auction_value - flight.model.auction_step
                    loop = True
                
                elif len(flight.agents_joined) == 0: #There are no agents left in the auction, so multiple agents left in the previous step. One of these agents is randomly chosen to be the target
                    if len(flight.high_agent) != 0: 
                        formation_target = flight.high_agent[0]
                        formation_savings = flight.auction_value - 2*flight.model.auction_step
                        loop = True                
                    else: 
                        flight.auction_value = 0
                        flight.agents_left = []
                if loop == True: 
                    if len(flight.agents_in_my_formation) > 0 and len(formation_target.agents_in_my_formation) == 0:
                        flight.add_to_formation(formation_target, formation_savings, discard_received_bids=True)
                    elif len(flight.agents_in_my_formation) > 0 and len(formation_target.agents_in_my_formation) > 0:
                        a=1
                    elif len(flight.agents_in_my_formation) == 0 and len(formation_target.agents_in_my_formation) > 0:
                        a=1
                    elif len(flight.agents_in_my_formation) == 0 and len(formation_target.agents_in_my_formation) == 0:
                        flight.start_formation(formation_target, formation_savings, discard_received_bids=True)
                    flight.auction_value = 0
                    flight.high_agent = []
                    flight.agents_joined = []
                    flight.agents_left = []
                flight.high_agent = flight.agents_joined[:] #list with joined agent in previous round, in case last agents leave at the same time
                flight.awaiting_bid = 0
        #flight.awaiting_bid += 1
