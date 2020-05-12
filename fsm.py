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

    def attack(self, my_pos, enemy_pos):
        print("I'm gonna kill you!!")
        if pf.manhattan_dist(my_pos, enemy_pos) > 20:
            self.set_state(States.CHASING)

    def chase(self, map, my_pos, enemy_pos):
        # use A* algorithm to move to Player position (get player as target as well)
        print("I'm gonna get you!")
        chase_path = pf.a_star(map, my_pos, enemy_pos)
        # Probably want the movement function here
        if pf.manhattan_dist(my_pos, enemy_pos) > 60:
            self.set_state(States.PATROLLING)
            print("Huh, must've been the wind")
        elif pf.manhattan_dist(my_pos, enemy_pos) < 20:
            self.set_state(States.ATTACKING)
            print("Got you now!")
        return chase_path

    def patrol(self, map, my_position, patrol_goal, enemy_pos):
        # use A* algorithm to calculate path between the two points
        print("*whistling jolly tune*")
        patrol_path = pf.a_star(map, my_position, patrol_goal)
        # Probably want the movement function here
        if pf.manhattan_dist(my_position, enemy_pos) < 60:
            self.set_state(States.CHASING)
        return patrol_path

    def behaviour(self, map, my_position, patrol_goal, enemy_pos):
        if self.get_state() == States.PATROLLING:  # If agent is patrolling, do patrol stuff
            while self.get_state() == States.PATROLLING:
                self.patrol(map, my_position, patrol_goal, enemy_pos)

        elif self.get_state() == States.CHASING:  # If agent is chasing, do chase stuff
            while agent.get_state() == States.CHASING:
                self.chase(map, my_position, enemy_pos)

        elif self.get_state() == States.ATTACKING:  # If agent is attacking, do attack stuff
            while self.get_state() == States.ATTACKING:
                self.attack(my_position, enemy_pos)

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

    # I think this is how we'll be calling it in main.py
    #agent.behaviour(grid, start2, goal2, start)
