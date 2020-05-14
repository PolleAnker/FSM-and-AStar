from enum import Enum
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

    def attack(self, my_pos, enemy_pos):
        print("Got you!")

    def chase(self, my_pos, enemy_pos):
        # use A* algorithm to move to Player position (get player as target as well)
        print("I see you! I'm gonna get you!")
        print("Activate super Speed!")
        # Probably want the movement function here
        if pf.manhattan_dist(my_pos, enemy_pos) > 60:
            self.set_state(States.PATROLLING)
            print("Huh, must've been the wind")
        elif pf.manhattan_dist(my_pos, enemy_pos) < 14:
            self.set_state(States.ATTACKING)
            print("Got you now!")

    def patrol(self, my_position, enemy_pos):
        # use A* algorithm to calculate path between the two points
        print("*whistling jolly tune*")
        # Probably want the movement function here
        if pf.manhattan_dist(my_position, enemy_pos) < 60:
            self.set_state(States.CHASING)
