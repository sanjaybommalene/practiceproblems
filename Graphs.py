"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

# Graph - Adjacency List
from collections import defaultdict, deque
import heapq

class Graph:
    def __init__(self, directed=False):
        self.adj_list = defaultdict(list)
        self.directed = directed
    
    def add_edge(self, u, v, weight=1):
        self.adj_list[u].append((v, weight))
        if not self.directed:
            self.adj_list[v].append((u, weight))
    
    # 1. BFS (Returns visited nodes in order)
    def bfs(self, start):
        res = []
        queue = deque([start])
        visited = set([start])
        
        while queue:
            node = queue.popleft()
            res.append(node)
            
            for neighbor, _ in self.adj_list[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return res
    
    # 2. DFS (Returns visited nodes in order)
    def dfs(self, start):
        res = []
        self._dfs_helper(start, set(), res)
        return res
    
    def _dfs_helper(self, node, visited, res):
        res.append(node)
        visited.add(node)
        
        for neighbor, _ in self.adj_list[node]:
            if neighbor not in visited:
                self._dfs_helper(neighbor, visited, res)
    
    # 3. Dijkstra's Algorithm (Returns shortest distances)
    def dijkstra(self, start):
        distances = {node: float('inf') for node in self.adj_list}
        distances[start] = 0
        heap = [(0, start)]
        
        while heap:
            current_dist, node = heapq.heappop(heap)
            
            if current_dist > distances[node]:
                continue
                
            for neighbor, weight in self.adj_list[node]:
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(heap, (distance, neighbor))
        
        return distances

# Example Usage
# g = Graph(directed=True)
# g.add_edge('A', 'B', 4)
# g.add_edge('A', 'C', 2)
# g.add_edge('B', 'C', 5)
# g.add_edge('B', 'D', 10)
# g.add_edge('C', 'D', 3)
# g.add_edge('D', 'E', 7)
# g.add_edge('E', 'A', 3)

# print("BFS Traversal:", g.bfs('A'))
# print("DFS Traversal:", g.dfs('A'))
# print("Dijkstra's Shortest Paths from 'A':", g.dijkstra('A'))



########################################################
### 1. Clone Graph (Leetcode 133)
########################################################

# **Problem Statement**:  
# Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph.

# **Example**:

# Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
# Output: [[2,4],[1,3],[2,4],[1,3]]
# Explanation:
# 1 -> 2 & 4
# 2 -> 1 & 3
# 3 -> 2 & 4
# 4 -> 1 & 3
# ```

# **Algorithm**:  
# 1. Use **DFS** to traverse the original graph.
# 2. Maintain a hash map to store `original_node -> cloned_node` mappings.
# 3. For each node, create its clone and recursively clone all neighbors.

# **Solution**:

class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def cloneGraph(node):
    if not node:
        return None
    
    # Hash map to store original node to its clone
    visited = {}
    
    def dfs(node):
        # If node already cloned, return its clone
        if node in visited:
            return visited[node]
        
        # Create clone of current node
        clone = Node(node.val)
        visited[node] = clone
        
        # Clone all neighbors recursively
        for neighbor in node.neighbors:
            clone.neighbors.append(dfs(neighbor))
        
        return clone
    
    return dfs(node)
# """
# Time Complexity: O(V + E) - Visits each node and edge once
# Space Complexity: O(V) - For the hash map and recursion stack
# """


########################################################
# Graph Valid Tree / Detech Cycles Undirected Graphs
########################################################
# Approach:
# Union-Find to detect cycles.
# Ensure all nodes are connected (edges == n-1).
# n = 5 and edges = [[0,1], [1,2], [2,3], [1,4]]
def validTree(n, edges):
    if len(edges) != n - 1:
        return False
    
    parent = [i for i in range(n)]
    
    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u
    
    for u, v in edges:
        pu, pv = find(u), find(v)
        if pu == pv:
            return False
        parent[pv] = pu # Performs Union p[1]=0
    
    return True
# Time: O(N α(N))



########################################################
# Detect Cycles in Graph - Directed O(V + E), O(V) (recursion stack)
########################################################
# Represent the Graph using an adjacency list.
# Track Node States:
#   0 = Unvisited
#   1 = Visiting (in current DFS stack)
#   2 = Visited (fully processed)
# Perform DFS:
#   If a node is encountered while it's still 1 (Visiting), a cycle exists.
#   After processing all neighbors, mark the node as 2 (Visited).
# DFS
def has_cycle(num_nodes, edges):
    # Build adjacency list
    adj = [[] for _ in range(num_nodes)]
    for u, v in edges:
        adj[u].append(v)
    
    visited = [0] * num_nodes  # 0=unvisited, 1=visiting, 2=visited

    def dfs(u):
        if visited[u] == 1:  # Cycle detected (back edge)
            return True
        if visited[u] == 2:  # Already processed
            return False
        
        visited[u] = 1  # Mark as visiting
        for v in adj[u]:
            if dfs(v):
                return True
        visited[u] = 2  # Mark as visited
        return False

    for i in range(num_nodes):
        if visited[i] == 0 and dfs(i):
            return True  # Cycle found
    return False  # No cycle
# edges = [[0, 1], [1, 2], [2, 0]]  # Contains a cycle (0 → 1 → 2 → 0)
# print(has_cycle(3, edges))  # Output: True

# BFS/ Kahn's Algo O(V + E)	O(V) (queue)	
from collections import defaultdict, deque

def detect_cycle(V, edges):
    # Create adjacency list
    graph = defaultdict(list)
    for src, dest in edges:
        graph[src].append(dest)
    
    # Step 1: Calculate in-degrees
    in_degree = [0] * V
    for u in range(V):
        for v in graph[u]:
            in_degree[v] += 1
    
    # Step 2: Initialize queue with nodes of in-degree 0
    queue = deque()
    for i in range(V):
        if in_degree[i] == 0:
            queue.append(i)
    
    # Step 3: Process nodes
    count = 0
    while queue:
        node = queue.popleft()
        count += 1
        # Reduce in-degree for neighbors
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Step 4: Check for cycle
    return "No cycle" if count == V else "Cycle exists"

# Example usage
# V = 4  # Number of vertices
# edges = [(0, 1), (1, 2), (2, 3), (3, 1)]  # Graph with a cycle
# print(detect_cycle(V, edges))  # Output: Cycle exists

# V = 4
# edges = [(0, 1), (1, 2), (2, 3)]  # Acyclic graph
# print(detect_cycle(V, edges))  # Output: No cycle

# Example Usage (Cycle Exists)
# g = Graph()
# g.add_edge(0, 1)
# g.add_edge(1, 2)
# g.add_edge(2, 0)  # Creates a cycle: 0 → 1 → 2 → 0
# print("Cycle detected (BFS)?", g.has_cycle_bfs())  # Output: True

# SKIP: Duplicate to above valid tree
def has_cycle_undirected(num_nodes, edges):
    adj = [[] for _ in range(num_nodes)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)  # Undirected graph
    
    visited = [False] * num_nodes

    def dfs(u, parent):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                if dfs(v, u):
                    return True
            elif v != parent:  # Cycle detected
                return True
        return False

    for i in range(num_nodes):
        if not visited[i] and dfs(i, -1):
            return True
    return False

########################################################
# Check if Graph is connected DFS
########################################################
def is_graph_connected(n, edges):
    if n == 0:
        return True  # empty graph is trivially connected

    # Build the adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Use DFS to check connectivity
    visited = set()

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    # Start DFS from node 0
    dfs(0)

    # Check if all nodes are visited
    return len(visited) == n
# Time: O(N + E) – where N is number of nodes and E is number of edges.
# Space: O(N + E) – adjacency list and visited set.

# BFS
from collections import deque
def is_graph_connected_bfs(n, edges):
    if n == 0:
        return True  # trivially connected if no nodes

    # Build the adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    queue = deque()

    # Start BFS from node 0
    queue.append(0)
    visited.add(0)

    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    # Check if all nodes are visited
    return len(visited) == n

########################################################
# Course Schedule I
########################################################
# There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. 
# You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.
# For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
# Return true if you can finish all courses. Otherwise, return false.
# Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
# Output: false
# Explanation: There are a total of 2 courses to take. 
# To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.
def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:

    pre = [[] for _ in range(numCourses)]

    for course, p in prerequisites:
        pre[course].append(p)
    
    taken = set()

    def dfs(course):
        if not pre[course]:  # If no prerequisites, the course can be taken
            return True
        
        if course in taken:  # Cycle detected → return False
            return False
        
        taken.add(course)  # Mark the course as being visited

        for p in pre[course]:  # Check all prerequisites recursively
            if not dfs(p):
                return False
        
        pre[course] = []  # Mark course as completed (memorization)
        return True
    
    for course in range(numCourses):
        if not dfs(course):
            return False

    return True

# Kahn's Algorithm - BFS
# Kahn's Algorithm
# Graph:
# 0 → 1 → 3  
# 0 → 2 → 3  
# In-Degree:
# 0: 0, 1: 1, 2: 1, 3: 2
# BFS Traversal (Process Nodes)

# Dequeue a course (u) and add it to the result.
# For each dependent course (v):
# Reduce in_degree[v] by 1 (since u is now taken).
# If in_degree[v] == 0, enqueue v.
def canFinish(numCourses, prerequisites):
    # Step 1: Initialize adjacency list and in-degree array
    adj = [[] for _ in range(numCourses)]  # Adjacency list to represent the graph
    in_degree = [0] * numCourses          # Tracks the number of prerequisites for each course

    # Step 2: Build the graph and in-degree counts
    for a, b in prerequisites:
        adj[b].append(a)    # Course `b` is a prerequisite for course `a` (directed edge b → a)
        in_degree[a] += 1   # Increment in-degree of course `a`

    # Step 3: Initialize a queue with courses having no prerequisites (in-degree = 0)
    q = deque([i for i in range(numCourses) if in_degree[i] == 0])
    courses_taken = 0  # Tracks the number of courses processed

    # Step 4: Process courses using BFS (Kahn's Algorithm for Topological Sort)
    while q:
        u = q.popleft()     # Take a course with no remaining prerequisites
        courses_taken += 1          # Increment the courses_taken of completed courses

        # Step 5: Reduce in-degree of neighbors (courses dependent on `u`)
        for v in adj[u]:
            in_degree[v] -= 1           # Remove the dependency on `u`
            if in_degree[v] == 0:       # If no more prerequisites, add to queue
                q.append(v)

    # Step 6: If all courses were processed, return True (no cycle)
    return courses_taken == numCourses
# Time: O(V + E) (V = numCourses, E = prerequisites)
# Space: O(V + E)

########################################################
# Course Schedule II usign DFS with prequisite
########################################################
# edge b → a means b is a prerequisite for a
# numCourses = 4
# prerequisites = [[1,0], [2,0], [3,1], [3,2]]
# Return course order O(V + E), O(V + E)
# Kahn's Algorithm
def findOrder(numCourses, prerequisites):
    adj = [[] for _ in range(numCourses)]
    in_degree = [0] * numCourses
    
    for a, b in prerequisites:
        adj[b].append(a)
        in_degree[a] += 1
    
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    result = []
    
    while queue:
        u = queue.popleft()
        result.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    return result if len(result) == numCourses else []
# DFS
class Solution:
    def findOrder(numCourses, prerequisites):
        adj = [[] for _ in range(numCourses)]
        for course, prereq in prerequisites:
            adj[course].append(prereq)
        
        visited = [0] * numCourses
        topo_order = []
        
        def dfs(node):
            if visited[node] == 1:
                return False
            if visited[node] == 2:
                return True
            
            visited[node] = 1
            for neighbor in adj[node]:
                if not dfs(neighbor):
                    return False
            
            visited[node] = 2
            topo_order.append(node)
            return True
        
        for course in range(numCourses):
            if not dfs(course):
                return []
        
        return topo_order

########################################################
# Course Schedule III
########################################################
# Given courses with [duration, lastDay], return the maximum number of courses you can take.
# Approach (Greedy + Max-Heap)
# Sort courses by lastDay (earliest deadlines first).
# Use a max-heap to track durations of selected courses.
# If adding a course exceeds its deadline, replace the longest course in the heap.
# Input: courses = [[100,200],[200,1300],[1000,1250],[2000,3200]]
# Output: 3
# Explanation: 
# There are totally 4 courses, but you can take 3 courses at most:
# First, take the 1st course, it costs 100 days so you will finish it on the 100th day, and 
# ready to take the next course on the 101st day.
# Second, take the 3rd course, it costs 1000 days so you will finish it on the 1100th day, and 
# ready to take the next course on the 1101st day. 
# Third, take the 2nd course, it costs 200 days so you will finish it on the 1300th day. 
# The 4th course cannot be taken now, since you will finish it on the 3300th day, which exceeds the closed date.
def scheduleCourse(courses):
    # Sort courses by lastDay (earliest deadline first)
    courses.sort(key=lambda x: x[1])
    max_heap = []  # Stores durations of selected courses (max-heap using negatives)
    time = 0       # Current time
    
    for duration, lastDay in courses:
        if time + duration <= lastDay:
            heapq.heappush(max_heap, -duration)  # Push negative for max-heap
            time += duration
        elif max_heap and -max_heap[0] > duration:
            # Replace the longest course with the current one
            time += duration + heapq.heappop(max_heap)  # Subtract the removed duration
            heapq.heappush(max_heap, -duration)
    
    return len(max_heap)
# Time: O(N log N) (due to sorting and heap operations)
# Space: O(N)

########################################################
# Course Schedule IV
########################################################
# Given numCourses, prerequisites, and queries [u, v], check if u is a prerequisite of v.
# Floyd-Warshall or BFS/DFS to precompute reachability. 
def checkIfPrerequisite(numCourses, prerequisites, queries):
    # Initialize reachability matrix
    reachable = [[False] * numCourses for _ in range(numCourses)]
    for u, v in prerequisites:
        reachable[u][v] = True
    
    # Floyd-Warshall to compute transitive closure
    for k in range(numCourses):
        for i in range(numCourses):
            for j in range(numCourses):
                if reachable[i][k] and reachable[k][j]:
                    reachable[i][j] = True
    
    return [reachable[u][v] for u, v in queries]
# Time: O(N³) (Floyd-Warshall)
# Space: O(N²)
         

########################################################
# Unweighted Graph (Shortest Path using BFS)
########################################################
def bfs_shortest_path(graph, start, goal):
    visited = set()
    queue = deque([[start]])

    if start == goal:
        return [start]

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node not in visited:
            for neighbor in graph[node]:
                new_path = list(path) # Used Traversed path so far 
                new_path.append(neighbor) # Append each neighbour to make new path
                queue.append(new_path)

                if neighbor == goal:
                    return new_path
            visited.add(node)
    return None
# Example graph as adjacency list
graph = defaultdict(list)
graph[0] = [1, 2]
graph[1] = [2]
graph[2] = [3]
graph[3] = [4]
graph[4] = []

print(bfs_shortest_path(graph, 0, 4))  # Output: [0, 2, 3, 4]
# [0]
# [0, 1]
# [0, 2]
# [0, 1, 2]
# [0, 2, 3]
# Traverse
# [0]
# deque([[0, 1]])
# deque([[0, 1], [0, 2]])
# [0, 1]
# deque([[0, 2], [0, 1, 2]])
# [0, 2]
# deque([[0, 1, 2], [0, 2, 3]])
# [0, 1, 2]
# [0, 2, 3]
# deque([[0, 2, 3, 4]])
# [0, 2, 3, 4]

########################################################
# Shortest path of weighted graph using Dijkstra's (Positive  Weights)
########################################################
# Priority Queue (Min-Heap): Selects the next node with the smallest tentative distance.
# Distance Array: Tracks the shortest known distance from the source to each node.
def dijkstra(graph, start):
    heap = [(start, 0)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    while heap:
        current_node, current_distance = heapq.heappop(heap)

        if current_distance > distances[current_node]:
            continue # Skip if a shorter path already exists

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(heap, (neighbor, distance))

    return distances
# Step 2: Process B (Distance = 1)

# Relax neighbors of B:
# B → C: 1 + 2 = 3 (Better than 4(A->C) → Update C).
# B → D: 1 + 5 = 6 (Update D).
# Update Queue: [(C,3), (D,6), (C,4)] (Old C:4 is ignored).
# Visited: {A, B}
# Example weighted graph
# graph = {
#     'A': [('B', 1), ('C', 4)],
#     'B': [('C', 2), ('D', 5)],
#     'C': [('D', 1)],
#     'D': []
# }
# print(dijkstra(graph, 'A'))  # Output: shortest distance from A to every node

########################################################
# Find the cheapest flight from src to dst with at most K stops.
########################################################
# Approach:
# Use Priority Queue (Min-Heap) to track (cost, node, stops_used).
# Relax edges only if stops are within K.
def findCheapestPrice(n, flights, src, dst, K):
    # Build adjacency list
    graph = defaultdict(list)
    for u, v, w in flights:
        graph[u].append((v, w))
    
    # Min-heap: (current_cost, current_city, remaining_stops)
    heap = [(0, src, K + 1)]  # K stops = K+1 edges
    visited = {}  # Tracks (city, remaining_stops) to avoid reprocessing
    
    while heap:
        cost, city, stops = heapq.heappop(heap)
        if city == dst:
            return cost
        if stops <= 0:
            continue
        if (city, stops) in visited and visited[(city, stops)] <= cost:
            continue
        visited[(city, stops)] = cost
        for neighbor, price in graph[city]:
            heapq.heappush(heap, (cost + price, neighbor, stops - 1))
    
    return -1
# Input: n = 3, flights = [[0,1,100],[1,2,100],[0,2,500]], src = 0, dst = 2, K = 1
# Output: 200 (Path: 0 → 1 → 2 with 1 stop)
# Heap: [(0, 0, 2)] (cost=0, city=0, stops left=2).
# Process (0, 0, 2):
# Push (100, 1, 1) (path 0→1) and (500, 2, 1) (path 0→2).
# Process (100, 1, 1):
# Push (200, 2, 0) (path 0→1→2).
# Process (200, 2, 0):
# Destination reached! Return 200.
# Output: 200 ✅
# Time: O(E + V log V) (Dijkstra’s with heap)

########################################################
# Network Delay Time (Dijkstra’s)
########################################################
# You are given a network of n nodes, labeled from 1 to n. You are also given times, a list of travel times as directed edges times[i] = (ui, vi, wi), 
# where ui is the source node, vi is the target node, and wi is the time it takes for a signal to travel from source to target.
# We will send a signal from a given node k. Return the minimum time it takes for all the n nodes to receive the signal. If it is impossible for all the n nodes to receive the signal, return -1.
# Approach:
# Build a weighted adjacency list to represent the graph.
# Use Dijkstra's Algorithm to compute the shortest path from k to all other nodes.
# Track the maximum distance from k to any node. If any node is unreachable, return -1.
def networkDelayTime(times, n, k):
    # Step 1: Build adjacency list
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))
    
    # Step 2: Initialize distance dictionary
    distances = {node: float('inf') for node in range(1, n + 1)}
    distances[k] = 0  # Distance from k to itself is 0
    
    # Step 3: Priority queue (min-heap) to process nodes
    heap = [(0, k)]
    
    while heap:
        current_time, u = heapq.heappop(heap)
        if current_time > distances[u]:
            continue  # Skip if a shorter path already exists
        
        # Step 4: Relax all outgoing edges from u
        for v, w in graph[u]:
            if distances[v] > current_time + w:
                distances[v] = current_time + w
                heapq.heappush(heap, (distances[v], v))
    
    # Step 5: Find the maximum distance
    max_distance = max(distances.values())
    return max_distance if max_distance != float('inf') else -1
# Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
# Output: 2
# Example Usage:
# n = 5
# edges = [[0, 1], [1, 2], [3, 4]]
# print(countComponents(n, edges))  # Output: 2


########################################################
### Min Cost to Connect All Points (Leetcode 1584) ###
########################################################

# **Problem Statement**:  
# Given `n` points on a 2D plane, connect them with minimum total cost where cost = Manhattan distance.
# The cost of connecting two points [xi, yi] and [xj, yj] is the manhattan distance between them: |xi - xj| + |yi - yj|, where |val| denotes the absolute value of val.


# **Example**:
# Input: points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
# Output: 20
# Explanation: 
# Connect [0,0] → [2,2] (cost=4)
# Connect [2,2] → [3,10] (cost=9)
# Connect [2,2] → [5,2] (cost=3)
# Connect [5,2] → [7,0] (cost=4)
# Total cost = 4 + 9 + 3 + 4 = 20
# ```

# Edge Generation: Compute Manhattan distance for all point pairs.
# Kruskal’s Algorithm: Sort edges by cost, use Union-Find to add edges to the MST until n-1 edges are used.

# **Solution**:
def minCostConnectPoints(points):
    n = len(points)
    if n <= 1:
        return 0
    
    # Create parent array for Union-Find
    parent = list(range(n))
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        parent[find(x)] = find(y)
    
    # Generate all edges with Manhattan distance
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            cost = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            edges.append((cost, i, j))
    
    # Sort edges by cost
    edges.sort()
    
    # Kruskal's algorithm
    total_cost = 0
    edges_used = 0
    for cost, u, v in edges:
        if find(u) != find(v):
            union(u, v)
            total_cost += cost
            edges_used += 1
            if edges_used == n - 1:
                break
    
    return total_cost
