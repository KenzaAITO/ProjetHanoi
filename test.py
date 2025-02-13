
# Importing the Image class from the vision module in the BlocVision package
import BlocRobot.InitPos as inititalisation
from BlocVision.vision import Image


def test_image():
    init = Image()
    init.initialize_game()

def test_robot_control():
    init = inititalisation.Robot()
    init.init()

if __name__ == "__main__":
    test_robot_control()