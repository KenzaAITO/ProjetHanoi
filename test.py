
# Importing the Image class from the vision module in the BlocVision package
from BlocRobot import InitPos
from BlocVision.vision import Image


def test_Image():
    init = Image()
    init.initialize_game()

def test_RobotControl():
    init = InitPos()
    init.Init()

if __name__ == "__main__":
    test_RobotControl()