# """
# Time Complexity: O(N² log N) - For heap operations
# Space Complexity: O(N²) - For storing edges
# """


########################################################
### 6. Connecting Cities With Minimum Cost (Leetcode 1135)
########################################################
# **Problem Statement**:  
# Given `n` cities and connections between them (with costs), return the minimum cost to connect all cities.

# **Example**:
# Input: n = 3, connections = [[1,2,5],[1,3,6],[2,3,1]]
# Output: 6
# Explanation: Use connections [1,2,5] and [2,3,1]
# ```

# **Algorithm** (Kruskal's MST):
# 1. Sort all edges by cost.
# 2. Use Union-Find to connect cities without cycles.
# 3. Add edges until all cities are connected.

# **Solution**:
class Solution:
    def minimumCost(self, n: int, connections: List[List[int]]) -> int:
        parent = [i for i in range(n+1)]
        
        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u
        
        connections.sort(key=lambda x: x[2])
        total_cost = 0
        edges_used = 0
        
        for u, v, cost in connections:
            root_u = find(u)
            root_v = find(v)
            if root_u != root_v:
                parent[root_v] = root_u
                total_cost += cost
                edges_used += 1
                if edges_used == n-1:
                    return total_cost
        
        return -1
# """
# Time Complexity: O(E log E) - Sorting dominates
# Space Complexity: O(N) - For Union-Find
# """


