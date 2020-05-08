from collections import deque


# Convert vector to integer
def vec_to_int(v):
    return (int(v.x), int(v.y))


# Heuristic / rule of thumb using Manhattan Distance
def heuristic(node1, node2):
    # Distance in straight line between the two nodes
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)


# Breadth first search algorithm, looping through everything from start point to edge of map
def breadth_first_search(graph, start):
    frontier = deque()
    frontier.append(start)
    path = {}
    path[vec_to_int(start)] = None

    while len(frontier) > 0:
        current = frontier.popleft()
        for next in graph.find_neighbors(current):
            if vec_to_int(next) not in path:
                frontier.append(next)
                path[vec_to_int(next)] = current - next
    return path


# A* Pathfinding algorithm
def a_star(inputs):
    return inputs