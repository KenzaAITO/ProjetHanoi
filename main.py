
import sys
import os


import BlocVision.vision as vision
import BlocRobot.InitPos as init

def main():
    intialisation = init.Robot()
    intialisation.init()
    print("Program Start:")

    
if __name__ == "__main__":
    main()
    