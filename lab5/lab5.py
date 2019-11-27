# Course: ECE 3822
# Lab: 5
# Date: 9/23/2019
# Username: kuang
# Name: Kuang Jiang
# Description: Lab5 file
# File Name: lab5.py

##############################################################
#   Libraries
##############################################################
# import datetime


##############################################################
#   Variable Definition
##############################################################


##############################################################
#   Class Definition
##############################################################
# ClockClass Class
# Break and store time input string as intgers
# API Operation     | Description
# ClockClass(time)  | a New clockclass of time, time could be three integers as Military Time or a integer
# str               | Print the input time, a string representation
class ClockClass():
    # Intialize the class
    # ClockClass(hours, minutes=None, seconds=None)
    # Input: hours, minures, seconds as integers
    # Output: None
    def __init__(self, hours, minutes=None, seconds=None):
        # Determine whether it inputs second_from_midnight or three numbers
        # The case of second_from_midnight
        if (minutes is None) and (seconds is None):
            since_midnight = hours
            self.h = since_midnight // (60 * 60)
            self.m = (since_midnight - self.h * 3600) // 60
            self.s = (since_midnight - self.h * 3600 - self.m * 60)
            # Generate self print string
            self.input = str(self.h) + ":" + str(self.m) + ":" + str(self.s)
        # The case of three numbers
        else:
            self.h = hours
            # Check if minutes is initialized
            if minutes is not None:
                self.m = minutes
            else:
                self.m = int(0)
                print("Minutes Not Initialized")
            # Check if seconds is initialized
            if seconds is not None:
                self.s = seconds
            else:
                self.s = int(0)
                print("Seconds not Initialized")
            # Generate self print string
            self.input = str(self.h) + ":" + str(self.m) + ":" + str(self.s)
        
    # Return current string
    def __str__(self):
        return self.input
        

##############################################################
#   Function Prototype
##############################################################
def class_tester():
    # Initial Input time, military
    hour = 20
    minute = 52
    second = 50
    # Set class
    time = ClockClass(hour, minute)
    # Print information of time
    print(time)
    # Obtain intger value of seconds since midnight
    second_to_midnight = hour * 3600 + minute * 60 + second
    # Print seconds since midnight
    time2 = ClockClass(second_to_midnight)
    print(time2)
    
    test_time = ClockClass(20,52,00)
    print(test_time)
    
   

##############################################################
#   Main Function
##############################################################
def main():
    print("Hello World!")
    class_tester()


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    main()
