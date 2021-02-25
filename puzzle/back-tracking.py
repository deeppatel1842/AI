# using back-tracking
N = 1000
adj = [[] for i in range(N)]
 
# Function to path complete DFS-traversal
def dfsUtil(u, node,visited, 
            road_used, parent, it):
    c = 0
 
    # Check if all th node is visited 
    # or not and count unvisited nodes
    for i in range(node):
        if (visited[i]):
            c += 1
 
    # If all the node is visited return
    if (c == node):
        return
 
    # Mark not visited node as visited
    visited[u] = True
 
    # Track the current edge
    road_used.append([parent, u])
 
    # Print the node
    print(u, end = " ")
 
    # Check for not visited node
    # and proceed with it.
    for x in adj[u]:
 
        # Call the DFs function 
        # if not visited
        if (not visited[x]):
            dfsUtil(x, node, visited, 
                    road_used, u, it + 1)
 
    # Backtrack through the last
    # visited nodes
    for y in road_used:
        if (y[1] == u):
            dfsUtil(y[0], node, visited,
                    road_used, u, it + 1)
 
# Function to call the DFS function
# which prints the DFS-travesal stepwise
def dfs(node):
 
    # Create a array of visited ndoe
    visited = [False for i in range(node)]
 
    # Vector to track last visited road
    road_used = []
 
    # Initialize all the node with false
    for i in range(node):
        visited[i] = False
 
    # Call the function
    dfsUtil(0, node, visited, 
            road_used, -1, 0)
             
# Function to insert edges in Graph
def insertEdge(u, v):
     
    adj[u].append(v)
    adj[v].append(u)
 
# Driver Code
if __name__ == '__main__':
     
    # Number of nodes and edges in the graph
    node = 11
    edge = 13
 
    # Function call to create the graph
    insertEdge(0, 1)
    insertEdge(0, 2)
    insertEdge(1, 5)
    insertEdge(1, 6)
    insertEdge(2, 4)
    insertEdge(2, 9)
    insertEdge(6, 7)
    insertEdge(6, 8)
    insertEdge(7, 8)
    insertEdge(2, 3)
    insertEdge(3, 9)
    insertEdge(3, 10)
    insertEdge(9, 10)
 
    # Call the function to print
    dfs(node)
