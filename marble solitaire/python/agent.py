from env import HeapQueue,State,move_east,move_north,move_south,move_west,dfs_board,bfs_board,bfs_goal,init_board,dfs_goal,legend,count_pegs
import time
class Agent:
    def __init__(self) -> None:
        pass

    def get_successors(self,state):
        children, moves = [], []
        count = 0
        isolated = 0
        for cell in range(0, len(state.board)):
            if state.board[cell] == 1:
                moveN = move_north(state, cell)
                moveS = move_south(state, cell)
                moveW = move_west(state, cell)
                moveE = move_east(state, cell)
                moves.append(moveN)
                moves.append(moveS)
                moves.append(moveW)
                moves.append(moveE)
                if moveN is None and moveS is None and moveE is None and moveW is None:
                    isolated += 1
        for move in moves:
            if move:
                children.append(move)
                count += 1
        state.children = count
        state.isolated = isolated
        return children

    def bfs(self,problem):
        queue, closed = [], set()
        queue.append(problem)
        while queue:
            state = queue.pop()
            if state not in closed:
                closed.add(state)
                if state.is_goal():
                    return state
                for newState in self.get_successors(state):
                    queue.insert(0, newState)
        return None


    '''
    Some ideas for heuristics:
        1. Number of successor nodes
        2. Number of isolated peg's
        3. Less peg's = better
        4. Sum of distances from center
        5. Distance from goal board
        6. Distance between parent and child state
    '''


    # Always prioritize greatest branch
    def heuristic1(self,goal, state):
        return -len(self.get_successors(state))


    # Always prioritize least isolated
    def heuristic2(self,goal, state):
        return state.get_isolated()


    def aStar(self,problem, heuristic):
        hq, origin, cost = HeapQueue(), {}, {}
        hq.put(problem, 0)
        origin[problem], cost[problem] = None, 0

        while not hq.empty():
            state = hq.get()
            if state.is_goal():
                return state
            for child in self.get_successors(state):
                new_cost = cost[state] + state.cost(child)
                if child not in cost or new_cost < cost[child]:
                    cost[child] = new_cost
                    priority = heuristic(state.goal, child) + new_cost
                    hq.put(child, priority)
                    origin[child] = state
                    child.parent = state
        return None


    def print_solution(self,solution):
        if not solution:
            print('No solution found')
        else:
            print('Solution found: ')
            path = [solution]
            parent = solution.parent
            while parent:
                path.append(parent)
                parent = parent.parent
            for t in range(len(path)):
                state = path[len(path) - t - 1]
                print('Move: %i' % (t+1))
                print(state)


    def bfs_solution(self,):
        print('[===============================BFS Solution===============================]')
        sTime = time.time()
        game = State(bfs_board, bfs_goal, 7, 7, count_pegs(bfs_board))
        print(game)
        solution = self.bfs(game)
        eTime = time.time()
        self.print_solution(solution)
        print('Total Time: approx. %s sec \n' % str(eTime - sTime))




    def astar_h1_solution(self,):
        print('[===============================A* Heuristic1 Solution===============================]')
        sTime = time.time()
        game = State(bfs_board, dfs_goal, 7, 7, count_pegs(dfs_board))
        print(game)
        solution = self.aStar(game, self.heuristic1)
        eTime = time.time()
        self.print_solution(solution)
        print('Total Time: approx. %s sec \n' % str(eTime - sTime))


    def astar_h2_solution(self,):
        print('[===============================A* Heuristic2 Solution===============================]')
        sTime = time.time()
        game = State(bfs_board, dfs_goal, 7, 7, count_pegs(dfs_board))
        print(game)
        solution = self.aStar(game, self.heuristic2)
        eTime = time.time()
        self.print_solution(solution)
        print('Total Time: approx. %s sec \n' % str(eTime - sTime))


   
