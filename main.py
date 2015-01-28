
##
## This project is for prototype design of
## "Logistics" a trunk transportation game
##

## Game
## City
## Road
## 
## Truck
## Cargo

## Python's PEP8 style

## Please use Lucida Console for a correct table view

from Display import Display
from GameEngine import GameEngine
import logging

def init_logger():
    global logger

    logger = logging.getLogger('demo_truck')
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(
        logging.Formatter('%(asctime)s-%(levelname)s %(message)s'))

    logger.addHandler(handler)


init_logger()


display = Display()

engine = GameEngine(display)
engine.initialize()
engine.run()

display.wait_anykey()
display.destroy()