########################################################
# ### Find the City With Smallest Neighbors (Leetcode 1334)
########################################################

# **Problem Statement**:  
# Given `n` cities connected by weighted edges, find the city with the smallest number of reachable cities within a distance threshold.

# **Example**:

# Input: n = 4, edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], distanceThreshold = 4
# Output: 3
# Explanation: City 3 has 1 reachable city (city 2) within distance 4.
# ```

# **Algorithm**:  
# 1. Use **Floyd-Warshall** to compute shortest paths between all pairs.
# 2. For each city, count reachable cities within the threshold.
# 3. Return the city with the smallest count (largest ID if tied).

# **Solution**:

class Solution:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        # Initialize distance matrix
        dist = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for u, v, w in edges:
            dist[u][v] = w
            dist[v][u] = w
        
        # Floyd-Warshall algorithm
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        
        min_cities = n
        result = 0
        for i in range(n):
            count = sum(1 for j in range(n) if i != j and dist[i][j] <= distanceThreshold)
            if count <= min_cities:
                min_cities = count
                result = i
        return result
# """
# Time Complexity: O(V³) - Floyd-Warshall
# Space Complexity: O(V²) - Distance matrix
# """


########################################################
# ### All Paths From Source to Target (Leetcode 797) ###
########################################################
# **Problem Statement**:  
# Given a DAG, return all possible paths from node `0` to node `n-1`.

