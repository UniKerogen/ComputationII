# Course: ECE 3822
# Lab: 2
# Date: 9/4/2019
# Username: kuang
# Name: Kuang Jiang
# Description: Lab2 file
# File Name: Lab2.py

##############################################################
#   Libraries
##############################################################
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import time


##############################################################
#   Variable Definition
##############################################################


##############################################################
#   Function Prototype
##############################################################
##############################################################
# Function Chaos for lab 2 theory
# chaos()
# Input: None
# Output: None
def chaos():
    # print("Hello World!")
    x = 0.01 # Initial Population
    
    # Question 1 - population stailize, aka, x=rx(1-x) where x=1-1/r
    result = []
    step = 1000
    for idx in range(1, step):
        r = 10 / step * idx
        result.append(sim(x, r, 1000))
    print("Question 1 Computed")
    
    # Question 2 - r in range of 3.5, 3.8, 5
    r = [3.5, 3.8, 5]
    result2 = []
    t = 100
    t1 = np.linspace(0, t)
    for item in r:
        result2.append(sim2(x, item, t))
    print("")
    print("These graphs show the change of population as time going by")
    print("If the population reaches 0, it means that it has all died")
    print("Otherwise, these graphs will provide a visiual represent of the relationship between time and population")
    # Explaination of the difference between graphs
    print("At r = 3.5 & 3.8, both figures indicates that it is in a continuous increase and decrease memonet")
    print(" This suggests that the system is still looking for the stable point")
    print("At r = 5, the figure shows that the population decreases to 0")
    print(" This suggests that it has all died")
    print("Question 2 Computed")


# Simulation for with x, r, t
# sim(x, r, t)
# Input: x, r, t are the initial population, repop rate, and time
# Output: Result of calculation
def sim(x, r, t):
    last_value = 0.0
    for ts in range(1, t):
        last_value = x
        x = r * x * (1 - x)
        # Check for stablization
        if x == last_value and x == 1 - 1/r:
            print("It stablized at", r, "with population of", x)
            return last_value
        # End of loop
        if ts == t:
            print("No Stable Result Found with ", r)
            return x


# Simulation for Population x, with repopulation rate & time for plot purose
# sim2(x, r, t)
# Input: x, r, t are the initial population, repop rate, and time
# Output: Result of calculation and Generated Plot
def sim2(x, r, t):
    xr1 = []
    xr2 = []
    for ts in range(1, t):
        xr1.append(ts)
        x = r * x * (1 - x)
        if x < 0:
            x = 0
        xr2.append(x)
    # Generate Plot
    plt.plot(np.asarray(xr1), np.asarray(xr2))
    title = "Population with Repop Rate at "
    title = title.__add__(str(r))
    plt.title(title)
    plt.xlabel("time")
    plt.ylabel("Population")
    save = title.__add__(".png")
    plt.savefig(save)
    plt.close()
    return xr1, xr2
    

##############################################################
#   Main Function
##############################################################
def main():
    print("Hello World!")
    chaos()


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    main()
