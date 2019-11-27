##############################################################
#   Libraries
##############################################################
import os
# os.chdir("lab8/")
import sys
import subprocess

from lab8 import *
from lab7_3 import *

##############################################################
#   Variable Definition
##############################################################


##############################################################
#   Function Prototype
##############################################################


##############################################################
#   Function Prototype
##############################################################
def test_api():
    try:
        wd = os.getcwd()
        # subprocess.call("cd " + wd)
        print("Running with all data")
        print("BlackRedTree Run Time:")
        subprocess.check_call(['python3', 'lab8.py', 'a'], cwd=wd)
        print("OneWayBinaryTree Run Time:")
        subprocess.check_call(['python3', 'lab7_3.py', 'a'], cwd=wd)
        print()
        
        print("Running with all data but random")
        print("BlackRedTree Run Time:")
        subprocess.check_call(['python3', 'lab8.py', 'rda'], cwd=wd)
        print("OneWayBinaryTree Run Time:")
        subprocess.check_call(['python3', 'lab7_3.py', 'rda'], cwd=wd)
    except OSError:
        print("Something went wrong")

##############################################################
#   Main Function
##############################################################
def main():
    print("Hello World!")
    test_api()


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    main()