# **Example**:

# Input: graph = [[1,2],[3],[3],[]]
# Output: [[0,1,3],[0,2,3]]
# Explanation: There are two paths: 0→1→3 and 0→2→3.
# ```

# **Algorithm**:  
# 1. Use **backtracking** to explore all paths.
# 2. Start from node `0` and recursively visit neighbors.
# 3. When reaching node `n-1`, add the current path to results.

# **Solution**:

class Solution:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        n = len(graph)
        paths = []
        
        def backtrack(node, path):
            if node == n-1:
                paths.append(path[:])
                return
            
            for neighbor in graph[node]:
                path.append(neighbor)
                backtrack(neighbor, path)
                path.pop()
        
        backtrack(0, [0])
        return paths
# """
# Time Complexity: O(2^V × V) - Exponential paths in worst case
# Space Complexity: O(V) - For recursion stack
# """


########################################################
# ### 10. Shortest Path in a DAG
########################################################

# **Problem Statement**:  
# Find shortest paths from a source node in a DAG.

# **Example**:

# Input: n = 6, edges = [[0,1,5],[0,2,3],[1,3,6],[2,3,1],[3,4,2],[4,5,4]], src = 0
# Output: [0, 5, 3, 4, 6, 10]
# ```

# **Algorithm** (Topological Sort + Relaxation):
# 1. Perform topological sort.
# 2. Relax edges in topological order.
# Topological Sort: Use Kahn’s algorithm to get nodes in topological order.
# Dynamic Programming: Process each node, updating distances to neighbors.

