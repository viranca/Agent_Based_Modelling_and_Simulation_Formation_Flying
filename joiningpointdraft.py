# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 15:02:48 2020

@author: viran
"""
#This code can run independently, and is a draft version for the joining/leaving point calculation.
#Moreover, the new path consumption can easily be derived.

from math import *
import numpy as np
from sympy import *

#this would be self.pos and target_agent.pos:
agent1 = [1, 2]
agent2 = [3, 2]

#this would be self.destination and target_agent.destination:
destination1 = [11, 9]
destination2 = [12, 9]


def calc_distance(p1, p2):
    # p1 = tuple(p1)
    # p2 = tuple(p2)
    dist = (((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** 0.5)
    return dist

def calc_middle_point(a, b):
    return [0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1])]

def calculate_new_joining_point(agent1, agent2, destination1, destination2):
    mp1 = calc_middle_point(agent1, agent2)
    mp2 = calc_middle_point(destination1, destination2)
    a = calc_distance(agent1, mp1)
    b = calc_distance(mp1, mp2)
    d = calc_distance(destination1, mp2)
    original_path = a + b + d
    
    #Solve for theta
    theta = Symbol('theta')
    phi = 0 #temporary
    L_1 = a/cos(theta)
    L_2 = d/cos(phi)
    new_path = L_1 + (b-a*tan(theta)-d*tan(phi))*0.75 + L_2
    d_new_path_d_theta = new_path.diff(theta)
    optimal_theta = solve(d_new_path_d_theta, theta)
    optimal_theta = optimal_theta[0]
    
    #solve for phi
    phi = Symbol('phi')
    theta = 0 #temporary
    L_1 = a/cos(theta)
    L_2 = d/cos(phi)
    new_path = L_1 + (b-a*tan(theta)-d*tan(phi))*0.75 + L_2
    d_new_path_d_phi = new_path.diff(phi)
    optimal_phi = solve(d_new_path_d_phi, phi)
    optimal_phi = optimal_phi[0]
    
    #The code below shows that the trigonometry checks out. 
    X = a*tan(optimal_theta)
    Y = d*tan(optimal_phi)
    Check = X + Y + b-a*tan(optimal_theta)-d*tan(optimal_phi)

    new_path = (a/cos(optimal_theta)) + (b-a*tan(optimal_theta)-d*tan(optimal_phi))*0.75 + (d/cos(optimal_phi))
    #new_path_consumption = new_path * f_c

    #Finally, the location of the joining and leaving point:
        
        
        
    return mp1, mp2, a, b, d, original_path, optimal_theta, optimal_phi, X, Y, Check, b, new_path
    
    
    
    
    
print(calc_distance(agent1, agent2))
        
print(calc_middle_point(agent1, agent2))
    
print(calculate_new_joining_point(agent1, agent2, destination1, destination2))









