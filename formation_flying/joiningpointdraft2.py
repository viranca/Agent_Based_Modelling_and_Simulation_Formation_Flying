# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 02:22:52 2020

@author: viran
"""

   from sympy import Symbol, pi, tan, atan, sin, cos, solveset, S

    def calc_distance(p1, p2):
        # p1 = tuple(p1)
        # p2 = tuple(p2)
        dist = (((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** 0.5)
        return dist
    
    def calc_middle_point(a, b):
        return [0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1])]


    def calculate_new_joining_point(self, target_agent):
        #for clarification on variables visit: https://app.lucidchart.com/invitations/accept/dd1c3d4b-d382-4365-884e-a81602c4a48c
        mp1 = calc_middle_point(self.pos, target_agent.pos)
        mp2 = calc_middle_point(self.destination, target_agent.destination)
        a = calc_distance(self.pos, mp1)
        b = calc_distance(mp1, mp2)
        d = calc_distance(self.destination, mp2)
        original_path = a + b + d
    
        #trigonometry flights
        v = abs(abs(self.pos[0]) - abs(mp1[0]))  
        u = abs(abs(self.pos[1]) - abs(mp1[1]))
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
        s = abs(abs(self.destination[0]) - abs(mp2[0]))         
        t = abs(abs(self.destination[1]) - abs(mp2[1])) 
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
        optimal_theta = float(str(optimal_theta.args[0])[30:46])*0.5
    
        #solve for phi
        ##Trigonometry to obtain the flight path equations
        ###Leaving point
        phi = Symbol('phi')
        theta = 0 #temporary
        mu = 90*(pi/180) - psi + rho
        sigma = 180*(pi/180) - phi - mu 
        L_2 = (d/sin(sigma)) * sin(mu)
        new_path = (b-a*tan(theta)-d*tan(phi))*0.75 + L_2
        d_new_path_d_phi = new_path.diff(phi)
        optimal_phi = solveset(d_new_path_d_phi)
        optimal_phi = float(str(optimal_phi.args[0])[30:46])*0.5
    
        new_path = (a/sin(180*(pi/180) - optimal_theta - delta)) * sin(delta) + (b-a*tan(optimal_theta)-d*tan(optimal_phi))*0.75 + (d/sin(180*(pi/180) - optimal_phi - mu )) * sin(mu)
        # #new_path_consumption = new_path * f_c
    
        #Finally, the location of the joining and leaving point:
        ##Joining point    
        joining_point = []
        X = ((a/sin(180*(pi/180) - optimal_theta - delta))) * sin(optimal_theta)
        m = X * cos(rho)
        n = X * sin(rho)
        joining_point.append(mp1[0] + m)
        joining_point.append(mp1[1] + n)  
        ##Leaving point
        Y = (d/sin(180*(pi/180) - optimal_phi - mu)) * sin(optimal_phi)
        Y_x = Y * cos(rho)
        Y_y = Y * sin(rho)
        leaving_point = []
        leaving_point.append(mp2[0] + Y_x)
        leaving_point.append(mp2[1] + Y_y)    
        
        
        return original_path , new_path, joining_point, leaving_point   

print(calculate_new_joining_point(agent1, agent2, destination1, destination2)[3])