# **Solution**:

from collections import deque

def shortestPathDAG(n, edges, source):
    # Build adjacency list with weights
    adj = defaultdict(list)
    for u, v, w in edges:
        adj[u].append((v, w))
    
    # Topological sort using Kahn's algorithm
    in_degree = [0] * n
    for u in range(n):
        for v, _ in adj[u]:
            in_degree[v] += 1
    
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    topo_order = []
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for neighbor, _ in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Initialize distances
    dist = [float('inf')] * n
    dist[source] = 0
    
    # Process nodes in topological order
    for u in topo_order:
        if dist[u] != float('inf'):
            for v, w in adj[u]:
                dist[v] = min(dist[v], dist[u] + w)
    
    return dist
# """
# Time Complexity: O(V + E)
# Space Complexity: O(V)
# """


########################################################
### 8. Critical Connections in a Network (Leetcode 1192)
########################################################

# **Problem Statement**:  
# Find all critical connections (bridges) in a network.

# **Example**:

# Input: n = 4, connections = [[0,1],[1,2],[2,0],[1,3]]
# Output: [[1,3]]
# ```

# **Algorithm** (Tarjan's Bridge Finding):
# 1. Track discovery time and low link values.
# 2. A bridge is found where `low[v] > disc[u]`.
# Tarjan’s Algorithm: Assign discovery and low-link times to nodes. An edge (u, v) is a bridge if low[v] > disc[u].
# DFS: Traverse the graph, updating low-link values for back edges and checking for bridges.

