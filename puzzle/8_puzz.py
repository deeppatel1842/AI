
from copy import deepcopy


dir = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
END = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]



def print_puzzle(array):
    
    for a in range(len(array)):
        for i in array[a]:
            if i == 0:
                print(end=' ')
            else:
                print(i, end=' ')
        
class Node:
    def __init__(self, current_node, previous_node, g, h, direction):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.direction = direction

    def f(self):
        return self.g + self.h


def get_position(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))


def euclidian_Cost(current_state):
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            pos = get_position(END, current_state[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost


def near_node(node):
    listNode = []
    emptyPos = get_position(node.current_node, 0)

    for direction in dir.keys():
        newPos = (emptyPos[0] + dir[direction][0], emptyPos[1] + dir[direction][1])
        if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
            newState = deepcopy(node.current_node)
            newState[emptyPos[0]][emptyPos[1]] = node.current_node[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            listNode += [Node(newState, node.current_node, node.g + 1, euclidian_Cost(newState), direction)]

    return listNode


def best_path_node(openSet):
    firstIter = True

    for node in openSet.values():
        if firstIter or node.f() < bestF:
            firstIter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode


def path(closedSet):
    node = closedSet[str(END)]
    initanch = list()

    while node.direction:
        initanch.append({
            'direction': node.direction,
            'node': node.current_node
        })
        node = closedSet[str(node.previous_node)]
    initanch.append({
        'direction': '',
        'node': node.current_node
    })
    initanch.reverse()

    return initanch


def main(puzzle):
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, euclidian_Cost(puzzle), "")}
    closed_set = {}

    while True:
        test_node = best_path_node(open_set)
        closed_set[str(test_node.current_node)] = test_node

        if test_node.current_node == END:
            return path(closed_set)

        adj_node = near_node(test_node)
        for node in adj_node:
            if str(node.current_node) in closed_set.keys() or str(node.current_node) in open_set.keys() and open_set[
                str(node.current_node)].f() < node.f():
                continue
            open_set[str(node.current_node)] = node

        del open_set[str(test_node.current_node)]


if __name__ == '__main__':
    init = main([[4, 8, 0],
               [6, 1, 5],
               [7, 3, 2]])

    print('total steps : ', len(init) - 1)
    print()
    print( "INPUT")
    for b in init:
        if b['direction'] != '':
            letter = ''
            if b['direction'] == 'U':
                letter = 'UP'
            elif b['direction'] == 'R':
                letter = "RIGHT"
            elif b['direction'] == 'L':
                letter = 'LEFT'
            elif b['direction'] == 'D':
                letter = 'DOWN'
           
        print()
        print(b['node'])

