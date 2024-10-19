import sys
import os

# Ajouter le chemin du dossier contenant DobotDllType.py
sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))

import BlocVision.vision as vision
import BlocRobot.InitPos as init

def main():
    intialisation = init.Robot()
    intialisation.init()
    print("Program Start:")


if __name__ == "__main__":
    main()
    