# **Solution**:

def criticalConnections(n, connections):
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in connections:
        adj[u].append(v)
        adj[v].append(u)
    
    # Initialize discovery and low-link arrays
    disc = [-1] * n
    low = [-1] * n
    time = [0]
    result = []
    
    def dfs(u, parent):
        # Set discovery and low-link time
        disc[u] = low[u] = time[0]
        time[0] += 1
        
        # Explore neighbors
        for v in adj[u]:
            if v == parent:
                continue
            if disc[v] == -1:  # Unvisited neighbor
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    result.append([u, v])
            else:  # Back edge
                low[u] = min(low[u], disc[v])
    
    # Run DFS from each unvisited node
    for i in range(n):
        if disc[i] == -1:
            dfs(i, -1)
    
    return result
# """
# Time Complexity: O(V + E) - Standard DFS
# Space Complexity: O(V) - For disc/low arrays
# """


########################################################
# Rotting Oranges with BFS
########################################################
from collections import deque
class Solution:
    def bfs(self, grid, q, cnt):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        made, sec = 0, 0
        m, n = len(grid), len(grid[0])

        while q:
            r, c, sec = q.popleft()

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    q.append((nr, nc, sec + 1))
                    grid[nr][nc] = -1
                    made += 1
        
        return sec if made == cnt else -1

    def orangesRotting(self, grid):
        m, n = len(grid), len(grid[0])
        cntFresh = 0
        q = deque()

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:
                    q.append((i, j, 0))
                    grid[i][j] = -1
                elif grid[i][j] == 1:
                    cntFresh += 1

        return self.bfs(grid, q, cntFresh)



