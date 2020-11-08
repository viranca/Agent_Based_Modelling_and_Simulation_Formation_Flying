# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 15:02:48 2020

@author: viran
"""
#This code can run independently, and is a draft version for the joining/leaving point calculation.
#Moreover, the new path consumption can easily be derived.


import numpy as np
from sympy import Symbol, pi, tan, atan, sin, cos, solveset, S
from sympy.solvers import solve
from sympy.utilities.lambdify import lambdify 

# #this would be self.pos and target_agent.pos:
# agent1 = [1 ,4]
# agent2 = [2 ,4]

# #this would be self.destination and target_agent.destination:
# destination2 = [10 ,8]
# destination1 = [12 ,8]

# #this would be self.pos and target_agent.pos:
# agent1 = [16.48666198 ,62.32513341]
# agent2 = [16.48666198 ,62.32513341]

# #this would be self.destination and target_agent.destination:
# destination2 = [659.73401057 ,683.92990393]
# destination1 = [659.73401057 ,683.92990393]

# #this would be self.pos and target_agent.pos:
# agent1 = [137.715185, 85.63925238]
# agent2 = [128.97490696, 81.20909496]

# #this would be self.destination and target_agent.destination:
# destination2 = [561.73605249 ,701.13394229]
# destination1 = [561.73605249 ,701.13394229]

# #this would be self.pos and target_agent.pos:
# agent2 = [70.45117301 ,100.15042236]
# agent1 = [43.34585629 ,92.98025186]

# #this would be self.destination and target_agent.destination:
# destination1 = [697.79699006 ,652.39709545]
# destination2 = [697.79699006 ,652.39709545]

#this would be self.pos and target_agent.pos:
agent2 = [36.00233305 ,12.43001743]
agent1 = [21.94102428 ,78.87649048]

#this would be self.destination and target_agent.destination:
destination1 = [721.2986299  ,598.35391607]
destination2 = [702.61065994 ,604.77080425]


def calc_distance(p1, p2):
    # p1 = tuple(p1)
    # p2 = tuple(p2)
    dist = (((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** 0.5)
    return dist

def calc_middle_point(a, b):
    return [0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1])]

def calculate_new_joining_point(agent1, agent2, destination1, destination2):
    #for clarification on variables visit: https://app.lucidchart.com/invitations/accept/dd1c3d4b-d382-4365-884e-a81602c4a48c
    mp1 = calc_middle_point(agent1, agent2)
    mp2 = calc_middle_point(destination1, destination2)
    a = calc_distance(agent1, mp1)
    b = calc_distance(mp1, mp2)
    d = calc_distance(destination1, mp2)
    original_path = a + b + d
    
    #trigonometry flights
    v = abs(abs(agent1[0]) - abs(mp1[0]))  
    u = abs(abs(agent1[1]) - abs(mp1[1]))
    if u == 0:
        epsilon = 0
    else:
        epsilon = atan(v/u)
    o = abs(abs(mp1[0]) - abs(mp2[0]))  
    p = abs(abs(mp1[1]) - abs(mp2[1]))
    if p == 0:
        rho = 0
    else:
        rho = atan(o/p)
    s = abs(abs(destination1[0]) - abs(mp2[0]))         
    t = abs(abs(destination1[1]) - abs(mp2[1])) 
    if t == 0:
        psi = 0
    else:
        psi = atan(s/t)    
    
    #Solve for theta
    ##Trigonometry to obtain the flight path equations
    ###Joining point
    theta = Symbol('theta')
    phi = 0 #temporary
    delta = 90*(pi/180) - epsilon - rho
    omega = 180*(pi/180) - theta - delta
    L_1 = (a/sin(omega)) * sin(delta) 
    #set up the equation for the newpath as a function of theta and phi    
    new_path = L_1 + (b-a*tan(theta)-d*tan(phi))*0.75
    #differentiate the new path
    d_new_path_d_theta = new_path.diff(theta)
    #solve for theta, at this theta the new path is minimal
    optimal_theta = solveset(d_new_path_d_theta) 
    optimal_theta_check = optimal_theta
    if agent1 == agent2:
        optimal_theta = 0
    else: 
        optimal_theta2 = optimal_theta.args[0]
        optimal_theta3 = str(optimal_theta.args[0])[-29:-12]
        str_is = str(optimal_theta.args[0])
        optimal_theta4 = float(str_is[str_is.rfind(".")-1:str_is.rfind(",")-1])*0.5
        optimal_theta = 0
        #optimal_theta = float(str(optimal_theta.args[0])[-29:-12])*0.5


    #solve for phi
    ##Trigonometry to obtain the flight path equations
    ###Leaving point
    del phi
    phi = Symbol('phi')
    theta = 0 #temporary
    mu = 90*(pi/180) - psi + rho
    sigma = 180*(pi/180) - phi - mu 
    L_2 = (d/sin(sigma)) * sin(mu)
    new_path = (b-a*tan(theta)-d*tan(phi))*0.75 + L_2
    new_path_phi = new_path
    d_new_path_d_phi = new_path.diff(phi)
    optimal_phi = solveset(d_new_path_d_phi)
    if destination1 == destination2:
        optimal_phi = 0
    else:     
        optimal_phi = float(str(optimal_phi.args[0])[-29:-12])*0.5

    #calculation of new path
    X = ((a/sin(180*(pi/180) - optimal_theta - delta))) * sin(optimal_theta)
    Y = (d/sin(180*(pi/180) - optimal_phi - mu)) * sin(optimal_phi)
    new_path = (a/sin((180*(pi/180)) - optimal_theta - delta)) * sin(delta) + (b-X-Y)*0.75 + (d/sin(180*(pi/180) - optimal_phi - mu )) * sin(mu)
    ##new_path_consumption = new_path * f_c

    #Finally, the location of the joining and leaving point:
    ##Joining point    
    joining_point = []
    m = X * cos(rho)
    n = X * sin(rho)
    joining_point.append(mp1[0] + m)
    joining_point.append(mp1[1] + n)  
    ##Leaving point
    Y_x = Y * cos(rho)
    Y_y = Y * sin(rho)
    leaving_point = []
    leaving_point.append(mp2[0] + Y_x)
    leaving_point.append(mp2[1] + Y_y)    
    
     
    return joining_point, leaving_point

def calculate_new_joining_point_2(agent1, agent2, destination1, destination2):
    #for clarification on variables visit: https://app.lucidchart.com/invitations/accept/dd1c3d4b-d382-4365-884e-a81602c4a48c\
    #define the optimizer granularity here    
    granularity = 1 #radian
    
    mp1 = calc_middle_point(agent1, agent2)
    mp2 = calc_middle_point(destination1, destination2)
    a = calc_distance(agent1, mp1)
    b = calc_distance(mp1, mp2)
    d = calc_distance(destination1, mp2)
    original_path = a + b + d
    
    #trigonometry flights
    v = abs(abs(agent1[0]) - abs(mp1[0]))  
    u = abs(abs(agent1[1]) - abs(mp1[1]))
    if u == 0:
        epsilon = 0
    else:
        epsilon = atan(v/u)
    o = abs(abs(mp1[0]) - abs(mp2[0]))  
    p = abs(abs(mp1[1]) - abs(mp2[1]))
    if p == 0:
        rho = 0
    else:
        rho = atan(o/p)
    s = abs(abs(destination1[0]) - abs(mp2[0]))         
    t = abs(abs(destination1[1]) - abs(mp2[1])) 
    if t == 0:
        psi = 0
    else:
        psi = atan(s/t)    

    
        
    #Solve for theta
    ##Trigonometry to obtain the flight path equations
    ###Joining point
    theta = 0
    phi = 0 
    delta = 90*(pi/180) - epsilon - rho
    omega = 180*(pi/180) - theta - delta
    mu = 90*(pi/180) - psi + rho
    sigma = 180*(pi/180) - phi - mu 
    L_1 = (a/sin(omega)) * sin(delta) 
    L_2 = (d/sin(sigma)) * sin(mu)
    #set up the equation for the newpath as a function of theta and phi    
    new_path = L_1 + (b-((a/sin(180*(pi/180) - theta - delta))) * sin(theta)-(d/sin(180*(pi/180) - phi - mu)) * sin(phi))*0.75 + L_2
    
    new_path_before = new_path
    while new_path_before < new_path:
        new_path_before = new_path
        theta = theta + granularity*(pi/180)
        new_path = L_1 + (b-((a/sin(180*(pi/180) - theta - delta))) * sin(theta)-(d/sin(180*(pi/180) - phi - mu)) * sin(phi))*0.75 + L_2

    while new_path_before < new_path:
        new_path_before = new_path
        phi = phi + granularity*(pi/180)
        new_path = L_1 + (b-((a/sin(180*(pi/180) - theta - delta))) * sin(theta)-(d/sin(180*(pi/180) - phi - mu)) * sin(phi))*0.75 + L_2

    #calculation of new path
    X = ((a/sin(180*(pi/180) - theta - delta))) * sin(theta)
    Y = (d/sin(180*(pi/180) - phi - mu)) * sin(phi)
    new_path = (a/sin((180*(pi/180)) - theta - delta)) * sin(delta) + (b-X-Y)*0.75 + (d/sin(180*(pi/180) - phi - mu )) * sin(mu)
    # #new_path_consumption = new_path * f_c

    #Finally, the location of the joining and leaving point:
    ##Joining point    
    joining_point = []
    m = X * cos(rho)
    n = X * sin(rho)
    joining_point.append(mp1[0] + m)
    joining_point.append(mp1[1] + n)  
    ##Leaving point
    Y_x = Y * cos(rho)
    Y_y = Y * sin(rho)
    leaving_point = []
    leaving_point.append(mp2[0] + Y_x)
    leaving_point.append(mp2[1] + Y_y)    
    
     
    return joining_point, leaving_point
    
print(calculate_new_joining_point_2(agent1, agent2, destination1, destination2))


# test = "ImageSet(Lambda(_n, 2_npi + 0.506275350332556), Integers))" 

# print(test[test.rfind(".")-1:test.rfind(",")-1]);






