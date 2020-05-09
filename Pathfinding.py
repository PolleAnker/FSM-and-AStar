import pygame as pg
from collections import deque
import heapq                # Like a queue, but all items have a priority and is ordered by it, highest priority first
vec = pg.math.Vector2


class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))    # When something is added to heapq, gives priority / cost, and node

    def get(self):
        return heapq.heappop(self.nodes)[1]         # Get the highest priority node in heapq

    def empty(self):
        return len(self.nodes) == 0                 # Return true if the queue is empty / done with searching


# Convert vector to integer
def vec_to_int(v):
    return int(v.x), int(v.y)


# Heuristic / rule of thumb using Manhattan Distance
def heuristic(node1, node2):
    # Distance in straight line between the two nodes
    return (abs(node1.x - node2.x) + abs(node1.y - node2.y)) * 10 # multiply by 10 to keep in line with cost magnitudes


# Breadth first search algorithm, searching via breadth first from start to goal points
def breadth_first_search(graph, start, goal):
    frontier = deque()                  # Frontier is a queue structure
    frontier.append(start)              # Add start to the frontier to begin with
    path = {}                           # Path dictionary to hold tuple nodes (x,y)
    path[vec_to_int(start)] = None      # At start you came from nowhere, eg. no path

    while len(frontier) > 0:
        current = frontier.popleft()                        # Current is the next one in the queue
        if current == goal:                                 # If we're at the goal, stop
            break
        for next in graph.find_neighbors(current):          # For every neighbor
            if vec_to_int(next) not in path:                # If the next node / neighbor isn't in the path / visited
                frontier.append(next)                       # Add whatever the next one is to the frontier
                path[vec_to_int(next)] = current - next     # Direction vector - pointing from next to the current one
    return path


# Dijkstra search algorithm
def dijkstra_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(vec_to_int(start), 0)  # Free start move :)
    path = {}                           # Keep track of where moves were done
    cost = {}                           # Cost of moving to squares as looked at
    path[vec_to_int(start)] = None
    cost[vec_to_int(start)] = 0

    while not frontier.empty():
        current = frontier.get()        # Get the lowest cost first on the frontier
        if current == goal:             # If this node is the goal, stop
            break
        for next in graph.find_neighbors(vec(current)):  # Look through neighbors
            next = vec_to_int(next)
            next_cost = cost[current] + graph.cost(current, next)  # Cost = current move cost + moving to next node cost
            if next not in cost or next_cost < cost[next]:         # If it's not in cost dictionary, or a lower cost
                cost[next] = next_cost                             # it should be looked at
                priority = next_cost
                frontier.put(next, priority)
                path[next] = vec(current) - vec(next)
    return path


# A* Pathfinding algorithm
def a_star(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(vec_to_int(start), 0)  # Free start move :)
    path = {}  # Keep track of where moves were done
    cost = {}  # Cost of moving to squares as looked at
    path[vec_to_int(start)] = None
    cost[vec_to_int(start)] = 0

    while not frontier.empty():
        current = frontier.get()  # Get the lowest cost first on the frontier
        if current == goal:  # If this node is the goal, stop
            break
        for next in graph.find_neighbors(vec(current)):  # Look through neighbors
            next = vec_to_int(next)
            next_cost = cost[current] + graph.cost(current, next)  # Cost = current move cost + moving to next node cost
            if next not in cost or next_cost < cost[next]:  # If it's not in cost dictionary, or a lower cost
                cost[next] = next_cost  # it should be looked at
                priority = next_cost + heuristic(goal, vec(next))   # Prioritise based on movement cost *and* distance
                frontier.put(next, priority)
                path[next] = vec(current) - vec(next)
    return path