########################################################
### 7. Alien Dictionary (Leetcode 269)
########################################################

# **Problem Statement**:  
# Given a sorted dictionary of an alien language, return its character order.

# **Example**:
# Input: words = ["wrt","wrf","er","ett","rftt"]
# Output: "wertf"
# ```

# **Algorithm** (Topological Sort):
# 1. Build a graph from adjacent word comparisons.
# 2. Perform topological sort using Kahn's algorithm (BFS + in-degree count).

# **Solution**:
def alienOrder(words):
    # Build adjacency list and reverse graph for in-degree
    adj = defaultdict(set)
    in_degree = defaultdict(int)
    chars = set(''.join(words))
    
    # Compare adjacent words to build graph
    for w1, w2 in zip(words, words[1:]):
        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                adj[c1].add(c2)
                in_degree[c2] += 1
                break
        else:
            if len(w1) > len(w2):
                return ""
    
    # Initialize queue for BFS (Kahn's algorithm)
    queue = deque([c for c in chars if in_degree[c] == 0])
    result = []
    
    # Perform topological sort
    while queue:
        c = queue.popleft()
        result.append(c)
        for neighbor in adj[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check for cycle or incomplete order
    return ''.join(result) if len(result) == len(chars) else ""

# Example usage:
# words = ["wrt","wrf","er","ett","rftt"]
# result = alienOrder(words)
# """
# Time Complexity: O(C) - Where C is total characters
# Space Complexity: O(1) - Fixed 26 letters
# """

########################################################
# ### 9. Minimum Height Trees (Leetcode 310)
########################################################

# **Problem Statement**:  
# Find root(s) of a tree that minimize its height.

# **Example**:

# Input: n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]
# Output: [3,4]
# ```

# **Algorithm** (Peel Onion BFS):
# 1. Repeatedly remove leaves until 1-2 nodes remain.
# 2. These nodes are the MHT roots.

# **Solution**:

from collections import deque

class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if n == 1:
            return [0]
        
        graph = defaultdict(set)
        degree = [0]*n
        for u, v in edges:
            graph[u].add(v)
            graph[v].add(u)
            degree[u] += 1
            degree[v] += 1
        
        queue = deque([i for i in range(n) if degree[i] == 1])
        remaining = n
        
        while remaining > 2:
            level_size = len(queue)
            remaining -= level_size
            for _ in range(level_size):
                u = queue.popleft()
                for v in graph[u]:
                    degree[v] -= 1
                    if degree[v] == 1:
                        queue.append(v)
        
        return list(queue)
# """
# Time Complexity: O(V + E) - Each node processed once
# Space Complexity: O(V) - For queue and graph
# """
