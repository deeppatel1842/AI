import heapq

class HeapQueue():
    def __init__(self):
        self.elems = []
        self.index = 0

    def put(self, elem, priority):
        heapq.heappush(self.elems, (-priority, self.index, elem))
        self.index += 1

    def get(self):
        return heapq.heappop(self.elems)[2]

    def __contains__(self, key):
        for elem in self.elems:
            if elem[1] == key: return True
        return False

    def empty(self):
        return not self.elems


# 0 = unused, 1 = peg, 2 = empty space
dfs_board = [0, 0, 2, 2, 2, 0, 0,
             0, 2, 2, 2, 2, 1, 0,
             1, 2, 1, 1, 1, 2, 2,
             1, 1, 1, 2, 1, 2, 2,
             1, 1, 2, 2, 1, 2, 2,
             0, 2, 1, 2, 1, 1, 0,
             0, 0, 1, 2, 1, 0, 0]


dfs_goal = [0, 0, 2, 2, 2, 0, 0,
            0, 2, 2, 1, 2, 2, 0,
            2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2,
            0, 2, 2, 2, 2, 2, 0,
            0, 0, 2, 2, 2, 0, 0]

init_board = [0, 0, 1, 1, 1, 0, 0,
              0, 1, 1, 1, 1, 1, 0,
              1, 1, 1, 2, 1, 1, 1,
              1, 1, 1, 1, 1, 1, 1,
              1, 1, 1, 1, 1, 1, 1,
              0, 1, 1, 1, 1, 1, 0,
              0, 0, 1, 1, 1, 0, 0]

bfs_board =  [0, 0, 2, 2, 2, 0, 0,
              0, 2, 2, 2, 2, 1, 0,
              1, 1, 2, 2, 1, 2, 2,
              1, 1, 1, 2, 1, 2, 2,
              1, 2, 2, 1, 1, 2, 2,
              0, 2, 2, 2, 1, 1, 0,
              0, 0, 2, 2, 1, 0, 0]

bfs_goal = [0, 0, 2, 2, 2, 0, 0,
            0, 2, 2, 1, 2, 2, 0,
            2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2,
            0, 2, 2, 2, 2, 2, 0,
            0, 0, 2, 2, 2, 0, 0]

legend = [0 , 1 , 2 , 3 , 4 , 5 , 6 ,
          7 , 8 , 9 , 10, 11, 12, 13,
          14, 15, 16, 17, 18, 19, 20,
          21, 22, 23, 24, 25, 26, 27,
          28, 29, 30, 31, 32, 33, 34,
          35, 36, 37, 38, 39, 40, 41,
          42, 43, 44, 45, 46, 47, 48]


class State():
    def __init__(self, board, goal, xSize, ySize, pegs):
        self.board = board
        self.goal = goal
        self.xSize = xSize
        self.ySize = ySize
        self.children = 0
        self.pegs = pegs
        self.isolated = 0
        self.parent = None
        if self.parent is not None:
            self.pegs = pegs - 1
            self.isolated = self.parent.isolated

    def is_goal(self):
        return self.board == self.goal

    # moves element at x1, y1 into x2, y2
    def move(self, x1, y1, x2, y2):
        # y = index / width. x = index % width;
        # cell = y * xSize  + x
        if not self.is_cell_valid(x1, y1) or not self.is_cell_valid(x2, y2):
            return None
        else:
            c1 = y1 * self.xSize + x1
            c2 = y2 * self.xSize + x2
            tmp = self.board[c2]
            self.board[c2] = self.board[c1]
            self.board[c1] = 2
            return tmp

    def remove(self, x, y):
        if not self.is_cell_valid(x, y):
            return None
        else:
            c = y * self.xSize + x
            tmp = self.board[c]
            self.board[c] = 2
            self.pegs -= 1
            return tmp

    def is_cell_valid(self, x, y):
        return (x < self.xSize and x >= 0) and (y < self.ySize and y >= 0)

    def get_isolated(self):
        return self.isolated

    def is_valid(self):
        self.todo = False

    def cost(self, state):
        return 1

    def __str__(self):
        X, Y = self.xSize, self.ySize
        out = ''
        for i in range(0, len(self.board)):
            s = ''
            if i % X == 0 and i != 0:
                out += '\n'
            if self.board[i] == 2:
                s += 'O'
            elif self.board[i] == 0:
                s += '-'
            elif self.board[i] == 1:
                s += '*'
            out += s
        return out

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(tuple(self.board))


def count_pegs(board):
    count = 0
    for peg in board:
        if peg == 1: count += 1
    return count


def move_north(state, cell):
    newState = State(list(state.board), state.goal, state.xSize, state.ySize, state.pegs)
    y = int(cell / state.xSize)
    x = cell % state.xSize

    # check if target cell is valid
    if not newState.is_cell_valid(x, y-2):
        return None
    else:
        newCell = (y-2) * state.xSize + x
        btwCell = (y-1) * state.xSize + x
        if newState.board[newCell] != 2 or newState.board[btwCell] != 1:
            return None
        else:
            newState.remove(x, y-1)
            newState.move(x, y, x, y-2)
            newState.parent = state
            return newState


def move_south(state, cell):
    newState = State(list(state.board), state.goal, state.xSize, state.ySize, state.pegs)
    y = int(cell / state.xSize)
    x = cell % state.xSize

    # check if target cell is valid
    if not newState.is_cell_valid(x, y+2):
        return None
    else:
        newCell = (y+2) * state.xSize + x
        btwCell = (y+1) * state.xSize + x
        if newState.board[newCell] != 2 or newState.board[btwCell] != 1:
            return None
        else:
            newState.remove(x, y+1)
            newState.move(x, y, x, y+2)
            newState.parent = state
            return newState


def move_east(state, cell):
    newState = State(list(state.board), state.goal, state.xSize, state.ySize, state.pegs)
    y = int(cell / state.xSize)
    x = cell % state.xSize

    # check if target cell is valid
    if not newState.is_cell_valid(x+2, y):
        return None
    else:
        newCell = y * state.xSize + (x+2)
        btwCell = y * state.xSize + (x+1)
        if newState.board[newCell] != 2 or newState.board[btwCell] != 1:
            return None
        else:
            newState.remove(x+1, y)
            newState.move(x, y, x+2, y)
            newState.parent = state
            return newState


def move_west(state, cell):
    newState = State(list(state.board), state.goal, state.xSize, state.ySize, state.pegs)
    y = int(cell / state.xSize)
    x = cell % state.xSize

    # check if target cell is valid
    if not newState.is_cell_valid(x-2, y):
        return None
    else:
        newCell = y * state.xSize + (x-2)
        btwCell = y * state.xSize + (x-1)
        if newState.board[newCell] != 2 or newState.board[btwCell] != 1:
            return None
        else:
            newState.remove(x-1, y)
            newState.move(x, y, x-2, y)
            newState.parent = state
            return newState
