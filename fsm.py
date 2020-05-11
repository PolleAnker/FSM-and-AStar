from enum import Enum
from time import sleep
import random
import Pathfinding as pf


class States(Enum):
    # All Enum states needs a unique value
    PATROLLING = 0
    CHASING = 1
    ATTACKING = 2


class Agent:
    def __init__(self):
        self.__state = States.PATROLLING

    def set_state(self, state):
        self.__state = state

    def get_state(self):
        return self.__state

    def attack(self, target):
        # while in attack range of player execute an attack function
        return target

    def chase(self, target):
        # use A* algorithm to move to Player position (get player as target as well)
        return target

    def patrol(self, map, point1, point2):
        # use A* algorithm to calculate path between the two points
        patrol_path = pf.a_star(map, point1, point2)
        print(patrol_path)
        # use move function (when written) to move between the points - reverse move when end is reached


agent = Agent()
while True:
    currentState = agent.get_state()
    print(currentState)
    sleep(1)
    changeTo = random.randrange(0, 3)
    if changeTo == 0:
        agent.set_state(States.PATROLLING)
    if changeTo == 1:
        agent.set_state(States.CHASING)
    if changeTo == 2:
        agent.set_state(States.ATTACKING)

# The commented stuff below is the actual logic for the Agent
'''
This is the actual logic that we should use when the A* algorithm is also written
agent = Agent() # Create instance of agent

if agent.get_state() == States.PATROLLING:    # If agent is patrolling, do patrol stuff
    while agent.get_state() == States.PATROLLING:
        agent.patrol()
        # if a player gets in chase range:
        #   agent.set_state(States.CHASING)
        
elif agent.get_state() == States.CHASING:     # If agent is chasing, do chase stuff
    while agent.get_state() == States.CHASING:
        agent.chase()
        # if a player is in attack range:
        #   agent.set_state(States.ATTACKING)
        # if a player is out of chase range:
        #   agent.set_state(States.PATROLLING)
        
elif agent.get_state() == States.ATTACKING:   # If agent is attacking, do attack stuff
    while agent.get_state() == States.ATTACKING:
        agent.attack()
    # if a player is out of attack range:
    #   agent.chase()

'''