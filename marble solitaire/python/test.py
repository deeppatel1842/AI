
import copy
import time
import sys
from collections import deque
import heapq




from agent import Agent

def main():
    agnt = Agent()
    agnt.bfs_solution()
    agnt.dfs_solution()
    agnt.astar_h1_solution()
    agnt.astar_h2_solution()
    
if __name__ == "__main__":
    main()